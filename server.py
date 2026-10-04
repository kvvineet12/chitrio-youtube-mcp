import os
import requests
from fastapi import FastAPI, Request

app = FastAPI()

CHITRIO_API_KEY = os.getenv("CHITRIO_API_KEY")
CHITRIO_URL = "https://chitrio.com/api/v1/videos"


@app.get("/")
def home():
    return {"status": "Chitrio YouTube MCP server is running"}


@app.post("/create-video")
async def create_video(request: Request):
    data = await request.json()

    if not CHITRIO_API_KEY:
        return {
            "error": "CHITRIO_API_KEY is not configured"
        }

    response = requests.post(
        CHITRIO_URL,
        headers={
            "X-Api-Key": CHITRIO_API_KEY,
            "Content-Type": "application/json"
        },
        json=data,
        timeout=60
    )

    return {
        "status_code": response.status_code,
        "result": response.json()
    }


@app.get("/video-status/{job_id}")
def video_status(job_id: str):
    response = requests.get(
        f"{CHITRIO_URL}/{job_id}",
        headers={
            "X-Api-Key": CHITRIO_API_KEY
        },
        timeout=30
    )

    return {
        "status_code": response.status_code,
        "result": response.json()
    }
