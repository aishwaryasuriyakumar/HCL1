import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_multiple_learning_paths_and_completion_logic():
    # 1. Create a learner profile
    res_profile = client.post("/api/profiles", json={
        "full_name": "Multi Path Learner",
        "email": "multipath@example.com",
        "selected_domain": "data_science",
        "experience_level": "intermediate",
        "learning_goal": "Master Data Science",
        "career_goal": "Data Scientist"
    })
    assert res_profile.status_code == 201
    user_id = res_profile.json()["user_id"]

    # 2. Take assessment for data_science
    res_start = client.post("/api/assessments/start", json={"user_id": user_id})
    assert res_start.status_code == 201
    attempt_id = res_start.json()["attempt_id"]
    questions = res_start.json()["questions"]

    res_sub = client.post(f"/api/assessments/{attempt_id}/submit", json={
        "answers": [{"question_id": q["id"], "selected_option_id": "A"} for q in questions]
    })
    assert res_sub.status_code == 200

    # 3. Analyze skill gap
    res_gap = client.post("/api/skill-gap/analyze", json={"user_id": user_id})
    assert res_gap.status_code == 200

    # 4. Generate first path (Data Science)
    res_path1 = client.post("/api/learning-paths/generate", json={"user_id": user_id})
    assert res_path1.status_code == 200
    path1_id = res_path1.json()["path_id"]

    # 5. Fetch all paths for the user
    res_all_1 = client.get(f"/api/learning-paths/user/{user_id}")
    assert res_all_1.status_code == 200
    paths_data1 = res_all_1.json()
    assert paths_data1["user_id"] == user_id
    assert len(paths_data1["paths"]) == 1
    p1_summary = paths_data1["paths"][0]
    assert p1_summary["path_id"] == path1_id
    assert p1_summary["completed_phases"] == 0
    assert p1_summary["total_phases"] > 0
    assert p1_summary["progress_percentage"] == 0.0

    # 6. Update profile to Machine Learning and generate second path
    client.put(f"/api/profiles/{user_id}", json={
        "selected_domain": "machine_learning",
        "learning_goal": "Master Machine Learning",
        "career_goal": "ML Engineer"
    })

    res_start_ml = client.post("/api/assessments/start", json={"user_id": user_id})
    assert res_start_ml.status_code == 201
    attempt_ml_id = res_start_ml.json()["attempt_id"]
    questions_ml = res_start_ml.json()["questions"]

    res_sub_ml = client.post(f"/api/assessments/{attempt_ml_id}/submit", json={
        "answers": [{"question_id": q["id"], "selected_option_id": "A"} for q in questions_ml]
    })
    assert res_sub_ml.status_code == 200

    client.post("/api/skill-gap/analyze", json={"user_id": user_id})
    res_path2 = client.post("/api/learning-paths/generate", json={"user_id": user_id})
    assert res_path2.status_code == 200
    path2_id = res_path2.json()["path_id"]
    assert path2_id != path1_id

    # 7. Fetch all paths for the user - verify BOTH paths exist!
    res_all_2 = client.get(f"/api/learning-paths/user/{user_id}")
    assert res_all_2.status_code == 200
    paths_data2 = res_all_2.json()
    assert len(paths_data2["paths"]) == 2
    path_ids = [p["path_id"] for p in paths_data2["paths"]]
    assert path1_id in path_ids
    assert path2_id in path_ids
