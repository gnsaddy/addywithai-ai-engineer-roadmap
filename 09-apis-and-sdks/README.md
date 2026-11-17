# AI Engineer Roadmap, Episode 9: APIs & SDKs (code)

Python 3.9+.

```
pip install -r requirements.txt
```

| File | What it does |
|---|---|
| `three_sdks.py` | The same system prompt + question through three official SDKs: OpenAI (Responses API), Anthropic Claude (Messages API) and Google Gemini (Google Gen AI SDK). Each returns text, input tokens, output tokens. |
| `gateway.py` | A tiny AI gateway: one `ask()` for every provider, with retries, fallback to the next provider, and a cost + token log. SDK retries are switched off (`max_retries=0`) so the gateway decides. |
| `stand_in_server.py` | Demo only: fake OpenAI, Claude and Gemini APIs on localhost. The real SDKs send real requests to it; only the answers are canned. |

## Demo (no keys, no internet)
```
python three_sdks.py --demo
python gateway.py --demo
```
In the gateway demo, Claude returns HTTP 503 twice and OpenAI once, so you see a fallback and a retry.

## Real run
1. Set the keys and model names (see `.env.example`). Copy current model names from each provider's docs; they change often.
2. `python three_sdks.py` then `python gateway.py`
3. Prices in `gateway.py` are example prices. Copy real ones from each pricing page.

Tested with openai 3.46, anthropic 2.6 and google-genai 3.0 (2026-11-07). Never paste API keys into the code.
