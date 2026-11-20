# server.py: an MCP server written by hand. No SDK: just JSON-RPC 2.0 over stdio.
# The client starts this file as a child process. Requests come in on stdin,
# one JSON message per line. Answers go out on stdout. Logs go to stderr ONLY.
import json, os, sys
from pydantic import ValidationError
from tools import TOOLS, tool_list

SUPPORTED = ["2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05"]
MAX_CHARS = 2000                      # never flood the model's context

def log(*parts):                      # stderr is safe: the client shows it as logs
    print("[server]", *parts, file=sys.stderr, flush=True)

def send(msg: dict):                  # stdout is the wire: JSON only, one per line
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()

def reply(id, result):
    send({"jsonrpc": "2.0", "id": id, "result": result})

def error(id, code, message):
    send({"jsonrpc": "2.0", "id": id, "error": {"code": code, "message": message}})

POLICY = ("Returns: books can be returned within 7 days of delivery if unread. "
          "Refunds reach the original payment method in 3 to 5 working days.")

def initialize(params):
    asked = params.get("protocolVersion")
    version = asked if asked in SUPPORTED else SUPPORTED[0]
    log("client:", params.get("clientInfo", {}).get("name"), "| version", version)
    return {"protocolVersion": version,
            "capabilities": {"tools": {"listChanged": False}, "resources": {}},
            "serverInfo": {"name": "pageturn-books", "version": "1.0.0"},
            "instructions": "Read-only tools for PageTurn Books orders and parcels."}

def result(text, is_error, data=None):   # the shape MCP clients expect from tools/call
    r = {"content": [{"type": "text", "text": text[:MAX_CHARS]}], "isError": is_error}
    if data is not None:
        r["structuredContent"] = data
    return r

def call_tool(params):
    name, args = params.get("name"), params.get("arguments") or {}
    tool = TOOLS.get(name)
    if tool is None:                  # unknown tool = protocol error
        raise KeyError(f"Unknown tool: {name}")
    try:
        data = tool["fn"](tool["args"].model_validate(args))
    except ValidationError as e:      # bad arguments = tool error the model can fix
        bad = [f"{'.'.join(map(str, x['loc']))}: {x['msg']}" for x in e.errors()]
        return result("Invalid arguments: " + "; ".join(bad), True)
    except LookupError as e:          # a known failure: tell the model what to do next
        return result(str(e), True)
    return result(json.dumps(data, ensure_ascii=False), False, data)

RESOURCE = {"uri": "policy://returns", "name": "returns-policy", "mimeType": "text/plain",
            "description": "PageTurn Books return and refund rules"}

def read_resource(params):
    if params.get("uri") != "policy://returns":
        raise KeyError(f"Unknown resource: {params.get('uri')}")
    return {"contents": [{"uri": "policy://returns", "mimeType": "text/plain",
                          "text": POLICY}]}

HANDLERS = {
    "initialize": initialize,
    "ping": lambda p: {},
    "tools/list": lambda p: {"tools": tool_list()},
    "tools/call": call_tool,
    "resources/list": lambda p: {"resources": [RESOURCE]},
    "resources/read": read_resource,
}

def handle(line: str):
    try:
        msg = json.loads(line)
    except json.JSONDecodeError:
        return error(None, -32700, "Parse error: not valid JSON")
    if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0" or "method" not in msg:
        return error(msg.get("id") if isinstance(msg, dict) else None, -32600, "Invalid Request")
    method, id = msg["method"], msg.get("id")
    if id is None:                    # a notification: never send a reply
        log("notification:", method)
        return
    handler = HANDLERS.get(method)
    if handler is None:
        log("method not found:", method)
        return error(id, -32601, f"Method not found: {method}")
    try:
        reply(id, handler(msg.get("params") or {}))
    except KeyError as e:
        error(id, -32602, e.args[0])
    except Exception as e:            # never crash the loop on one bad request
        log("internal error:", repr(e))
        error(id, -32603, "Internal error")

def main():
    log("pageturn-books MCP server ready (stdio)")
    if os.environ.get("BAD_PRINT"):   # the classic bug, on purpose: a print() to stdout
        print("Server started!")
    for line in sys.stdin:            # one JSON-RPC message per line
        if line.strip():
            handle(line)
    log("stdin closed, bye")

if __name__ == "__main__":
    main()
