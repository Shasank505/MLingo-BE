from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Quest, Submission, User, Level
from app.ml_engine import MLEvaluator
from typing import List, Optional, Dict, Any
import os
import shutil


class QuestService:
    """Service for managing quests and submissions"""
    
    def __init__(self, db: Session):
        self.db = db
        self.evaluator = MLEvaluator()
    
    def get_all_quests(self) -> List[Quest]:
        """Get all quests ordered by level and quest order"""
        return self.db.query(Quest).join(Level).order_by(Level.order, Quest.order).all()
    
    def get_quest_by_id(self, quest_id: int) -> Optional[Quest]:
        """Get a specific quest by ID"""
        return self.db.query(Quest).filter(Quest.id == quest_id).first()
    
    def get_user_quest_status(self, user_id: int, quest_id: int) -> Dict[str, Any]:
        """Check if user has completed a quest and get best score"""
        submissions = (
            self.db.query(Submission)
            .filter(Submission.user_id == user_id, Submission.quest_id == quest_id)
            .all()
        )
        
        if not submissions:
            return {"completed": False, "best_score": None, "attempts": 0}
        
        passed_submissions = [s for s in submissions if s.passed]
        best_score = max([s.score for s in submissions if s.score is not None], default=None)
        
        return {
            "completed": len(passed_submissions) > 0,
            "best_score": best_score,
            "attempts": len(submissions)
        }
    
    def submit_quest(
        self, 
        user_id: int, 
        quest_id: int, 
        model_file, 
        upload_dir: str = "./uploads"
    ) -> Submission:
        """
        Submit a model for quest evaluation
        
        Args:
            user_id: User ID
            quest_id: Quest ID
            model_file: Uploaded model file
            upload_dir: Directory to save uploaded models
            
        Returns:
            Submission object with evaluation results
        """
        # Get quest details
        quest = self.get_quest_by_id(quest_id)
        if not quest:
            raise ValueError("Quest not found")
        
        # Get user
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Save uploaded model
        os.makedirs(upload_dir, exist_ok=True)
        model_filename = f"user_{user_id}_quest_{quest_id}_{model_file.filename}"
        model_path = os.path.join(upload_dir, model_filename)
        
        with open(model_path, "wb") as buffer:
            shutil.copyfileobj(model_file.file, buffer)
        
        # Evaluate model
        evaluation_result = self.evaluator.evaluate_model(
            model_path=model_path,
            dataset_name=quest.dataset_name,
            metric_name=quest.metric_name,
            config=quest.config or {}
        )
        
        # Check if passed
        passed = False
        xp_awarded = 0
        
        if evaluation_result["success"]:
            score = evaluation_result["score"]
            passed = score >= quest.threshold
            
            if passed:
                # Check if this is the first time passing
                previous_passed = (
                    self.db.query(Submission)
                    .filter(
                        Submission.user_id == user_id,
                        Submission.quest_id == quest_id,
                        Submission.passed == True
                    )
                    .first()
                )
                
                if not previous_passed:
                    # Award XP only on first completion
                    xp_awarded = quest.xp_reward
                    user.add_xp(xp_awarded)
                    user.update_streak()
                    self.db.commit()
        
        # Create submission record
        submission = Submission(
            user_id=user_id,
            quest_id=quest_id,
            model_path=model_path,
            score=evaluation_result.get("score", 0.0),
            passed=passed,
            evaluation_logs=evaluation_result.get("logs", ""),
            xp_awarded=xp_awarded
        )
        
        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)
        
        return submission
    
    def get_user_submissions(self, user_id: int, quest_id: Optional[int] = None) -> List[Submission]:
        """Get user's submissions, optionally filtered by quest"""
        query = self.db.query(Submission).filter(Submission.user_id == user_id)
        
        if quest_id:
            query = query.filter(Submission.quest_id == quest_id)
        
        return query.order_by(Submission.submission_date.desc()).all()
    
    def get_quest_completion_count(self, user_id: int) -> int:
        """Get number of unique quests completed by user"""
        return (
            self.db.query(func.count(func.distinct(Submission.quest_id)))
            .filter(Submission.user_id == user_id, Submission.passed == True)
            .scalar()
        )