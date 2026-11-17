# models.py: two embedding models, ONE shape: embed(texts) -> list of vectors.
# Real mode: any OpenAI-compatible /embeddings API (Ollama, OpenAI, Jina...).
#   e.g. Ollama: ollama pull nomic-embed-text   and   ollama pull all-minilm
# Demo mode (--demo): two TOY models, so you can see why models differ.
import json, os, re, urllib.request, zlib

def api_model(name):
    def embed(texts):
        body = {"model": name, "input": texts}
        key = os.environ.get("API_KEY", "none")
        req = urllib.request.Request(os.environ["BASE_URL"] + "/embeddings",
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer " + key})
        with urllib.request.urlopen(req, timeout=60) as r:
            return [d["embedding"] for d in json.load(r)["data"]]
    return embed

def words(text):
    return re.findall(r"[a-z0-9]+", text.lower())

# TOY model A: "word match". Each word lands in one of 64 buckets (a hash).
# Same word = same bucket. It knows nothing about meaning.
def toy_word_match(texts):
    vecs = []
    for t in texts:
        v = [0.0] * 64
        for w in words(t):
            v[zlib.crc32(w.encode()) % 64] += 1
        vecs.append(v)
    return vecs

# TOY model B: "meaning". A tiny hand-made table maps words to 8 ideas,
# so different words with the same meaning get the same numbers.
IDEAS = ["account", "power", "money", "printer", "settings", "time", "app", "plan"]
TABLE = {  # word -> idea number (a real model LEARNS this from billions of texts)
    "password": 0, "login": 0, "forgot": 0, "battery": 1, "power": 1, "dies": 1,
    "runs": 1, "laptop": 1, "computer": 1, "refunds": 2, "money": 2, "bank": 2,
    "back": 2, "printer": 3, "paper": 3, "language": 4, "settings": 4, "office": 5,
    "closed": 5, "holidays": 5, "days": 5, "app": 6, "crashes": 6, "closes": 6,
    "upload": 6, "photo": 6, "picture": 6, "cancel": 7, "stop": 7, "plan": 7,
    "subscription": 7, "billing": 7,
}
def toy_meaning(texts):
    vecs = []
    for t in texts:
        v = [0.0] * len(IDEAS)
        for w in words(t):
            if w in TABLE:
                v[TABLE[w]] += 1
        vecs.append(v)
    return vecs
