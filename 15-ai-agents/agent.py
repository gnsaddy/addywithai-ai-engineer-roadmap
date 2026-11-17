# agent.py: an AI agent from scratch. Two tools, one ReAct loop.
import json
from models import chat
from schemas import SCHEMAS
from tools import TOOLS

SYSTEM = ("You help with travel expenses. Think step by step. Use a tool "
          "when you need a policy fact or maths. Never guess numbers. "
          "When you are done, give a short final answer.")

def short(text, n=64):
    return text if len(text) <= n else text[:n - 3] + "..."

def act(call):
    name = call["function"]["name"]
    args = json.loads(call["function"]["arguments"] or "{}")
    try:
        return name, args, TOOLS[name](**args)
    except Exception as e:                  # bad tool or bad input
        return name, args, f"error: {e}"

def run_agent(question, max_steps=6):
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": question}]
    for step in range(1, max_steps + 1):
        reply = chat(messages, SCHEMAS)     # 1 Reason
        messages.append(reply)
        if not reply.get("tool_calls"):     # no tool call = final answer
            return reply["content"]
        print(f"  think {step}: {reply.get('content') or '...'}")
        for call in reply["tool_calls"]:
            name, args, result = act(call)  # 2 Act
            arg = next(iter(args.values()), "")
            print(f"  act   {step}: {name}({arg!r})")
            print(f"  see   {step}: {short(result)}")
            messages.append({"role": "tool", "content": result,
                             "tool_call_id": call["id"]})  # 3 Observe
    return "Stopped: too many steps."   # a safety limit, always

QUESTIONS = [
    "I stay 3 nights in Tokyo, with 3 days of meals. What is my max budget?",
    "When must I submit my expense claim?",
]

if __name__ == "__main__":
    for q in QUESTIONS:
        print("Q:", q)
        print("A:", run_agent(q), "\n")
