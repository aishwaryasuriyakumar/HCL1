from fastapi.testclient import TestClient
from app.main import app
from app.database.session import engine
from app.database.base import Base

# Setup DB for tests
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_get_domains():
    response = client.get("/api/domains")
    assert response.status_code == 200
    data = response.json()
    assert "domains" in data
    assert len(data["domains"]) == 5
    
    domain_ids = [d["id"] for d in data["domains"]]
    assert "generative_ai" in domain_ids
    assert "machine_learning" in domain_ids
    
    # check skills count for gen AI
    gen_ai = next(d for d in data["domains"] if d["id"] == "generative_ai")
    assert len(gen_ai["skills"]) == 10

def test_get_domain_by_id():
    response = client.get("/api/domains/generative_ai")
    assert response.status_code == 200
    assert response.json()["id"] == "generative_ai"

def test_get_invalid_domain():
    response = client.get("/api/domains/invalid_domain")
    assert response.status_code == 404

def test_create_profile():
    payload = {
        "full_name": "Demo User",
        "email": "demo@example.com",
        "selected_domain": "generative_ai",
        "experience_level": "intermediate",
        "learning_goal": "Learn RAG and AI agents",
        "career_goal": "Become an AI Engineer",
        "current_skills": ["Python", "Machine Learning"]
    }
    response = client.post("/api/profiles", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "Demo User"
    assert data["selected_domain"]["id"] == "generative_ai"
    assert "user_id" in data
    
    return data["user_id"]

def test_create_profile_duplicate_email():
    payload = {
        "full_name": "Demo User 2",
        "email": "demo@example.com",
        "selected_domain": "generative_ai",
        "experience_level": "beginner",
        "learning_goal": "goal",
        "career_goal": "goal",
    }
    response = client.post("/api/profiles", json=payload)
    assert response.status_code == 409

def test_create_profile_invalid_domain():
    payload = {
        "full_name": "Demo User 3",
        "email": "demo3@example.com",
        "selected_domain": "invalid_domain",
        "experience_level": "beginner",
        "learning_goal": "goal",
        "career_goal": "goal",
    }
    response = client.post("/api/profiles", json=payload)
    assert response.status_code == 422 # Pydantic validation error

def test_get_profile():
    # first create one
    payload = {
        "full_name": "Get User",
        "email": "get@example.com",
        "selected_domain": "data_science",
        "experience_level": "beginner",
        "learning_goal": "Learn DS",
        "career_goal": "Data Scientist"
    }
    response = client.post("/api/profiles", json=payload)
    user_id = response.json()["user_id"]
    
    # now get it
    get_res = client.get(f"/api/profiles/{user_id}")
    assert get_res.status_code == 200
    assert get_res.json()["email"] == "get@example.com"
    assert get_res.json()["selected_domain"]["id"] == "data_science"

def test_update_profile():
    # first create one
    payload = {
        "full_name": "Update User",
        "email": "update@example.com",
        "selected_domain": "web_development",
        "experience_level": "beginner",
        "learning_goal": "Learn React",
        "career_goal": "Frontend Dev"
    }
    response = client.post("/api/profiles", json=payload)
    user_id = response.json()["user_id"]
    
    # now update it
    update_payload = {
        "full_name": "Updated Name",
        "experience_level": "advanced",
        "projects": [
            {
                "name": "My App",
                "technologies": ["React", "TS"]
            }
        ]
    }
    put_res = client.put(f"/api/profiles/{user_id}", json=update_payload)
    assert put_res.status_code == 200
    data = put_res.json()
    assert data["full_name"] == "Updated Name"
    assert data["experience_level"] == "advanced"
    assert len(data["projects"]) == 1
    assert data["projects"][0]["name"] == "My App"
