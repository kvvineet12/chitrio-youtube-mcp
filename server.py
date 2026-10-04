import os
import requests
from mcp.server.fastmcp import FastMCP

CHITRIO_API_KEY = os.getenv("CHITRIO_API_KEY")
CHITRIO_URL = "https://chitrio.com/api/v1/videos"

mcp = FastMCP(
    "Chitrio YouTube",
    stateless_http=True,
    json_response=True
)


@mcp.tool()
def create_video(
    topic: str,
    duration_in_minutes: int = 3,
    language: str = "en"
) -> str:
    """Create an AI video using Chitrio."""

    if not CHITRIO_API_KEY:
        return "Error: CHITRIO_API_KEY is not configured."

    payload = {
        "topic": topic,
        "durationInMinutes": duration_in_minutes,
        "language": language
    }

    response = requests.post(
        CHITRIO_URL,
        headers={
            "X-Api-Key": CHITRIO_API_KEY,
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=60
    )

    return response.text


app = mcp.streamable_http_app()
