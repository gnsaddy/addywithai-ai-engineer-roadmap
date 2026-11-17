# AI Engineer Roadmap, Episode 11: Embedding Models (code)

Python 3.9+, standard library only. Compare two embedding models on the SAME search task.

| File | What it does |
|---|---|
| `testset.py` | 8 help-desk notes + 6 test questions, each with the note that should come back. |
| `models.py` | `api_model(name)` = any OpenAI-compatible `/embeddings` API. Plus two TOY models for the demo: `toy_word_match` (64 hash buckets, words only) and `toy_meaning` (a tiny hand-made word-to-idea table). Real models learn hundreds to thousands of dimensions from data. |
| `compare_models.py` | Embeds the notes once, ranks them for every question, prints the rank of the right note per model, then recall@1, recall@3 and MRR. |

## Demo (no setup)
```
python compare_models.py --demo
```

## Real run with two free local models
1. Install [Ollama](https://ollama.com), then `ollama pull nomic-embed-text` and `ollama pull all-minilm`
2. Set `BASE_URL=http://localhost:11434/v1` (see `.env.example`; hosted APIs also need `API_KEY`).
3. `python compare_models.py nomic-embed-text all-minilm`

Use 20-50 real questions from your own users for a fair test. Some models want a prefix or a task type for queries (BGE, E5, nomic, Gemini, Cohere): check the model card.
