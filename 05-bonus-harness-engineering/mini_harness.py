# mini_harness.py: a tiny agent harness
import json, sys
from fake_model import fake_model, stuck_model  # stand-in LLMs

# 1. TOOLS: plain Python functions the model can ask for
def get_weather(city):
    return {"city": city, "temp_c": 31, "sky": "sunny"}  # demo

def delete_file(path):
    return {"deleted": path}  # demo: nothing is really deleted

TOOLS = {"get_weather": get_weather, "delete_file": delete_file}

# 2. GUARDRAILS: what runs alone, and what needs a human
ALLOW = {"get_weather"}   # safe, read-only: runs by itself
ASK = {"delete_file"}     # risky: a human must say yes
MAX_STEPS = 5             # stop rule: never loop forever

def run_tool(name, args):
    if name not in ALLOW | ASK:
        return {"error": f"tool not allowed: {name}"}
    if name in ASK:
        ok = input(f"  Allow {name}({args})? [y/N] ")
        if ok.strip().lower() != "y":
            return {"error": "the user said no"}
    try:
        return TOOLS[name](**args)
    except Exception as e:
        return {"error": str(e)}  # errors go back to the model

# 3. LOGS: write every step to a file
def log(step, action, result=None):
    with open("harness_log.jsonl", "a") as f:
        f.write(json.dumps({"step": step, "action": action,
                            "result": result}) + "\n")

# 4. THE LOOP: model decides, harness acts, result goes back
def run_agent(task, model=fake_model):
    messages = [{"role": "user", "content": task}]
    for step in range(1, MAX_STEPS + 1):
        action = model(messages)
        if action["type"] == "answer":
            log(step, action)
            return action["text"]
        print(f"[step {step}] {action['tool']} {action['args']}")
        result = run_tool(action["tool"], action["args"])
        log(step, action, result)
        content = json.dumps(result)
        messages.append({"role": "tool", "content": content})
    return "Stopped: step limit reached."

if __name__ == "__main__":
    model = stuck_model if "--stuck" in sys.argv else fake_model
    task = "Weather in Bengaluru? Then delete notes.txt."
    print("Answer:", run_agent(task, model))
