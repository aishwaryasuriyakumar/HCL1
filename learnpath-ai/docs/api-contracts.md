# API Contracts
Contracts are implemented as Pydantic models in `backend/app/schemas/`.

## Skill Gap Module Contracts

### 1. SkillGapAgentInput
```json
{
  "learner": {
    "user_id": "UUID",
    "email": "string",
    "full_name": "string",
    "selected_domain": "string",
    "experience_level": "string",
    "learning_goal": "string",
    "career_goal": "string",
    "current_skills": ["string"],
    "interests": ["string"]
  },
  "assessment": {
    "attempt_id": "UUID",
    "domain": "string",
    "overall": {
      "score": 0.0,
      "proficiency": "string"
    },
    "skill_results": [
      {
        "skill": "string",
        "score": 0.0,
        "proficiency": "string",
        "confidence": "string"
      }
    ]
  }
}
```

### 2. SkillGapItem
```json
{
  "skill": "string",
  "current_score": 0.0,
  "current_proficiency": "string",
  "target_score": 0.0,
  "gap_score": 0.0,
  "severity": "string (strong | minor_gap | moderate_gap | high_gap | critical_gap)",
  "confidence": "string (low | medium | high)",
  "priority_score": 0.0,
  "priority": "string (low | medium | high | critical)",
  "prerequisites": ["string"],
  "reason": "string"
}
```

### 3. SkillGapResult
```json
{
  "analysis_id": "UUID",
  "user_id": "UUID",
  "assessment_attempt_id": "UUID",
  "domain": "string",
  "career_goal": "string",
  "learning_goal": "string",
  "overall_assessment_score": 0.0,
  "overall_proficiency": "string",
  "skills": ["SkillGapItem"],
  "strong_skills": ["string"],
  "minor_gaps": ["string"],
  "moderate_gaps": ["string"],
  "high_gaps": ["string"],
  "critical_gaps": ["string"],
  "recommended_focus": [
    {
      "order": 1,
      "skill": "string",
      "reason": "string"
    }
  ],
  "summary": "string",
  "generated_at": "datetime"
}
```

### 4. LearningPathAgentInput (Future)
```json
{
  "learner": "LearnerProfileResponse",
  "skill_gap": "SkillGapResult"
}
```
