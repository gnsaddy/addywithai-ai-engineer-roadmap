# stand_in.py: DEMO ONLY. A fake model with made-up answers, token counts and
# speed, so the logging runs offline. It does not think. A real API returns
# real token counts in "usage", and takes real time.
import random, time

rng = random.Random(7)                # same "random" numbers on every run
SPEED = {"small-model": 0.1, "large-model": 0.3}   # seconds, scaled down

def fake_chat(model, messages):
    time.sleep(SPEED[model] * rng.uniform(0.6, 1.4))
    if rng.random() < 0.08:           # sometimes the API fails
        raise TimeoutError("model timed out")
    if rng.random() < 0.06:           # sometimes it is very slow
        time.sleep(SPEED[model] * 6)
    words = sum(len(m["content"].split()) for m in messages)
    return {"choices": [{"message": {"content": "(demo answer)"}}],
            "usage": {"prompt_tokens": words * 4 // 3 + rng.randint(200, 900),
                      "completion_tokens": rng.randint(40, 400)}}
