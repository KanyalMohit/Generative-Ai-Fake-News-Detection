import os
import io
import logging
from PIL import Image
from google import genai
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Analyzes an image using Google Gemini Vision (new google-genai SDK).
    Returns extracted text + visual description for fake news analysis.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY not set — cannot run image analysis.")
        return "Error: GEMINI_API_KEY not found in environment variables."

    try:
        client = genai.Client(api_key=api_key)

        image = Image.open(io.BytesIO(image_bytes))
        logger.info(f"Image opened: size={image.size}, mode={image.mode}")

        prompt = """
Analyze this image for a Fake News Detection system.
1. Extract all legible text from the image exactly as it appears.
2. Describe the visual content (persons, objects, setting, context).
3. Note any signs of manipulation or potential misinformation (e.g., meme, doctored photo, screenshot).

Format your output clearly under these three headings.
"""
        # The new SDK accepts PIL images directly as part of the contents list
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, image],
        )

        logger.info("Gemini Vision response received successfully.")
        return response.text

    except Exception as e:
        logger.error(f"Gemini Vision analysis failed: {e}", exc_info=True)
        return f"Error executing Gemini Vision analysis: {str(e)}"
