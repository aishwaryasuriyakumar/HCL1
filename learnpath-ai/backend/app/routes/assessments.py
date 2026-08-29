from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.services.assessment_service import assessment_service
from app.schemas.assessment import (
    AssessmentStartRequest, AssessmentStartResponse,
    AssessmentSubmitRequest, AssessmentResult,
    ReviewAnswerDetail, AssessmentHistoryResponse
)

router = APIRouter()

@router.post("/start", response_model=AssessmentStartResponse, status_code=201)
def start_assessment(request: AssessmentStartRequest, db: Session = Depends(get_db)):
    return assessment_service.start_assessment(db, user_id=str(request.user_id))

@router.get("/{attempt_id}", response_model=AssessmentStartResponse)
def get_attempt(attempt_id: str, db: Session = Depends(get_db)):
    return assessment_service.get_attempt(db, attempt_id=attempt_id)

@router.post("/{attempt_id}/submit", response_model=AssessmentResult)
def submit_assessment(attempt_id: str, submission: AssessmentSubmitRequest, db: Session = Depends(get_db)):
    return assessment_service.submit_assessment(db, attempt_id=attempt_id, submission=submission)

@router.get("/{attempt_id}/result", response_model=AssessmentResult)
def get_result(attempt_id: str, db: Session = Depends(get_db)):
    return assessment_service.get_result(db, attempt_id=attempt_id)

@router.get("/{attempt_id}/review", response_model=List[ReviewAnswerDetail])
def get_review(attempt_id: str, db: Session = Depends(get_db)):
    return assessment_service.get_review(db, attempt_id=attempt_id)

@router.get("/user/{user_id}", response_model=AssessmentHistoryResponse)
def get_user_history(user_id: str, db: Session = Depends(get_db)):
    return assessment_service.get_user_history(db, user_id=user_id)
