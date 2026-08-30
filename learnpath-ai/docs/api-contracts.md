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

---

## Mastery Assessment Module Contracts

### 1. MasteryAgentInput
```json
{
  "user_id": "UUID",
  "learning_path_id": "UUID",
  "phase": {
    "phase_id": "phase_01",
    "order": 1,
    "title": "Retrieval-Augmented Generation",
    "skills": ["RAG"],
    "resource_topics": ["Chunking", "Embeddings", "Retrieval", "Context Injection"],
    "status": "available"
  },
  "assessment_result": {}
}
```

### 2. MasteryTopicResult
```json
{
  "topic": "Chunking",
  "questions_attempted": 3,
  "correct_answers": 3,
  "score": 100.0,
  "status": "mastered (mastered | needs_improvement)"
}
```

### 3. MasteryResult
```json
{
  "mastery_attempt_id": "UUID",
  "user_id": "UUID",
  "learning_path_id": "UUID",
  "phase_id": "phase_01",
  "phase_title": "Retrieval-Augmented Generation",
  "score": 80.0,
  "pass_threshold": 75.0,
  "passed": true,
  "topic_results": [
    {
      "topic": "Chunking",
      "questions_attempted": 2,
      "correct_answers": 2,
      "score": 100.0,
      "status": "mastered"
    },
    {
      "topic": "Retrieval",
      "questions_attempted": 3,
      "correct_answers": 2,
      "score": 66.67,
      "status": "mastered"
    }
  ],
  "weak_topics": [],
  "next_action": "unlock_next_phase (unlock_next_phase | remediation_required | retest_required | learning_path_completed)",
  "attempt_number": 1,
  "submitted_at": "2026-08-30T10:00:00Z",
  "explanation": "Congratulations! You scored 80.0%, exceeding the required 75.0% mastery threshold."
}
```

### 4. RemediationRequest
```json
{
  "user_id": "UUID",
  "phase_id": "phase_01",
  "domain": "generative_ai",
  "weak_topics": [
    "Chunking",
    "Retrieval"
  ]
}
```
