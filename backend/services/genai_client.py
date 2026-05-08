import os
import json
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class GenAIClient:
    def __init__(self):
        if GEMINI_API_KEY:
            self.client = genai.Client(api_key=GEMINI_API_KEY)
            self.model = "gemini-2.5-flash"
        else:
            print("Warning: GEMINI_API_KEY not set. GenAI features will not work.")
            self.client = None
            self.model = None

    def clean_json_output(self, text: str):
        try:
            text = re.sub(r'```json\s*', '', text)
            text = re.sub(r'```\s*', '', text)
            return json.loads(text.strip())
        except json.JSONDecodeError:
            try:
                start = text.find('{')
                end = text.rfind('}') + 1
                if start != -1 and end != -1:
                    return json.loads(text[start:end])
            except Exception:
                pass
            return {"error": "Failed to parse JSON output", "raw_reply": text}

    def generate_text(self, prompt: str):
        if not self.client:
            return {"error": "GenAI not configured — missing GEMINI_API_KEY."}
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return {"text": response.text}
        except Exception as e:
            return {"error": f"Gemini generation failed: {str(e)}"}

    def refine_analysis(self, claim_text: str, prompt: str, citations: list):
        if not self.client:
            return {"error": "GenAI not configured — missing GEMINI_API_KEY."}

        # Use the passed prompt directly if it already has the JSON structure
        if 'Return ONLY valid JSON with exactly these keys:' not in prompt:
            prompt = f"""
You are an expert Fact Checker and News Analyst.

Original Claim/Content:
\"{claim_text[:2000]}\"

Return ONLY valid JSON with these keys:
{{
    "label": "REAL" | "FAKE" | "MISLEADING" | "UNVERIFIED",
    "confidence": 0,
    "summary": "A short summary.",
    "credibility_analysis": {{
        "source_reputation": "Short source analysis",
        "credibility_score": 0
    }},
    "key_facts": ["Fact 1", "Fact 2"],
    "cross_verification": {{
        "common_points": "What matches across sources",
        "discrepancies": "What conflicts across sources"
    }},
    "citations": {json.dumps(citations)}
}}
"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return self.clean_json_output(response.text)
        except Exception as e:
            return {"error": f"Gemini refinement failed: {str(e)}"}


genai_client = GenAIClient()
