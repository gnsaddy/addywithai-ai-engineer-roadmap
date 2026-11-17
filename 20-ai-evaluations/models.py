# models.py: one chat() call to any OpenAI-compatible API (real runs only).
import json, os, urllib.request

def chat(system, user):
    body = {"model": os.getenv("CHAT_MODEL", "llama3.2"), "temperature": 0,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}]}
    req = urllib.request.Request(
        os.getenv("BASE_URL", "http://localhost:11434/v1") + "/chat/completions",
        json.dumps(body).encode(), {"Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("API_KEY", "none")})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)["choices"][0]["message"]["content"]
