# app.py: a pretend app with three features. Every call goes through
# logged_chat(), so every call lands in llm_calls.jsonl.
import os, uuid
from llm_log import LOG, logged_chat

FEATURES = {                     # feature -> (model, calls in this demo)
    "chat": ("small-model", 60),
    "summary": ("small-model", 25),
    "report": ("large-model", 15),
}

def handle_request(feature, model, text):
    trace_id = uuid.uuid4().hex[:8]       # one id for the whole request
    messages = [{"role": "user", "content": text}]
    try:
        if feature == "report":           # 2 steps, same trace id
            plan = logged_chat("small-model", messages, "report", trace_id)
            messages.append({"role": "user", "content": plan})
        return logged_chat(model, messages, feature, trace_id)
    except Exception:
        return "Sorry, please try again."   # the user sees a kind message

if __name__ == "__main__":
    if os.path.exists(LOG):
        os.remove(LOG)
    for feature, (model, calls) in FEATURES.items():
        for i in range(calls):
            handle_request(feature, model, f"request {i} " * 20)
    print("done. calls logged to", LOG)
