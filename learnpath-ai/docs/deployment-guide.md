# Deployment Guide for LearnPath AI

This guide details how to deploy **LearnPath AI** locally using Docker Compose as well as to cloud platforms (Render for Backend + Vercel for Frontend).

---

## 1. Local Containerized Deployment (Docker Compose)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (v20+ installed and running)
- Docker Compose v2+

### Step-by-Step Instructions

1. **Clone & Navigate to Project Directory**
   ```bash
   cd learnpath-ai
   ```

2. **Configure Environment Variables**
   Set your Gemini API key in your terminal session or `.env` file:
   - **Linux/macOS:**
     ```bash
     export GEMINI_API_KEY="your_actual_gemini_api_key"
     ```
   - **Windows PowerShell:**
     ```powershell
     $env:GEMINI_API_KEY="your_actual_gemini_api_key"
     ```

3. **Build and Launch Containers**
   ```bash
   docker compose up --build -d
   ```

4. **Verify Application Services**
   - **Frontend App:** Navigate to [http://localhost](http://localhost)
   - **Backend API Root:** [http://localhost:8000/](http://localhost:8000/)
   - **Backend API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Backend Health Check:** [http://localhost:8000/api/health](http://localhost:8000/api/health)

5. **Stop Container Stack**
   ```bash
   docker compose down
   ```

---

## 2. Cloud Deployment: Render (Backend) & Vercel (Frontend)

### A. Deploy Backend to Render

1. Log into [Render.com](https://render.com).
2. Click **New +** -> **Blueprints**.
3. Connect your Git repository containing `learnpath-ai/backend/render.yaml`.
4. Render will automatically detect `render.yaml` and configure the web service:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. In Environment Variables, set:
   - `GEMINI_API_KEY`: Your Gemini API key
   - `FRONTEND_URL`: Your deployed frontend Vercel URL (e.g., `https://learnpath-ai.vercel.app`)

---

### B. Deploy Frontend to Vercel

1. Log into [Vercel.com](https://vercel.com).
2. Click **Add New Project** and import your Git repository.
3. Set **Root Directory** to `learnpath-ai/frontend`.
4. Vercel automatically detects Vite settings.
5. In **Environment Variables**, add:
   - `VITE_API_URL`: Your backend URL on Render (e.g., `https://learnpath-ai-backend.onrender.com/api`)
6. Click **Deploy**.

---

## 3. Deployment Verification Checklist

- [ ] Backend `/api/health` returns status `200 OK`.
- [ ] Frontend successfully communicates with backend without CORS errors.
- [ ] Learning Path generation, Domain Profile selection, and Assessment workflows pass smoothly end-to-end.
