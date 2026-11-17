# stand_in_server.py: DEMO ONLY. A fake multimodal API on your computer.
# It speaks the same HTTP shapes as OpenAI, Gemini, Vertex AI and ElevenLabs, but
# answers with FIXED data (no model, no thinking), so --demo runs offline.
# Run: python stand_in_server.py   (then: python vision.py --demo, etc.)
import base64, io, json, math, re, struct, wave
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from PIL import Image, ImageDraw

RECEIPT = {"shop": "UDUPI CAFE", "total": 273.0, "items": 4}
HEARD = "Book a table for two at 7:30 tomorrow, near the window."
JOBS = {}                                # video jobs: id -> polls

def image_tokens(b64, detail):          # same GPT-4o style tile rule as Ep 21
    w, h = Image.open(io.BytesIO(base64.b64decode(b64))).size
    if detail == "low":
        return 85
    s = min(1, 2048 / max(w, h)); w, h = w * s, h * s
    s = min(1, 768 / min(w, h)); w, h = w * s, h * s
    return 85 + 170 * math.ceil(w / 512) * math.ceil(h / 512)

def beep_wav(seconds=1.0, sr=16000):    # a short tone, not a real voice
    buf = io.BytesIO(); f = wave.open(buf, "wb")
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(sr)
    f.writeframes(b"".join(struct.pack("<h", int(3000 * math.sin(i / 8)))
                           for i in range(int(sr * seconds))))
    f.close(); return buf.getvalue()

def poster_png():
    img = Image.new("RGB", (1024, 1024), (244, 235, 221))
    ImageDraw.Draw(img).text((420, 500), "DEMO IMAGE", fill=(124, 45, 18))
    buf = io.BytesIO(); img.save(buf, "PNG"); return buf.getvalue()

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def send(self, body, ctype="application/json", code=200):
        if not isinstance(body, bytes):
            body = json.dumps(body).encode()
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body))); self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        raw = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        p = self.path.split("?")[0]
        if p == "/v1/chat/completions":
            part = [c for c in json.loads(raw)["messages"][0]["content"]
                    if c["type"] == "image_url"][0]["image_url"]
            tok = 20 + image_tokens(part["url"].split(",", 1)[1],
                                    part.get("detail", "auto"))
            msg = {"role": "assistant", "content": json.dumps(RECEIPT)}
            return self.send({"id": "demo", "object": "chat.completion",
                "created": 0, "model": "stand-in", "choices": [{"index": 0,
                "message": msg, "finish_reason": "stop"}], "usage": {
                "prompt_tokens": tok, "completion_tokens": 18,
                "total_tokens": tok + 18}})
        if re.match(r"/v1(beta)?/models/.+:generateContent", p):
            return self.send({"candidates": [{"content": {"role": "model",
                "parts": [{"text": json.dumps(RECEIPT)}]}}],
                "usageMetadata": {"promptTokenCount": 258 + 24,
                "candidatesTokenCount": 18, "totalTokenCount": 300}})
        if p == "/v1/audio/transcriptions":
            return self.send({"text": HEARD})
        if p == "/v1/audio/speech" or p.startswith("/v1/text-to-speech/"):
            return self.send(beep_wav(), "audio/mpeg")
        if p == "/v1/images/generations":
            b64 = base64.b64encode(poster_png()).decode()
            return self.send({"created": 0, "data": [{"b64_json": b64}]})
        if p.endswith(":predictLongRunning"):        # start a video job
            vid = f"veo_demo{len(JOBS) + 1}"; JOBS[vid] = 0
            return self.send({"name": f"models/veo/operations/{vid}"})
        if p.endswith(":fetchPredictOperation"):     # poll the job
            vid = json.loads(raw)["operationName"].rsplit("/", 1)[-1]
            JOBS[vid] += 1                           # done on the 3rd poll
            op = {"name": f"models/veo/operations/{vid}",
                  "done": JOBS[vid] >= 3}
            if op["done"]:
                clip = open("stand_in_clip.mp4", "rb").read()
                op["response"] = {"videos": [{"mimeType": "video/mp4",
                    "bytesBase64Encoded": base64.b64encode(clip).decode()}]}
            return self.send(op)
        self.send({"error": "not in the stand-in: " + p}, code=404)


if __name__ == "__main__":
    print("DEMO stand-in on http://127.0.0.1:8022 (fixed answers, no model)")
    ThreadingHTTPServer(("127.0.0.1", 8022), H).serve_forever()
