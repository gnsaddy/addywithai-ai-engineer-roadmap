# switch_platform.py: the same prompt on three platforms, one loop.
import sys
from platforms import chat

PROMPT = "In one sentence: what is an AI platform?"
RUNS = [  # (platform, model name on THAT platform: copy it from its docs)
    ("ollama", "llama3.2"),
    ("groq", "llama-3.1-8b-instant"),
    ("openrouter", "meta-llama/llama-3.1-8b-instruct"),
]

if "--demo" in sys.argv:
    import stand_in_server
    stand_in_server.start()  # fake platforms on localhost, see the file

for platform, model in RUNS:
    text, out_tokens, secs = chat(platform, model, PROMPT)
    print(f"[{platform:<10}] {secs:4.1f}s {out_tokens:>3} tokens | {text}")
