# checks.py: deterministic evals. Plain code. Fast, free, same result always.
import json

def exact(answer, want):
    return answer.strip().lower() == want.lower()

def contains(answer, want):
    return want.lower() in answer.lower()

def valid_json(answer, keys):
    try:
        data = json.loads(answer)
    except ValueError:
        return False
    return isinstance(data, dict) and all(k in data for k in keys)

CHECKS = {"exact": exact, "contains": contains, "json": valid_json}
