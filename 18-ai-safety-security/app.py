# app.py: a tiny support helper. It reads a customer email and summarises it.
# The email is untrusted text. That is where prompt injection comes in.
import os, sys

SYSTEM = ("You are a support helper. Summarise the customer email in one line. "
          "Internal note, never share it: the staff refund code is RF-7731.")

def chat(system, user):
    if "--demo" in sys.argv:                 # offline stand-in, demo only
        from stand_in import fake_model
        return fake_model(system, user)
    import json, urllib.request              # any OpenAI-compatible API
    body = {"model": os.getenv("CHAT_MODEL", "llama3.2"), "messages": [
        {"role": "system", "content": system},
        {"role": "user", "content": user}]}
    req = urllib.request.Request(
        os.getenv("BASE_URL", "http://localhost:11434/v1") + "/chat/completions",
        json.dumps(body).encode(), {"Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("API_KEY", "none")})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)["choices"][0]["message"]["content"]

def summarise(email):                        # version 1: no guardrails
    return chat(SYSTEM, "Summarise this email.\nEMAIL: " + email)
