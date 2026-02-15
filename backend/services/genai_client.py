import os
import google.generativeai as genai
import json
import re
from dotenv import load_dotenv

load_dotenv()

# Boilerplate for Gemini (or OpenAI)
# You should set GEMINI_API_KEY in your .env
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
        """
        Helper to extract JSON from text that might contain markdown backticks.
        """
        try:
            # Remove markdown code blocks if present
            text = re.sub(r'```json\s*', '', text)
            text = re.sub(r'```\s*', '', text)
            return json.loads(text.strip())
        except json.JSONDecodeError:
            # Fallback: try to find the first { and last }
            try:
                start = text.find('{')
                end = text.rfind('}') + 1
                if start != -1 and end != -1:
                    return json.loads(text[start:end])
            except:
                pass
            return {"error": "Failed to parse JSON output", "raw_reply": text}

    def refine_analysis(self, claim_text: str, research_data: str, citations: list):
        if not self.model:
             return {"error": "Gen AI functionality not configured."}
        
        prompt = f"""
        You are an expert Fact Checker and News Analyst.
        
        Your task is to analyze a claim based on the provided Research Data.
        
        Original Claim/Content:
        "{claim_text[:2000]}"
        
        Research Data (from Perplexity/Web Search):
        "{research_data[:10000]}"
        
        Based ONLY on the research data provided (and your internal knowledge for verification), 
        produce a FINAL JSON report.
        
        Rule 1: If the research data says the claim is false, label it FAKE.
        Rule 2: If the research data says the claim is true, label it REAL.
        Rule 3: If the research data is inconclusive, label it UNKNOWN.
        
        Return a valid JSON object with these EXACT keys:
        {{
            "label": "REAL", "FAKE", or "UNKNOWN",
            "confidence": (integer 0-100),
            "summary": "A 2-3 sentence summary of the verification.",
            "credibility_analysis": {{
                "source_reputation": "Analysis of the source's history/bias based on research",
                "credibility_score": (integer 0-100)
            }},
            "key_facts": ["Fact 1", "Fact 2", "Fact 3"],
            "cross_verification": {{
                "common_points": "What matches across sources",
                "discrepancies": "What conflicts across sources"
            }},
            "citations": {json.dumps(citations)} 
        }}
        
        IMPORTANT: return ONLY the JSON. No markdowns, no backticks.
        """
        
        try:
             response = self.model.generate_content(prompt)
             return self.clean_json_output(response.text)
        except Exception as e:
            return {"error": f"Gemini Refinement Failed: {str(e)}"}

genai_client = GenAIClient()
