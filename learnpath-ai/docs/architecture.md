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
Gemini LLM (Dynamic Phase & Objective Grouping)
      ↓
LearningPathResult (Validated & Topologically Ordered)
      ↓
Resource Curator Agent (Discovers, Validates, Ranks, Explains)
      ↓
Public Resource Providers (YouTube, freeCodeCamp, Official Docs, MIT OCW)
      ↓
Original Platform URLs & Card Data (No content proxying or mirroring)
      ↓
Frontend Navigation ("Start Learning" -> Opens Original Platform)
      ↓
Future Mastery Agent
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
