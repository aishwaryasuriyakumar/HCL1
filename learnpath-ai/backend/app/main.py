from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import settings
from app.database.session import engine
from app.database.base import Base

# Import models to ensure they are registered with Base metadata
from app.models.learner import Learner
from app.models.assessment import AssessmentAttempt, AssessmentAnswer, SkillAssessmentResult, SkillGapAnalysis
from app.models.learning_path import LearningPath

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

from app.routes import health
app.include_router(health.router, tags=["health"])

@app.get("/")
def read_root():
    return {"message": "LearnPath AI API", "status": "running"}
