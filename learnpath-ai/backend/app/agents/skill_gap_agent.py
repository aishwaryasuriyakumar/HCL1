import uuid
from datetime import datetime
from typing import List, Dict, Optional, Any
import json
import logging

from app.agents.base_agent import BaseAgent
from app.data.skill_requirements import SKILL_TARGET_SCORES, SKILL_IMPORTANCE_LEVELS, PREREQUISITES
from app.schemas.skill_gap import SkillGapAgentInput, SkillGapResult, SkillGapItem, RecommendedFocusItem
from app.integrations.llm.base import BaseLLMProvider

logger = logging.getLogger(__name__)

class SkillGapAgent(BaseAgent):
    def __init__(self, llm_provider: Optional[BaseLLMProvider] = None):
        self.llm_provider = llm_provider

    async def run(self, input_data: SkillGapAgentInput) -> SkillGapResult:
        logger.info(f"Running SkillGapAgent for user {input_data.learner.user_id}")
        
        learner = input_data.learner
        assessment = input_data.assessment
        domain = assessment.domain

        # Retrieve configurations
        target_scores = SKILL_TARGET_SCORES.get(domain, {})
        importance_levels = SKILL_IMPORTANCE_LEVELS.get(domain, {})
        prereqs_map = PREREQUISITES.get(domain, {})

        skills_list: List[Dict[str, Any]] = []
        strong_skills = []
        minor_gaps = []
        moderate_gaps = []
        high_gaps = []
        critical_gaps = []

        # Phase 1: Deterministic Calculations
        for sr in assessment.skill_results:
            skill_name = sr.skill
            current_score = sr.score
            current_proficiency = sr.proficiency
            confidence = sr.confidence

            target_score = target_scores.get(skill_name, 70.0)
            importance = importance_levels.get(skill_name, "intermediate")
            prereqs = prereqs_map.get(skill_name, [])

            # Gap Score
            gap_score = max(target_score - current_score, 0.0)

            # Severity Mapping
            if gap_score == 0:
                severity = "strong"
                strong_skills.append(skill_name)
            elif gap_score <= 14:
                severity = "minor_gap"
                minor_gaps.append(skill_name)
            elif gap_score <= 29:
                severity = "moderate_gap"
                moderate_gaps.append(skill_name)
            elif gap_score <= 44:
                severity = "high_gap"
                high_gaps.append(skill_name)
            else:
                severity = "critical_gap"
                critical_gaps.append(skill_name)

            # Priority Score & Label
            if gap_score == 0:
                priority_score = 0.0
                priority = "low"
            else:
                base_priority = gap_score * 2
                # Importance Bonus
                bonus = 15 if importance == "foundation" else 10 if importance == "intermediate" else 5
                priority_score = min(base_priority + bonus, 100.0)
                
                if priority_score >= 80.0:
                    priority = "critical"
                elif priority_score >= 60.0:
                    priority = "high"
                elif priority_score >= 40.0:
                    priority = "medium"
                else:
                    priority = "low"

            # Fallback deterministic explanation
            if gap_score == 0:
                reason = f"Your score of {current_score}% meets the target of {target_score}% for {skill_name} in {domain}."
            else:
                reason = (
                    f"Your score is {current_score}%, below the configured target of {target_score}%. "
                    f"This produces a {gap_score}-point proficiency gap, making {skill_name} a {severity.replace('_', ' ')}."
                )
                if prereqs:
                    reason += f" Prerequisite skills for {skill_name} are: {', '.join(prereqs)}."

            skills_list.append({
                "skill": skill_name,
                "current_score": current_score,
                "current_proficiency": current_proficiency,
                "target_score": target_score,
                "gap_score": gap_score,
                "severity": severity,
                "confidence": confidence,
                "priority_score": priority_score,
                "priority": priority,
                "prerequisites": prereqs,
                "reason": reason
            })

        # Recommended Focus Topological Scheduling (Prerequisites before depending skills)
        active_gaps = [s for s in skills_list if s["gap_score"] > 0]
        # Sort by priority score descending initially
        active_gaps.sort(key=lambda x: x["priority_score"], reverse=True)

        recommended_focus_skills = []
        remaining = list(active_gaps)

        while remaining:
            found = False
            for idx, item in enumerate(remaining):
                # Prerequisites of this item that still have gaps and haven't been scheduled yet
                unresolved_prereqs = [p for p in item["prerequisites"] if any(r["skill"] == p for r in remaining)]
                if not unresolved_prereqs:
                    # No unfulfilled prerequisites in our gaps, safe to schedule
                    recommended_focus_skills.append(item)
                    remaining.pop(idx)
                    found = True
                    break
            if not found:
                # Cycle fallback (should never happen with DAG configs)
                item = remaining.pop(0)
                recommended_focus_skills.append(item)

        # Build recommended focus items
        recommended_focus = []
        for i, item in enumerate(recommended_focus_skills):
            focus_reason = f"Priority: {item['priority'].capitalize()}. Gap: {item['gap_score']} points below target."
            if item["prerequisites"]:
                # Mention if this serves as prerequisite or depends on something else
                focus_reason += f" Foundation/prerequisite connections: {', '.join(item['prerequisites'])}."
            
            recommended_focus.append(RecommendedFocusItem(
                order=i + 1,
                skill=item["skill"],
                reason=focus_reason
            ))

        # Default deterministic summary
        overall_gaps_count = len(skills_list) - len(strong_skills)
        summary = (
            f"Based on your diagnostic assessment for {domain}, you demonstrated {overall_gaps_count} skill gaps "
            f"out of 10 evaluated skills. Your primary recommended area of focus is {recommended_focus[0].skill if recommended_focus else 'None'}."
        )

        # Phase 2: Optional LLM Enhancement
        if self.llm_provider:
            try:
                enhanced_data = self._generate_llm_explanations(learner, skills_list, recommended_focus_skills)
                if enhanced_data:
                    # Update summary and reason fields
                    summary = enhanced_data.get("summary", summary)
                    focus_reasons = enhanced_data.get("focus_reasons", {})
                    
                    # Update reasons in primary skills list
                    for s_dict in skills_list:
                        s_name = s_dict["skill"]
                        if s_name in focus_reasons:
                            s_dict["reason"] = focus_reasons[s_name]

                    # Update reasons in recommended focus list
                    for rf in recommended_focus:
                        if rf.skill in focus_reasons:
                            rf.reason = focus_reasons[rf.skill]
                            
                    logger.info("Successfully enhanced skill gap analysis using LLM provider.")
            except Exception as e:
                logger.warning(f"LLM enhancement failed, falling back to deterministic explanations: {e}")

        # Construct final output
        final_skills = [SkillGapItem(**s) for s in skills_list]

        return SkillGapResult(
            analysis_id=uuid.uuid4(),
            user_id=learner.user_id,
            assessment_attempt_id=assessment.attempt_id,
            domain=domain,
            career_goal=learner.career_goal,
            learning_goal=learner.learning_goal,
            overall_assessment_score=assessment.overall.score,
            overall_proficiency=assessment.overall.proficiency,
            skills=final_skills,
            strong_skills=strong_skills,
            minor_gaps=minor_gaps,
            moderate_gaps=moderate_gaps,
            high_gaps=high_gaps,
            critical_gaps=critical_gaps,
            recommended_focus=recommended_focus,
            summary=summary,
            generated_at=datetime.utcnow()
        )

    def _generate_llm_explanations(self, learner, skills_list, recommended_focus_skills) -> Optional[dict]:
        # Formulate instructions and details
        domain = skills_list[0]["skill"] # Domain context is inside the skill models
        skills_summary_str = ""
        for s in skills_list:
            skills_summary_str += (
                f"- {s['skill']}: Score {s['current_score']}%, Target {s['target_score']}%, "
                f"Gap {s['gap_score']}, Priority {s['priority']}, Confidence {s['confidence']}\n"
            )

        prompt = f"""
Learner Profile:
- Name: {learner.full_name}
- Domain: {skills_list[0].get('domain', 'current domain')}
- Career Goal: {learner.career_goal}
- Learning Goal: {learner.learning_goal}
- Self-reported skills: {', '.join(learner.current_skills)}
- Self-reported interests: {', '.join(learner.interests)}

Deterministic Skill Gap Analysis:
{skills_summary_str}

Please generate a personalized, learner-friendly analysis containing:
1. A concise, encouraging summary of the learner's overall situation, explaining where they are strong and highlighting why the suggested path aligns with their career goal: "{learner.career_goal}".
2. For each skill with a gap, write a 1-2 sentence explanation of why this skill is critical for their specific learning goal: "{learner.learning_goal}" and career goal. If the measurement confidence is "low", acknowledge the limited diagnostic evidence in a supportive way.

You MUST respond strictly in the following JSON format:
{{
  "summary": "overall friendly summary string",
  "focus_reasons": {{
    "Skill Name 1": "contextual reason why this skill matters",
    "Skill Name 2": "contextual reason why this skill matters"
  }}
}}
"""

        system_instruction = (
            "You are a professional software architect and technical learning advisor. "
            "You must output your responses in the exact JSON format requested, mapping explanations only to the exact skills provided in the prompt. "
            "Do not invent any new skills."
        )

        res_text = self.llm_provider.generate_text(prompt, system_instruction)
        
        # Clean potential markdown JSON syntax wrapping
        if res_text.startswith("```json"):
            res_text = res_text[7:]
        if res_text.endswith("```"):
            res_text = res_text[:-3]
        res_text = res_text.strip()
        
        try:
            return json.loads(res_text)
        except Exception as e:
            logger.error(f"Failed to parse LLM response JSON: {e}. Raw response: {res_text}")
            return None
