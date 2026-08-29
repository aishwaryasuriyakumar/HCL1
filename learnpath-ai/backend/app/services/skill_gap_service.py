from sqlalchemy.orm import Session
from fastapi import HTTPException
import logging
from typing import Optional

from app.models.assessment import AssessmentAttempt, SkillGapAnalysis
from app.repositories.learner_repository import learner_repo
from app.services.profile_service import profile_service
from app.services.assessment_service import assessment_service
from app.agents.skill_gap_agent import SkillGapAgent
from app.integrations.llm.provider import llm_provider
from app.schemas.skill_gap import SkillGapAgentInput, SkillGapResult
from app.core.config import settings

logger = logging.getLogger(__name__)

class SkillGapService:
    async def analyze_skill_gaps(self, db: Session, user_id: str) -> SkillGapResult:
        logger.info(f"Initiating skill gap analysis for user {user_id}")
        
        # 1. Retrieve learner profile
        learner = learner_repo.get_by_id(db, user_id=user_id)
        if not learner:
            raise HTTPException(status_code=404, detail="Learner profile not found")
            
        # 2. Retrieve latest submitted assessment for the selected domain
        latest_attempt = db.query(AssessmentAttempt).filter(
            AssessmentAttempt.user_id == user_id,
            AssessmentAttempt.domain == learner.selected_domain,
            AssessmentAttempt.status == "submitted"
        ).order_by(AssessmentAttempt.started_at.desc()).first()
        
        if not latest_attempt:
            raise HTTPException(
                status_code=409, 
                detail="No submitted assessment found for the learner's selected domain"
            )
            
        # 3. Check for idempotency: return existing analysis if it already exists for this attempt
        existing_analysis = db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.assessment_attempt_id == latest_attempt.id
        ).first()
        
        if existing_analysis:
            logger.info(f"Found existing skill gap analysis for attempt {latest_attempt.id}. Returning cached result.")
            return SkillGapResult(**existing_analysis.result_json)

        # 4. Map entities to Pydantic schemas for the Agent boundary
        learner_pydantic = profile_service._map_to_response(learner)
        assessment_pydantic = assessment_service._map_to_result_response(latest_attempt)
        
        agent_input = SkillGapAgentInput(
            learner=learner_pydantic,
            assessment=assessment_pydantic
        )

        # 5. Initialize hybrid agent based on LLM configuration
        provider = llm_provider if settings.llm_api_key else None
        agent = SkillGapAgent(llm_provider=provider)
        
        # 6. Execute analysis
        result = await agent.run(agent_input)
        
        # 7. Persist analysis JSON serialized (Pydantic v2 mode='json' turns models/UUIDs/datetimes to primitives)
        db_analysis = SkillGapAnalysis(
            id=str(result.analysis_id),
            user_id=user_id,
            assessment_attempt_id=latest_attempt.id,
            domain=latest_attempt.domain,
            overall_assessment_score=latest_attempt.overall_score,
            result_json=result.model_dump(mode="json")
        )
        
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        logger.info(f"Persisted new skill gap analysis {db_analysis.id} for user {user_id}")
        
        return result

    def get_latest_analysis(self, db: Session, user_id: str) -> SkillGapResult:
        analysis = db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.user_id == user_id
        ).order_by(SkillGapAnalysis.created_at.desc()).first()
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Skill gap analysis not found")
            
        return SkillGapResult(**analysis.result_json)

    def get_analysis(self, db: Session, analysis_id: str) -> SkillGapResult:
        analysis = db.query(SkillGapAnalysis).filter(
            SkillGapAnalysis.id == analysis_id
        ).first()
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Skill gap analysis not found")
            
        return SkillGapResult(**analysis.result_json)

skill_gap_service = SkillGapService()
