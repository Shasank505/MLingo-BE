from .auth import router as auth_router
from .quests import router as quests_router
from .user import router as user_router
from .leaderboard import router as leaderboard_router

__all__ = ["auth_router", "quests_router", "user_router", "leaderboard_router"]