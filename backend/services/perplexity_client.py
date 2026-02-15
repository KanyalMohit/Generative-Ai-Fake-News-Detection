import os
from perplexity import Perplexity
from dotenv import load_dotenv

from dotenv import load_dotenv
from .genai_client import genai_client

load_dotenv()

# We will instantiate the client once. 
# Note: The 'perplexity' library might expect PERPLEXITY_API_KEY env var automatically.
# If the user hasn't set it in .env, we might need to handle that gracefully or wait for them to provide it.

def get_perplexity_client():
    # Perplexity() reads PERPLEXITY_API_KEY from env
    try:
        if not os.getenv("PERPLEXITY_API_KEY"):
            print("Warning: PERPLEXITY_API_KEY not found in environment variables.")
        return Perplexity()
    except Exception as e:
        print(f"Error initializing Perplexity client: {e}")
        return None

def analyze_claim(text_content: str, context_url: str = None) -> dict:
    """
    Analyzes the given text using Perplexity for research, 
    then Gemini for structured JSON refinement.
    """
    client = get_perplexity_client()
    if not client:
        return {"error": "Perplexity client not initialized. Check API Key."}

    # 1. Perplexity Research Phase
    system_message = {
        "role": "system",
        "content": (
            "You are a skilled research assistant. "
            "Your goal is to gather comprehensive facts, check credibility, and "
            "find sources that support or refute the given claim. "
            "Provide a detailed, factual research report. Do NOT format as JSON."
        )
    }

    user_prompt = (
        f"Research the following claim/article:\n"
        f"Context URL: {context_url if context_url else 'N/A'}\n"
        f"Content: {text_content[:4000]}\n\n"
        "Provide a detailed report covering:\n"
        "1. Is this true or false? Why?\n"
        "2. What do major reliable sources say?\n"
        "3. Are there any discrepancies?\n"
        "4. What is the reputation of the source/URL?\n"
        "Include as many specific citations as possible."
    )

    try:
        completion = client.chat.completions.create(
            model="sonar-pro",
            messages=[
                system_message,
                {"role": "user", "content": user_prompt}
            ]
        )
        
        research_text = completion.choices[0].message.content
        citations = getattr(completion, "search_results", []) or getattr(completion, "citations", [])
        
        print(f"Perplexity Search Complete. Length: {len(research_text)}")
        print(f"Citations found: {len(citations)}")
        
# 2. Gemini Refinement Phase
        print("Refining with Gemini...")
        
        # Serialize citations to avoid JSON errors
        serialized_citations = []
        for c in citations:
            if isinstance(c, str):
                serialized_citations.append(c)
            elif hasattr(c, 'url'):
                serialized_citations.append(c.url)
            elif isinstance(c, dict) and 'url' in c:
                serialized_citations.append(c['url'])
            else:
                serialized_citations.append(str(c))

        final_result = genai_client.refine_analysis(text_content, research_text, serialized_citations)
        
        return final_result

    except Exception as e:
        return {"error": f"Analysis Pipeline Failed: {str(e)}"}
