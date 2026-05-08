import json
import logging
from dotenv import load_dotenv

from .genai_client import genai_client

load_dotenv()
logger = logging.getLogger(__name__)


def build_research_prompt(text_content: str) -> str:
    return f'''
You are a careful misinformation research assistant.

Analyze the following news claim or article and produce concise, grounded research notes.
Do not act overly certain. State explicitly if you are relying on general model knowledge rather than live retrieval.

Content:
"""
{text_content[:5000]}
"""

Your research notes should cover:
1. The main claims present in the text
2. Evidence that would support those claims
3. Evidence or common knowledge that contradicts those claims
4. What remains uncertain or unverifiable
5. A short note on source/reliability signals visible in the text
6. A caveat if this analysis is limited by the lack of live web search
'''


def build_verification_prompt(text_content: str, research_text: str, citations: list) -> str:
    return f'''
You are an expert misinformation analyst.

Your task is to produce a structured, evidence-based fact-check report.
Use the research notes below as your evidence base. Be honest about uncertainty.

Original content:
"""
{text_content[:5000]}
"""

Research notes:
"""
{research_text[:12000]}
"""

Return ONLY valid JSON — no markdown, no code fences — with exactly these keys:
{{
  "label": "REAL" | "FAKE" | "MISLEADING" | "UNVERIFIED" | "UNKNOWN",
  "confidence": <integer 0-100>,
  "summary": "<2-4 sentence verdict summary>",
  "detected_claims": ["<claim 1>", "<claim 2>"],
  "verification_strategy": ["<step 1>", "<step 2>"],
  "evidence_for": ["<supporting evidence point>"],
  "evidence_against": ["<contradicting evidence point>"],
  "uncertainty_notes": ["<what remains unclear>"],
  "credibility_analysis": {{
    "source_reputation": "<paragraph about source reliability or lack thereof>",
    "credibility_score": <integer 0-100>
  }},
  "key_facts": ["<fact 1>", "<fact 2>"],
  "cross_verification": {{
    "common_points": "<what reliable sources agree on>",
    "discrepancies": "<what conflicts or is disputed>"
  }},
  "final_reasoning": "<clear explanation tying the verdict to the evidence>",
  "recommended_user_action": "<what the user should do, e.g. trust cautiously, verify further, avoid sharing>",
  "citations": {json.dumps(citations)}
}}

Labeling rules:
- REAL: evidence strongly supports the claim
- FAKE: evidence strongly contradicts the claim
- MISLEADING: partly true but framing or context is deceptive
- UNVERIFIED / UNKNOWN: evidence is insufficient to judge
- Confidence must reflect actual evidence quality.
'''


def analyze_claim(text_content: str) -> dict:
    """
    Two-phase Gemini analysis:
    1. Gemini produces research notes about the claim.
    2. Gemini uses those notes to produce a structured verification report.
    """
    text_content = text_content.strip()
    logger.info(f"Starting analyze_claim() — input length: {len(text_content)} chars")

    # Phase 1: Research
    logger.info("Phase 1: Gemini Research...")
    print("Phase 1: Gemini Research...")
    research_result = genai_client.generate_text(build_research_prompt(text_content))
    if "error" in research_result:
        logger.error(f"Phase 1 FAILED: {research_result['error']}")
        return {"error": f"Research phase failed: {research_result['error']}"}

    research_text = research_result["text"]
    logger.info(f"Phase 1 complete — research notes: {len(research_text)} chars")

    # Phase 2: Structured Verification
    logger.info("Phase 2: Gemini Verification...")
    print("Phase 2: Gemini Verification...")
    result = genai_client.refine_analysis(
        text_content,
        build_verification_prompt(text_content, research_text, []),
        []
    )

    if isinstance(result, dict) and "error" in result:
        logger.error(f"Phase 2 FAILED: {result['error']}")
        return result

    if isinstance(result, dict):
        result["research_mode"] = "gemini_only"
        notes = result.get("uncertainty_notes") or []
        caveat = "Analysis performed using Gemini AI internal knowledge. No live web search was used."
        if caveat not in notes:
            notes.append(caveat)
        result["uncertainty_notes"] = notes
        logger.info(f"Analysis complete — label={result.get('label')} confidence={result.get('confidence')}")
    else:
        logger.error(f"Unexpected result type from refine_analysis: {type(result)}")

    return result
