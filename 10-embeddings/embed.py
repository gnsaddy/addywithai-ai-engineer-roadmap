# embed.py: turn text into embeddings (lists of numbers) + cosine similarity.
# Real mode: any OpenAI-compatible /embeddings API, e.g. Ollama:
#   ollama pull nomic-embed-text   (BASE_URL=http://localhost:11434/v1)
# Demo mode (--demo): a toy embedder with 4 hand-made meaning dimensions.
import json, math, os, sys, urllib.request  # standard library only

def embed_api(texts):
    body = {"model": os.environ.get("EMBED_MODEL", "nomic-embed-text"),
            "input": texts}
    req = urllib.request.Request(os.environ["BASE_URL"] + "/embeddings",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + os.environ.get("API_KEY", "none")})
    with urllib.request.urlopen(req, timeout=60) as r:
        return [d["embedding"] for d in json.load(r)["data"]]

def cosine(a, b):  # 1.0 = same meaning, near 0 = unrelated
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

if "--demo" in sys.argv:
    from toy_embedder import embed
else:
    embed = embed_api
