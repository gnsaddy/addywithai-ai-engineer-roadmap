# voice_agent.py: a tiny voice agent = ears -> brain -> voice (Episode 21)
# The "brain" here is a DEMO stand-in with fixed rules (no real LLM),
# so you can see the pipeline and time every stage.
import re
import time
from ears_and_voice import speak, listen

def think(text):                       # demo brain: fixed rules only
    people = re.search(r"for (\w+)", text)
    when = re.search(r"at (\d{1,2}):?(\d{2})", text)
    if not (people and when):
        return "Sorry, how many people, and what time?"
    h, m = when.groups()
    return (f"Done. A table for {people.group(1)}, tomorrow at "
            f"{h}:{m} pm, by the window.")

if __name__ == "__main__":
    times = {}
    t = time.time(); heard = listen("order.wav"); times["hear"] = time.time() - t
    t = time.time(); reply = think(heard); times["think"] = time.time() - t
    t = time.time(); speak(reply, "reply.wav"); times["speak"] = time.time() - t
    print("heard :", heard)
    print("reply :", reply)
    print(" | ".join(f"{k} {v:.2f}s" for k, v in times.items()),
          f"| total {sum(times.values()):.2f}s")
