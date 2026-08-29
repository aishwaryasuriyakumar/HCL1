from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.learner_repository import learner_repo
from app.schemas.learner import LearnerProfileCreate, LearnerProfileUpdate, LearnerProfileResponse, DomainInfo
from app.data.domains import DOMAINS

class ProfileService:
    def _map_to_response(self, db_obj):
        domain_data = DOMAINS.get(db_obj.selected_domain)
        
        return LearnerProfileResponse(
            user_id=db_obj.user_id,
            full_name=db_obj.full_name,
            email=db_obj.email,
            selected_domain=DomainInfo(id=domain_data["id"], name=domain_data["name"]),
            experience_level=db_obj.experience_level,
            years_of_experience=db_obj.years_of_experience,
            learning_goal=db_obj.learning_goal,
            career_goal=db_obj.career_goal,
            motivation=db_obj.motivation,
            current_skills=db_obj.current_skills,
            interests=db_obj.interests,
            projects=db_obj.projects,
            certifications=db_obj.certifications,
            completed_courses=db_obj.completed_courses,
            preferred_learning_formats=db_obj.preferred_learning_formats,
            daily_learning_time=db_obj.daily_learning_time,
            created_at=db_obj.created_at,
            updated_at=db_obj.updated_at
        )

    def create_profile(self, db: Session, learner_in: LearnerProfileCreate):
        existing = learner_repo.get_by_email(db, email=learner_in.email)
        if existing:
            raise HTTPException(status_code=409, detail="A learner profile with this email already exists")
        
        db_obj = learner_repo.create(db, learner_in)
        if not db_obj:
            raise HTTPException(status_code=400, detail="Could not create learner profile")
            
        return self._map_to_response(db_obj)

    def get_profile(self, db: Session, user_id: str):
        db_obj = learner_repo.get_by_id(db, user_id=user_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Learner profile not found")
        return self._map_to_response(db_obj)

    def get_profile_by_email(self, db: Session, email: str):
        db_obj = learner_repo.get_by_email(db, email=email)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Learner profile not found")
        return self._map_to_response(db_obj)

    def update_profile(self, db: Session, user_id: str, obj_in: LearnerProfileUpdate):
        db_obj = learner_repo.get_by_id(db, user_id=user_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Learner profile not found")
            
        if obj_in.email and obj_in.email != db_obj.email:
            existing = learner_repo.get_by_email(db, email=obj_in.email)
            if existing:
                raise HTTPException(status_code=409, detail="A learner profile with this email already exists")
                
        db_obj = learner_repo.update(db, db_obj, obj_in)
        return self._map_to_response(db_obj)

profile_service = ProfileService()
