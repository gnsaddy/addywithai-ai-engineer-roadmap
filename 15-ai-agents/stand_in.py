# stand_in.py: DEMO ONLY. A scripted fake model, so the loop runs offline.
# It does not think. It follows fixed rules for the two demo questions.
# A real model (models.py without --demo) makes these choices itself.
import json, re
def call(tool, arg, thought, n):
    key = "query" if tool == "search_policy" else "expression"
    return {"role": "assistant", "content": thought, "tool_calls": [{
        "id": f"call_{n}", "type": "function", "function": {
            "name": tool, "arguments": json.dumps({key: arg})}}]}
def fake_model(messages):
    num = lambda pattern, text: re.search(pattern, text).group(1)
    q, n, last = messages[1]["content"], len(messages), messages[-1]
    seen = " ".join(m["content"] for m in messages if m["role"] == "tool")
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
    if not last["content"].isdigit():
        d, h = num(r"(\d+) nights", q), num(r"Tokyo .*? (\d+) US", seen)
        m = num(r"up to (\d+) US", seen)
        return call("calculator", f"{d} * {h} + {d} * {m}",
                    f"Hotel {h} a night, meals {m} a day. Add it up.", n)
    return {"role": "assistant", "content":
            f"Your max budget is {last['content']} US dollars."}
