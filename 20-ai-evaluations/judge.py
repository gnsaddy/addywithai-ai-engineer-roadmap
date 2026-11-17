# judge.py: a model-based eval. An LLM grades the answer against a rubric.
import json, sys
from stand_in import fake_judge

RUBRIC = """You are a strict grader. Compare the ANSWER with the REFERENCE.
Score 5 = same facts, nothing wrong. 3 = partly right. 1 = wrong or missing.
Reply as JSON only: {{"score": 1-5, "reason": "one short sentence"}}
QUESTION: {ask}
REFERENCE: {want}
ANSWER: {got}"""

def judge(case, got, pass_score=4):
    prompt = RUBRIC.format(ask=case["ask"], want=case["want"], got=got)
    if "--demo" in sys.argv:                 # offline stand-in, demo only
        raw = fake_judge(prompt)
    else:
        from models import chat              # use a strong model as the judge
        raw = chat("You grade answers.", prompt)
    result = json.loads(raw)                 # the judge must return JSON
    return result["score"] >= pass_score, result
