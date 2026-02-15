from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routes import auth_router, quests_router, user_router, leaderboard_router

# Create FastAPI app
app = FastAPI(
    title="ML Game Platform API",
    description="Gamified Machine Learning Learning Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
import os

# Create datasets directory if it doesn't exist
if not os.path.exists("datasets"):
    os.makedirs("datasets")

app.mount("/datasets", StaticFiles(directory="datasets"), name="datasets")

# Include routers
app.include_router(auth_router)
app.include_router(quests_router)
app.include_router(user_router)
app.include_router(leaderboard_router)


@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    init_db()
    print("✅ Database initialized")


@app.get("/")
def root():
    """API root endpoint"""
    return {
        "message": "Welcome to ML Game Platform API",
        "version": "1.0.0",
        "docs_url": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)