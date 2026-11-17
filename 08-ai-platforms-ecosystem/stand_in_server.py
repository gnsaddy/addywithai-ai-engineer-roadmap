# stand_in_server.py: fake OpenAI-compatible platforms on localhost, for --demo.
# Real HTTP requests go through platforms.chat(); only the answers are canned.
import json, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import platforms

PORT = 8765
DELAY = {"ollama": 0.9, "lmstudio": 1.0, "openrouter": 0.7,
         "together": 0.6, "groq": 0.2, "fireworks": 0.3}  # demo seconds
ANSWERS = {
    "In one sentence: what is an AI platform?":
        "A service that runs AI models for you behind an API.",
    "Give me one tip to learn AI faster.":
        "Build one tiny project every week.",
}

class Handler(BaseHTTPRequestHandler):
    rate_limited = set()
    def log_message(self, *a): pass
    def do_POST(self):
        name = self.path.split("/")[1]
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        if name in self.rate_limited:
            self.send_response(429); self.end_headers(); return
        time.sleep(DELAY.get(name, 0.5))
        text = ANSWERS.get(body["messages"][-1]["content"], "Hello from " + name)
        out = {"choices": [{"message": {"role": "assistant", "content": text}}],
               "usage": {"prompt_tokens": 12, "completion_tokens": len(text.split()) + 3}}
        data = json.dumps(out).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)

def start(offline=(), rate_limited=()):
    Handler.rate_limited = set(rate_limited)
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    for name in platforms.PLATFORMS:  # point every platform at the stand-in
        url = f"http://127.0.0.1:{PORT}/{name}/v1"
        if name in offline:
            url = "http://127.0.0.1:9/v1"  # nothing listens here = offline
        platforms.PLATFORMS[name] = (url, None)
