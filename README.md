# LearnPath AI

## AI-Powered Personalized Learning Path Recommender

LearnPath AI is an AI-powered personalized learning assistant that analyzes a learner's background, interests, skills, projects, certifications, learning goals, and career objectives to identify skill gaps and generate a personalized learning journey.

Instead of simply recommending individual courses, the system creates a structured roadmap consisting of learning phases, resources, practical projects, assessments, and milestones.

---

## 🚀 Features

- Personalized learner onboarding
- Domain-specific goal selection
- Domain and goal-specific skill assessment
- AI-powered skill gap analysis
- Dynamic personalized learning path generation
- Prerequisite-aware learning phases
- Learning resource curation
- Public resource recommendations with external navigation
- Explainable recommendations
- Phase-wise mastery assessment
- Learning phase unlocking
- Remediation and retesting
- Progress tracking
- Personalized learning dashboard
- Multi-agent AI architecture

---

## 🎯 Problem Statement

Online learning platforms provide thousands of courses and resources, but learners often struggle to determine:

- What they already know
- What they need to learn
- Which skills they are missing
- What they should learn first
- Which resources are suitable for their level
- Whether they have actually understood a topic
- What they should learn next

A one-size-fits-all learning path is ineffective because learners have different experience levels, skills, interests, goals, and learning preferences.

LearnPath AI addresses this problem by creating a personalized, goal-oriented learning journey for every learner.

---

# 💡 Solution

The application follows this pipeline:

```text
Learner
   ↓
User Onboarding
   ↓
Domain Selection
   ↓
Goal Selection
   ↓
Skill Assessment
   ↓
Skill Gap Analysis
   ↓
Dynamic Learning Path
   ↓
Resource Curation
   ↓
Learning
   ↓
Mastery Assessment
   ↓
Phase Unlock / Remediation
   ↓
Progress Tracking
   ↓
Dashboard
```

---

# 🧠 Multi-Agent Architecture

```text
                    ┌──────────────┐
                    │    Learner   │
                    └──────┬───────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Assessment Agent  │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │  Skill Gap Agent  │
                 └─────────┬─────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │  Learning Path Agent    │
              └────────────┬────────────┘
                           │
                           ▼
             ┌──────────────────────────┐
             │ Resource Curator Agent   │
             └────────────┬─────────────┘
                          │
                          ▼
                       Learning
                          │
                          ▼
                ┌────────────────────┐
                │   Mastery Agent    │
                └─────────┬──────────┘
                          │
                    ┌─────┴─────┐
                    │           │
                   PASS        FAIL
                    │           │
                    ▼           ▼
              Next Phase    Remediation
                                │
                                ▼
                              Retest
                                │
                                ▼
                         Progress Dashboard
```

---

# 🤖 Agents

## 1. Assessment Agent

Conducts a personalized assessment based on:

- Selected domain
- Target learning goal
- Experience level
- Existing skills

It evaluates the learner's current proficiency.

## 2. Skill Gap Agent

Analyzes assessment results and identifies:

- Existing strengths
- Weak skills
- Missing skills
- Skill gaps
- Priority skills
- Required prerequisites

## 3. Learning Path Agent

Generates a dynamic learning roadmap using:

```text
Learner Profile
+
Domain
+
Goal
+
Assessment Results
+
Skill Gap Analysis
+
Prerequisites
```

The path is generated dynamically rather than using one static roadmap for every learner.

## 4. Resource Curator Agent

Finds and ranks learning resources according to:

- Relevance
- Learner level
- Topic
- Quality
- Rating
- Reviews
- Freshness
- Platform reliability
- Accessibility

The application provides the original public resource URL so learners can navigate to the external platform.

## 5. Mastery Agent

Conducts an assessment after a learner completes a learning phase.

It determines:

- Whether the learner understood the module
- Mastery score
- Weak topics
- Pass/fail status
- Whether the next phase should be unlocked

---

# 🌐 Supported Domains

The current application supports five domains:

| Domain | Identifier |
|---|---|
| Machine Learning | `machine_learning` |
| Data Science | `data_science` |
| Generative AI | `generative_ai` |
| Web Development | `web_development` |
| Cloud & DevOps | `cloud_devops` |

The architecture can be extended with additional domains.

---

# 🎯 Goal-Aware Personalization

The learner first selects a domain and then provides a goal within that domain.

For example:

```text
Domain:
Cloud & DevOps

Goal:
Become a Cloud Engineer
```

The selected goal is passed to the assessment and learning-path pipeline.

Two learners selecting the same domain can therefore receive different learning paths based on their goals, skills, and assessment results.

---

# 📋 User Onboarding

The learner provides:

- Full name
- Email
- Selected domain
- Experience level
- Years of experience
- Learning goal
- Career goal
- Current skills
- Interests
- Projects
- Certifications
- Completed courses
- GitHub repository links
- Deployed project links
- Certification links
- Preferred learning formats
- Daily learning time

This information is used throughout the personalization pipeline.

---

# 📝 Skill Assessment

The assessment engine uses domain-specific and goal-relevant questions.

```text
Selected Domain
       +
Target Goal
       +
Learner Background
       ↓
Personalized Assessment
       ↓
Assessment Results
```

The objective is to determine the learner's current proficiency before generating the learning path.

---

# 📊 Skill Gap Analysis

The Skill Gap Agent compares:

```text
Current Skill Level
        vs
Required Skill Level
```

and produces a structured skill-gap report.

Example:

```text
Skill               Current     Required     Gap
---------------------------------------------------
Python              Advanced    Advanced     None
ML Fundamentals     Intermediate Advanced    Medium
Deep Learning       Beginner    Advanced     High
MLOps               Beginner    Intermediate High
Deployment          Beginner    Intermediate High
```

---

# 🗺️ Dynamic Learning Path

The Learning Path Agent generates phases based on the learner's individual requirements.

Each phase can contain:

- Phase title
- Description
- Skills
- Topics
- Learning objectives
- Prerequisites
- Estimated effort
- Practical project
- Recommended resources
- Completion status

The exact path depends on the learner's profile, goal, and skill gaps.

---

# 📚 Resource Curation

The Resource Curator Agent follows a provider-adapter architecture.

```text
                 Resource Curator
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
    Provider A      Provider B      Provider C
        │               │               │
        └───────────────┼───────────────┘
                        ▼
                Normalized Resources
                        │
                        ▼
                  Ranked Resources
```

This allows new resource providers to be added without modifying the core recommendation logic.

Only publicly accessible resources are recommended, and the system navigates the learner to the original external resource.

---

# 🧪 Mastery-Based Progression

After completing a learning phase:

```text
Complete Phase
      ↓
Take Mastery Assessment
      ↓
Evaluate Understanding
      ↓
Calculate Score
      ↓
Determine Mastery
```

If the learner passes, the next phase is unlocked.

If the learner fails, weak topics are identified and remediation and retesting can be provided.

---

# 📈 Dashboard

The dashboard displays:

- Overall learning progress
- Completed phases
- Current phase
- Locked phases
- Mastery scores
- Assessment attempts
- Skill development
- Weak topics
- Learning speed
- Remaining modules
- Recommended next action

---

# 🏗️ Technology Stack

## Frontend

- React
- TypeScript
- Vite
- React Router
- Axios
- Lucide React

## Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- SQLite
- HTTPX
- python-dotenv

## AI

- Google Gemini
- Google GenAI SDK
- Structured LLM outputs

## Testing

- Pytest
- FastAPI TestClient

---

# 📁 Project Structure

```text
HCL1/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── assessment_agent.py
│   │   │   ├── skill_gap_agent.py
│   │   │   ├── learning_path_agent.py
│   │   │   ├── resource_curator_agent.py
│   │   │   └── mastery_agent.py
│   │   │
│   │   ├── api/
│   │   ├── core/
│   │   ├── data/
│   │   ├── database/
│   │   ├── integrations/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.*
│
├── docs/
│
└── README.md
```

---

# 🔄 Backend Architecture

```text
HTTP Request
     ↓
FastAPI Routes
     ↓
Pydantic Validation
     ↓
Application Services
     ↓
AI Agents
     ↓
Repositories / Integrations
     ↓
Database / External APIs
```

---

# 🔗 Agent Communication

```text
Learner Profile
      ↓
Assessment Agent
      ↓
Assessment Result
      ↓
Skill Gap Agent
      ↓
Skill Gap Result
      ↓
Learning Path Agent
      ↓
Learning Path
      ↓
Resource Curator Agent
      ↓
Learning Resources
      ↓
Mastery Agent
      ↓
Mastery Result
      ↓
Progress Service
      ↓
Dashboard
```

---

# 🗄️ Database

The application uses:

```text
SQLite
+
SQLAlchemy
```

The database stores information related to:

- Learners
- Assessments
- Questions
- Answers
- Skill gaps
- Learning paths
- Learning phases
- Resources
- Mastery assessments
- Assessment attempts
- Progress

---

# 🔌 API

The backend exposes REST APIs through FastAPI.

Major API areas include:

```text
/api/health
/api/domains
/api/profiles
/api/assessments
/api/skill-gaps
/api/learning-paths
/api/resources
/api/mastery
/api/progress
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🤖 LLM Architecture

```text
Agent
  ↓
LLM Service
  ↓
Gemini API
  ↓
Structured Output
  ↓
Pydantic Validation
  ↓
Agent
```

The LLM is isolated behind an integration layer so the underlying provider can be replaced or extended in the future.

---

# ⚙️ Installation

## Prerequisites

- Python 3.11+
- Node.js
- npm
- Git

## Clone Repository

```bash
git clone <REPOSITORY_URL>
cd HCL1
```

## Backend Setup

```bash
cd backend
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Frontend Setup

```bash
cd frontend
npm install
```

---

# 🔐 Environment Configuration

Create:

```text
backend/.env
```

Example:

```env
APP_NAME=LearnPath AI
APP_ENV=development

DATABASE_URL=sqlite:///./learnpath.db

FRONTEND_URL=http://localhost:5173

GEMINI_API_KEY=your_api_key
GEMINI_MODEL=your_model
```

Do not commit `.env` or API keys to GitHub.

---

# ▶️ Running the Application

## Backend

```bash
cd backend
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## Frontend

```bash
cd frontend
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# 🧪 Testing

Run all backend tests:

```bash
pytest
```

Run unit tests:

```bash
pytest tests/unit
```

Run integration tests:

```bash
pytest tests/integration
```

---

# 🔍 End-to-End Flow Testing

```text
Create Learner
      ↓
Select Domain
      ↓
Enter Domain-Specific Goal
      ↓
Complete Onboarding
      ↓
Start Assessment
      ↓
Submit Answers
      ↓
Generate Skill Gap
      ↓
Generate Learning Path
      ↓
Retrieve Resources
      ↓
Complete Learning Phase
      ↓
Take Mastery Test
      ↓
Validate Mastery
      ↓
Unlock Next Phase
      ↓
Update Progress
      ↓
View Dashboard
```

---

# 🔒 Security

The application follows basic security practices:

- Environment variables for API keys
- Input validation
- Structured API schemas
- External API error handling
- No hard-coded secrets
- Controlled third-party integrations
- Public-resource-only navigation
- No bypassing of authentication or paywalls

---

# 🚀 Future Enhancements

- Additional learning domains
- Additional resource providers
- Advanced GitHub repository analysis
- Project evaluation agent
- Adaptive learning paths
- Advanced learner analytics
- Career recommendations
- AI learning tutor
- Knowledge graph-based prerequisite modeling
- Vector database and semantic retrieval
- Personalized difficulty adjustment
- Advanced recommendation ranking
- Learning-time prediction
- Certification recommendations

---

# 🌟 Why LearnPath AI?

Traditional recommendation systems:

```text
Learner
   ↓
Course Recommendation
```

LearnPath AI:

```text
Learner
   ↓
Personalized Profile
   ↓
Domain + Goal
   ↓
Assessment
   ↓
Skill Gap Analysis
   ↓
Dynamic Learning Path
   ↓
Resource Curation
   ↓
Learning
   ↓
Mastery Assessment
   ↓
Progress Tracking
   ↓
Next Learning Action
```

LearnPath AI focuses on the **complete learning journey**, rather than simply recommending individual courses.

---

# 👥 Team Architecture

The modular architecture enables parallel development:

```text
Frontend
    ↓
UI + Dashboard

Assessment Agent
    ↓
Domain / Goal Assessment

Skill Gap Agent
    ↓
Skill Analysis

Learning Path Agent
    ↓
Personalized Roadmap

Resource Curator Agent
    ↓
Learning Resources

Mastery Agent
    ↓
Mastery + Phase Unlocking
```

---

# 📌 Project Vision

LearnPath AI aims to evolve from a course recommendation system into an intelligent learning companion that understands:

```text
Who you are
      +
What you know
      +
What you want to achieve
      +
What you are missing
      +
What you should learn
      +
How you should learn it
      +
Whether you actually mastered it
```

## LearnPath AI

**Learn smarter. Learn what matters. Learn what comes next.**
