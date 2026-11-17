# AI Engineer Roadmap, Episode 15: AI Agents (code)

An AI agent from scratch: two tools and one ReAct loop (reason, act, observe). Python 3.9+, standard library only, no framework.

| File | What it does |
|---|---|
| `tools.py` | The two tools: `search_policy()` (finds the policy sentences that share the most words with a query) and `calculator()` (safe maths: it parses the expression with `ast` and allows only numbers and + - * /, never `eval()`). |
| `schemas.py` | How the tools are described to the model: name, description and a JSON schema for the input (OpenAI tool format). |
| `models.py` | `chat(messages, tools)` through any OpenAI-compatible API with tool calling (e.g. Ollama). With `--demo` it uses `stand_in.py`. |
| `agent.py` | The ReAct loop: call the model with the tools, run every tool call it makes, send the results back as `tool` messages, repeat until it answers. Tool errors go back to the model as text, and `max_steps` always stops the loop. |
| `stand_in.py` | DEMO ONLY: a scripted fake model with fixed rules for the two demo questions, so the loop runs offline. It does not think. A real model makes these choices itself. |

## Demo (no model needed)
```
python agent.py --demo
```

## Real run with a free local model
1. Install [Ollama](https://ollama.com) and pull a model that supports tool calling, e.g. `ollama pull llama3.2` (or `qwen2.5`).
2. Set `BASE_URL=http://localhost:11434/v1` and `CHAT_MODEL` (see `.env.example`).
3. `python agent.py`

A real model words its thoughts its own way and may take a different number of steps. Check that every number in the answer came from a tool result.

## Safety notes
- Keep the step limit. Add a cost or time budget for real agents.
- Tool results are data, not instructions: a web page or file can hide text like "ignore your rules".
- Put risky actions (payments, emails, deletes) behind a human approval step.
