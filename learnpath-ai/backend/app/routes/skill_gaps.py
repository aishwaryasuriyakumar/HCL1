from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel

from app.database.session import get_db
from app.services.skill_gap_service import skill_gap_service
from app.schemas.skill_gap import SkillGapResult

router = APIRouter()

class AnalyzeRequest(BaseModel):
    user_id: UUID

@router.post("/analyze", response_model=SkillGapResult, status_code=200)
async def analyze_skill_gaps(request: AnalyzeRequest, db: Session = Depends(get_db)):
    return await skill_gap_service.analyze_skill_gaps(db, user_id=str(request.user_id))

@router.get("/user/{user_id}", response_model=SkillGapResult)
def get_latest_analysis(user_id: str, db: Session = Depends(get_db)):
    return skill_gap_service.get_latest_analysis(db, user_id=user_id)

@router.get("/{analysis_id}", response_model=SkillGapResult)
def get_analysis(analysis_id: str, db: Session = Depends(get_db)):
    return skill_gap_service.get_analysis(db, analysis_id=analysis_id)
