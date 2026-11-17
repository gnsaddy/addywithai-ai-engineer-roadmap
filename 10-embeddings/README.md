# AI Engineer Roadmap, Episode 10: Embeddings (code)

Python 3.9+, standard library only.

| File | What it does |
|---|---|
| `embed.py` | `embed(texts)` turns text into vectors through any OpenAI-compatible `/embeddings` API (for example Ollama with `nomic-embed-text`), plus `cosine(a, b)`. |
| `toy_embedder.py` | Demo only: a TOY embedder with 4 hand-made meaning dimensions (food, sport, tech, money), so you can check every number. Real models learn hundreds to thousands of dimensions. |
| `search.py` | Semantic search: embed 6 notes once, embed the question, print the top 3 by cosine similarity. |
| `uses.py` | The same vectors for classification (nearest label), recommendation (nearest item) and anomaly detection (far from every normal ticket). |

## Demo (no setup)
```
python search.py --demo
python uses.py --demo
```

## Real run with a free local model
1. Install [Ollama](https://ollama.com), then `ollama pull nomic-embed-text`
2. Set `BASE_URL=http://localhost:11434/v1` (any OpenAI-compatible embeddings API works; set `API_KEY` and `EMBED_MODEL` for hosted ones, see `.env.example`).
3. `python search.py` and `python uses.py`

With a real model the scores are different from the toy (unrelated texts often score above 0), so tune thresholds like the anomaly `0.5` on your own data.
