# fake_llm.py: a stand-in model for the demo. NOT a real LLM: fixed answers, no API key.
# It can "fail" on purpose, like a busy provider returning 503, so we can test retries.
import time

PRICE = {"big-model": 2.00, "small-model": 0.20}   # rupees per 1K tokens (made-up demo prices)
FAIL = {"big-model": 2}                             # fail the next N calls to this model


class Overloaded(Exception):
    pass


def call(model, prompt):
    time.sleep(0.05)                                 # pretend network + thinking time
    if FAIL.get(model, 0) > 0:
        FAIL[model] -= 1
        raise Overloaded(f"{model}: 503 overloaded")
    tokens = 50 + 2 * len(prompt.split())
    cost = round(tokens / 1000 * PRICE[model], 3)
    return {"text": f"[{model}] answer to: {prompt[:28]}", "tokens": tokens, "cost": cost}
