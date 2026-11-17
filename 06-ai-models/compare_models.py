# compare_models.py: same questions, two models, one score card.
# Real mode: any OpenAI-compatible API (Ollama on a laptop, or hosted).
# Demo mode: python compare_models.py --demo  (two stand-ins, no setup)
import json, os, sys, time, urllib.request  # standard library only

TESTS = [  # (question, a word the right answer must contain)
    ("What is the capital of France?", "paris"),
    ("What is 12 * 12?", "144"),
    ("Which planet is called the red planet?", "mars"),
    ("What is H2O usually called?", "water"),
    ("Which gas do plants take in for photosynthesis?", "carbon dioxide"),
]

def chat(base_url, model, question, key="none"):
    msgs = [{"role": "user", "content": question}]
    body = {"model": model, "messages": msgs}
    req = urllib.request.Request(base_url + "/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + key})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)["choices"][0]["message"]["content"]

MODELS = {  # name: (ask function, US$ per 1M tokens)
    "local": (lambda q: chat("http://localhost:11434/v1",
              os.environ.get("LOCAL_MODEL", "llama3.2:3b"), q), 0.0),
    "hosted": (lambda q: chat(os.environ.get("HOSTED_BASE_URL", ""),
               os.environ.get("HOSTED_MODEL", ""), q,
               os.environ.get("HOSTED_API_KEY", "")),
               float(os.environ.get("HOSTED_PRICE_PER_M", "1.0"))),
}

if "--demo" in sys.argv:  # stand-ins: canned answers + a fake delay
    from stand_in import MODELS

def score(ask):
    correct, secs, chars = 0, 0.0, 0
    for question, must in TESTS:
        start = time.time()
        answer = ask(question)
        secs += time.time() - start
        correct += must in answer.lower()
        chars += len(question) + len(answer)
    return correct, secs / len(TESTS), chars / 4  # ~4 chars a token

print(f"{'model':<8}{'correct':>9}{'avg time':>10}{'cost / 1k runs':>16}")
for name, (ask, price_per_m) in MODELS.items():
    correct, avg, tokens = score(ask)
    cost = "$%.2f" % (tokens / 1_000_000 * price_per_m * 1000)
    print(f"{name:<8}{correct:>6}/{len(TESTS)}{avg:>9.2f}s{cost:>16}")
