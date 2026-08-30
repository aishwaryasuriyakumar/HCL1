from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database.session import get_db
from app.services.mastery_service import mastery_service
from app.schemas.mastery import (
    MasteryStartRequest,
    MasteryStartResponse,
    MasterySubmitRequest,
    MasteryResult,
    MasteryReviewResponse,
    MasteryAttemptHistoryItem,
)

router = APIRouter()

@router.post("/start", response_model=MasteryStartResponse, status_code=status.HTTP_201_CREATED)
def start_mastery_assessment(
    request: MasteryStartRequest,
    db: Session = Depends(get_db)
):
    """
    Start a mastery assessment for the specified user and phase.
    Returns 8-10 questions covering phase topics with correct answers stripped.
    """
    return mastery_service.start_assessment(
        db=db,
        user_id=str(request.user_id),
        phase_id=request.phase_id
    )

@router.post("/{attempt_id}/submit", response_model=MasteryResult)
async def submit_mastery_assessment(
    attempt_id: str,
    submission: MasterySubmitRequest,
    db: Session = Depends(get_db)
):
    """
    Submit answers for an active mastery assessment attempt.
    Scores the assessment deterministically and unlocks the next phase if passed.
    """
    return await mastery_service.submit_assessment(
        db=db,
        attempt_id=attempt_id,
        submission=submission
    )

@router.get("/{attempt_id}/result", response_model=MasteryResult)
def get_mastery_result(
    attempt_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve persisted mastery result for a submitted attempt.
    Returns 409 if the attempt is still in progress.
    """
    return mastery_service.get_result(db=db, attempt_id=attempt_id)

@router.get("/user/{user_id}/phase/{phase_id}", response_model=List[MasteryAttemptHistoryItem])
def get_mastery_history(
    user_id: str,
    phase_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve attempt history for a specific user and phase.
    """
    return mastery_service.get_history(db=db, user_id=user_id, phase_id=phase_id)

@router.post("/{attempt_id}/remediation-complete")
def complete_remediation(
    attempt_id: str,
    db: Session = Depends(get_db)
):
    """
    Mark remediation as completed for a failed attempt, enabling retest.
    """
    return mastery_service.complete_remediation(db=db, attempt_id=attempt_id)

@router.get("/{attempt_id}/review", response_model=MasteryReviewResponse)
def get_mastery_review(
    attempt_id: str,
    db: Session = Depends(get_db)
):
    """
    Review questions, selected answers, correct answers, and explanations after submission.
    """
    return mastery_service.get_review(db=db, attempt_id=attempt_id)
