# check_with_sdk.py: optional check.
# Connect the OFFICIAL MCP Python SDK client to our hand-written server.
# If a real client can list and call our tools, our server speaks proper MCP.
# Needs: pip install mcp   (only for this check; server.py itself uses no SDK)
import asyncio, os, sys
from mcp import Client
from mcp.client.stdio import StdioServerParameters

HERE = os.path.dirname(os.path.abspath(__file__))
SERVER = StdioServerParameters(command=sys.executable, args=[os.path.join(HERE, "server.py")])

async def main():
    async with Client(SERVER) as client:   # tries the newest handshake first, then initialize
        print("connected to", client.server_info.name, "| protocol", client.protocol_version)
        tools = await client.list_tools()
        print("tools:", [t.name for t in tools.tools])
        r = await client.call_tool("get_order", {"order_id": "PT-1001"})
        print("get_order PT-1001 ->", r.content[0].text[:80], "| isError", r.is_error)
        r = await client.call_tool("get_order", {"order_id": "abc"})
        print("get_order abc     ->", r.content[0].text[:80], "| isError", r.is_error)

asyncio.run(main())
