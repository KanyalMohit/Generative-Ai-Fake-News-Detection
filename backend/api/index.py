"""
Unified Vercel serverless entry point.
Merges gateway + content_service into a single FastAPI app.
No Redis / RabbitMQ — text and image analysis only.
"""

import os
import sys
import logging

# Make sure 'backend/' is on the path so relative imports work on Vercel
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.claim_analyzer import analyze_claim
from services.image_analyzer import extract_text_from_image

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Satya — Unified API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextAnalysisRequest(BaseModel):
    content: str


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Satya API is running"}


@app.post("/analyze/text")
def analyze_text(payload: TextAnalysisRequest):
    text = payload.content.strip()
    logger.info(f"[/analyze/text] {len(text)} chars")

    if len(text) < 10:
        raise HTTPException(status_code=400, detail="Text is too short for analysis.")

    result = analyze_claim(text)

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result


@app.post("/analyze/image")
async def analyze_image(file: UploadFile = File(...)):
    try:
        logger.info(f"[/analyze/image] File: {file.filename}")
        contents = await file.read()

        extracted_text = extract_text_from_image(contents)

        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="No readable text detected in the image.")

        result = analyze_claim(extracted_text)
        result["extracted_text"] = extracted_text

        if isinstance(result, dict) and "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[/analyze/image] Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/video")
async def analyze_video(file: UploadFile = File(...)):
    raise HTTPException(
        status_code=503,
        detail="Video analysis is not available in the hosted version. Run locally with Docker Compose for full video support."
    )
