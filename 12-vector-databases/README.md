# AI Engineer Roadmap, Episode 12: Vector Databases (code)

Python 3.9+. Chunk two small documents, store them in a vector database, and search with a metadata filter.

| File | What it does |
|---|---|
| `docs/` | Two tiny company documents: `leave-policy.txt`, `it-help.txt`. |
| `chunker.py` | `chunk(text)`: packs whole sentences into chunks of up to 120 characters, with a 1-sentence overlap. Run it alone to see the chunks. |
| `embedder.py` | `embed(texts)`: any OpenAI-compatible `/embeddings` API (e.g. Ollama `nomic-embed-text`). With `--demo`, a TOY embedder with 6 hand-made ideas. |
| `mini_vector_db.py` | What a vector database does, in a few lines: a FLAT index (compare with every vector) + metadata filters. Standard library only. |
| `store_and_query.py` | The real thing with [Chroma](https://www.trychroma.com/): a persistent collection (cosine), upsert chunks + vectors + metadata, query top-k, query with a `where` filter. |

## Demo (no model needed)
```
pip install chromadb
python chunker.py
python mini_vector_db.py --demo
python store_and_query.py --demo
```

## Real run with a free local embedding model
1. Install [Ollama](https://ollama.com), then `ollama pull nomic-embed-text`
2. Set `BASE_URL=http://localhost:11434/v1` (see `.env.example`).
3. Delete the `vector_db` folder (vectors from different models must never mix), then `python store_and_query.py`

Tested with chromadb 1.5. We pass our own vectors (`embeddings=`, `query_embeddings=`), so Chroma never downloads its default model.
