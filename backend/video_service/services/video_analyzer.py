from .genai_client import genai_client
import json
import re

def clean_json_output(text: str):
    try:
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        return json.loads(text.strip())
    except:
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end != -1:
                return json.loads(text[start:end])
        except:
            pass
        return {"error": "Failed to parse JSON output", "raw_reply": text}

def analyze_video(video_path: str):
    """
    Analyzes a video specifically for Deepfake cues.
    """
    print(f"Starting analysis for: {video_path}")
    
    prompt = """
    Analyze this video STRICTLY for Deepfake and AI manipulation detection.
    Do NOT summarize the news content. Focus ONLY on authenticity.
    
    Check for:
    1. Lip-sync issues (Audio-visual mismatch).
    2. Unnatural facial movements or blinking.
    3. Lighting/Shadow inconsistencies.
    4. Digital artifacts around edges/faces.
    
    Return a JSON object with these keys:
    {
        "is_deepfake": true/false,
        "confidence_score": 0-100,
        "visual_anomalies": ["List of specific visual glitches found"],
        "audio_anomalies": ["List of audio issues found"],
        "verdict_explanation": "Technical explanation of why it is or isn't a deepfake"
    }
    """
    
    result = genai_client.analyze_video_content(video_path, prompt)
    
    if "text" in result:
        parsed = clean_json_output(result["text"])
        return parsed
    
    return result
