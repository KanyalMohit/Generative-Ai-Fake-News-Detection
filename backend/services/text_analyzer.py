import requests
from bs4 import BeautifulSoup

def fetch_text_from_url(url: str) -> str:
    """
    Fetches the main text content from a given URL.
    """
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Naive extraction: join main <p> tags
        # This is a basic heuristic that works for many news sites as per original todo
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        text = "\n\n".join(paragraphs)
        
        # Limit text length to avoid token limits later
        return text[:40000]
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return ""
