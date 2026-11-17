# embedder.py: embed(texts) -> vectors.
# Real mode: any OpenAI-compatible /embeddings API, e.g. Ollama + nomic-embed-text.
# Demo mode (--demo): a TOY embedder with 6 hand-made ideas, so you can check it.
import json, os, re, sys, urllib.request

def embed_api(texts):
    body = {"model": os.environ.get("EMBED_MODEL", "nomic-embed-text"), "input": texts}
    req = urllib.request.Request(os.environ["BASE_URL"] + "/embeddings",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + os.environ.get("API_KEY", "none")})
    with urllib.request.urlopen(req, timeout=60) as r:
        return [d["embedding"] for d in json.load(r)["data"]]

IDEAS = {  # toy only: idea -> words that point to it
    "time off": "leave holiday holidays days vacation off sick weeks",
    "family":   "parents parental baby child family",
    "laptop":   "laptop computer slow restart apps new",
    "security": "password share two-factor login lost phone report",
    "manager":  "manager ask notice approval",
    "money":    "paid salary pay bonus",
}
def embed_toy(texts):
    out = []
    for t in texts:
        ws = re.findall(r"[a-z-]+", t.lower())
        out.append([float(sum(w in words.split() for w in ws)) for words in IDEAS.values()])
    return out

embed = embed_toy if "--demo" in sys.argv else embed_api
