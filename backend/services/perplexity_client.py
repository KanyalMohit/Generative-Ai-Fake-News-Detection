import os
import json
from perplexity import Perplexity
from dotenv import load_dotenv

from .genai_client import genai_client

load_dotenv()


def get_perplexity_client():
    try:
        if not os.getenv("PERPLEXITY_API_KEY"):
            print("Warning: PERPLEXITY_API_KEY not found in environment variables.")
        return Perplexity()
    except Exception as e:
        print(f"Error initializing Perplexity client: {e}")
        return None


def normalize_citations(citations):
    normalized = []
    for item in citations or []:
        if isinstance(item, str):
            normalized.append(item)
        elif isinstance(item, dict):
            normalized.append(item.get("url") or json.dumps(item))
        elif hasattr(item, "url"):
            normalized.append(item.url)
        else:
            normalized.append(str(item))
    return normalized


def build_genai_prompt(text_content: str, context_url: str, research_text: str, citations: list[str]) -> str:
    return f'''
You are an expert misinformation analyst and verification assistant.

Your job is not only to classify content, but to generate a grounded verification report.
Use the research notes below as the main evidence base.
If the evidence is weak, conflicting, or incomplete, clearly say so.
Do not pretend certainty when it does not exist.

Input claim/article:
"""
{text_content[:5000]}
"""

Context URL: {context_url or "N/A"}

Research notes:
"""
{research_text[:12000]}
"""

Return ONLY valid JSON with exactly these keys:
{{
  "label": "REAL" | "FAKE" | "MISLEADING" | "UNVERIFIED" | "UNKNOWN",
  "confidence": 0,
  "summary": "2-4 sentence high-level verdict summary",
  "detected_claims": ["claim 1", "claim 2"],
  "verification_strategy": ["step 1 used to verify", "step 2 used to verify"],
  "evidence_for": ["evidence supporting the claim"],
  "evidence_against": ["evidence contradicting the claim"],
  "uncertainty_notes": ["what remains unclear or unverified"],
  "credibility_analysis": {{
    "source_reputation": "short paragraph about source reliability, bias, or lack of source clarity",
    "credibility_score": 0
  }},
  "key_facts": ["fact 1", "fact 2", "fact 3"],
  "cross_verification": {{
    "common_points": "what reliable sources broadly agree on",
    "discrepancies": "what differs, conflicts, or remains disputed"
  }},
  "final_reasoning": "clear explanation tying the verdict to the evidence",
  "recommended_user_action": "what the user should do next, e.g. trust cautiously, verify further, avoid sharing",
  "citations": {json.dumps(citations)}
}}

Rules:
- REAL only when evidence strongly supports the claim.
- FAKE only when evidence strongly contradicts the claim.
- MISLEADING when parts are true but framing/context is deceptive.
- UNVERIFIED or UNKNOWN when evidence is insufficient.
- Confidence must reflect evidence quality, not bravado.
- Return JSON only. No markdown. No code fences.
'''


def build_gemini_research_prompt(text_content: str, context_url: str = None) -> str:
    return f'''
You are a careful misinformation research assistant.

Analyze the following claim/article and create concise research notes.
Do not act overly certain. If you rely on general model knowledge rather than live retrieval, say that explicitly.
If a URL is provided, treat it as context only unless you can actually access and verify it.

Content:
"""
{text_content[:5000]}
"""

Context URL: {context_url or "N/A"}

Return plain text research notes covering:
1. Main claims present
2. Evidence that would support the claims
3. Evidence or common knowledge that may contradict the claims
4. What remains uncertain
5. A short source/reliability note
6. A warning if this analysis is limited by lack of live search
'''


def try_perplexity_research(text_content: str, context_url: str = None):
    client = get_perplexity_client()
    if not client:
        return None, [], None

    system_message = {
        "role": "system",
        "content": (
            "You are a skilled research assistant focused on fact-checking and misinformation analysis. "
            "Gather reliable evidence, highlight conflicts between sources, and avoid overclaiming. "
            "Provide detailed research notes with citations, but do NOT format the response as JSON."
        )
    }

    user_prompt = (
        f"Research and verify the following claim/article.\n"
        f"Context URL: {context_url if context_url else 'N/A'}\n"
        f"Content: {text_content[:4000]}\n\n"
        "Return a careful research brief covering:\n"
        "1. The main verifiable claims present in the content.\n"
        "2. Evidence supporting those claims.\n"
        "3. Evidence contradicting those claims.\n"
        "4. What reliable sources say.\n"
        "5. What remains uncertain or unverified.\n"
        "6. A short note on source reputation or source transparency.\n"
        "Include as many relevant citations as possible."
    )

    try:
        completion = client.chat.completions.create(
            model="sonar-pro",
            messages=[system_message, {"role": "user", "content": user_prompt}]
        )
        research_text = completion.choices[0].message.content
        citations = normalize_citations(
            getattr(completion, "search_results", []) or getattr(completion, "citations", [])
        )
        return research_text, citations, None
    except Exception as e:
        return None, [], str(e)


def analyze_claim(text_content: str, context_url: str = None) -> dict:
    """
    Gemini is the default active research + verification path for now.
    Perplexity is kept as an optional fallback integration for later use.
    """
    citations = []
    research_mode = "gemini_primary"

    fallback = genai_client.generate_text(build_gemini_research_prompt(text_content, context_url))
    if "error" in fallback:
        return {"error": f"Research stage failed. {fallback['error']}"}

    research_text = fallback["text"]

    # Optional secondary attempt: if Perplexity is available later, it can enrich the run.
    perplexity_text, perplexity_citations, perplexity_error = try_perplexity_research(text_content, context_url)
    if perplexity_text:
        research_text = f"Gemini research notes:\n{research_text}\n\nPerplexity research notes:\n{perplexity_text}"
        citations = perplexity_citations
        research_mode = "gemini_primary+perplexity_enrichment"
        print(f"Perplexity enrichment complete. Citations found: {len(citations)}")
    elif perplexity_error:
        print(f"Perplexity enrichment unavailable: {perplexity_error}")

    print(f"Refining with Gemini into structured verification report ({research_mode})...")
    final_result = genai_client.refine_analysis(
        text_content,
        build_genai_prompt(text_content, context_url, research_text, citations),
        citations,
    )

    if isinstance(final_result, dict) and "error" not in final_result:
        final_result.setdefault("research_mode", research_mode)
        final_result.setdefault("research_snapshot", research_text[:2000])
        if research_mode == "gemini_primary":
            notes = final_result.get("uncertainty_notes") or []
            note = "This run used Gemini as the primary research path. Live external search enrichment was not available."
            if note not in notes:
                notes.append(note)
            final_result["uncertainty_notes"] = notes

    return final_result
