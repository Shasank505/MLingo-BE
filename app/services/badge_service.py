from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Badge, UserBadge, User, Submission
from typing import List


class BadgeService:
    """Service for managing badges and achievements"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_badges(self) -> List[Badge]:
        """Get all available badges"""
        return self.db.query(Badge).all()
    
    def get_user_badges(self, user_id: int) -> List[Badge]:
        """Get all badges earned by a user"""
        user_badges = (
            self.db.query(Badge)
            .join(UserBadge)
            .filter(UserBadge.user_id == user_id)
            .all()
        )
        return user_badges
    
    def check_and_award_badges(self, user_id: int) -> List[Badge]:
        """
        Check user's progress and award any new badges they've earned
        
        Returns:
            List of newly awarded badges
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return []
        
        all_badges = self.get_all_badges()
        user_badges = self.get_user_badges(user_id)
        user_badge_ids = {badge.id for badge in user_badges}
        
        newly_awarded = []
        
        for badge in all_badges:
            # Skip if user already has this badge
            if badge.id in user_badge_ids:
                continue
            
            # Check if user meets badge condition
            if self._check_badge_condition(user_id, badge):
                self._award_badge(user_id, badge.id)
                newly_awarded.append(badge)
        
        return newly_awarded
    
    def _check_badge_condition(self, user_id: int, badge: Badge) -> bool:
        """Check if user meets the condition for a badge"""
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if badge.condition_type == "xp_threshold":
            return user.xp >= badge.condition_value
        
        elif badge.condition_type == "quest_completion":
            completed_quests = (
                self.db.query(func.count(func.distinct(Submission.quest_id)))
                .filter(Submission.user_id == user_id, Submission.passed == True)
                .scalar()
            )
            return completed_quests >= badge.condition_value
        
        elif badge.condition_type == "streak":
            return user.current_streak >= badge.condition_value
        
        elif badge.condition_type == "perfect_score":
            # Check if user has achieved perfect score (1.0) on any quest
            perfect_submissions = (
                self.db.query(Submission)
                .filter(
                    Submission.user_id == user_id,
                    Submission.score >= 0.99,  # Allow for floating point precision
                    Submission.passed == True
                )
                .count()
            )
            return perfect_submissions >= badge.condition_value
        
        return False
    
    def _award_badge(self, user_id: int, badge_id: int):
        """Award a badge to a user"""
        user_badge = UserBadge(user_id=user_id, badge_id=badge_id)
        self.db.add(user_badge)
        self.db.commit()
    
    def create_badge(
        self, 
        name: str, 
        description: str, 
        condition_type: str, 
        condition_value: int,
        icon: str = "🏆"
    ) -> Badge:
        """Create a new badge"""
        badge = Badge(
            name=name,
            description=description,
            icon=icon,
            condition_type=condition_type,
            condition_value=condition_value
        )
        self.db.add(badge)
        self.db.commit()
        self.db.refresh(badge)
        return badge