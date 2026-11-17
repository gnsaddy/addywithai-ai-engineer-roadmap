# gateway.py: a tiny AI gateway. One ask() for every provider, plus
# retries, fallback and a cost log. Demo: python gateway.py --demo
import sys, time
from three_sdks import ask_openai, ask_claude, ask_gemini

PROVIDERS = {"claude": ask_claude, "openai": ask_openai, "gemini": ask_gemini}
PRICE = {"claude": (3.00, 15.00), "openai": (1.25, 10.00),
         "gemini": (0.30, 2.50)}  # example US$ per 1M in / out tokens
LOG = []

def ask(prompt, route=("claude", "openai", "gemini"), retries=2):
    for name in route:                      # fallback: next provider
        for attempt in range(1, retries + 1):   # retry: same provider
            try:
                start = time.time()
                text, n_in, n_out = PROVIDERS[name](prompt)
            except Exception as e:
                print(f"  {name} try {attempt}: {type(e).__name__}")
                time.sleep(0.5 * attempt)   # back off a little
                continue
            p_in, p_out = PRICE[name]
            cost = (n_in * p_in + n_out * p_out) / 1_000_000
            LOG.append((name, round(time.time() - start, 2), n_in, n_out, cost))
            return text
    raise RuntimeError("all providers failed")

if __name__ == "__main__":
    if "--demo" in sys.argv:
        import stand_in_server
        stand_in_server.start(fail={"claude": 2, "openai": 1})
    print("Answer 1:", ask("What is an API? One sentence."))
    print("Answer 2:", ask("What is an API? One sentence."))
    for name, secs, n_in, n_out, cost in LOG:
        print(f"log: {name:<7} {secs}s in={n_in} out={n_out} ${cost:.6f}")
