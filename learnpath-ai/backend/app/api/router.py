from fastapi import APIRouter
from app.routes import health, domains, profiles, assessments, skill_gaps, learning_paths, resources, mastery, progress

api_router = APIRouter()


api_router.include_router(domains.router, prefix="/domains", tags=["domains"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(assessments.router, prefix="/assessments", tags=["assessments"])
api_router.include_router(skill_gaps.router, prefix="/skill-gap", tags=["skill_gaps"])
api_router.include_router(learning_paths.router, prefix="/learning-path", tags=["learning_paths"])
api_router.include_router(learning_paths.router, prefix="/learning-paths", tags=["learning_paths"])
api_router.include_router(resources.router, prefix="/resources", tags=["resources"])
api_router.include_router(mastery.router, prefix="/mastery", tags=["mastery"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress"])
