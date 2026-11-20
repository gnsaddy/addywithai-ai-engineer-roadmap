# client.py: a tiny scripted MCP client.
# It starts server.py, then talks JSON-RPC over the server's stdin and stdout.
# Run: python client.py          (the full demo)
#      python client.py --bad    (the server prints to stdout by mistake: watch it break)
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))

class Client:
    def __init__(self, env=None):
        self.p = subprocess.Popen([sys.executable, os.path.join(HERE, "server.py")],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, text=True, env=env)
        self.next_id = 0

    def request(self, method, params=None):
        self.next_id += 1
        self.notify(method, params, id=self.next_id)
        line = self.p.stdout.readline()           # the answer is the next line on stdout
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            raise RuntimeError(f"server sent something that is not JSON: {line.strip()!r}")
        if msg.get("id") != self.next_id:
            raise RuntimeError(f"wrong id in answer: {msg}")
        return msg

    def notify(self, method, params=None, id=None):
        msg = {"jsonrpc": "2.0", "method": method, **({"id": id} if id else {}),
               **({"params": params} if params is not None else {})}
        self.p.stdin.write(json.dumps(msg) + "\n")
        self.p.stdin.flush()

    def close(self):
        self.p.stdin.close()
        self.p.wait(timeout=5)

def show(title, msg):
    print(f"\n>> {title}")
    if "error" in msg:
        print("   ERROR", msg["error"]["code"], msg["error"]["message"])
        return
    r = msg["result"]
    for c in r.get("content", []):
        print("   isError:", r["isError"], "|", c["text"])

def main():
    bad = "--bad" in sys.argv
    c = Client(env=dict(os.environ, BAD_PRINT="1") if bad else None)
    # 1) handshake: initialize, then the initialized notification
    init = c.request("initialize", {"protocolVersion": "2025-11-25", "capabilities": {},
                                    "clientInfo": {"name": "tiny-client", "version": "0.1"}})
    r = init["result"]
    print(">> initialize:", r["serverInfo"]["name"], "| version", r["protocolVersion"],
          "| capabilities", list(r["capabilities"]))
    c.notify("notifications/initialized")
    # 2) discover the tools
    tools = c.request("tools/list")["result"]["tools"]
    print(">> tools/list:", [t["name"] for t in tools])
    print("   get_order schema:", json.dumps(tools[0]["inputSchema"]["properties"]))
    call = lambda name, **args: c.request("tools/call", {"name": name, "arguments": args})
    # 3) call them, like an AI would for "Where is my order PT-1002?"
    order = call("get_order", order_id="PT-1002")
    show("tools/call get_order PT-1002", order)
    trk = order["result"]["structuredContent"]["tracking_id"]
    show(f"tools/call track_parcel {trk}", call("track_parcel", tracking_id=trk))
    # 4) mistakes: bad arguments, a missing order, an unknown tool, a slow API
    show("bad arguments", call("get_order", order_id="1002"))
    show("missing order", call("get_order", order_id="PT-9999"))
    show("unknown tool", call("delete_order", order_id="PT-1002"))
    show("slow courier API", call("track_parcel", tracking_id="TRK-9000"))
    # 5) a resource: plain data the app can read
    res = c.request("resources/read", {"uri": "policy://returns"})["result"]["contents"][0]
    print(f"\n>> resources/read {res['uri']}:", res["text"][:60] + "...")
    c.close()
    print("\nall good: server closed cleanly")

if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print("CLIENT FAILED:", e)
        sys.exit(1)
