# AI Engineer Roadmap, Episode 16: AI Agent Frameworks (code)

One small agent, built in two frameworks. It is the same travel-expense agent as Episode 15 (two tools, one loop), so you can compare it with the from-scratch version. Python 3.10+.

| File | What it does |
|---|---|
| `tools.py` | The two tools as plain Python functions with type hints and docstrings: `search_policy()` and a safe `calculator()` (parses with `ast`, never `eval()`). |
| `settings.py` | Model settings (`BASE_URL`, `CHAT_MODEL`, `API_KEY`), the system rules and the two demo questions. `--demo` starts the stand-in server. |
| `agent_langgraph.py` | Version 1, LangGraph: a graph with a `model` node, a `tools` node, a conditional edge (tool call or end) and an edge back. The step limit is `recursion_limit`. |
| `agent_openai_sdk.py` | Version 2, OpenAI Agents SDK: an `Agent` with instructions, a model and tools; `Runner.run_sync()` runs the loop. The step limit is `max_turns`. |
| `stand_in_server.py` | DEMO ONLY: a tiny local server that looks like an OpenAI-compatible chat API and answers with fixed rules for the two demo questions. It does not think. Both frameworks talk to it over HTTP, so the framework code runs for real. |

## Demo (no model needed)
```
pip install -r requirements.txt
python agent_langgraph.py --demo
python agent_openai_sdk.py --demo
```
Both print the same steps and the same answers (930 US dollars; 30 days).

## Real run with a free local model
1. Install [Ollama](https://ollama.com) and pull a model that supports tool calling, e.g. `ollama pull llama3.2` (or `qwen2.5`).
2. Set `BASE_URL=http://localhost:11434/v1` and `CHAT_MODEL` (see `.env.example`).
3. `python agent_langgraph.py` and `python agent_openai_sdk.py`

A real model words things its own way and may take a different number of steps. Check that every number in the answer came from a tool result.

## Notes
- The OpenAI Agents SDK works with other providers through any OpenAI-compatible Chat Completions endpoint, as shown here. Its built-in tracing uploads to OpenAI, so this demo switches it off.
- Framework APIs change fast. These files were tested with the versions in `requirements.txt` on 2026-11-10. If something breaks, check the current docs for your installed version.
- Keep the step limit, treat tool results as data (not instructions), and put risky actions behind a human approval step.
