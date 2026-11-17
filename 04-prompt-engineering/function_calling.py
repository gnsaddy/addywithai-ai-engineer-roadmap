# Function calling: the model asks, YOUR code runs it. Stdlib only.
import json

ORDERS = {1042: "shipped, arriving Friday", 1043: "being packed"}

def get_order_status(order_id):
    return ORDERS.get(order_id, "not found")

TOOLS = [{  # what the model sees: name, description, JSON schema
    "name": "get_order_status",
    "description": "Look up where a customer's order is.",
    "parameters": {"type": "object",
                   "properties": {"order_id": {"type": "integer"}},
                   "required": ["order_id"]},
}]
FUNCTIONS = {"get_order_status": get_order_status}

def stand_in_model(messages, tools):
    """Offline stand-in for a chat API, so no API key is needed."""
    last = messages[-1]
    if last["role"] == "user":                 # model picks a tool
        return {"tool_call": {"name": "get_order_status",
                              "arguments": '{"order_id": 1042}'}}
    return {"text": f"Good news! Your order is {last['content']}."}

messages = [{"role": "user", "content": "Where is my order 1042?"}]
while True:
    reply = stand_in_model(messages, TOOLS)
    if "text" in reply:
        print("AI:", reply["text"])
        break
    call = reply["tool_call"]
    if call["name"] not in FUNCTIONS:          # only tools you allow
        raise ValueError("unknown tool")
    args = json.loads(call["arguments"])       # arguments = JSON text
    print(f"Model asks: {call['name']}({args})")
    result = FUNCTIONS[call["name"]](**args)   # YOUR code runs it
    print("Tool result:", result)
    messages.append({"role": "tool", "content": result})
