import logging
from typing import List, Optional
from datetime import datetime
from app.agents.base_agent import BaseAgent
from app.integrations.llm.llm_service import LLMService, llm_service as default_llm_service
from app.integrations.resource_providers.base_provider import ResourceProvider
from app.integrations.resource_providers.youtube_adapter import YouTubeAdapter
from app.integrations.resource_providers.freecodecamp_adapter import FreeCodeCampAdapter
from app.integrations.resource_providers.documentation_adapter import DocumentationAdapter
from app.integrations.resource_providers.mit_ocw_adapter import MITOpenCourseWareAdapter
from app.services.resource_validator import ResourceValidator
from app.services.resource_scorer import ResourceScorer
from app.schemas.resource import (
    ResourceCandidate,
    ResourceCardData,
    PhaseResources,
    CuratedPathResources,
    VerificationStatus,
    ProviderStatusItem
)
from app.schemas.learning_path import LearningPathResult, PhaseSpec
from app.schemas.learner import LearnerProfileResponse

logger = logging.getLogger(__name__)

class ResourceCuratorAgent(BaseAgent):
    """
    Discovers, validates, ranks, and recommends learning resources for each phase
    of a personalized LearningPathResult using active public resource providers,
    deterministic multi-factor scoring, and Gemini explanation generation.
    """

    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
        providers: Optional[List[ResourceProvider]] = None,
        validator: Optional[ResourceValidator] = None,
        scorer: Optional[ResourceScorer] = None
    ):
        self.llm_service = llm_service or default_llm_service
        self.providers = providers or [
            YouTubeAdapter(),
            FreeCodeCampAdapter(),
            DocumentationAdapter(),
            MITOpenCourseWareAdapter()
        ]
        self.validator = validator or ResourceValidator()
        self.scorer = scorer or ResourceScorer()

    def get_providers_status(self) -> List[ProviderStatusItem]:
        """
        Returns health/availability status for all configured providers.
        """
        return [p.get_provider_status() for p in self.providers]

    async def run(
        self,
        path_result: LearningPathResult,
        learner: LearnerProfileResponse
    ) -> CuratedPathResources:
        """
        Curates resources across all phases of a learning path.
        """
        curated_phases: List[PhaseResources] = []

        for phase in path_result.phases:
            phase_resources = await self._curate_phase_resources(phase, path_result, learner)
            curated_phases.append(phase_resources)

        return CuratedPathResources(
            path_id=path_result.path_id,
            phases=curated_phases,
            curated_at=datetime.utcnow()
        )

    async def _curate_phase_resources(
        self,
        phase: PhaseSpec,
        path_result: LearningPathResult,
        learner: LearnerProfileResponse
    ) -> PhaseResources:
        """
        Curates top 3 to 5 resources for a single learning path phase.
        """
        raw_candidates: List[ResourceCandidate] = []
        phase_skills = phase.skills or phase.target_skills
        query = f"{phase.title} {' '.join(phase.resource_topics[:2])}".strip()
        learner_level = getattr(learner.experience_level, "value", str(learner.experience_level or "intermediate"))

        # 1. Search candidates across all available providers (Fault Isolated)
        for provider in self.providers:
            status = provider.get_provider_status()
            if status.status != "available":
                logger.info(f"Provider {provider.platform_name} is unavailable ({status.reason}), skipping.")
                continue

            try:
                found = await provider.search(
                    query=query,
                    skills=phase_skills,
                    difficulty=phase.difficulty,
                    limit=4
                )
                raw_candidates.extend(found)
            except Exception as e:
                logger.error(f"Provider {provider.platform_name} search failed for phase {phase.phase_id}: {e}")

        # 2. Validate URLs & Public Access
        validated_candidates: List[ResourceCandidate] = []
        for cand in raw_candidates:
            v_cand, v_status = await self.validator.validate_candidate(cand)
            if v_status in (VerificationStatus.VERIFIED, VerificationStatus.UNVERIFIED) and v_cand.is_active and v_cand.is_publicly_accessible:
                validated_candidates.append(v_cand)

        # 3. Score Candidates Deterministically
        for cand in validated_candidates:
            cand.overall_score = self.scorer.calculate_score(
                candidate=cand,
                phase_skills=phase_skills,
                phase_title=phase.title,
                learner_level=learner_level
            )

        # 4. Select Format-Diverse Top Candidates
        top_candidates = self.scorer.select_diverse_top_resources(validated_candidates, target_count=4)

        # 5. Generate Personalized LLM Explanations (Gemini)
        final_cards: List[ResourceCardData] = []
        for cand in top_candidates:
            why_explanation = await self._generate_why_explanation(cand, phase, learner)
            card = ResourceCardData(
                resource_id=cand.resource_id,
                title=cand.title,
                platform=cand.platform,
                description=cand.description,
                resource_type=cand.resource_type,
                difficulty=cand.difficulty,
                is_free=cand.is_free,
                access_type=cand.access_type,
                duration_minutes=cand.duration_minutes,
                rating=cand.rating,
                review_count=cand.review_count,
                overall_score=cand.overall_score or 85.0,
                why_recommended=why_explanation,
                original_url=cand.original_url,  # Original URL PRESERVED
                is_active=cand.is_active,
                last_verified_at=cand.last_verified_at or datetime.utcnow()
            )
            final_cards.append(card)

        return PhaseResources(
            phase_id=phase.phase_id,
            resources=final_cards
        )

    async def _generate_why_explanation(
        self,
        candidate: ResourceCandidate,
        phase: PhaseSpec,
        learner: LearnerProfileResponse
    ) -> str:
        """
        Uses Gemini LLM to generate a personalized explanation of why this specific resource
        is recommended for the learner's skill gap and career goal.
        """
        fallback_explanation = (
            f"Recommended because this {candidate.platform} {candidate.resource_type} directly covers "
            f"{', '.join(phase.skills[:2])} matching your {learner.career_goal or 'learning'} objectives."
        )

        prompt = f"""Generate a concise 1-2 sentence explanation of why this resource is recommended for the learner.

Learner Profile:
- Career Goal: {learner.career_goal or 'AI Developer'}
- Learning Goal: {learner.learning_goal or 'Master skill gaps'}
- Experience Level: {getattr(learner.experience_level, 'value', str(learner.experience_level))}

Learning Phase:
- Phase Title: {phase.title}
- Target Skills: {phase.skills}

Resource Details:
- Title: {candidate.title}
- Platform: {candidate.platform}
- Resource Type: {candidate.resource_type}
- Difficulty: {candidate.difficulty}

Return JSON with format:
{{"why_recommended": "1-2 sentence clear personalized explanation..."}}
"""
        try:
            res = self.llm_service.generate_text(
                system_instruction="You are an expert learning curator explaining resource recommendations clearly to learners.",
                prompt=prompt,
                temperature=0.3
            )
            if "why_recommended" in res and res["why_recommended"]:
                return res["why_recommended"]
        except Exception as e:
            logger.debug(f"LLM explanation fallback used: {e}")

        return fallback_explanation
