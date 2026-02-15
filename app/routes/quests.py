from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import QuestResponse, QuestDetailResponse, SubmissionResponse
from app.services import QuestService, BadgeService
from app.models import User
from app.routes.dependencies import get_current_user

router = APIRouter(prefix="/quests", tags=["Quests"])


@router.get("/", response_model=List[QuestDetailResponse])
def get_quests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all available quests with user completion status
    """
    quest_service = QuestService(db)
    quests = quest_service.get_all_quests()
    
    result = []
    for quest in quests:
        status = quest_service.get_user_quest_status(current_user.id, quest.id)
        
        quest_detail = QuestDetailResponse(
            id=quest.id,
            title=quest.title,
            description=quest.description,
            task_type=quest.task_type,
            xp_reward=quest.xp_reward,
            metric_name=quest.metric_name,
            threshold=quest.threshold,
            level_id=quest.level_id,
            order=quest.order,
            level=quest.level,
            user_completed=status["completed"],
            best_score=status["best_score"]
        )
        result.append(quest_detail)
    
    return result


@router.get("/{quest_id}", response_model=QuestDetailResponse)
def get_quest(
    quest_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get details of a specific quest
    """
    quest_service = QuestService(db)
    quest = quest_service.get_quest_by_id(quest_id)
    
    if not quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quest not found"
        )
    
    status_info = quest_service.get_user_quest_status(current_user.id, quest.id)
    
    return QuestDetailResponse(
        id=quest.id,
        title=quest.title,
        description=quest.description,
        task_type=quest.task_type,
        xp_reward=quest.xp_reward,
        metric_name=quest.metric_name,
        threshold=quest.threshold,
        level_id=quest.level_id,
        order=quest.order,
        level=quest.level,
        user_completed=status_info["completed"],
        best_score=status_info["best_score"]
    )


@router.post("/{quest_id}/submit", response_model=SubmissionResponse)
async def submit_quest(
    quest_id: int,
    model_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit a trained model for quest evaluation
    
    - **quest_id**: ID of the quest to submit for
    - **model_file**: Trained model file (.pkl or .joblib)
    """
    # Validate file extension
    if not (model_file.filename.endswith('.pkl') or model_file.filename.endswith('.joblib')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Model file must be .pkl or .joblib format"
        )
    
    quest_service = QuestService(db)
    badge_service = BadgeService(db)
    
    try:
        # Submit and evaluate
        submission = quest_service.submit_quest(
            user_id=current_user.id,
            quest_id=quest_id,
            model_file=model_file
        )
        
        # Check for new badges
        if submission.passed:
            badge_service.check_and_award_badges(current_user.id)
        
        return submission
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Submission failed: {str(e)}"
        )


@router.get("/{quest_id}/submissions", response_model=List[SubmissionResponse])
def get_quest_submissions(
    quest_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all submissions for a specific quest by current user
    """
    quest_service = QuestService(db)
    submissions = quest_service.get_user_submissions(current_user.id, quest_id)
    
    return submissions