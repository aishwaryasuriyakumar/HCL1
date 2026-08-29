from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.learner import LearnerProfileCreate, LearnerProfileUpdate, LearnerProfileResponse
from app.services.profile_service import profile_service

router = APIRouter()

@router.post("", response_model=LearnerProfileResponse, status_code=201)
def create_profile(learner_in: LearnerProfileCreate, db: Session = Depends(get_db)):
    return profile_service.create_profile(db, learner_in)

@router.get("/{user_id}", response_model=LearnerProfileResponse)
def get_profile(user_id: str, db: Session = Depends(get_db)):
    return profile_service.get_profile(db, user_id=user_id)

@router.put("/{user_id}", response_model=LearnerProfileResponse)
def update_profile(user_id: str, learner_in: LearnerProfileUpdate, db: Session = Depends(get_db)):
    return profile_service.update_profile(db, user_id, learner_in)

@router.get("/by-email/{email}", response_model=LearnerProfileResponse)
def get_profile_by_email(email: str, db: Session = Depends(get_db)):
    return profile_service.get_profile_by_email(db, email=email)
