# Generative AI Fake News Detection

This project is a comprehensive solution for detecting fake news using Generative AI. It consists of a React-based frontend and a FastAPI backend, leveraging advanced AI models to analyze and verify news content.

## Features

- **Fake News Detection**: Uses GenAI to analyze text and determine its credibility.
- **Deepfake Video Detection**: (If applicable based on project analysis) Analyzes video content for signs of manipulation.
- **User-Friendly Interface**: Built with React and Tailwind CSS for a smooth user experience.
- **Robust Backend**: Powered by FastAPI for high performance and easy API management.

## Tech Stack

### Frontend
- **Framework**: React (Vite)
- **Styling**: Tailwind CSS
- **Language**: JavaScript/TypeScript

### Backend
- **Framework**: FastAPI
- **AI/ML**: Python, OpenAI/Google Gemini/Perplexity APIs (as per configuration)
- **Other libraries**: `uvicorn`, `requests`, `beautifulsoup4`, `python-multipart`

## Setup Instructions

### Prerequisites
- Node.js (v18+ recommended)
- Python (v3.8+ recommended)

### Backend Setup

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```

2.  Create a virtual environment:
    ```bash
    python -m venv venv
    ```

3.  Activate the virtual environment:
    - **Windows**: `venv\Scripts\activate`
    - **Mac/Linux**: `source venv/bin/activate`

4.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5.  Set up environment variables:
    - Create a `.env` file in the `backend` directory.
    - Add necessary API keys (e.g., OPENAI_API_KEY, GEMINI_API_KEY).

6.  Run the server:
    ```bash
    uvicorn main:app --reload
    ```
    The backend will be available at `http://127.0.0.1:8000`.

### Frontend Setup

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

3.  Run the development server:
    ```bash
    npm run dev
    ```
    The frontend will be available at `http://localhost:5173` (or the port shown in the terminal).

## Usage

1.  Start both backend and frontend servers.
2.  Open the frontend URL in your browser.
3.  Input the text or upload the media you want to verify.
4.  View the detailed analysis and credibility score.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
