import os
import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

CHITRIO_API_KEY = os.getenv("CHITRIO_API_KEY")
CHITRIO_URL = "https://chitrio.com/api/v1/videos"


@app.get("/")
def home():
    return {"status": "Chitrio YouTube MCP server is running"}


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/mcp")
async def mcp(request_data: dict):
    if not CHITRIO_API_KEY:
        return JSONResponse(
            {"error": "CHITRIO_API_KEY is not configured"},
            status_code=500
        )

    method = request_data.get("method")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_data.get("id"),
            "result": {
                "protocolVersion": "2025-06-18",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "chitrio-youtube-mcp",
                    "version": "1.0.0"
                }
            }
        }

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_data.get("id"),
            "result": {
                "tools": [
                    {
                        "name": "create_video",
                        "description": "Create a video using Chitrio AI",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "topic": {
                                    "type": "string"
                                },
                                "durationInMinutes": {
                                    "type": "integer",
                                    "default": 3
                                },
                                "language": {
                                    "type": "string",
                                    "default": "en"
                                }
                            },
                            "required": ["topic"]
                        }
                    }
                ]
            }
        }

    if method == "tools/call":
        params = request_data.get("params", {})
        name = params.get("name")
        arguments = params.get("arguments", {})

        if name != "create_video":
            return {
                "jsonrpc": "2.0",
                "id": request_data.get("id"),
                "error": {
                    "code": -32601,
                    "message": "Unknown tool"
                }
            }

        response = requests.post(
            CHITRIO_URL,
            headers={
                "X-Api-Key": CHITRIO_API_KEY,
                "Content-Type": "application/json"
            },
            json=arguments,
            timeout=60
        )

        return {
            "jsonrpc": "2.0",
            "id": request_data.get("id"),
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": response.text
                    }
                ]
            }
        }

    return {
        "jsonrpc": "2.0",
        "id": request_data.get("id"),
        "error": {
            "code": -32601,
            "message": "Method not found"
        }
    }
