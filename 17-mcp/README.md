# AI Engineer Roadmap, Episode 17: MCP, the Model Context Protocol (code)

A small MCP server in Python with two tools and one resource, plus a tiny client that plays the role of an MCP host. No model and no API key needed. Python 3.10+.

| File | What it does |
|---|---|
| `server.py` | The MCP server `travel-policy`: tools `search_policy(query)` and `calculator(expression)` (safe maths with `ast`, never `eval()`), and the read-only resource `policy://travel`. Runs over stdio by default, or over Streamable HTTP with `--http`. |
| `client.py` | A tiny MCP client: connects, lists the tools (name, inputs, description), calls both, sends one bad input to show a tool error, and reads the resource. |

## Run it
```
pip install -r requirements.txt
python client.py
```
`client.py` starts `server.py` for you as a child process and talks to it over stdin and stdout (the stdio transport).

Expected output:
```
server: travel-policy
tool:   search_policy(query)
        Search the company travel policy. Example query: hotel limit Tokyo
tool:   calculator(expression)
        Do maths with + - * / on numbers. Example: 3 * 250 + 3 * 60
search: In London, New York and Tokyo the hotel limit is 250 US dollars pe
calc:   930
bad:    error | Error executing tool calculator: only numbers and + - * /
policy: 4 lines
```
(The server also writes one log line about the failed call to stderr. That is normal.)

## Remote style (Streamable HTTP)
```
python server.py --http                      # terminal 1
python client.py http://127.0.0.1:8000/mcp   # terminal 2
```
Same tools, same answers. Only the transport changed. A real remote server also needs HTTPS and authorization (OAuth).

## Use it from a real host
Add the server to your MCP host's config (Claude Desktop, VS Code, Cursor and others have an MCP servers setting). The usual shape is:
```json
{ "mcpServers": { "travel-policy": { "command": "python", "args": ["C:/path/to/server.py"] } } }
```
Check your host's docs for the exact file and format.

## Notes
- This code uses version 2 of the official `mcp` Python SDK (`MCPServer`, `Client`). On version 1 the server class is `FastMCP` (`from mcp.server.fastmcp import FastMCP`) and the client uses `ClientSession` with `stdio_client`. The ideas are the same.
- In a stdio server, never `print()` to stdout: stdout carries the protocol messages. Log to stderr.
- Security: validate every tool input, give each server the least access it needs, only install servers you trust, and keep risky tools behind a human approval step.
