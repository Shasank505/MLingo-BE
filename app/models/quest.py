from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class Quest(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, index=True)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)
    
    # Quest info
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    task_type = Column(String, nullable=False)  # "regression", "classification", "clustering"
    order = Column(Integer, nullable=False)  # Order within level
    
    # Rewards
    xp_reward = Column(Integer, default=100)
    
    # Evaluation criteria
    dataset_name = Column(String, nullable=False)  # Reference to dataset file
    metric_name = Column(String, nullable=False)  # "accuracy", "r2_score", "f1_score"
    threshold = Column(Float, nullable=False)  # Minimum score to pass
    
    # Additional config (JSON field for flexibility)
    config = Column(JSON, nullable=True)  # {"target_column": "price", "test_size": 0.2}
    
    # Relationships
    level = relationship("Level", back_populates="quests")
    submissions = relationship("Submission", back_populates="quest", cascade="all, delete-orphan")