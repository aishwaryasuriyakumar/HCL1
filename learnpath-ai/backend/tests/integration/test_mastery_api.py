import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import engine
from app.database.base import Base
from app.services.question_bank_service import question_bank_service
from app.services.mastery_question_service import mastery_question_service
from app.core.constants import (
    MASTERY_PASS_THRESHOLD,
    TOPIC_MASTERY_THRESHOLD,
    ACTION_UNLOCK_NEXT_PHASE,
    ACTION_REMEDIATION_REQUIRED,
    ACTION_LEARNING_PATH_COMPLETED,
)

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def setup_learner_with_learning_path(domain="generative_ai"):
    # 1. Create Profile
    profile_payload = {
        "full_name": "Mastery Tester",
        "email": "mastery_tester@example.com",
        "selected_domain": domain,
        "experience_level": "beginner",
        "learning_goal": "Master Generative AI and RAG",
        "career_goal": "AI Engineer",
        "current_skills": []
    }
    res = client.post("/api/profiles", json=profile_payload)
    assert res.status_code == 201
    user_id = res.json()["user_id"]

    # 2. Complete Diagnostic Assessment
    res_diag_start = client.post("/api/assessments/start", json={"user_id": user_id})
    assert res_diag_start.status_code == 201
    attempt_id = res_diag_start.json()["attempt_id"]
    diag_questions = res_diag_start.json()["questions"]

    diag_answers = []
    for q in diag_questions:
        q_full = question_bank_service.get_question(q["id"])
        diag_answers.append({
            "question_id": q["id"],
            "selected_option_id": q_full["correct_option_id"]
        })
    res_diag_sub = client.post(f"/api/assessments/{attempt_id}/submit", json={"answers": diag_answers})
    assert res_diag_sub.status_code == 200

    # 3. Analyze Skill Gap
    res_gap = client.post("/api/skill-gap/analyze", json={"user_id": user_id})
    assert res_gap.status_code == 200

    # 4. Generate Learning Path
    res_path = client.post("/api/learning-paths/generate", json={"user_id": user_id})
    assert res_path.status_code == 200
    path_data = res_path.json()
    assert len(path_data["phases"]) >= 2

    return user_id, path_data

def test_mastery_full_flow_fail_remediate_retest_and_unlock():
    user_id, path_data = setup_learner_with_learning_path()

    phase_1 = path_data["phases"][0]
    phase_2 = path_data["phases"][1]
    phase_1_id = phase_1["phase_id"]
    phase_2_id = phase_2["phase_id"]

    assert phase_1["status"] in ["available", "in_progress"]
    assert phase_2["status"] == "locked"

    # 1. Start Mastery Assessment for Phase 1
    start_payload = {
        "user_id": user_id,
        "phase_id": phase_1_id
    }
    res_start = client.post("/api/mastery/start", json=start_payload)
    assert res_start.status_code == 201
    start_data = res_start.json()
    attempt_id = start_data["mastery_attempt_id"]
    questions = start_data["questions"]

    assert start_data["attempt_number"] == 1
    assert len(questions) == 10

    # Verify no answer keys are leaked in questions
    for q in questions:
        assert "correct_option_id" not in q
        assert "explanation" not in q
        assert "is_correct" not in q
        assert len(q["options"]) >= 2

    # Verify 409 when trying to get result before submission
    res_early_result = client.get(f"/api/mastery/{attempt_id}/result")
    assert res_early_result.status_code == 409

    # Verify 409 when trying to get review before submission
    res_early_review = client.get(f"/api/mastery/{attempt_id}/review")
    assert res_early_review.status_code == 409

    # 2. Submit FAILING Assessment (5 correct, 5 wrong = 50%)
    answers_fail = []
    for i, q in enumerate(questions):
        qid = q.get("question_id") or q.get("id")
        full_q = mastery_question_service.get_question_by_id(path_data["domain"], qid)
        correct_opt = full_q["correct_option_id"]
        wrong_opt = next(opt["id"] for opt in full_q["options"] if opt["id"] != correct_opt)

        selected = correct_opt if i < 5 else wrong_opt
        answers_fail.append({
            "question_id": qid,
            "selected_option_id": selected
        })

    res_submit_fail = client.post(
        f"/api/mastery/{attempt_id}/submit",
        json={"answers": answers_fail}
    )
    assert res_submit_fail.status_code == 200
    fail_result = res_submit_fail.json()

    assert fail_result["score"] == 50.0
    assert fail_result["passed"] is False
    assert fail_result["next_action"] == ACTION_REMEDIATION_REQUIRED
    assert len(fail_result["weak_topics"]) > 0

    # Verify learning path phase 2 remains locked after failure
    res_path_check = client.get(f"/api/learning-paths/user/{user_id}")
    assert res_path_check.status_code == 200
    data_check = res_path_check.json()
    current_phases = data_check.get("phases") or data_check["paths"][0]["phases"]
    assert current_phases[0]["phase_id"] == phase_1_id
    assert current_phases[1]["phase_id"] == phase_2_id
    assert current_phases[1]["status"] == "locked"

    # Verify Review endpoint returns full explanations after submission
    res_review = client.get(f"/api/mastery/{attempt_id}/review")
    assert res_review.status_code == 200
    review_data = res_review.json()
    assert review_data["score"] == 50.0
    assert review_data["passed"] is False
    assert len(review_data["questions"]) == 10
    for r_item in review_data["questions"]:
        assert "explanation" in r_item and len(r_item["explanation"]) > 0
        assert "correct_option_id" in r_item

    # Verify attempt cannot be re-submitted (409 Conflict)
    res_resubmit = client.post(
        f"/api/mastery/{attempt_id}/submit",
        json={"answers": answers_fail}
    )
    assert res_resubmit.status_code == 409

    # 3. Mark Remediation Complete
    res_remed = client.post(f"/api/mastery/{attempt_id}/remediation-complete")
    assert res_remed.status_code == 200
    assert res_remed.json()["next_action"] == "retest_required"

    # 4. Start Retest (Attempt 2)
    res_start_retest = client.post("/api/mastery/start", json=start_payload)
    assert res_start_retest.status_code == 201
    retest_data = res_start_retest.json()
    retest_attempt_id = retest_data["mastery_attempt_id"]
    retest_questions = retest_data["questions"]

    assert retest_attempt_id != attempt_id
    assert retest_data["attempt_number"] == 2
    assert len(retest_questions) == 10

    # 5. Submit PASSING Assessment on Retest (8 correct, 2 wrong = 80%)
    answers_pass = []
    for i, q in enumerate(retest_questions):
        qid = q.get("question_id") or q.get("id")
        full_q = mastery_question_service.get_question_by_id(path_data["domain"], qid)
        correct_opt = full_q["correct_option_id"]
        wrong_opt = next(opt["id"] for opt in full_q["options"] if opt["id"] != correct_opt)

        selected = correct_opt if i < 8 else wrong_opt
        answers_pass.append({
            "question_id": qid,
            "selected_option_id": selected
        })

    res_submit_pass = client.post(
        f"/api/mastery/{retest_attempt_id}/submit",
        json={"answers": answers_pass}
    )
    assert res_submit_pass.status_code == 200
    pass_result = res_submit_pass.json()

    assert pass_result["score"] == 80.0
    assert pass_result["passed"] is True
    assert pass_result["next_action"] == ACTION_UNLOCK_NEXT_PHASE

    # 6. Verify Phase 1 is Completed and Phase 2 is Unlocked ("available")!
    res_path_unlocked = client.get(f"/api/learning-paths/user/{user_id}")
    assert res_path_unlocked.status_code == 200
    data_unlocked = res_path_unlocked.json()
    updated_phases = data_unlocked.get("phases") or data_unlocked["paths"][0]["phases"]
    assert updated_phases[0]["status"] == "completed"
    assert updated_phases[1]["status"] == "available"

    # 7. Verify History endpoint
    res_hist = client.get(f"/api/mastery/user/{user_id}/phase/{phase_1_id}")
    assert res_hist.status_code == 200
    history = res_hist.json()
    assert len(history) == 2
    assert history[0]["attempt_number"] == 1
    assert history[0]["passed"] is False
    assert history[1]["attempt_number"] == 2
    assert history[1]["passed"] is True

def test_mastery_locked_phase_rejected():
    user_id, path_data = setup_learner_with_learning_path()
    phase_2_id = path_data["phases"][1]["phase_id"]

    # Attempting to start mastery on locked Phase 2
    res = client.post("/api/mastery/start", json={"user_id": user_id, "phase_id": phase_2_id})
    assert res.status_code == 400
    assert "locked" in res.json()["detail"]

def test_mastery_validation_errors():
    user_id, path_data = setup_learner_with_learning_path()
    phase_1_id = path_data["phases"][0]["phase_id"]

    # 1. Non-existent learner
    fake_user = str(uuid.uuid4())
    res_fake_user = client.post("/api/mastery/start", json={"user_id": fake_user, "phase_id": phase_1_id})
    assert res_fake_user.status_code == 404

    # 2. Non-existent phase
    res_fake_phase = client.post("/api/mastery/start", json={"user_id": user_id, "phase_id": "nonexistent_phase_99"})
    assert res_fake_phase.status_code == 404

    # 3. Start valid attempt
    res_start = client.post("/api/mastery/start", json={"user_id": user_id, "phase_id": phase_1_id})
    assert res_start.status_code == 201
    attempt_id = res_start.json()["mastery_attempt_id"]
    questions = res_start.json()["questions"]

    # 4. Duplicate answers
    q0_id = questions[0].get("question_id") or questions[0].get("id")
    dup_answers = [
        {"question_id": q0_id, "selected_option_id": "A"},
        {"question_id": q0_id, "selected_option_id": "B"}
    ]
    res_dup = client.post(f"/api/mastery/{attempt_id}/submit", json={"answers": dup_answers})
    assert res_dup.status_code == 400
    assert "Duplicate" in res_dup.json()["detail"]

    # 5. Incomplete answers
    partial_answers = [
        {"question_id": q0_id, "selected_option_id": "A"}
    ]
    res_part = client.post(f"/api/mastery/{attempt_id}/submit", json={"answers": partial_answers})
    assert res_part.status_code == 400
    assert "Missing answers" in res_part.json()["detail"]

def test_mastery_final_phase_completion():
    user_id, path_data = setup_learner_with_learning_path()
    phases = path_data["phases"]
    final_phase = phases[-1]
    final_phase_id = final_phase["phase_id"]

    # Manually unlock the final phase for test
    from app.services.learning_path_service import learning_path_service
    from app.database.session import SessionLocal
    db = SessionLocal()
    try:
        db_path = learning_path_service.get_path_model(db, path_data["path_id"])
        path_dict = dict(db_path.path_json)
        for p in path_dict["phases"]:
            p["status"] = "available"
        db_path.path_json = path_dict
        from sqlalchemy.orm.attributes import flag_modified
        flag_modified(db_path, "path_json")
        db.commit()
    finally:
        db.close()

    # Start assessment on final phase
    res_start = client.post("/api/mastery/start", json={"user_id": user_id, "phase_id": final_phase_id})
    assert res_start.status_code == 201
    attempt_id = res_start.json()["mastery_attempt_id"]
    questions = res_start.json()["questions"]

    # Submit 100% correct answers
    answers_pass = []
    for q in questions:
        qid = q.get("question_id") or q.get("id")
        full_q = mastery_question_service.get_question_by_id(path_data["domain"], qid)
        answers_pass.append({
            "question_id": qid,
            "selected_option_id": full_q["correct_option_id"]
        })

    res_submit = client.post(f"/api/mastery/{attempt_id}/submit", json={"answers": answers_pass})
    assert res_submit.status_code == 200
    res_data = res_submit.json()

    assert res_data["passed"] is True
    assert res_data["score"] == 100.0
    assert res_data["next_action"] == ACTION_LEARNING_PATH_COMPLETED
