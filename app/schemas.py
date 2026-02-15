from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ===== Auth Schemas =====
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


# ===== User Schemas =====
class UserBase(BaseModel):
    username: str
    email: str


class UserResponse(UserBase):
    id: int
    xp: int
    level: int
    current_streak: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserProgress(BaseModel):
    user: UserResponse
    completed_quests: int
    total_quests: int
    badges: List["BadgeResponse"]
    
    class Config:
        from_attributes = True


# ===== Level Schemas =====
class LevelBase(BaseModel):
    name: str
    description: Optional[str] = None
    order: int
    required_xp: int = 0


class LevelResponse(LevelBase):
    id: int
    
    class Config:
        from_attributes = True


# ===== Quest Schemas =====
class QuestBase(BaseModel):
    title: str
    description: str
    task_type: str
    xp_reward: int = 100
    metric_name: str
    threshold: float


class QuestResponse(QuestBase):
    id: int
    level_id: int
    order: int
    dataset_name: Optional[str] = None  # Add this line
    
    class Config:
        from_attributes = True


class QuestDetailResponse(QuestResponse):
    level: LevelResponse
    user_completed: bool = False
    best_score: Optional[float] = None


# ===== Submission Schemas =====
class SubmissionCreate(BaseModel):
    quest_id: int


class SubmissionResponse(BaseModel):
    id: int
    quest_id: int
    score: Optional[float]
    passed: bool
    xp_awarded: int
    submission_date: datetime
    evaluation_logs: Optional[str]
    
    class Config:
        from_attributes = True


# ===== Badge Schemas =====
class BadgeBase(BaseModel):
    name: str
    description: str
    icon: Optional[str] = "🏆"


class BadgeResponse(BadgeBase):
    id: int
    earned_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ===== Leaderboard Schemas =====
class LeaderboardEntry(BaseModel):
    rank: int
    username: str
    xp: int
    level: int
    completed_quests: int


class LeaderboardResponse(BaseModel):
    leaderboard: List[LeaderboardEntry]
    user_rank: Optional[int] = None