# Architecture

Frontend -> FastAPI -> Services -> Agents/Repositories/Integrations -> Database/External APIs

## Main Pipeline
USER -> USER ONBOARDING -> DOMAIN SELECTION -> DIAGNOSTIC ASSESSMENT -> SKILL-WISE SCORING -> SKILL GAP AGENT -> PERSONALIZED LEARNING PATH AGENT -> RESOURCE CURATOR AGENT -> LEARNING -> MASTERY ASSESSMENT AGENT -> PASS / REMEDIATION -> PROGRESS TRACKING -> DASHBOARD

## Detailed Data Pipeline Flow
```
LearnerProfile 
      ↓
AssessmentResult 
      ↓
SkillGapResult 
      ↓
Skill Knowledge (Prerequisites & Domain Rules)
      ↓
Learning Path Agent
      ↓
Gemini LLM / Fallback (Dynamic Phase & Objective Grouping)
      ↓
LearningPathResult (Validated & Topologically Ordered)
      ↓
Current Phase Learning
      ↓
Learner Marks Phase Complete
      ↓
Mastery Assessment (POST /api/mastery/start)
      ↓
Backend Scores Assessment Deterministically
      ↓
Mastery Agent Evaluates Result (MasteryResult)
      ↓
   PASS / FAIL
      ↓
PASS → Unlock Next Phase (status: available) & Complete Current Phase
FAIL → Identify Weak Topics (< 60%) & Set Remediation Required
      ↓
Remediation Completed (POST /api/mastery/{attempt_id}/remediation-complete)
      ↓
Retest (Attempt increments, prioritizes weak topics)
      ↓
Pass → Unlock Next Phase (or Learning Path Completed if final phase)
      ↓
Progress Tracking / Dashboard
```

### Dynamic Path Generation Principles
The system does **NOT** use pre-built learning paths (e.g. `generative_ai_learning_path.json`). Instead:
1. **Configured Knowledge**: Domain skills, difficulty, target proficiency, and prerequisite graphs are stored as domain knowledge in `backend/app/data/skill_requirements.py`.
2. **Generated Intelligence**: The Learning Path Agent passes learner context, specific skill gaps, and domain prerequisites to Gemini. The LLM dynamically constructs phase titles, phase descriptions, project assignments, effort estimates, and personalized recommendation explanations.
3. **Deterministic Validation**: The backend independently validates generated skills against domain isolation boundaries, normalizes effort hours, enforces prerequisite dependency ordering via topological sorting, and sets phase availability statuses (`Phase 1` = `available`, subsequent phases = `locked`).

### Resource Curator Agent Principles
1. **Original Platform Navigation**: The system does NOT host, copy, mirror, or proxy learning content. The backend strictly stores and returns original platform URLs (`original_url`) so the learner navigates directly to the original learning platform (e.g., YouTube, freeCodeCamp, official docs, MIT OCW) in a new browser tab.
2. **Public Access Compliance**: Queries only public APIs, public structured data, public documentation, and public curriculum metadata. Does not bypass paywalls, require user logins, or harvest credentials.
3. **Multi-Factor Scoring & Format Diversity**: Deterministically ranks candidates across 7 factors (relevance 40%, quality 15%, rating 10%, review confidence 10%, freshness 10%, level match 10%, platform reliability 5%) and selects a balanced mix of video, documentation, interactive, and course formats.
4. **No LLM URL Hallucination**: All factual metadata and URLs originate strictly from verified provider adapters. Gemini LLM is used ONLY to evaluate semantic fit and generate personalized `why_recommended` explanations.

### Mastery Assessment Agent Principles
1. **Deterministic Backend Scoring**: Scoring is calculated strictly on the backend. The overall passing threshold is 75% (`MASTERY_PASS_THRESHOLD`), and topic mastery threshold is 60% (`TOPIC_MASTERY_THRESHOLD`).
2. **Phase Topic Alignment**: Mastery tests evaluate precisely the topics and skills defined in the current phase.
3. **Information Security**: Before submission, answers and explanations are completely stripped. Full reviews are accessible only after valid submission.
4. **Phase Progression Boundary**: When a learner passes, `MasteryService` calls `LearningPathService.complete_phase` and `LearningPathService.unlock_next_phase` to update existing phase statuses atomically without regenerating the path.
5. **Remediation & Retest Weighted Coverage**: If a learner fails, weak topics (`< 60%`) are pinpointed. Once marked complete, retesting prioritizes weak topics while still assessing the full phase with varied questions.
