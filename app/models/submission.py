from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quest_id = Column(Integer, ForeignKey("quests.id"), nullable=False)
    
    # Submission details
    model_path = Column(String, nullable=False)  # Path to saved model file
    submission_date = Column(DateTime, default=datetime.utcnow)
    
    # Evaluation results
    score = Column(Float, nullable=True)
    passed = Column(Boolean, default=False)
    evaluation_logs = Column(Text, nullable=True)
    
    # Rewards given
    xp_awarded = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="submissions")
    quest = relationship("Quest", back_populates="submissions")