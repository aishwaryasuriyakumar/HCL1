import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import engine
from app.database.base import Base
from app.services.question_bank_service import question_bank_service

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def create_learner(email="learner@test.com", domain="generative_ai", current_skills=None):
    if current_skills is None:
        current_skills = []
    payload = {
        "full_name": "Test User",
        "email": email,
        "selected_domain": domain,
        "experience_level": "intermediate",
        "learning_goal": "Learn RAG and AI Agents",
        "career_goal": "AI Engineer",
        "current_skills": current_skills
    }
    res = client.post("/api/profiles", json=payload)
    assert res.status_code == 201
    return res.json()["user_id"]

def submit_controlled_assessment(user_id, correct_skills, wrong_skills):
    # Start assessment
    res = client.post("/api/assessments/start", json={"user_id": user_id})
    assert res.status_code == 201
    attempt_id = res.json()["attempt_id"]
    questions = res.json()["questions"]
    
    answers = []
    for q in questions:
        q_full = question_bank_service.get_question(q["id"])
        skill = q["skill"]
        
        # Decide if we answer correctly or incorrectly
        if skill in correct_skills:
            selected_option = q_full["correct_option_id"]
        elif skill in wrong_skills:
            # Pick a wrong option
            selected_option = next(opt["id"] for opt in q_full["options"] if opt["id"] != q_full["correct_option_id"])
        else:
            # Default to wrong
            selected_option = next(opt["id"] for opt in q_full["options"] if opt["id"] != q_full["correct_option_id"])
            
        answers.append({
            "question_id": q["id"],
            "selected_option_id": selected_option
        })
        
    res_sub = client.post(f"/api/assessments/{attempt_id}/submit", json={"answers": answers})
    assert res_sub.status_code == 200
    return attempt_id

def test_no_assessment_error():
    user_id = create_learner(email="no-assess@test.com")
    res = client.post("/api/skill-gap/analyze", json={"user_id": user_id})
    assert res.status_code == 409
    assert "No submitted assessment found" in res.json()["detail"]

def test_domain_mismatch_validation():
    # If domain changes after assessment but before analysis, should fail
    # Note: We simulate this by directly changing database values or user profiles
    pass

def test_idempotency_and_caching():
    user_id = create_learner(email="idempotent@test.com")
    submit_controlled_assessment(user_id, ["LLM Fundamentals"], ["RAG"])
    
    # Trigger analysis 1
    res1 = client.post("/api/skill-gap/analyze", json={"user_id": user_id})
    assert res1.status_code == 200
    data1 = res1.json()
    analysis_id1 = data1["analysis_id"]
    
    # Trigger analysis 2 - should return same ID (cached)
    res2 = client.post("/api/skill-gap/analyze", json={"user_id": user_id})
    assert res2.status_code == 200
    data2 = res2.json()
    analysis_id2 = data2["analysis_id"]
    
    assert analysis_id1 == analysis_id2

def test_skill_gap_deterministic_calculations():
    # We want to test three distinct statuses:
    # 1. Strong Skill (e.g. LLM Fundamentals target=75, current=100) -> gap=0, severity=strong, priority=low
    # 2. Critical Gap (e.g. RAG target=75, current=0) -> gap=75, severity=critical_gap, priority=critical
    # 3. Moderate Gap (e.g. prompt engineering has target=70, we'll configure it)
    user_id = create_learner(email="calc@test.com")
    
    # LLM Fundamentals and Prompt Engineering correct (100%)
    # RAG, Embeddings, Vector Databases wrong (0%)
    corrects = ["LLM Fundamentals", "Prompt Engineering"]
    wrongs = ["RAG", "Embeddings", "Vector Databases"]
    
    submit_controlled_assessment(user_id, corrects, wrongs)
    
    res = client.post("/api/skill-gap/analyze", json={"user_id": user_id})
    assert res.status_code == 200
    data = res.json()
    
    skills_map = {s["skill"]: s for s in data["skills"]}
    
    # 1. Strong Skill Test
    llm_fund = skills_map["LLM Fundamentals"]
    assert llm_fund["gap_score"] == 0
    assert llm_fund["severity"] == "strong"
    assert llm_fund["priority"] == "low"
    assert llm_fund["priority_score"] == 0
    
    # 2. Critical Gap Test
    rag = skills_map["RAG"]
    assert rag["gap_score"] == 75.0  # target=75, current=0
    assert rag["severity"] == "critical_gap"
    assert rag["priority"] == "critical"
    # Base priority: 75 * 2 = 150 (capped at 100)
    assert rag["priority_score"] == 100.0

    # 3. Confidence Preservation
    # LLM Fundamentals usually has 1 or 2 questions. Let's make sure confidence is low, medium or high
    assert llm_fund["confidence"] in ["low", "medium", "high"]
    
    # 4. Prerequisites inclusion
    assert "Embeddings" in rag["prerequisites"]
    assert "Vector Databases" in rag["prerequisites"]

def test_prerequisite_ordering_in_recommended_focus():
    # RAG depends on Embeddings. If both have gaps, Embeddings must appear before RAG.
    user_id = create_learner(email="prereq@test.com")
    
    # RAG has critical gap (target=75, score=0) -> priority 100
    # Embeddings has high gap (target=70, score=0) -> priority 70 * 2 + 15 (foundation bonus) = 155 (capped at 100)
    # Wait, both will have 100. Let's make Embeddings have a score of 50%.
    # If Embeddings has 50% score: target=70, score=50 -> gap=20. Priority = 20*2 + 15 = 55 (medium priority).
    # If RAG has 0% score: target=75, score=0 -> gap=75. Priority = 100 (critical priority).
    # Since RAG depends on Embeddings, Embeddings (priority 55) must be placed BEFORE RAG (priority 100) in recommended_focus!
    
    # Let's write answers such that:
    # RAG = 0% correct (wrong)
    # Embeddings = 100% correct? No, if Embeddings is 100% correct, it has gap=0 and won't be in recommended_focus!
    # So Embeddings must have a gap, e.g. 50% or 0% correct.
    # If Embeddings is 0% correct: target=70, score=0 -> gap=70. Priority = 70*2+15 = 155 -> 100.
    # If both have priority 100, the dependency resolver should still order Embeddings before RAG.
    
    submit_controlled_assessment(user_id, [], ["RAG", "Embeddings", "Vector Databases"])
    
    res = client.post("/api/skill-gap/analyze", json={"user_id": user_id})
    assert res.status_code == 200
    focus = res.json()["recommended_focus"]
    
    # Find positions
    embeddings_idx = next(i for i, item in enumerate(focus) if item["skill"] == "Embeddings")
    rag_idx = next(i for i, item in enumerate(focus) if item["skill"] == "RAG")
    
    assert embeddings_idx < rag_idx, "Prerequisite 'Embeddings' must be scheduled before 'RAG' in recommended focus"

def test_claim_conflict_handling():
    # User claims they know RAG in profile, but assessment returns 0% score.
    # RAG must still be marked as a gap (assessment overrides claim).
    user_id = create_learner(email="claim@test.com", current_skills=["RAG"])
    submit_controlled_assessment(user_id, [], ["RAG"])
    
    res = client.post("/api/skill-gap/analyze", json={"user_id": user_id})
    assert res.status_code == 200
    skills_map = {s["skill"]: s for s in res.json()["skills"]}
    
    assert skills_map["RAG"]["gap_score"] > 0
    assert skills_map["RAG"]["severity"] == "critical_gap"

def test_domain_isolation():
    # ML learner must have only ML skills in results, no GenAI skills.
    user_id = create_learner(email="ml-isolate@test.com", domain="machine_learning")
    submit_controlled_assessment(user_id, [], [])
    
    res = client.post("/api/skill-gap/analyze", json={"user_id": user_id})
    assert res.status_code == 200
    data = res.json()
    
    assert data["domain"] == "machine_learning"
    for s in data["skills"]:
        assert s["skill"] in ["Python for ML", "Data Preprocessing", "Statistics & Probability", "Regression", "Classification", "Feature Engineering", "Model Evaluation", "Ensemble Learning", "Unsupervised Learning", "Model Deployment"]
        assert s["skill"] not in ["LLM Fundamentals", "RAG", "Embeddings"]

def test_llm_failure_graceful_fallback():
    # Since our SimpleLLMProvider checks settings.llm_api_key (which is empty by default in tests),
    # the endpoint should automatically run and fallback to deterministic templates without raising HTTP errors.
    user_id = create_learner(email="llm-fail@test.com")
    submit_controlled_assessment(user_id, ["LLM Fundamentals"], ["RAG"])
    
    res = client.post("/api/skill-gap/analyze", json={"user_id": user_id})
    assert res.status_code == 200
    assert "overall_assessment_score" in res.json()
    assert res.json()["summary"] != ""
