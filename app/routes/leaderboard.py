from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import LeaderboardResponse
from app.services import LeaderboardService
from app.models import User
from app.routes.dependencies import get_current_user

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("/", response_model=LeaderboardResponse)
def get_leaderboard(
    limit: int = Query(100, ge=1, le=500, description="Maximum number of entries"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get global leaderboard
    
    Returns top users ranked by XP with their stats:
    - Rank
    - Username
    - XP
    - Level
    - Completed quests
    
    Also includes current user's rank
    """
    leaderboard_service = LeaderboardService(db)
    
    leaderboard = leaderboard_service.get_leaderboard(limit=limit)
    user_rank = leaderboard_service.get_user_rank(current_user.id)
    
    return LeaderboardResponse(
        leaderboard=leaderboard,
        user_rank=user_rank
    )