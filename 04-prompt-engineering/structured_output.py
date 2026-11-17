# Structured output: ask for JSON, then check it. Stdlib only.
import json

PROMPT = '''Read the customer message. Reply with ONLY this JSON:
{"order_id": number, "issue": "damaged" | "late" | "other",
 "refund": true or false}
Message: "Order 1042 came torn. I want my money back."'''

SCHEMA = {"order_id": int, "issue": str, "refund": bool}
ISSUES = {"damaged", "late", "other"}

def parse(reply):
    try:
        data = json.loads(reply)
    except json.JSONDecodeError as e:
        return None, f"not JSON ({e.msg})"
    for key, kind in SCHEMA.items():
        if not isinstance(data.get(key), kind):
            return None, f"'{key}' missing or wrong type"
    if data["issue"] not in ISSUES:
        return None, "unknown issue"
    return data, "ok"

# Three replies a model might give (sample text, no API call).
# Not ok? Send the error back to the model and ask again.
replies = [
    'Sure! Here is the JSON: {"order_id": 1042, "issue": "damaged"}',
    '{"order_id": 1042, "issue": "damaged"}',
    '{"order_id": 1042, "issue": "damaged", "refund": true}',
]
for reply in replies:
    data, status = parse(reply)
    print(f"{status:<31} -> {data}")
