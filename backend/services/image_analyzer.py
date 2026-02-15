import os
import google.generativeai as genai
from PIL import Image
import io

def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Analyzes the provided image bytes using Google Gemini 1.5 Pro.
    Returns extracted text and a description of the visual content.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "Error: GEMINI_API_KEY not found in environment variables."

        genai.configure(api_key=api_key)
        
        # Use gemini-1.5-pro for best vision capabilities
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        prompt = """
        Analyze this image for a Fake News Detection system.
        1. Extract all legible text from the image exactly as it appears.
        2. Describe the visual content (persons, objects, setting, context).
        3. Note any signs of manipulation or potential misinformation context (e.g., is it a meme, a tweet, a doctored photo?).
        
        Format the output clearly.
        """
        
        response = model.generate_content([prompt, image])
        
        return response.text
    except Exception as e:
        return f"Error executing Gemini Vision analysis: {str(e)}"
