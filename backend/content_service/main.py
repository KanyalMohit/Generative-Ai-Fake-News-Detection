import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from services.perplexity_client import analyze_claim
from services.text_analyzer import fetch_text_from_url
from services.image_analyzer import extract_text_from_image

app = FastAPI(title="Fake News Detector - Content Service")

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextAnalysisRequest(BaseModel):
    content: str
    is_url: bool = False

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Content Service is running"}

@app.post("/analyze/text")
def analyze_text_route(request: TextAnalysisRequest):
    """
    Analyzes text or content from a URL to check if it's Real or Fake.
    """
    try:
        text_to_analyze = request.content
        context_url = None

        if request.is_url:
            print(f"Fetching text from URL: {request.content}")
            fetched_text = fetch_text_from_url(request.content)
            if not fetched_text:
                raise HTTPException(status_code=400, detail="Could not extract text from URL.")
            text_to_analyze = fetched_text
            context_url = request.content
        
        if not text_to_analyze or len(text_to_analyze.strip()) < 10:
             raise HTTPException(status_code=400, detail="Text is too short for analysis.")

        print(f"Analyzing text length: {len(text_to_analyze)}")
        result = analyze_claim(text_to_analyze, context_url)
        
        if "error" in result:
             raise HTTPException(status_code=500, detail=result["error"])
             
        return result

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error in text analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/image")
async def analyze_image_route(file: UploadFile = File(...)):
    """
    Extracts text from an uploaded image using OCR and analyzes it.
    """
    try:
        print(f"Received image: {file.filename}")
        contents = await file.read()
        
        # 1. Extract text
        extracted_text = extract_text_from_image(contents)
        print(f"OCR Result: {extracted_text[:100]}...")
        
        if "Error:" in extracted_text and "Tesseract" in extracted_text:
             raise HTTPException(status_code=500, detail=extracted_text)
        
        if not extracted_text.strip():
             raise HTTPException(status_code=400, detail="No text detected in the image.")

        # 2. Analyze text
        result = analyze_claim(extracted_text)
        
        # Merge OCR text into result for frontend display
        result["extracted_text"] = extracted_text
        
        if "error" in result:
             raise HTTPException(status_code=500, detail=result["error"])

        return result

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error in image analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # HTTP Service runs on 8001 (or env PORT)
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
