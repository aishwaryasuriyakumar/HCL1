import logging
import uuid
from datetime import datetime
from typing import List, Dict, Set, Any, Optional
from collections import defaultdict, deque

from app.schemas.learning_path import (
    LearningPathAgentInput,
    LearningPathLLMOutput,
    LearningPathResult,
    PhaseSpec,
    ProjectSpec,
    CompletionCriteria,
    CapstoneProject,
)
from app.data.skill_requirements import PREREQUISITES, SKILL_TARGET_SCORES, SKILL_IMPORTANCE_LEVELS
from app.integrations.llm.llm_service import llm_service, LLMService

logger = logging.getLogger(__name__)

class LearningPathAgent:
    def __init__(self, llm_service_instance: Optional[LLMService] = None):
        self.llm_service = llm_service_instance or llm_service

    def _get_domain_str(self, domain_field: Any) -> str:
        if hasattr(domain_field, "id"):
            return getattr(domain_field, "id")
        if isinstance(domain_field, dict):
            return domain_field.get("id", str(domain_field))
        return str(domain_field)

    async def run(self, input_data: LearningPathAgentInput) -> LearningPathResult:
        domain = self._get_domain_str(input_data.learner_profile.selected_domain)
        logger.info(f"learning_path_generation_started user_id={input_data.learner_profile.user_id} domain={domain}")
        
        domain_skills = self._get_valid_domain_skills(domain)
        logger.info(f"skill_knowledge_loaded valid_skills_count={len(domain_skills)} domain={domain}")

        # 1. Build system instruction & prompt
        system_instruction = (
            "You are a personalized learning path architect.\n"
            "Your task is to create a learner-specific roadmap from structured learner information and skill-gap information.\n"
            "Do not create a generic roadmap.\n"
            "Prioritize the learner's actual gaps.\n"
            "Respect prerequisites.\n"
            "Do not invent skills outside the supplied domain knowledge.\n"
            "Do not generate external resource URLs.\n"
            "Return only the requested structured output."
        )

        prompt = self._build_llm_prompt(input_data, domain_skills)

        # 2. Call LLM Service for structured output (with deterministic fallback if unavailable)
        try:
            llm_output: LearningPathLLMOutput = self.llm_service.generate_structured(
                prompt=prompt,
                system_instruction=system_instruction,
                response_model=LearningPathLLMOutput
            )
        except Exception as e:
            logger.warning(f"LLM generation unavailable ({e}), generating deterministic fallback path.")
            llm_output = self._generate_deterministic_fallback_path(input_data, domain, domain_skills)

        # 3. Validate & sanitize domain skills (Domain Isolation)
        sanitized_phases = self._sanitize_domain_skills(llm_output.phases, domain_skills)

        # 4. Topological prerequisite sorting & deterministic validation
        ordered_phases = self._enforce_prerequisite_ordering(sanitized_phases, domain)
        logger.info("prerequisite_validation_completed deterministic topological sorting verified")

        # 5. Hours normalization & status setting
        final_phases = self._finalize_phases(ordered_phases)

        # 6. Calculate summary metrics
        total_hours = sum(p.estimated_hours for p in final_phases) + llm_output.capstone_project.estimated_hours
        
        result = LearningPathResult(
            path_id=uuid.uuid4(),
            user_id=input_data.learner_profile.user_id,
            skill_gap_analysis_id=input_data.skill_gap_result.analysis_id,
            domain=domain,
            title=llm_output.title,
            description=llm_output.description,
            learning_goal=input_data.learner_profile.learning_goal,
            career_goal=input_data.learner_profile.career_goal,
            overall_level=llm_output.overall_level,
            total_phases=len(final_phases),
            estimated_total_hours=round(total_hours, 1),
            phases=final_phases,
            capstone_project=llm_output.capstone_project,
            generated_at=datetime.utcnow()
        )
        
        logger.info(f"learning_path_persisted_prep path_id={result.path_id} total_phases={result.total_phases}")
        return result

    def _get_valid_domain_skills(self, domain: str) -> Set[str]:
        if domain in SKILL_TARGET_SCORES:
            return set(SKILL_TARGET_SCORES[domain].keys())
        if domain in PREREQUISITES:
            return set(PREREQUISITES[domain].keys())
        return set()

    def _build_llm_prompt(self, input_data: LearningPathAgentInput, valid_skills: Set[str]) -> str:
        learner = input_data.learner_profile
        gap = input_data.skill_gap_result
        domain = self._get_domain_str(learner.selected_domain)
        domain_prereqs = PREREQUISITES.get(domain, {})

        return f"""
Generate a personalized learning path for the following learner in domain '{domain}'.

=== LEARNER PROFILE ===
User ID: {learner.user_id}
Domain: {domain}
Experience Level: {learner.experience_level}
Years of Experience: {learner.years_of_experience or 'Not specified'}
Learning Goal: {learner.learning_goal}
Career Goal: {learner.career_goal}
Current Skills: {learner.current_skills}
Interests: {learner.interests}
Completed Courses: {learner.completed_courses}
Projects: {learner.projects}

=== SKILL GAP ANALYSIS ===
Overall Assessment Score: {gap.overall_assessment_score}% ({gap.overall_proficiency})
Critical Gaps: {gap.critical_gaps}
High Gaps: {gap.high_gaps}
Moderate Gaps: {gap.moderate_gaps}
Minor Gaps: {gap.minor_gaps}
Strong Skills: {gap.strong_skills}
Recommended Focus: {[f.skill + ': ' + f.reason for f in gap.recommended_focus]}

=== VALID DOMAIN SKILLS & PREREQUISITES ===
Valid Domain Skills: {list(valid_skills)}
Prerequisite Graph: {domain_prereqs}

=== REQUIREMENTS ===
1. Create 3 to 8 sequential learning phases targeting the learner's skill gaps and learning goal.
2. Every phase MUST reference ONLY valid domain skills from: {list(valid_skills)}.
3. Do NOT include strong skills as standalone phases unless required as prerequisites for critical/high gaps.
4. Ensure prerequisite skills appear in earlier phases before dependent skills.
5. Provide 3-6 measurable action-oriented learning objectives per phase (e.g. 'Implement...', 'Evaluate...').
6. Provide resource topics (topics only, NO URLs).
7. Tailor the project deliverable and capstone project specifically to the learner's experience level ({learner.experience_level}) and career goal ({learner.career_goal}).
8. Estimate effort between 2 and 18 hours per phase.
"""

    def _sanitize_domain_skills(self, phases: List[PhaseSpec], valid_skills: Set[str]) -> List[PhaseSpec]:
        """
        Filters out skills that do not belong to the learner's domain (Domain Isolation),
        matching case-insensitively to ensure canonical domain skill names are preserved.
        """
        skill_lookup = {s.lower(): s for s in valid_skills}
        sanitized = []
        for p in phases:
            filtered_skills = []
            for s in p.skills:
                canonical = skill_lookup.get(s.strip().lower())
                if canonical and canonical not in filtered_skills:
                    filtered_skills.append(canonical)
            
            # If phase skills were empty or all filtered out, retain phase with a fallback valid domain skill
            if not filtered_skills and valid_skills:
                filtered_skills = [next(iter(valid_skills))]

            updated_phase = p.model_copy(update={"skills": filtered_skills})
            sanitized.append(updated_phase)
        return sanitized

    def _enforce_prerequisite_ordering(self, phases: List[PhaseSpec], domain: str) -> List[PhaseSpec]:
        """
        Deterministically orders phases using topological sorting on skill prerequisites.
        Guarantees that if Skill B depends on Skill A, Skill A's phase is placed before Skill B's phase.
        """
        prereq_graph = PREREQUISITES.get(domain, {})
        if not prereq_graph or not phases:
            return phases

        # Map each phase to its primary skills
        phase_map = {p.phase_id: p for p in phases}

        # Build skill to phase mapping
        skill_to_phase_id = {}
        for p in phases:
            for s in p.skills:
                skill_to_phase_id[s] = p.phase_id

        # Build phase dependency graph
        phase_dependencies = defaultdict(set)
        in_degree = defaultdict(int)
        phase_ids = [p.phase_id for p in phases]

        for p in phases:
            in_degree[p.phase_id] = 0

        for p in phases:
            for skill in p.skills:
                skill_prereqs = prereq_graph.get(skill, [])
                for prereq in skill_prereqs:
                    prereq_phase_id = skill_to_phase_id.get(prereq)
                    if prereq_phase_id and prereq_phase_id != p.phase_id:
                        if p.phase_id not in phase_dependencies[prereq_phase_id]:
                            phase_dependencies[prereq_phase_id].add(p.phase_id)

        # Recalculate in_degree
        in_degree = {pid: 0 for pid in phase_ids}
        for pid in phase_ids:
            for dep in phase_dependencies[pid]:
                in_degree[dep] += 1

        # Topological sort (Kahn's Algorithm preserving initial LLM relative order where possible)
        queue = deque([pid for pid in phase_ids if in_degree[pid] == 0])
        sorted_phase_ids = []

        while queue:
            current = queue.popleft()
            sorted_phase_ids.append(current)
            for neighbor in phase_dependencies[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # If a cycle was detected or missing items, fall back to initial order
        if len(sorted_phase_ids) != len(phases):
            logger.warning("Cycle or incomplete topological sort detected, maintaining original phase ordering.")
            sorted_phase_ids = phase_ids

        # Reconstruct ordered phase objects
        ordered_phases = []
        for pid in sorted_phase_ids:
            ordered_phases.append(phase_map[pid])

        return ordered_phases

    def _finalize_phases(self, phases: List[PhaseSpec]) -> List[PhaseSpec]:
        """
        Normalizes effort hours (2 to 18 hours per phase), assigns correct sequential ordering,
        updates prerequisite_phase_ids, and sets initial statuses (Phase 1 available, Phase 2+ locked).
        """
        final_list = []
        prev_phase_id: Optional[str] = None

        for idx, p in enumerate(phases, start=1):
            phase_id = f"phase_{idx:02d}"
            
            # Normalize effort hours (clamp between 2.0 and 18.0)
            hours = max(2.0, min(18.0, float(p.estimated_hours)))

            # Normalize project effort hours
            proj_hours = max(1.0, min(hours, float(p.project.estimated_hours)))
            normalized_project = p.project.model_copy(update={"estimated_hours": proj_hours})

            # Set prerequisite phase IDs
            prereq_ids = [prev_phase_id] if prev_phase_id else []

            # Set status: Phase 1 is available, all others locked
            status = "available" if idx == 1 else "locked"

            final_phase = p.model_copy(update={
                "phase_id": phase_id,
                "order": idx,
                "estimated_hours": hours,
                "project": normalized_project,
                "prerequisite_phase_ids": prereq_ids,
                "status": status
            })
            
            final_list.append(final_phase)
            prev_phase_id = phase_id

        return final_list

    def _generate_deterministic_fallback_path(
        self,
        input_data: LearningPathAgentInput,
        domain: str,
        domain_skills: List[str]
    ) -> LearningPathLLMOutput:
        """
        Creates a structured deterministic fallback learning path when LLM is offline.
        """
        gap_items = input_data.skill_gap_result.skills
        prioritized_skills = [g.skill for g in gap_items if g.skill in domain_skills]

        # Ensure we have at least 3 skills to partition into 3+ phases
        for sk in domain_skills:
            if len(prioritized_skills) >= 3:
                break
            if sk not in prioritized_skills:
                prioritized_skills.append(sk)

        if not prioritized_skills:
            prioritized_skills = list(domain_skills)

        # Partition skills into 3-4 phases (max 2 skills per phase so we get 3+ phases)
        chunk_size = max(1, min(2, len(prioritized_skills) // 3))
        skill_chunks = [
            prioritized_skills[i:i + chunk_size]
            for i in range(0, len(prioritized_skills), chunk_size)
        ]


        phases = []
        for idx, chunk in enumerate(skill_chunks, start=1):
            main_skill = chunk[0] if chunk else "Core Fundamentals"
            phase_spec = PhaseSpec(
                phase_id=f"phase_{idx:02d}",
                order=idx,
                title=f"{main_skill} Mastery",
                description=f"Focused learning module on {', '.join(chunk)}.",
                skills=chunk,
                resource_topics=[f"{s} Concepts" for s in chunk],
                learning_objectives=[f"Master practical implementations of {s}" for s in chunk],
                learning_outcomes=[f"Able to apply {s} in production environments" for s in chunk],
                project=ProjectSpec(
                    title=f"{main_skill} Practical Project",
                    description=f"Hands-on project developing real-world solutions using {', '.join(chunk)}.",
                    deliverable="Source code and project documentation",
                    estimated_hours=4.0
                ),
                estimated_hours=6.0,
                difficulty="intermediate",
                recommendation_reason=f"Targeting critical skill gaps in {', '.join(chunk)}.",
                status="available" if idx == 1 else "locked"
            )
            phases.append(phase_spec)

        capstone = CapstoneProject(
            title=f"Comprehensive {domain.replace('_', ' ').title()} Capstone",
            description=f"End-to-end capstone synthesizing {', '.join(prioritized_skills[:4])}.",
            deliverables=["Full GitHub Repository", "Architecture Documentation"],
            estimated_hours=12.0
        )

        return LearningPathLLMOutput(
            title=f"Personalized {domain.replace('_', ' ').title()} Learning Path",
            description=f"Tailored learning path focusing on {', '.join(prioritized_skills[:3])}.",
            overall_level="intermediate",
            summary_recommendation="Structured roadmap prioritizing prerequisite mastery.",
            phases=phases,
            capstone_project=capstone
        )
