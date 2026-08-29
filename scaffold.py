import os
import subprocess

def create_file(path, content=""):
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# ROOT STRUCTURE
project_root = "learnpath-ai"
os.makedirs(project_root, exist_ok=True)
os.chdir(project_root)

# 1. Backend Structure
backend_dirs = [
    "backend/app/api",
    "backend/app/routes",
    "backend/app/models",
    "backend/app/schemas",
    "backend/app/services",
    "backend/app/agents",
    "backend/app/repositories",
    "backend/app/database",
    "backend/app/core",
    "backend/app/data/skills",
    "backend/app/data/questions",
    "backend/app/integrations/llm",
    "backend/app/integrations/resource_providers",
    "backend/app/utils",
    "backend/tests/unit",
    "backend/tests/integration"
]

for d in backend_dirs:
    os.makedirs(d, exist_ok=True)
    # Create __init__.py in almost all dirs
    if "data/" not in d and "tests/" not in d:
        create_file(f"{d}/__init__.py")

# Create specific backend files
create_file("backend/app/__init__.py")
create_file("backend/tests/__init__.py")
create_file("backend/tests/unit/__init__.py")
create_file("backend/tests/integration/__init__.py")

# Requirements
create_file("backend/requirements.txt", """
fastapi==0.111.0
uvicorn==0.30.1
pydantic==2.7.4
pydantic-settings==2.3.4
sqlalchemy==2.0.31
pytest==8.2.2
httpx==0.27.0
""")

# .env.example
create_file("backend/.env.example", """
APP_NAME=LearnPath AI
APP_ENV=development
DATABASE_URL=sqlite:///./learnpath.db
FRONTEND_URL=http://localhost:5173
LLM_API_KEY=
LLM_MODEL=
""")

# core/config.py
create_file("backend/app/core/config.py", """
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "LearnPath AI"
    app_env: str = "development"
    database_url: str = "sqlite:///./learnpath.db"
    frontend_url: str = "http://localhost:5173"
    llm_api_key: str = ""
    llm_model: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
""")

# core/constants.py
create_file("backend/app/core/constants.py", """
# Constants placeholder
""")

# core/exceptions.py
create_file("backend/app/core/exceptions.py", """
class ResourceNotFoundError(Exception):
    pass

class InvalidDomainError(Exception):
    pass

class AssessmentAlreadySubmittedError(Exception):
    pass

class AgentExecutionError(Exception):
    pass
""")

# core/logging.py
create_file("backend/app/core/logging.py", """
# Logging config placeholder
""")

# database/base.py
create_file("backend/app/database/base.py", """
from sqlalchemy.orm import declarative_base

Base = declarative_base()
""")

# database/session.py
create_file("backend/app/database/session.py", """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""")

# schemas/common.py
create_file("backend/app/schemas/common.py", """
from pydantic import BaseModel
class HealthCheck(BaseModel):
    status: str
""")

# schemas/learner.py
create_file("backend/app/schemas/learner.py", """
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class LearnerProfile(BaseModel):
    user_id: UUID
    full_name: str
    email: str
    selected_domain: str
    experience_level: str
    career_goal: str
    learning_goal: str
    motivation: str
    current_skills: List[str]
    interests: List[str]
    projects: List[str]
    certifications: List[str]
    completed_courses: List[str]
    preferred_learning_formats: List[str]
    daily_learning_time: Optional[int]
""")

# schemas/assessment.py
create_file("backend/app/schemas/assessment.py", """
from pydantic import BaseModel
from typing import List
from uuid import UUID

class SkillResult(BaseModel):
    skill: str
    questions_attempted: int
    correct_answers: int
    score: float
    proficiency: str
    confidence: str

class OverallResult(BaseModel):
    total_questions: int
    correct_answers: int
    score: float
    proficiency: str

class AssessmentResult(BaseModel):
    attempt_id: UUID
    user_id: UUID
    domain: str
    overall: OverallResult
    skill_results: List[SkillResult]
""")

# schemas/skill_gap.py
create_file("backend/app/schemas/skill_gap.py", """
from pydantic import BaseModel
from typing import List
from uuid import UUID

class SkillGapDetail(BaseModel):
    skill: str
    score: float
    proficiency: str
    confidence: str
    status: str

class SkillGapResult(BaseModel):
    user_id: UUID
    domain: str
    career_goal: str
    overall_score: float
    skills: List[SkillGapDetail]
    strong_skills: List[str]
    moderate_skills: List[str]
    skill_gaps: List[str]
    critical_gaps: List[str]
    recommended_focus: List[str]
    summary: str
""")

# schemas/learning_path.py
create_file("backend/app/schemas/learning_path.py", """
from pydantic import BaseModel
from typing import List
from uuid import UUID

class Phase(BaseModel):
    phase_id: str
    order: int
    title: str
    description: str
    skills: List[str]
    prerequisites: List[str]
    estimated_hours: int
    status: str

class LearningPathResult(BaseModel):
    user_id: UUID
    domain: str
    goal: str
    phases: List[Phase]
""")

# schemas/resource.py
create_file("backend/app/schemas/resource.py", """
from pydantic import BaseModel
from uuid import UUID

class RecommendedResource(BaseModel):
    resource_id: UUID
    phase_id: str
    title: str
    provider: str
    url: str
    resource_type: str
    is_free: bool
    availability_status: str
    relevance_score: float
    quality_score: float
    why_recommended: str
    learning_outcome: str
""")

# schemas/mastery.py
create_file("backend/app/schemas/mastery.py", """
from pydantic import BaseModel
from typing import List
from uuid import UUID

class MasteryResult(BaseModel):
    user_id: UUID
    phase_id: str
    score: float
    passed: bool
    weak_topics: List[str]
    next_action: str
""")

# schemas/progress.py
create_file("backend/app/schemas/progress.py", """
from pydantic import BaseModel
from typing import List
from uuid import UUID

class ProgressSummary(BaseModel):
    user_id: UUID
    overall_progress: float
    completed_phases: int
    total_phases: int
    current_phase_id: str
    average_score: float
    completed_modules: List[str]
    remaining_modules: List[str]
    learning_speed: str
""")

# agents/base_agent.py
create_file("backend/app/agents/base_agent.py", """
class BaseAgent:
    async def run(self, input_data):
        raise NotImplementedError("This agent has not been implemented yet.")
""")

# agents/skill_gap_agent.py
create_file("backend/app/agents/skill_gap_agent.py", """
from .base_agent import BaseAgent

class SkillGapAgent(BaseAgent):
    \"\"\"
    Expected Input: AssessmentResult
    Expected Output: SkillGapResult
    Future Responsibility: Analyze assessment scores to determine specific skill gaps.
    \"\"\"
    pass
""")

# agents/learning_path_agent.py
create_file("backend/app/agents/learning_path_agent.py", """
from .base_agent import BaseAgent

class LearningPathAgent(BaseAgent):
    \"\"\"
    Expected Input: SkillGapResult
    Expected Output: LearningPathResult
    Future Responsibility: Generate a phased learning path based on skill gaps.
    \"\"\"
    pass
""")

# agents/resource_curator_agent.py
create_file("backend/app/agents/resource_curator_agent.py", """
from .base_agent import BaseAgent

class ResourceCuratorAgent(BaseAgent):
    \"\"\"
    Expected Input: Phase (from LearningPathResult)
    Expected Output: List[RecommendedResource]
    Future Responsibility: Find and recommend free learning resources for a phase.
    \"\"\"
    pass
""")

# agents/mastery_agent.py
create_file("backend/app/agents/mastery_agent.py", """
from .base_agent import BaseAgent

class MasteryAgent(BaseAgent):
    \"\"\"
    Expected Input: User answers for a phase
    Expected Output: MasteryResult
    Future Responsibility: Grade mastery assessment and determine if remediation is needed.
    \"\"\"
    pass
""")

# data/domains.py
create_file("backend/app/data/domains.py", """
DOMAINS = {
    "machine_learning": {
        "name": "Machine Learning",
        "skills": [
            "Python for ML", "Data Preprocessing", "Statistics & Probability",
            "Regression", "Classification", "Feature Engineering",
            "Model Evaluation", "Ensemble Learning", "Unsupervised Learning",
            "Model Deployment"
        ]
    },
    "data_science": {
        "name": "Data Science",
        "skills": [
            "Python", "NumPy", "Pandas", "Statistics", "Data Cleaning",
            "Exploratory Data Analysis", "Data Visualization", "SQL",
            "Machine Learning Basics", "Data Interpretation"
        ]
    },
    "generative_ai": {
        "name": "Generative AI",
        "skills": [
            "LLM Fundamentals", "Prompt Engineering", "Tokens & Context Windows",
            "Embeddings", "Vector Databases", "RAG", "Fine-tuning",
            "Transformers", "AI Agents", "LLM Evaluation"
        ]
    },
    "web_development": {
        "name": "Web Development",
        "skills": [
            "HTML", "CSS", "JavaScript", "DOM", "HTTP & REST APIs",
            "React", "State Management", "Backend Fundamentals",
            "Authentication", "Databases"
        ]
    },
    "cloud_devops": {
        "name": "Cloud & DevOps",
        "skills": [
            "Linux", "Networking", "Git", "Docker", "Containers",
            "CI/CD", "Cloud Fundamentals", "Virtual Machines",
            "Kubernetes Basics", "Cloud Security"
        ]
    }
}
""")

# main.py
create_file("backend/app/main.py", """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import settings
from app.database.session import engine
from app.database.base import Base

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

@app.get("/")
def read_root():
    return {"message": "LearnPath AI API", "status": "running"}
""")

# api/router.py
create_file("backend/app/api/router.py", """
from fastapi import APIRouter
from app.routes import health, domains, profiles, assessments, skill_gaps, learning_paths, resources, mastery, progress

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(domains.router, prefix="/domains", tags=["domains"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(assessments.router, prefix="/assessments", tags=["assessments"])
api_router.include_router(skill_gaps.router, prefix="/skill-gap", tags=["skill_gaps"])
api_router.include_router(learning_paths.router, prefix="/learning-paths", tags=["learning_paths"])
api_router.include_router(resources.router, prefix="/resources", tags=["resources"])
api_router.include_router(mastery.router, prefix="/mastery", tags=["mastery"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress"])
""")

# routes files
create_file("backend/app/routes/health.py", """
from fastapi import APIRouter
router = APIRouter()
@router.get("/health")
def health_check():
    return {"status": "healthy"}
""")

for route in ["domains", "profiles", "assessments", "skill_gaps", "learning_paths", "resources", "mastery", "progress"]:
    create_file(f"backend/app/routes/{route}.py", f"""
from fastapi import APIRouter
router = APIRouter()
# Placeholder for {route} routes
""")

# Placeholder for models
for model in ["learner", "assessment", "learning_path", "resource", "progress"]:
    create_file(f"backend/app/models/{model}.py", f"# Placeholder for {model} SQLAlchemy model")

# Placeholder for services
for service in ["profile", "assessment", "scoring", "skill_gap", "learning_path", "resource", "mastery", "progress"]:
    create_file(f"backend/app/services/{service}_service.py", f"# Placeholder for {service} service logic")

# Placeholder for repositories
for repo in ["learner", "assessment", "learning_path", "progress"]:
    create_file(f"backend/app/repositories/{repo}_repository.py", f"# Placeholder for {repo} database access")

# Tests
create_file("backend/tests/unit/test_health.py", """
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "LearnPath AI API", "status": "running"}
""")

# Gitignore
create_file(".gitignore", """
__pycache__/
*.py[cod]
*$py.class
.env
venv/
env/
.venv/
node_modules/
dist/
build/
.pytest_cache/
*.db
.idea/
.vscode/
""")

# README
create_file("README.md", """
# AI-Powered Personalized Learning Path Recommender

**Initial architecture scaffold — feature modules to be implemented incrementally.**

## Purpose
Create personalized learning journeys by assessing learner skills, detecting skill gaps, generating structured learning paths, recommending verified resources and validating mastery.

## Supported Domains
1. Machine Learning
2. Data Science
3. Generative AI
4. Web Development
5. Cloud & DevOps

## Technology Stack
- Backend: Python, FastAPI, SQLAlchemy, SQLite (dev)
- Frontend: React, Vite, TypeScript, Tailwind CSS

## Project Structure
- `backend/`: FastAPI application, Agents, SQLite
- `frontend/`: React + Vite application
- `docs/`: Documentation and API Contracts

## Setup Instructions
(See docs/development-guide.md)

## Team Module Ownership
(See docs/team-ownership.md)
""")

# Docs
create_file("docs/architecture.md", """
# Architecture

Frontend -> FastAPI -> Services -> Agents/Repositories/Integrations -> Database/External APIs

## Main Pipeline
USER -> USER ONBOARDING -> DOMAIN SELECTION -> DIAGNOSTIC ASSESSMENT -> SKILL-WISE SCORING -> SKILL GAP AGENT -> PERSONALIZED LEARNING PATH AGENT -> RESOURCE CURATOR AGENT -> LEARNING -> MASTERY ASSESSMENT AGENT -> PASS / REMEDIATION -> PROGRESS TRACKING -> DASHBOARD
""")

create_file("docs/api-contracts.md", """
# API Contracts
Contracts are implemented as Pydantic models in `backend/app/schemas/`.
""")

create_file("docs/team-ownership.md", """
# Team Module Ownership

- MEMBER 1: Learner onboarding, Domain selection, Diagnostic assessment, Skill scoring, Skill Gap Agent
- MEMBER 2: Personalized Learning Path Agent
- MEMBER 3: Resource Curator Agent, Free learning resource discovery, Resource validation and ranking
- MEMBER 4: Mastery Assessment Agent, Remediation flow
- MEMBER 5: Progress tracking, Dashboard backend, Frontend integration
""")

create_file("docs/development-guide.md", """
# Development Guide

1. No feature should directly modify another team's agent.
2. Modules communicate using shared Pydantic contracts.
3. Do not duplicate domain definitions.
4. Do not calculate deterministic values with an LLM.
5. API keys stay only in backend environment variables.
6. Routes should remain thin.
7. Business logic goes in services.
8. Database access goes through repositories where useful.
9. Intelligent reasoning belongs in agents.
10. External platform/API code goes in integrations.

## Setup Backend
cd backend
python -m venv venv
source venv/bin/activate # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload

## Run Tests
pytest

## Setup Frontend
cd frontend
npm install
npm run dev
""")
