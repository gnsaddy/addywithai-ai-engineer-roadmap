# fallback.py: try the free local model first, then hosted backups.
import sys, urllib.error
from platforms import chat

CHAIN = [  # first that answers wins
    ("ollama", "llama3.2"),                 # free, private, on your laptop
    ("groq", "llama-3.1-8b-instant"),       # hosted backup 1
    ("together", "meta-llama/Llama-3.3-70B-Instruct-Turbo"),  # backup 2
]

def ask(prompt):
    for platform, model in CHAIN:
        try:
            text, _, secs = chat(platform, model, prompt, timeout=20)
            print(f"  OK   {platform} ({secs:.1f}s)")
            return text
        except urllib.error.HTTPError as e:   # e.g. 429 rate limit
            print(f"  SKIP {platform}: HTTP {e.code}")
        except (urllib.error.URLError, TimeoutError):  # offline
            print(f"  SKIP {platform}: not reachable")
    raise RuntimeError("every platform failed")

if "--demo" in sys.argv:
    import stand_in_server
    stand_in_server.start(offline=["ollama"], rate_limited=["groq"])

print("Answer:", ask("Give me one tip to learn AI faster."))
