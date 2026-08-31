FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing bytecode and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

ENV PORT=8000

# Expose default port
EXPOSE 8000

# Start FastAPI app with Uvicorn
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
