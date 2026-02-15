from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # e.g., "Regression Basics"
    description = Column(Text, nullable=True)
    order = Column(Integer, nullable=False, unique=True)  # 1, 2, 3...
    required_xp = Column(Integer, default=0)  # XP needed to unlock this level
    
    # Relationships
    quests = relationship("Quest", back_populates="level", cascade="all, delete-orphan")