import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

CHITRIO_API_KEY = os.getenv("CHITRIO_API_KEY")
CHITRIO_URL = "https://chitrio.com/api/v1/videos"


class VideoRequest(BaseModel):
    topic: str
    durationInMinutes: int = 3
    language: str = "en"
    generateShort: bool = True
    tone: str = "storytelling"
    visualStyle: str = "realistic"
    autoUpload: bool = False
    autoUploadPrivacy: str = "private"


@app.get("/")
def home():
    return {"status": "Chitrio YouTube MCP server is running"}


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/create-video")
def create_video(request: VideoRequest):

    if not CHITRIO_API_KEY:
        return {"error": "CHITRIO_API_KEY is not configured"}

    payload = request.model_dump()

    response = requests.post(
        CHITRIO_URL,
        headers={
            "X-Api-Key": CHITRIO_API_KEY,
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=30
    )

    return {
        "status_code": response.status_code,
        "result": response.json()
    }
