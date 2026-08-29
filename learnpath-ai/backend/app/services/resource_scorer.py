import logging
from datetime import datetime
from typing import List, Dict, Any
from app.schemas.resource import ResourceCandidate, AccessType

logger = logging.getLogger(__name__)

DEFAULT_SCORING_WEIGHTS = {
    "relevance": 0.40,
    "quality": 0.15,
    "rating": 0.10,
    "review_confidence": 0.10,
    "freshness": 0.10,
    "learner_level_match": 0.10,
    "platform_reliability": 0.05,
}

PLATFORM_RELIABILITY_SCORES = {
    "Official Documentation": 100.0,
    "MIT OpenCourseWare": 95.0,
    "freeCodeCamp": 90.0,
    "YouTube": 85.0,
}

class ResourceScorer:
    """
    Multi-factor deterministic scoring and format diversity engine for resource candidates.
    """

    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or DEFAULT_SCORING_WEIGHTS

    def calculate_score(
        self,
        candidate: ResourceCandidate,
        phase_skills: List[str],
        phase_title: str,
        learner_level: str = "intermediate"
    ) -> float:
        """
        Calculates an overall score (0.0 to 100.0) for a resource candidate based on multi-factor analysis.
        """
        # 1. Skill Relevance Score (0-100)
        matched_skills = 0
        candidate_skills_lower = [s.lower() for s in candidate.skills]
        for sk in phase_skills:
            if any(sk.lower() in csk or csk in sk.lower() for csk in candidate_skills_lower):
                matched_skills += 1

        relevance_ratio = (matched_skills / len(phase_skills)) if phase_skills else 1.0
        if any(term in candidate.title.lower() for term in phase_title.lower().split()):
            relevance_ratio = min(1.0, relevance_ratio + 0.2)
        score_relevance = relevance_ratio * 100.0

        # 2. Quality Score (0-100)
        score_quality = 85.0
        if candidate.description and len(candidate.description) > 50:
            score_quality += 10.0
        if candidate.is_free and candidate.access_type == AccessType.PUBLIC_FREE:
            score_quality += 5.0
        score_quality = min(100.0, score_quality)

        # 3. Rating Score (0-100)
        if candidate.rating is not None:
            score_rating = min(100.0, (candidate.rating / 5.0) * 100.0)
        else:
            score_rating = 80.0  # Neutral default for unrated public resources

        # 4. Review Confidence Score (0-100)
        if candidate.review_count is not None:
            if candidate.review_count >= 1000:
                score_review_conf = 100.0
            elif candidate.review_count >= 100:
                score_review_conf = 85.0
            else:
                score_review_conf = 70.0
        else:
            score_review_conf = 75.0

        # 5. Freshness Score (0-100)
        if candidate.published_at:
            years_old = (datetime.utcnow() - candidate.published_at).days / 365.25
            if years_old <= 1:
                score_freshness = 100.0
            elif years_old <= 3:
                score_freshness = 85.0
            else:
                score_freshness = 70.0
        else:
            score_freshness = 80.0

        # 6. Learner Level Match Score (0-100)
        if candidate.difficulty.lower() == learner_level.lower():
            score_level_match = 100.0
        elif candidate.difficulty.lower() in ("all_levels", "beginner") and learner_level.lower() == "intermediate":
            score_level_match = 85.0
        else:
            score_level_match = 70.0

        # 7. Platform Reliability Score (0-100)
        score_platform = PLATFORM_RELIABILITY_SCORES.get(candidate.platform, 75.0)

        # Weighted calculation
        overall = (
            score_relevance * self.weights["relevance"] +
            score_quality * self.weights["quality"] +
            score_rating * self.weights["rating"] +
            score_review_conf * self.weights["review_confidence"] +
            score_freshness * self.weights["freshness"] +
            score_level_match * self.weights["learner_level_match"] +
            score_platform * self.weights["platform_reliability"]
        )

        # Access Type Bonus (public_free priority)
        if candidate.access_type == AccessType.PUBLIC_FREE:
            overall += 3.0
        elif candidate.access_type == AccessType.PUBLIC_ACCOUNT_REQUIRED:
            overall -= 2.0

        return round(min(100.0, max(0.0, overall)), 1)

    def select_diverse_top_resources(
        self,
        candidates: List[ResourceCandidate],
        target_count: int = 4
    ) -> List[ResourceCandidate]:
        """
        Ranks candidates by overall score and enforces resource format diversity
        (e.g., mixing video, documentation, article, and interactive resources).
        """
        # Sort candidates descending by overall_score
        sorted_candidates = sorted(candidates, key=lambda c: c.overall_score or 0.0, reverse=True)

        selected: List[ResourceCandidate] = []
        seen_types = set()
        seen_urls = set()

        # Pass 1: Select top candidate per distinct resource_type
        for c in sorted_candidates:
            if c.original_url in seen_urls:
                continue
            if c.resource_type not in seen_types and len(selected) < target_count:
                selected.append(c)
                seen_types.add(c.resource_type)
                seen_urls.add(c.original_url)

        # Pass 2: Fill remaining slots with remaining highest scoring candidates
        for c in sorted_candidates:
            if len(selected) >= target_count:
                break
            if c.original_url not in seen_urls:
                selected.append(c)
                seen_urls.add(c.original_url)

        return selected
