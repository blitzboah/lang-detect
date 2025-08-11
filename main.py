from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from coordinator import detect_language_all

app = FastAPI()

class DetectLanguageRequest(BaseModel):
    audio_file_path: str
    ground_truth_language: Optional[str] = None

@app.post("/detect/language")
def detect_language(request: DetectLanguageRequest):
    results = detect_language_all(
        file_path=request.audio_file_path,
        ground_truth=request.ground_truth_language
    )
    return results
