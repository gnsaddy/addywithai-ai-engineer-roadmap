# models.py: embed() and chat() through any OpenAI-compatible API (e.g. Ollama).
# With --demo, both use stand_in.py instead (labelled stand-ins, no model).
import json, os, sys, urllib.request
DEMO = "--demo" in sys.argv

def post(path, body):
    req = urllib.request.Request(os.environ["BASE_URL"] + path,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + os.environ.get("API_KEY", "x")})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)

def embed(texts):
    if DEMO:
        from stand_in import toy_embed
        return toy_embed(texts)
    model = os.environ.get("EMBED_MODEL", "nomic-embed-text")
    data = post("/embeddings", {"model": model, "input": texts})
    return [d["embedding"] for d in data["data"]]

def chat(messages):
    if DEMO:
        from stand_in import fake_llm
        return fake_llm(messages)
    model = os.environ.get("CHAT_MODEL", "llama3.2")
    data = post("/chat/completions",
                {"model": model, "messages": messages, "temperature": 0})
    return data["choices"][0]["message"]["content"]
