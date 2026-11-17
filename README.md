# AI Engineer Roadmap: code for every episode

Python code for the **AI Engineer Roadmap** series by **@addywithai**. Each folder matches one episode and has its own `README.md`, `requirements.txt` and, where an API key is needed, a `.env.example`.

## How to run any episode

```bash
cd 13-rag
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # only if the folder has one, then paste your own key
```

Then follow the run steps in that folder's `README.md`. Many episodes include a local "stand-in" so the demo works without a paid key.

Never commit your `.env` file. It is already listed in `.gitignore`.

## Episodes

| # | Episode | Code |
|---|---|---|
| 1 | Introduction to AI Engineering | Concept episode, no code |
| 2 | LLM Fundamentals | [02-llm-fundamentals](02-llm-fundamentals) |
| 3 | How LLMs Work | [03-how-llms-work](03-how-llms-work) |
| 4 | Prompt Engineering | [04-prompt-engineering](04-prompt-engineering) |
| 5 | Context Engineering | [05-context-engineering](05-context-engineering) |
| Bonus | Harness Engineering | [05-bonus-harness-engineering](05-bonus-harness-engineering) |
| 6 | AI Models | [06-ai-models](06-ai-models) |
| 7 | Model Selection | [07-model-selection](07-model-selection) |
| 8 | AI Platforms & Ecosystem | [08-ai-platforms-ecosystem](08-ai-platforms-ecosystem) |
| 9 | APIs & SDKs | [09-apis-and-sdks](09-apis-and-sdks) |
| 10 | Embeddings | [10-embeddings](10-embeddings) |
| 11 | Embedding Models | [11-embedding-models](11-embedding-models) |
| 12 | Vector Databases | [12-vector-databases](12-vector-databases) |
| 13 | RAG (Retrieval-Augmented Generation) | [13-rag](13-rag) |
| 14 | RAG Frameworks | [14-rag-frameworks](14-rag-frameworks) |
| 15 | AI Agents | [15-ai-agents](15-ai-agents) |
| 16 | AI Agent Frameworks | [16-ai-agent-frameworks](16-ai-agent-frameworks) |
| 17 | MCP (Model Context Protocol) | [17-mcp](17-mcp) |
| 18 | AI Safety & Security | [18-ai-safety-security](18-ai-safety-security) |
| 19 | AI Observability | [19-ai-observability](19-ai-observability) |
| 20 | AI Evaluations | [20-ai-evaluations](20-ai-evaluations) |
| 21 | Multimodal AI | [21-multimodal-ai](21-multimodal-ai) |
| 22 | Multimodal APIs | [22-multimodal-apis](22-multimodal-apis) |
| 23 | AI Development Tools | [23-ai-development-tools](23-ai-development-tools) |
| 24 | Production AI Systems | [24-production-ai-systems](24-production-ai-systems) |
| 25 | AI Career Growth | Career episode, no code |

Small sample inputs used by the demos (a made-up policy PDF, a receipt image, a short audio clip and a tiny test clip) are kept next to the code that reads them.

## Requirements

Python 3.10 or newer. Each episode lists its own packages in `requirements.txt`.
