from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Game stats
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    current_streak = Column(Integer, default=0)
    last_activity_date = Column(DateTime, nullable=True)
    
    # Account info
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    submissions = relationship("Submission", back_populates="user", cascade="all, delete-orphan")
    user_badges = relationship("UserBadge", back_populates="user", cascade="all, delete-orphan")
    
    def calculate_level(self):
        """Calculate level based on XP (logarithmic scaling)"""
        import math
        # Level = floor(sqrt(XP / 100)) + 1
        self.level = math.floor(math.sqrt(self.xp / 100)) + 1
        return self.level
    
    def add_xp(self, amount: int):
        """Add XP and recalculate level"""
        self.xp += amount
        self.calculate_level()
        
    def update_streak(self):
        """Update daily streak"""
        today = datetime.utcnow().date()
        if self.last_activity_date:
            last_activity = self.last_activity_date.date()
            days_diff = (today - last_activity).days
            
            if days_diff == 1:
                # Consecutive day
                self.current_streak += 1
            elif days_diff > 1:
                # Streak broken
                self.current_streak = 1
            # If same day, don't update streak
        else:
            # First activity
            self.current_streak = 1
            
        self.last_activity_date = datetime.utcnow()