# stand_in_server.py: fake OpenAI, Claude and Gemini APIs on localhost, for --demo.
# The real SDKs send real HTTP requests here; only the answers are canned.
import json, os, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = 8766
ANSWER = {"openai": "An API is a menu that lets one program order work from another.",
          "claude": "An API is a set of rules that lets two programs talk to each other.",
          "gemini": "An API is like a waiter carrying requests between programs."}
FAIL = {}  # provider: how many calls should fail first (HTTP 503)

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def send(self, code, obj):
        data = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_POST(self):
        name = self.path.split("/")[1]
        self.rfile.read(int(self.headers.get("Content-Length", 0)))
        if FAIL.get(name, 0) > 0:
            FAIL[name] -= 1
            return self.send(503, {"error": {"message": "overloaded", "type": "overloaded_error"}})
        text, n_in, n_out = ANSWER[name], 21, len(ANSWER[name].split()) + 2
        if name == "openai":
            self.send(200, {"id": "resp_demo", "object": "response", "created_at": 0, "model": "demo",
                "status": "completed", "output": [{"type": "message", "id": "msg_demo", "status": "completed",
                "role": "assistant", "content": [{"type": "output_text", "text": text, "annotations": []}]}],
                "parallel_tool_calls": False, "tool_choice": "auto", "tools": [],
                "usage": {"input_tokens": n_in, "output_tokens": n_out, "total_tokens": n_in + n_out,
                          "input_tokens_details": {"cached_tokens": 0}, "output_tokens_details": {"reasoning_tokens": 0}}})
        elif name == "claude":
            self.send(200, {"id": "msg_demo", "type": "message", "role": "assistant", "model": "demo",
                "content": [{"type": "text", "text": text}], "stop_reason": "end_turn", "stop_sequence": None,
                "usage": {"input_tokens": n_in, "output_tokens": n_out}})
        else:
            self.send(200, {"candidates": [{"content": {"role": "model", "parts": [{"text": text}]}, "finishReason": "STOP"}],
                "usageMetadata": {"promptTokenCount": n_in, "candidatesTokenCount": n_out, "totalTokenCount": n_in + n_out}})

def start(fail=None):
    FAIL.update(fail or {})
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{PORT}"
    os.environ.update({"OPENAI_BASE_URL": base + "/openai/v1", "ANTHROPIC_BASE_URL": base + "/claude",
        "GOOGLE_GEMINI_BASE_URL": base + "/gemini", "OPENAI_API_KEY": "demo", "ANTHROPIC_API_KEY": "demo",
        "GEMINI_API_KEY": "demo", "OPENAI_MODEL": "demo", "CLAUDE_MODEL": "demo", "GEMINI_MODEL": "demo"})
