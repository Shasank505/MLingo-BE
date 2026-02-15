from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String, nullable=True)  # Icon name or emoji
    condition_type = Column(String, nullable=False)  # "xp_threshold", "quest_completion", "streak", "accuracy"
    condition_value = Column(Integer, nullable=False)  # Threshold value
    
    # Relationships
    user_badges = relationship("UserBadge", back_populates="badge", cascade="all, delete-orphan")