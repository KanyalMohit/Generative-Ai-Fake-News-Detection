# Backend Architecture - How This Project Actually Operates

This project does **not** have a single all-in-one backend process.
It uses multiple backend pieces that work together.

## High-Level Flow

### For text and image requests
Desktop GUI / Frontend
-> **API Gateway** on `127.0.0.1:8000`
-> **Content Service** on `127.0.0.1:8001`
-> Gemini / verification logic
-> response comes back to the Gateway
-> response returns to the GUI

### For video requests
Desktop GUI / Frontend
-> **API Gateway** on `127.0.0.1:8000`
-> saves uploaded video + creates job id
-> stores job status in **Redis**
-> publishes job to **RabbitMQ**
-> **Video Worker Service** consumes the job
-> worker analyzes video and writes result back to Redis
-> Gateway exposes job status/result at `/analyze/video/{job_id}`
-> GUI polls that endpoint until completion

---

## Backend Pieces

### 1) API Gateway
**File:** `backend/gateway/main.py`
**Port:** `8000`

This is the entry point the GUI/web app should talk to.

It handles:
- `/analyze/text`
- `/analyze/image`
- `/analyze/video`
- `/analyze/video/{job_id}`

For text and image:
- it **proxies** the request to the Content Service on port `8001`

For video:
- it accepts the upload
- saves it temporarily
- creates a Redis job entry
- pushes a message to RabbitMQ
- returns a `job_id`

### 2) Content Service
**File:** `backend/content_service/main.py`
**Port:** `8001`

This is where the real text/image analysis happens.

It handles:
- URL text fetching
- image text extraction / image analysis
- claim analysis through the GenAI pipeline

If the Gateway is running but the Content Service is not,
text and image requests will fail.

### 3) Video Worker Service
**File:** `backend/video_service/main.py`

This is a separate background worker.
It listens for video jobs from RabbitMQ.

It:
- receives the queued job
- analyzes the video
- writes the final result/status into Redis

If this worker is not running,
video jobs may remain queued or never complete.

### 4) Redis
Used for:
- video job status
- video job result storage

### 5) RabbitMQ
Used for:
- queueing video analysis jobs

---

## What the Desktop GUI Should Call

The desktop GUI should call:

- **Gateway:** `http://127.0.0.1:8000`

Not:
- content service directly for normal app usage
- worker directly

Why?
Because the Gateway is the orchestration layer and exposes the unified API surface.

---

## Run Order

### Terminal 1 - Infrastructure
```bash
cd backend
docker-compose up -d
```

This starts:
- Redis
- RabbitMQ

### Terminal 2 - API Gateway
```bash
cd backend
.\venv\Scripts\python -m uvicorn gateway.main:app --port 8000 --host 127.0.0.1
```

### Terminal 3 - Content Service
```bash
cd backend
.\venv\Scripts\python -m uvicorn content_service.main:app --port 8001
```

### Terminal 4 - Video Worker
```bash
cd backend\video_service
..\venv\Scripts\python main.py
```

### Terminal 5 - UI
For web UI:
```bash
cd frontend
npm run dev
```

For desktop GUI:
```bash
cd desktopgui
pip install -r requirements.txt
python main.py
```

---

## Common Failure Cases

### Case 1: Gateway is running, but text/image fail
Most likely:
- Content Service on `8001` is not running

### Case 2: Video upload works, but result never completes
Most likely one of these is missing:
- Redis
- RabbitMQ
- Video Worker

### Case 3: Desktop GUI says backend connection failed
Check:
- Gateway is on `127.0.0.1:8000`
- not just some other backend file
- Content Service is also running if using text/image
- worker + queue services are also running if using video

---

## Recommended Mental Model

Think of the project like this:

- **Gateway = front door**
- **Content Service = brain for text/image**
- **Video Worker = background specialist for video**
- **Redis + RabbitMQ = plumbing for async video jobs**

That is the real backend architecture of this application.
