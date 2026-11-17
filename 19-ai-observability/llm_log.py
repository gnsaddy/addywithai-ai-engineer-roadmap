# llm_log.py: wrap every LLM call. Log tokens, cost, latency and errors.
import json, time, uuid
from stand_in import fake_chat   # demo only. Swap in your real client here.

LOG = "llm_calls.jsonl"          # one JSON line per call
PRICES = {                       # EXAMPLE prices, US dollars per 1M tokens
    "small-model": {"in": 0.15, "out": 0.60},
    "large-model": {"in": 2.50, "out": 10.00},
}

def cost_usd(model, tokens_in, tokens_out):
    p = PRICES[model]
    return (tokens_in * p["in"] + tokens_out * p["out"]) / 1_000_000

def logged_chat(model, messages, feature, trace_id=None):
    row = {"time": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "trace_id": trace_id or uuid.uuid4().hex[:8],
           "feature": feature, "model": model, "status": "ok"}
    start = time.perf_counter()
    try:
        reply = fake_chat(model, messages)
        usage = reply["usage"]                    # the API counts the tokens
        row["tokens_in"] = usage["prompt_tokens"]
        row["tokens_out"] = usage["completion_tokens"]
        row["cost_usd"] = round(cost_usd(model, row["tokens_in"],
                                         row["tokens_out"]), 6)
        return reply["choices"][0]["message"]["content"]
    except Exception as e:
        row["status"], row["error"] = "error", str(e)
        raise
    finally:                                      # runs on success AND error
        row["latency_ms"] = round((time.perf_counter() - start) * 1000)
        with open(LOG, "a") as f:
            f.write(json.dumps(row) + "\n")
