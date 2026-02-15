import os
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uuid
import redis
import shutil  # For saving uploaded video temporarily

from gateway.utils import publish_video_job

app = FastAPI(title="Fake News Detector - API Gateway")

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CONTENT_SERVICE_URL = os.getenv("CONTENT_SERVICE_URL", "http://localhost:8001")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Redis Client
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "API Gateway is running"}

@app.post("/analyze/text")
async def proxy_analyze_text(payload: dict):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{CONTENT_SERVICE_URL}/analyze/text", json=payload, timeout=60.0)
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Content service unavailable: {str(exc)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/image")
async def proxy_analyze_image(file: UploadFile = File(...)):
    async with httpx.AsyncClient() as client:
        try:
            # Re-upload the file to the content service
            files = {'file': (file.filename, await file.read(), file.content_type)}
            response = await client.post(f"{CONTENT_SERVICE_URL}/analyze/image", files=files, timeout=60.0)
            return response.json()
        except httpx.RequestError as exc:
             raise HTTPException(status_code=503, detail=f"Content service unavailable: {str(exc)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/video")
async def analyze_video_route(file: UploadFile = File(...)):
    """
    Accepts video, saves it locally (shared volume in prod, local dir here),
    publishes job to RabbitMQ, returns job_id.
    """
    job_id = str(uuid.uuid4())
    
    # Save video temporarily
    # Ensure uploads dir exists
    os.makedirs("uploads", exist_ok=True)
    video_path = f"uploads/{job_id}_{file.filename}"
    
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Set initial status in Redis
    r.hset(f"job:{job_id}", mapping={"status": "QUEUED", "filename": file.filename})
    
    # Publish to RabbitMQ
    success = publish_video_job(video_path, job_id)
    
    if not success:
        r.hset(f"job:{job_id}", mapping={"status": "FAILED", "error": "Could not publish job"})
        raise HTTPException(status_code=500, detail="Failed to queue video analysis job")
    
    return {"job_id": job_id, "status": "QUEUED", "message": "Video queued for analysis. Check status with /analyze/video/{job_id}"}

@app.get("/analyze/video/{job_id}")
def get_video_status(job_id: str):
    job = r.hgetall(f"job:{job_id}")
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
