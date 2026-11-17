# Context Engineering: context builder (AI Engineer Roadmap)
A tiny Python demo from the video. It builds the context for one support question the "engineered" way
(instructions, the 2 best documents, a short summary of old chat, the last 2 messages, the question last)
and compares its size with the "naive" way (send everything).

## Run
```
python context_builder.py
```
No packages and no API key needed (Python 3.9+, standard library only).

## Files
- `data.py`: sample instructions, 6 help-centre documents, an 8-message chat and the question.
- `context_builder.py`: `count_tokens()` (rule of thumb: 1 token ~ 4 characters), `retrieve()` (keyword overlap,
  a stand-in for embeddings + a vector database), `build_context()` and the naive vs engineered comparison.

## Notes
- Token counts are estimates. Use your model's real token counter (for example `count_tokens` in the Gemini API) in a real app.
- The summary line is written by hand here. In a real app an LLM writes it (compaction).
- Next step: send `build_context(...)` to any chat model as the messages of one request.
