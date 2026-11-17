# AI Engineer Roadmap, Episode 7: Model Selection (code)

Two small Python files, standard library only. Python 3.9+.

## 1. time_and_price.py: the same prompt on several models, timed and priced
Demo (no setup, stand-in models from `stand_in.py`, example prices):
```
python time_and_price.py --demo
```
Real run against any OpenAI-compatible API:
1. Put your provider's real model names and prices (US$ per 1M input / output tokens, from its pricing page) in `MODELS`.
2. Set `BASE_URL` (the provider's OpenAI-compatible base URL, e.g. `http://localhost:11434/v1` for Ollama) and `API_KEY` in your environment (see `.env.example`).
3. `python time_and_price.py`

The token counts come from the API's `usage` field. The month column = 10,000 calls a day for 30 days.

## 2. pick_model.py: drop models that miss a must, then score the trade-offs
```
python pick_model.py
```
`CANDIDATES` holds example data. Replace it with your own numbers: quality = % correct on your own eval set, seconds and cost from time_and_price.py, context size and tool support from the provider docs. Change `MUSTS` and the weights in `APPS` to match your app.

Never paste API keys into the code.
