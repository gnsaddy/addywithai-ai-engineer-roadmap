# AI Engineer Roadmap, Episode 8: AI Platforms & Ecosystem (code)

Python 3.9+, standard library only. No SDK to install.

| File | What it does |
|---|---|
| `platforms.py` | A table of 6 platforms (Ollama, LM Studio, OpenRouter, Together AI, Groq, Fireworks AI) and one `chat()` function. They all speak the OpenAI-compatible chat API, so only the base URL, key and model name change. |
| `switch_platform.py` | The same prompt on three platforms in one loop. |
| `fallback.py` | Tries the free local model first, then hosted backups. Skips a platform that is offline or rate limited (HTTP 429). |
| `stand_in_server.py` | Demo only: fake OpenAI-compatible platforms on localhost (canned answers, example delays). |

## Demo (no keys, no internet)
```
python switch_platform.py --demo
python fallback.py --demo
```
The demo sends real HTTP requests through `chat()` to the stand-in server. Delays and answers are demo values.

## Real run
1. Local: install [Ollama](https://ollama.com), then `ollama pull llama3.2` (server on `http://localhost:11434/v1`). Or LM Studio: download a model and start its local server (`http://localhost:1234/v1`).
2. Hosted: create a key on the platforms you want and set it as an environment variable (see `.env.example`).
3. Model names differ per platform. Copy the exact name from each platform's model list and edit `RUNS` / `CHAIN`.
4. `python switch_platform.py` and `python fallback.py`

Never paste API keys into the code.
