import os
import google.generativeai as genai
import json
import re
from dotenv import load_dotenv

load_dotenv()

GENAI_API_KEY = os.getenv("GEMINI_API_KEY")


class GenAIClient:
    def __init__(self):
        if GENAI_API_KEY:
            genai.configure(api_key=GENAI_API_KEY)
            self.model = genai.GenerativeModel('gemini-3-flash-preview')
        else:
            print("Warning: GEMINI_API_KEY not set. Gen AI features will not work.")
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
        if not self.model:
            return {"error": "Gen AI functionality not configured."}
        try:
            response = self.model.generate_content(prompt)
            return {"text": response.text}
        except Exception as e:
            return {"error": f"Gemini Generation Failed: {str(e)}"}

    def refine_analysis(self, claim_text: str, prompt_or_research_data: str, citations: list):
        if not self.model:
            return {"error": "Gen AI functionality not configured."}

        prompt = prompt_or_research_data.strip()

        if 'Return ONLY valid JSON with exactly these keys:' not in prompt:
            prompt = f"""
You are an expert Fact Checker and News Analyst.

Original Claim/Content:
\"{claim_text[:2000]}\"

Research Data:
\"{prompt_or_research_data[:10000]}\"

Return ONLY valid JSON with these keys:
{{
    "label": "REAL", "FAKE", or "UNKNOWN",
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
            response = self.model.generate_content(prompt)
            return self.clean_json_output(response.text)
        except Exception as e:
            return {"error": f"Gemini Refinement Failed: {str(e)}"}


genai_client = GenAIClient()
