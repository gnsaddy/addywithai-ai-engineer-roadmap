# Build an MCP Server from Scratch (AI Engineer Roadmap, Bonus B5)

An MCP server written by hand in Python: **no MCP SDK**, just JSON-RPC 2.0 over stdio.
Runs offline on CPU. No API keys.

Running example: **PageTurn Books**, a made-up online bookshop. The server gives an AI two read-only tools:

| Tool | What it does | Backed by |
|---|---|---|
| `get_order` | Look up one order: status, total, items, tracking ID | SQLite (`shop.db`, opened read-only) |
| `track_parcel` | Where is the parcel now, and the ETA | `courier_api.py`, a stand-in for an internal HTTP API |

Plus one resource, `policy://returns` (the return policy as text).

## Files
| File | What it is |
|---|---|
| `server.py` | The MCP server: stdio loop, `initialize`, `tools/list`, `tools/call`, `resources/list`, `resources/read`, JSON-RPC errors |
| `tools.py` | The two tools, with Pydantic models that give each tool its JSON Schema and validate arguments |
| `courier_api.py` | Stand-in internal API with fake data (and one parcel that times out) |
| `make_db.py` | Creates `shop.db` with 3 made-up orders |
| `client.py` | A tiny scripted MCP client that starts the server and runs the whole demo |
| `check_readonly.py` | Shows that the tools' database connection cannot write |
| `check_with_sdk.py` | Optional: connects the official MCP Python SDK client to our server |
| `mcp_config.json` | Example config to add the server to an MCP client app |

## Run it
```bash
pip install -r requirements.txt
python make_db.py
python client.py          # the full demo
python client.py --bad    # the classic bug: a print() to stdout breaks the protocol
python check_readonly.py
```
Optional check with a real MCP client library:
```bash
pip install mcp
python check_with_sdk.py
```
To use it from an MCP client app (for example a desktop AI app or a code editor), add the block in `mcp_config.json`
to the app's MCP settings and change the path to where `server.py` lives.

## Rules this server follows
* **stdout is the wire.** Only JSON-RPC messages go to stdout, one per line. Logs go to stderr.
* **Notifications get no reply** (messages without an `id`).
* **Bad arguments are tool errors** (`isError: true`) so the model can fix them. Unknown tools and methods are JSON-RPC errors.
* **Read-only by default:** SQLite opened with `mode=ro` + `PRAGMA query_only`, only the columns the AI needs (no phone numbers).
* **Small, specific tools** with clear descriptions, no "run any SQL" god-tool, results capped at 2,000 characters.

Protocol: the `initialize` handshake (versions 2024-11-05 to 2025-11-25). Newer clients first try `server/discover`
(protocol 2026-07-28); this server answers "method not found" and the client falls back to `initialize`.
