from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserResponse, UserProgress, BadgeResponse
from app.services import QuestService, BadgeService
from app.models import User
from app.routes.dependencies import get_current_user

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user's profile information
    """
    return current_user


@router.get("/progress", response_model=UserProgress)
def get_user_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's learning progress
    
    Includes:
    - User profile
    - Completed quests count
    - Total available quests
    - Earned badges
    """
    quest_service = QuestService(db)
    badge_service = BadgeService(db)
    
    # Get quest completion stats
    completed_quests = quest_service.get_quest_completion_count(current_user.id)
    
    from app.models import Quest, Badge, UserBadge
    total_quests = db.query(Quest).count()
    
    # Get earned badges with earned_at timestamps
    user_badges_with_time = (
        db.query(Badge, UserBadge.earned_at)
        .join(UserBadge)
        .filter(UserBadge.user_id == current_user.id)
        .all()
    )
    
    badges = [
        BadgeResponse(
            id=badge.id,
            name=badge.name,
            description=badge.description,
            icon=badge.icon,
            earned_at=earned_at
        )
        for badge, earned_at in user_badges_with_time
    ]
    
    return UserProgress(
        user=current_user,
        completed_quests=completed_quests,
        total_quests=total_quests,
        badges=badges
    )