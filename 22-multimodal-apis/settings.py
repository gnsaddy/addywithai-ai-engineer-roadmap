# settings.py: one place for keys, endpoints and model names (Episode 22)
# Real run: set OPENAI, GEMINI, ELEVENLABS and VERTEX API keys (.env.example).
# --demo: everything goes to stand_in_server.py on your own computer.
import os
import sys

DEMO = "--demo" in sys.argv
LOCAL = "http://127.0.0.1:8022"

VISION = os.getenv("VISION_MODEL", "gpt-5.4-mini")
GEMINI = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
STT = os.getenv("STT_MODEL", "whisper-1")
TTS = os.getenv("TTS_MODEL", "gpt-4o-mini-tts")
IMAGE = os.getenv("IMAGE_MODEL", "gpt-image-2")
VIDEO = os.getenv("VIDEO_MODEL", "veo-3.1-lite-generate-001")

def openai_client():
    from openai import OpenAI
    if DEMO:
        return OpenAI(base_url=LOCAL + "/v1", api_key="demo-key")
    return OpenAI()                     # reads OPENAI_API_KEY

def gemini_client():
    from google import genai
    if DEMO:
        return genai.Client(api_key="demo-key",
                            http_options={"base_url": LOCAL})
    return genai.Client()               # reads GEMINI_API_KEY

def video_client():                     # Veo runs on Google Cloud Vertex AI
    from google import genai
    key = "demo-key" if DEMO else os.getenv("VERTEX_API_KEY")
    opts = {"base_url": LOCAL} if DEMO else None
    return genai.Client(vertexai=True, api_key=key, http_options=opts)

ELEVEN_URL = LOCAL if DEMO else "https://api.elevenlabs.io"
ELEVEN_KEY = "demo-key" if DEMO else os.getenv("ELEVENLABS_API_KEY", "")
