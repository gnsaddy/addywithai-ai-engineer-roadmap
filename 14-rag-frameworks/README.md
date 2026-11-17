# AI Engineer Roadmap, Episode 14: RAG Frameworks (code)

One RAG app, built three times: plain Python, LangChain and LlamaIndex. Same PDF, same questions, same `embed()` and `chat()` (from Episode 13). Python 3.9+.

| File | What it does |
|---|---|
| `travel-policy.pdf` | The 2-page sample policy from Episode 13 (made up for the demo). |
| `ingest.py`, `models.py` | From Episode 13: PDF loading + page-aware chunks, and `embed()` / `chat()` through any OpenAI-compatible API (e.g. Ollama). `--demo` switches to `stand_in.py`. |
| `questions.py` | The three questions and the shared system rules ("answer only from the sources, cite them, else say I don't know"). |
| `rag_plain.py` | Version 1, plain Python: ingest, top 3 by cosine, numbered sources, chat. 25 lines. |
| `rag_langchain.py` | Version 2, LangChain: our models plugged in as `Embeddings` and a `RunnableLambda`, `RecursiveCharacterTextSplitter`, `InMemoryVectorStore` retriever (k=3), an LCEL chain joined with pipes. |
| `rag_llamaindex.py` | Version 3, LlamaIndex: our models as `BaseEmbedding` and `CustomLLM`, `Settings`, `SentenceSplitter`, `VectorStoreIndex`, a query engine with top 3. |
| `compare_all.py` | Runs all three versions and prints their answers side by side. |
| `stand_in.py` | DEMO ONLY: a toy embedder and a fake "LLM" that quotes the best-matching source sentence (with its citation) or says "I don't know". It does not think. |

## Demo (no model needed)
```
pip install -r requirements.txt
python compare_all.py --demo
```
Each version also runs on its own: `python rag_langchain.py --demo`.

The three builds give the same answers. The citation numbers can differ, because each framework chunks the PDF its own way.

## Real run with free local models
1. Install [Ollama](https://ollama.com), then `ollama pull nomic-embed-text` and `ollama pull llama3.2`
2. Set `BASE_URL=http://localhost:11434/v1` (see `.env.example`).
3. `python compare_all.py`

Framework APIs change fast. These files were tested with the versions in `requirements.txt` on 2026-11-07; if something breaks, check the current docs for your installed version.
