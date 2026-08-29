# Architecture

Frontend -> FastAPI -> Services -> Agents/Repositories/Integrations -> Database/External APIs

## Main Pipeline
USER -> USER ONBOARDING -> DOMAIN SELECTION -> DIAGNOSTIC ASSESSMENT -> SKILL-WISE SCORING -> SKILL GAP AGENT -> PERSONALIZED LEARNING PATH AGENT -> RESOURCE CURATOR AGENT -> LEARNING -> MASTERY ASSESSMENT AGENT -> PASS / REMEDIATION -> PROGRESS TRACKING -> DASHBOARD

## Pipeline Flow (Phase 2 Detail)
1. **Onboarding**: Learner profile is captured (interests, goals, selected domain).
2. **Diagnostic Assessment**: Core 15 questions test assessing the 10 domain skills.
3. **Skill Gap Agent**: Performs a Hybrid deterministic/AI gap calculation:
   - Compares assessment score against configurable target requirements.
   - Computes gap scores and maps priority using a local prerequisite graph.
   - Generates fallback descriptions or optional Gemini summaries.
4. **Personalized Learning Path Agent (Future)**: Will consume `SkillGapResult` + `LearnerProfile` to construct the curriculum.

