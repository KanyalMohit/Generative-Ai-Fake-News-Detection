import os
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.claim_analyzer import analyze_claim
from services.image_analyzer import extract_text_from_image

# ── Logging config: show INFO+ from all our modules ─────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Satya — Content Analysis Service")

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
    return {"status": "ok", "message": "Satya Content Service is running"}


@app.post("/analyze/text")
def analyze_text_route(request: TextAnalysisRequest):
    """
    Analyzes plain text for fake news / misinformation.
    URL support has been removed — text input only.
    """
    text = request.content.strip()
    logger.info(f"[/analyze/text] Received request — {len(text)} chars")

    if len(text) < 10:
        logger.warning("[/analyze/text] Rejected: text too short.")
        raise HTTPException(status_code=400, detail="Text is too short for analysis. Please provide at least a sentence.")

    result = analyze_claim(text)

    if isinstance(result, dict) and "error" in result:
        logger.error(f"[/analyze/text] analyze_claim returned error: {result['error']}")
        raise HTTPException(status_code=500, detail=result["error"])

    logger.info(f"[/analyze/text] Done — label={result.get('label')} confidence={result.get('confidence')}")
    return result


@app.post("/analyze/image")
async def analyze_image_route(file: UploadFile = File(...)):
    """
    Extracts text from an uploaded image using Gemini Vision and analyzes it.
    """
    try:
        logger.info(f"[/analyze/image] Received file: {file.filename}")
        contents = await file.read()
        logger.info(f"[/analyze/image] File size: {len(contents)} bytes")

        extracted_text = extract_text_from_image(contents)
        logger.info(f"[/analyze/image] Extraction complete — {len(extracted_text)} chars")

        if "Error:" in extracted_text and "Tesseract" in extracted_text:
            logger.error(f"[/analyze/image] Tesseract error: {extracted_text[:200]}")
            raise HTTPException(status_code=500, detail=extracted_text)

        if not extracted_text.strip():
            logger.warning("[/analyze/image] No text extracted from image.")
            raise HTTPException(status_code=400, detail="No readable text detected in the image.")

        result = analyze_claim(extracted_text)
        result["extracted_text"] = extracted_text

        if isinstance(result, dict) and "error" in result:
            logger.error(f"[/analyze/image] analyze_claim returned error: {result['error']}")
            raise HTTPException(status_code=500, detail=result["error"])

        logger.info(f"[/analyze/image] Done — label={result.get('label')}")
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[/analyze/image] Unhandled exception: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
