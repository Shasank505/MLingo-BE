from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models import User, Submission
from typing import List, Dict, Any, Optional


class LeaderboardService:
    """Service for managing leaderboard"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_leaderboard(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get leaderboard rankings
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of leaderboard entries with rank, username, xp, level, completed quests
        """
        # Get users with their completed quest counts
        leaderboard_query = (
            self.db.query(
                User.id,
                User.username,
                User.xp,
                User.level,
                func.count(func.distinct(Submission.quest_id)).label('completed_quests')
            )
            .outerjoin(Submission, (Submission.user_id == User.id) & (Submission.passed == True))
            .group_by(User.id)
            .order_by(desc(User.xp), desc('completed_quests'))
            .limit(limit)
            .all()
        )
        
        # Format results with rankings
        leaderboard = []
        for rank, entry in enumerate(leaderboard_query, start=1):
            leaderboard.append({
                "rank": rank,
                "username": entry.username,
                "xp": entry.xp,
                "level": entry.level,
                "completed_quests": entry.completed_quests or 0
            })
        
        return leaderboard
    
    def get_user_rank(self, user_id: int) -> Optional[int]:
        """
        Get a user's rank on the leaderboard
        
        Args:
            user_id: User ID
            
        Returns:
            User's rank (1-indexed) or None if user not found
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        # Count users with higher XP
        higher_ranked_count = (
            self.db.query(func.count(User.id))
            .filter(User.xp > user.xp)
            .scalar()
        )
        
        return higher_ranked_count + 1
    
    def get_user_leaderboard_context(self, user_id: int, context_size: int = 5) -> Dict[str, Any]:
        """
        Get leaderboard with context around a specific user
        
        Args:
            user_id: User ID
            context_size: Number of entries to show above and below user
            
        Returns:
            Dict with full leaderboard and user's position
        """
        leaderboard = self.get_leaderboard()
        user_rank = self.get_user_rank(user_id)
        
        return {
            "leaderboard": leaderboard,
            "user_rank": user_rank
        }