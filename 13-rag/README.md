# AI Engineer Roadmap, Episode 13: RAG (code)

RAG from scratch: chat with your PDF. Python 3.9+, `pypdf` for reading the PDF, everything else is the standard library.

| File | What it does |
|---|---|
| `travel-policy.pdf` | A 2-page sample company policy (made up for the demo). Use your own PDF too. |
| `ingest.py` | `load_pdf()` reads text per page with pypdf; `chunk_pages()` packs whole sentences into chunks of up to 200 characters that remember their page. |
| `models.py` | `embed()` and `chat()` through any OpenAI-compatible API (e.g. Ollama). With `--demo` they use `stand_in.py`. |
| `rag.py` | 1 ingest, 2 retrieve (top 3 by cosine), 3 augment (numbered sources + "answer only from the sources, else say I don't know"), 4 generate. |
| `stand_in.py` | DEMO ONLY: a toy 6-idea embedder and a fake "LLM" that quotes the best-matching source sentence or says "I don't know". It does not think. A real LLM writes its own answer. |

## Demo (no model needed)
```
pip install pypdf
python rag.py travel-policy.pdf --demo
```

## Real run with free local models
1. Install [Ollama](https://ollama.com), then `ollama pull nomic-embed-text` and `ollama pull llama3.2`
2. Set `BASE_URL=http://localhost:11434/v1` (see `.env.example`).
3. `python rag.py travel-policy.pdf` (or your own PDF)

A real model will word the answers its own way. Check that it cites the right source and says "I don't know" for the wifi question.
