# Development Guide

1. No feature should directly modify another team's agent.
2. Modules communicate using shared Pydantic contracts.
3. Do not duplicate domain definitions.
4. Do not calculate deterministic values with an LLM.
5. API keys stay only in backend environment variables.
6. Routes should remain thin.
7. Business logic goes in services.
8. Database access goes through repositories where useful.
9. Intelligent reasoning belongs in agents.
10. External platform/API code goes in integrations.

## Setup Backend
cd backend
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload

## Run Tests
pytest

## Setup Frontend
cd frontend
npm install
npm run dev
