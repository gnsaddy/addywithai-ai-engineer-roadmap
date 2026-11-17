# client.py: a tiny MCP client. It starts server.py, asks what it offers,
# and calls both tools. This is what an MCP host does for the model.
import asyncio, sys
from mcp import Client, StdioServerParameters

# local server: start it as a child process and talk over stdin and stdout
SERVER = StdioServerParameters(command=sys.executable, args=["server.py"])
if len(sys.argv) > 1:                # remote server: pass its URL instead
    SERVER = sys.argv[1]             # e.g. http://127.0.0.1:8000/mcp

def text(result):
    return result.content[0].text

async def main():
    async with Client(SERVER) as client:          # connect + handshake
        print("server:", client.server_info.name)

        tools = await client.list_tools()         # 1 discover
        for t in tools.tools:
            print(f"tool:   {t.name}({', '.join(t.input_schema['properties'])})")
            print(f"        {t.description}")

        hit = await client.call_tool(             # 2 call a tool
            "search_policy", {"query": "hotel limit Tokyo"})
        print("search:", text(hit)[:66])
        total = await client.call_tool(
            "calculator", {"expression": "3 * 250 + 3 * 60"})
        print("calc:  ", text(total))

        bad = await client.call_tool(             # 3 a bad input
            "calculator", {"expression": "__import__('os')"})
        print("bad:   ", "error" if bad.is_error else "ok", "|", text(bad))

        res = await client.read_resource("policy://travel")   # 4 a resource
        print("policy:", len(res.contents[0].text.splitlines()), "lines")

asyncio.run(main())
