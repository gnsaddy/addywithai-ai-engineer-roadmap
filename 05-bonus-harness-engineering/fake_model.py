# fake_model.py: stand-in "LLMs" so the harness runs with no API key.
# A real LLM reads the messages and decides the next action.
# These follow a fixed script, so you can see what the harness does.
import json

def fake_model(messages):
    results = [json.loads(m["content"]) for m in messages if m["role"] == "tool"]
    if len(results) == 0:
        return {"type": "tool", "tool": "get_weather", "args": {"city": "Bengaluru"}}
    if len(results) == 1:
        return {"type": "tool", "tool": "delete_file", "args": {"path": "notes.txt"}}
    w, last = results[0], results[-1]
    did = "deleted notes.txt" if "deleted" in last else f"did not delete notes.txt ({last['error']})"
    return {"type": "answer", "text": f"{w['city']}: {w['temp_c']}°C, {w['sky']}. I {did}."}

def stuck_model(messages):
    # a confused model that keeps asking for the same tool, forever
    return {"type": "tool", "tool": "get_weather", "args": {"city": "Bengaluru"}}
