from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel

from app.database.session import get_db
from app.services.learning_path_service import learning_path_service
from app.schemas.learning_path import LearningPathResult

router = APIRouter()

class GeneratePathRequest(BaseModel):
    user_id: UUID

@router.post("/generate", response_model=LearningPathResult, status_code=200)
async def generate_learning_path(request: GeneratePathRequest, db: Session = Depends(get_db)):
    return await learning_path_service.generate_learning_path(db, user_id=str(request.user_id))

@router.get("/user/{user_id}", response_model=LearningPathResult)
def get_latest_learning_path(user_id: str, db: Session = Depends(get_db)):
    return learning_path_service.get_latest_path(db, user_id=user_id)

@router.get("/{path_id}", response_model=LearningPathResult)
def get_learning_path_by_id(path_id: str, db: Session = Depends(get_db)):
    return learning_path_service.get_path(db, path_id=path_id)
