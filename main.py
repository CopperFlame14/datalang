from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from intent_extractor import IntentExtractor

app = FastAPI(
    title="AI Task Automation - NLP Backend",
    description="Simple intent extraction service for generating structured task data from natural language.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For hackathon/demo, allow all. In prod, specify domain.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize NLP Engine
nlp_engine = IntentExtractor()

# --- Data Models ---
class VoiceInput(BaseModel):
    text: str

class IntentOutput(BaseModel):
    intent: str
    task_title: str
    datetime: Optional[str] = None
    priority: str
    confidence: float

# --- Endpoints ---

@app.get("/")
def read_root():
    """Serves the frontend application."""
    return FileResponse("static/index.html")

@app.get("/health")
def health_check():
    return {"status": "online", "service": "nlp-intent-extractor"}

@app.post("/extract-intent", response_model=IntentOutput)
def extract_intent(user_input: VoiceInput):
    """
    Analyzes text input to determine user intent, task details, and time.
    """
    if not user_input.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty")

    print(f"DEBUG: Receiving Text -> {user_input.text}")
    
    # Run NLP Logic
    result = nlp_engine.extract(user_input.text)
    
    print(f"DEBUG: Extracted -> {result}")
    
    return result

if __name__ == "__main__":
    import uvicorn
    # Run with: python main.py
    uvicorn.run(app, host="127.0.0.1", port=8000)
