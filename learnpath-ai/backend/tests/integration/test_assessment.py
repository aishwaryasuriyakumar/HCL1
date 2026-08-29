import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import engine
from app.database.base import Base
from app.services.question_bank_service import question_bank_service

# Reset DB for tests
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

import uuid

@pytest.fixture
def test_user():
    # Create a user profile first
    unique_email = f"learner_{uuid.uuid4()}@assessment.com"
    payload = {
        "full_name": "Assessment Learner",
        "email": unique_email,
        "selected_domain": "generative_ai",
        "experience_level": "intermediate",
        "learning_goal": "Learn RAG",
        "career_goal": "AI Engineer"
    }
    response = client.post("/api/profiles", json=payload)
    assert response.status_code == 201
    return response.json()["user_id"]

def test_start_assessment_flow(test_user):
    # 1. Start assessment
    payload = {"user_id": test_user}
    res = client.post("/api/assessments/start", json=payload)
    assert res.status_code == 201
    data = res.json()
    
    assert "attempt_id" in data
    assert data["domain"] == "generative_ai"
    assert data["status"] == "in_progress"
    assert len(data["questions"]) == 15
    
    # 2. Verify security constraints: no correct answers or explanations leaked
    for q in data["questions"]:
        assert "correct_option_id" not in q
        assert "explanation" not in q
        assert len(q["options"]) == 4

    attempt_id = data["attempt_id"]
    
    # 3. Double start must resume the same attempt
    res_resume = client.post("/api/assessments/start", json=payload)
    assert res_resume.status_code == 201
    data_resume = res_resume.json()
    assert data_resume["attempt_id"] == attempt_id
    assert [q["id"] for q in data_resume["questions"]] == [q["id"] for q in data["questions"]]

    # 4. Get active attempt via GET /{attempt_id}
    res_get = client.get(f"/api/assessments/{attempt_id}")
    assert res_get.status_code == 200
    assert res_get.json()["attempt_id"] == attempt_id
    # Also verify correct answers are hidden on resume fetch
    for q in res_get.json()["questions"]:
        assert "correct_option_id" not in q
        assert "explanation" not in q

def test_invalid_submission_rules(test_user):
    payload = {"user_id": test_user}
    res = client.post("/api/assessments/start", json=payload)
    attempt_id = res.json()["attempt_id"]
    questions = res.json()["questions"]
    
    # Check that requesting results/review before submit fails with 409
    res_res = client.get(f"/api/assessments/{attempt_id}/result")
    assert res_res.status_code == 409
    res_rev = client.get(f"/api/assessments/{attempt_id}/review")
    assert res_rev.status_code == 409
    
    # Case A: Incomplete submission (only 14 answers)
    answers_14 = [{"question_id": q["id"], "selected_option_id": "A"} for q in questions[:-1]]
    res_sub = client.post(f"/api/assessments/{attempt_id}/submit", json={"answers": answers_14})
    assert res_sub.status_code == 422
    
    # Case B: Duplicate answers
    answers_dupe = [{"question_id": questions[0]["id"], "selected_option_id": "A"} for _ in range(15)]
    res_sub = client.post(f"/api/assessments/{attempt_id}/submit", json={"answers": answers_dupe})
    assert res_sub.status_code == 422
    
    # Case C: Invalid option ID (e.g. 'E')
    answers_invalid_opt = [{"question_id": q["id"], "selected_option_id": "A"} for q in questions]
    answers_invalid_opt[0]["selected_option_id"] = "E"
    res_sub = client.post(f"/api/assessments/{attempt_id}/submit", json={"answers": answers_invalid_opt})
    assert res_sub.status_code == 422
    
    # Case D: Question not assigned to attempt
    answers_unassigned = [{"question_id": q["id"], "selected_option_id": "A"} for q in questions]
    answers_unassigned[0]["question_id"] = "ml_python_001"  # ML question instead of GenAI
    res_sub = client.post(f"/api/assessments/{attempt_id}/submit", json={"answers": answers_unassigned})
    assert res_sub.status_code == 422

def test_successful_scoring_all_correct(test_user):
    # Start fresh attempt
    # Since active attempt is resumed, we can fetch it
    payload = {"user_id": test_user}
    res = client.post("/api/assessments/start", json=payload)
    attempt_id = res.json()["attempt_id"]
    questions = res.json()["questions"]
    
    # Generate 100% correct answers
    correct_answers = []
    for q in questions:
        q_full = question_bank_service.get_question(q["id"])
        correct_answers.append({
            "question_id": q["id"],
            "selected_option_id": q_full["correct_option_id"]
        })
        
    # Submit correct answers
    res_sub = client.post(f"/api/assessments/{attempt_id}/submit", json={"answers": correct_answers})
    assert res_sub.status_code == 200
    data = res_sub.json()
    
    # Verify overall results
    assert data["status"] == "submitted"
    assert data["overall"]["total_questions"] == 15
    assert data["overall"]["correct_answers"] == 15
    assert data["overall"]["incorrect_answers"] == 0
    assert data["overall"]["score"] == 100.00
    assert data["overall"]["proficiency"] == "Expert"
    
    # Verify all 10 skills are listed and graded as Expert
    assert len(data["skill_results"]) == 10
    for sr in data["skill_results"]:
        assert sr["score"] == 100.00
        assert sr["proficiency"] == "Expert"
        # Confidence should match length (either low (1 q) or medium (2 qs) or high (3+ qs))
        assert sr["confidence"] in ["low", "medium", "high"]

    # Verify duplicates block subsequent attempts
    res_sub_dupe = client.post(f"/api/assessments/{attempt_id}/submit", json={"answers": correct_answers})
    assert res_sub_dupe.status_code == 409  # Already submitted

    # Check GET /result works
    res_res = client.get(f"/api/assessments/{attempt_id}/result")
    assert res_res.status_code == 200
    assert res_res.json()["overall"]["score"] == 100.00

    # Check GET /review works and returns explanations/correct options
    res_rev = client.get(f"/api/assessments/{attempt_id}/review")
    assert res_rev.status_code == 200
    review_data = res_rev.json()
    assert len(review_data) == 15
    for item in review_data:
        assert item["is_correct"] is True
        assert item["explanation"] != ""
        assert item["correct_answer"]["id"] == item["selected_answer"]["id"]

    # Check GET /user/{user_id} history
    res_hist = client.get(f"/api/assessments/user/{test_user}")
    assert res_hist.status_code == 200
    history = res_hist.json()
    assert history["user_id"] == test_user
    assert len(history["attempts"]) == 1
    assert history["attempts"][0]["score"] == 100.00
    assert history["attempts"][0]["status"] == "submitted"
