# time_and_price.py: the same prompt on several models, timed and priced.
# Real mode: any OpenAI-compatible API (set BASE_URL and API_KEY).
# Demo mode: python time_and_price.py --demo  (stand-ins, example prices)
import json, os, sys, time, urllib.request  # standard library only

PROMPT = "Explain what an API is to a 10 year old, in 3 sentences."
MODELS = {  # model: (US$ per 1M input tokens, US$ per 1M output tokens)
    "small": (0.10, 0.40),
    "medium": (0.50, 2.00),
    "large": (3.00, 15.00),
}  # example prices: copy real ones from your provider's pricing page

def ask(model, prompt):
    msgs = [{"role": "user", "content": prompt}]
    key = os.environ.get("API_KEY", "")  # never write keys in code
    req = urllib.request.Request(os.environ["BASE_URL"] + "/chat/completions",
        data=json.dumps({"model": model, "messages": msgs}).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + key})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.load(r)
    use = data["usage"]  # the API counts the tokens for us
    text = data["choices"][0]["message"]["content"]
    return text, use["prompt_tokens"], use["completion_tokens"]

if "--demo" in sys.argv:
    from stand_in import ask

print(f"{'model':<9}{'time':>7}{'in':>5}{'out':>5}{'1 call':>11}{'month*':>10}")
for model, (price_in, price_out) in MODELS.items():
    start = time.time()
    text, n_in, n_out = ask(model, PROMPT)
    secs = time.time() - start
    cost = (n_in * price_in + n_out * price_out) / 1_000_000
    month = cost * 10_000 * 30  # 10,000 calls a day for 30 days
    print(f"{model:<9}{secs:>6.1f}s{n_in:>5}{n_out:>5}"
          f"{'$%.5f' % cost:>11}{'$%.0f' % month:>10}")
print("* month = 10,000 calls a day for 30 days")
