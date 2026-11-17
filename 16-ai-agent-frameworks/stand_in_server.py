# stand_in_server.py: DEMO ONLY. A tiny local server that looks like an
# OpenAI-compatible chat API, so both frameworks run with no real model.
# It does not think. It follows fixed rules for the two demo questions.
# A real model (run without --demo) makes these choices itself.
import json, re, threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def text_of(m):
    c = m.get("content") or ""
    return c if isinstance(c, str) else " ".join(p.get("text", "") for p in c)

def call(tool, arg, thought, n):
    key = "query" if tool == "search_policy" else "expression"
    return {"role": "assistant", "content": thought, "tool_calls": [{
        "id": f"call_{n}", "type": "function", "function": {
            "name": tool, "arguments": json.dumps({key: arg})}}]}

def fake_model(messages):
    num = lambda pattern, text: re.search(pattern, text).group(1)
    q = next(text_of(m) for m in messages if m["role"] == "user")
    n, last = len(messages), text_of(messages[-1])
    seen = " ".join(text_of(m) for m in messages if m["role"] == "tool")
    if "claim" in q:
        if "claim" not in seen:
            return call("search_policy", "submit expense claim",
                        "I need the claim deadline.", n)
        return {"role": "assistant", "content": seen.split(". ")[0] + "."}
    if "Tokyo the hotel" not in seen:
        return call("search_policy", "hotel limit Tokyo",
                    "First, the hotel limit for Tokyo.", n)
    if "Meals" not in seen:
        return call("search_policy", "meals per day",
                    "Now the daily meal limit.", n)
    if not last.strip().isdigit():
        d, h = num(r"(\d+) nights", q), num(r"Tokyo .*? (\d+) US", seen)
        m = num(r"up to (\d+) US", seen)
        return call("calculator", f"{d} * {h} + {d} * {m}",
                    f"Hotel {h} a night, meals {m} a day. Add it up.", n)
    return {"role": "assistant",
            "content": f"Your max budget is {last.strip()} US dollars."}

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        msg = fake_model(body["messages"])
        done = "tool_calls" if msg.get("tool_calls") else "stop"
        out = json.dumps({
            "id": "demo", "object": "chat.completion", "created": 0,
            "model": body.get("model", "stand-in"),
            "choices": [{"index": 0, "message": msg, "finish_reason": done}],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0,
                      "total_tokens": 0}}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)
    def log_message(self, *args):
        pass

def start():
    server = HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{server.server_port}/v1"
