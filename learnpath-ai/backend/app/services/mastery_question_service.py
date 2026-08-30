import json
import os
import random
import logging
from typing import Dict, List, Any, Optional
from app.schemas.mastery import MasteryQuestionPublic, MasteryQuestionOption

logger = logging.getLogger(__name__)

MASTERY_QUESTIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "mastery_questions")

class MasteryQuestionService:
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = data_dir or MASTERY_QUESTIONS_DIR
        self._cache: Dict[str, List[Dict[str, Any]]] = {}
        self._load_all_banks()

    def _load_all_banks(self) -> None:
        if not os.path.exists(self.data_dir):
            logger.warning(f"Mastery questions directory not found at {self.data_dir}")
            return

        for filename in os.listdir(self.data_dir):
            if filename.endswith(".json"):
                domain = filename[:-5]
                filepath = os.path.join(self.data_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            self._cache[domain] = data
                            logger.info(f"Loaded {len(data)} mastery questions for domain '{domain}'")
                except Exception as e:
                    logger.error(f"Failed to load mastery question bank '{filename}': {e}")

    def get_questions_by_domain(self, domain: str) -> List[Dict[str, Any]]:
        return self._cache.get(domain, [])

    def get_question_by_id(self, domain: str, question_id: str) -> Optional[Dict[str, Any]]:
        questions = self.get_questions_by_domain(domain)
        for q in questions:
            if q.get("id") == question_id:
                return q
        # Also check all domains in cache in case domain is generic
        for dom, qlist in self._cache.items():
            for q in qlist:
                if q.get("id") == question_id:
                    return q
        return None

    def select_questions_for_phase(
        self,
        domain: str,
        phase_skills: List[str],
        phase_topics: List[str],
        weak_topics: Optional[List[str]] = None,
        previous_question_ids: Optional[List[str]] = None,
        target_count: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Selects 8 to 10 questions covering phase topics with appropriate difficulty balance.
        If weak_topics are provided (retest), prioritizes weak topics.
        """
        all_domain_questions = self.get_questions_by_domain(domain)
        if not all_domain_questions:
            # Fallback across all questions if domain exact match is missing
            all_domain_questions = [q for dom in self._cache.values() for q in dom]

        # Filter questions relevant to this phase's skills or topics
        normalized_skills = [s.strip().lower() for s in phase_skills]
        normalized_topics = [t.strip().lower() for t in phase_topics]

        relevant_questions = []
        for q in all_domain_questions:
            q_skill = q.get("skill", "").strip().lower()
            q_topic = q.get("topic", "").strip().lower()
            if q_topic in normalized_topics or q_skill in normalized_skills:
                relevant_questions.append(q)

        # If no specific matches found, use domain questions
        if not relevant_questions:
            relevant_questions = list(all_domain_questions)

        weak_topics_norm = [t.strip().lower() for t in (weak_topics or [])]

        # Partition questions by weak vs standard topics
        weak_pool = []
        standard_pool = []
        for q in relevant_questions:
            if q.get("topic", "").strip().lower() in weak_topics_norm:
                weak_pool.append(q)
            else:
                standard_pool.append(q)

        # Shuffle deterministically or with seed
        rng = random.Random(42 + len(previous_question_ids or []))
        rng.shuffle(weak_pool)
        rng.shuffle(standard_pool)

        selected: List[Dict[str, Any]] = []
        selected_ids = set()

        # Retest logic: allocate more questions to weak topics if present
        if weak_topics_norm and weak_pool:
            weak_target = min(len(weak_pool), max(len(weak_topics_norm) * 2, int(target_count * 0.6)))
            # Prioritize questions not in previous attempts if available
            unseen_weak = [q for q in weak_pool if q["id"] not in (previous_question_ids or [])]
            seen_weak = [q for q in weak_pool if q["id"] in (previous_question_ids or [])]
            for q in (unseen_weak + seen_weak):
                if len(selected) < weak_target and q["id"] not in selected_ids:
                    selected.append(q)
                    selected_ids.add(q["id"])

        # Topic coverage guarantee: ensure at least one question per phase topic if available
        for topic in phase_topics:
            t_norm = topic.strip().lower()
            if not any(q.get("topic", "").strip().lower() == t_norm for q in selected):
                matching = [q for q in relevant_questions if q.get("topic", "").strip().lower() == t_norm and q["id"] not in selected_ids]
                if matching:
                    chosen = matching[0]
                    selected.append(chosen)
                    selected_ids.add(chosen["id"])

        # Fill remaining slots with difficulty balance: ~2 easy, ~5 medium, ~3 hard
        remaining_needed = target_count - len(selected)
        if remaining_needed > 0:
            candidate_pool = [q for q in relevant_questions if q["id"] not in selected_ids]
            
            # Separate by difficulty
            easy = [q for q in candidate_pool if q.get("difficulty") == "easy"]
            medium = [q for q in candidate_pool if q.get("difficulty") == "medium"]
            hard = [q for q in candidate_pool if q.get("difficulty") == "hard"]
            other = [q for q in candidate_pool if q.get("difficulty") not in ("easy", "medium", "hard")]

            # Prioritize unseen over seen
            if previous_question_ids:
                easy.sort(key=lambda q: q["id"] in previous_question_ids)
                medium.sort(key=lambda q: q["id"] in previous_question_ids)
                hard.sort(key=lambda q: q["id"] in previous_question_ids)

            for bucket in [medium, hard, easy, other]:
                while bucket and len(selected) < target_count:
                    q = bucket.pop(0)
                    if q["id"] not in selected_ids:
                        selected.append(q)
                        selected_ids.add(q["id"])

        # If still under target, draw from any remaining domain questions
        if len(selected) < target_count:
            for q in all_domain_questions:
                if q["id"] not in selected_ids:
                    selected.append(q)
                    selected_ids.add(q["id"])
                    if len(selected) >= target_count:
                        break

        return selected[:target_count]

    def format_public_questions(self, raw_questions: List[Dict[str, Any]]) -> List[MasteryQuestionPublic]:
        public_list = []
        for q in raw_questions:
            options = [
                MasteryQuestionOption(id=opt["id"], text=opt["text"])
                for opt in q.get("options", [])
            ]
            public_q = MasteryQuestionPublic(
                id=q["id"],
                question_id=q["id"],
                topic=q.get("topic", ""),
                difficulty=q.get("difficulty", "medium"),
                question=q.get("question", ""),
                options=options
            )
            public_list.append(public_q)
        return public_list

mastery_question_service = MasteryQuestionService()
