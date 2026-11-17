# app.py: the app we are testing. Two prompt versions of a policy helper.
import sys
from stand_in import fake_app

PROMPTS = {
    "v1": "You answer questions about the travel policy.",
    "v2": ("You answer questions about the travel policy. Follow the format "
           "the user asks for. If it is not in the policy, say I don't know. "
           "Keep answers very short."),
}

def answer(version, case):
    if "--demo" in sys.argv:                 # offline stand-in, demo only
        return fake_app(version, case["id"])
    from models import chat                  # your real model call goes here
    return chat(PROMPTS[version], case["ask"])
