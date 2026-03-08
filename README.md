# GenAI-Powered Fake News Detection and Verification

This project is a multimodal misinformation analysis system built with a React frontend and a FastAPI backend. Instead of acting like a simple classifier, it is being shaped into a **GenAI verification assistant** that can analyze text, images, and video, gather evidence, and generate an evidence-grounded verification report.

## What it does

- **Text verification**
  - Accepts raw text or article URLs
  - Extracts and analyzes the underlying claims
  - Uses LLM-driven research plus reasoning to generate a verdict
- **Image verification**
  - Extracts visible text and context from images
  - Routes that content through the same verification flow
- **Deepfake video inspection**
  - Uses an asynchronous pipeline for video analysis
  - Flags potential visual and audio manipulation cues

## Why this counts as a GenAI project

This app is not just forwarding prompts to an API and dumping the reply. The intended architecture is:

1. **Input understanding** — identify claims from text, URLs, or media
2. **Evidence retrieval / research synthesis** — gather supporting and contradicting signals
3. **Generative verification** — produce a structured report with:
   - verdict
   - confidence
   - detected claims
   - evidence for and against
   - uncertainty notes
   - final reasoning
   - recommended next action
4. **User-facing explanation** — present the result in a readable verification workflow

That makes it closer to a **GenAI-powered verification assistant** than a plain classifier.

## Tech Stack

### Frontend
- React (Vite)
- Tailwind CSS

### Backend
- FastAPI
- Python
- BeautifulSoup for URL text extraction
- Gemini for primary research synthesis, structured report generation, and multimodal analysis
- Perplexity integration retained as optional enrichment when available
- RabbitMQ + Redis for async video processing

## Current Direction

The project is being reframed from a basic "fake news detector" into a more accurate and stronger concept:

**GenAI-Powered Fake News Detection and Verification**

This wording better reflects that the system:
- performs evidence-based analysis
- generates explanations
- surfaces uncertainty
- supports verification instead of pretending perfect truth detection

## Runtime Note

Right now, the active runtime path is **Gemini-first**.
Perplexity integration is still present in the codebase and can be used again later for external research enrichment when quota or billing is available.

## Suggested future improvements

- Claim decomposition for long articles
- Bias / framing analysis
- Evidence ranking by source quality
- Contradiction highlighting across sources
- Explain-like-I’m-5 / student / journalist output modes
- Chat with the article
- Exportable verification reports

## Setup Instructions

### Prerequisites
- Node.js (v18+ recommended)
- Python (v3.8+ recommended)
- API keys for Gemini
- Optional: Perplexity API key for enrichment

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in `backend/` and add keys such as:

```env
GEMINI_API_KEY=your_key_here
PERPLEXITY_API_KEY=your_key_here
```

Run the backend:

```bash
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Usage

1. Start backend and frontend
2. Open the frontend in your browser
3. Paste a claim, article, or URL — or upload image/video input
4. Review the generated verification report
5. Inspect the evidence and citations before trusting or sharing the result

## Important note

This system should be presented as an **AI-assisted verification tool**, not as a perfect truth engine. Real-world misinformation analysis still requires source judgment, careful reading, and human oversight.
