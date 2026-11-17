# models.py: one chat() call to any OpenAI-compatible API, with tools.
# Works with Ollama on your laptop, or a hosted API. --demo uses stand_in.py.
import json, os, sys, urllib.request

DEMO = "--demo" in sys.argv
BASE_URL = os.getenv("BASE_URL", "http://localhost:11434/v1")
MODEL = os.getenv("CHAT_MODEL", "llama3.2")

def chat(messages, tools):
    if DEMO:
        from stand_in import fake_model
        return fake_model(messages)
    body = {"model": MODEL, "messages": messages, "tools": tools}
    req = urllib.request.Request(
        BASE_URL + "/chat/completions", json.dumps(body).encode(),
        {"Content-Type": "application/json",
         "Authorization": "Bearer " + os.getenv("API_KEY", "none")})
    with urllib.request.urlopen(req, timeout=120) as r:
        msg = json.load(r)["choices"][0]["message"]
    keep = ("role", "content", "tool_calls")
    return {k: v for k, v in msg.items() if k in keep and v is not None}
