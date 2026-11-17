# Episode 24 code: Production AI Systems (AI Engineer Roadmap)

A small AI gateway in FastAPI that sits between your app and the model. It shows the production basics
in about 100 lines: **authentication, rate limiting, caching, cost control, retries with backoff,
fallback to a cheaper model, background jobs, and a health endpoint for alerts**.

| File | What it is |
|---|---|
| `gateway.py` | The FastAPI app (`/ask`, `/jobs`, `/jobs/{id}`, `/health`) |
| `fake_llm.py` | **Demo stand-in model**: fixed answers, made-up prices, fails on purpose to test retries. Not a real LLM. |
| `try_gateway.py` | Sends real HTTP requests to the app in-process and prints what happened |

## Run it (CPU only, no API key)
```
pip install -r requirements.txt
python try_gateway.py           # the demo shown in the video
uvicorn gateway:app --reload    # or run it as a real server on http://127.0.0.1:8000/docs
```
Demo keys: `demo-key-asha`, `demo-key-ravi` (send as the `X-API-Key` header).

## Going to real production
- Swap `fake_llm.call` for your provider's SDK call (OpenAI, Anthropic, Gemini...). Keep the retry + fallback around it.
- The dicts (`buckets`, `spent`, `cache`, `jobs`) live in one process. With many servers, move them to **Redis** (or a database), so every server sees the same limits, budget and cache.
- `BackgroundTasks` runs after the response in the same process. For real work use a **queue + workers** (Celery, RQ, Arq, Cloud Tasks, SQS...).
- Store hashed keys (as here) or use your login system (OAuth / JWT). Never log raw keys or full prompts with personal data.
- Send `/health` numbers (errors, retries, fallbacks, cost) to your monitoring and alert on them.
