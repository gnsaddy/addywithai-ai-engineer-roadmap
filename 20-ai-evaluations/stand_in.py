# stand_in.py: DEMO ONLY. Fixed answers for two prompt versions, and a fake
# judge, so the evals run offline. Nothing here thinks. With a real model,
# app.py sends the prompt and judge.py asks a strong model to grade.
import json, re

V1 = {   # answers "from prompt version 1"
    1: "The hotel limit in Tokyo is 250 US dollars.", 2: "60",
    3: "30", 4: "The wifi password is guest1234.",
    5: "Tokyo has a limit of 250.",
    6: "Hotels are covered up to 150 dollars per night, and 250 in London, "
       "New York and Tokyo.",
    7: "Submit your claim in the Expenses app within 30 days of the trip.",
    8: "Yes. Meals are covered up to 60 dollars per day.",
}
V2 = dict(V1)   # prompt version 2 fixes three answers, and breaks one
V2.update({1: "250", 4: "I don't know. It is not in the policy.",
           5: '{"city": "Tokyo", "limit": 250}',
           7: "Just send your receipts to your manager."})

def fake_app(version, case_id):
    return (V1 if version == "v1" else V2)[case_id]

def fake_judge(prompt):
    """Scores by counting shared key words. A real judge reads the meaning."""
    want = re.search(r"REFERENCE: (.*)", prompt).group(1)
    got = re.search(r"ANSWER: (.*)", prompt).group(1)
    key = set(re.findall(r"\d+|[a-z]{5,}", want.lower()))
    hit = len(key & set(re.findall(r"\d+|[a-z]{5,}", got.lower()))) / len(key)
    score = 5 if hit >= 0.6 else 3 if hit >= 0.4 else 1
    why = "matches the reference" if score == 5 else "misses key facts"
    return json.dumps({"score": score, "reason": why})
