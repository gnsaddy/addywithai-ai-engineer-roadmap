# AI Engineer Roadmap, Episode 6: AI Models (code)

Two small Python files, standard library only. Python 3.9+.

## 1. quantize_demo.py: why quantization makes models smaller
```
python quantize_demo.py
```
Prints the memory needed just for the weights of a 1B, 8B and 70B model at 16, 8 and 4 bits, then quantizes 10,000 random "weights" to 8-bit and 4-bit, and shows the average error (plus 4-bit with one scale per group of 64 weights, like real 4-bit methods).

## 2. compare_models.py: same questions, two models, one score card
Demo (no setup, two stand-in models from `stand_in.py`):
```
python compare_models.py --demo
```
The demo numbers come from canned answers and a fixed delay. They only show how the score card works.

Real run (a local open model + a hosted model, both through an OpenAI-compatible API):
1. Install Ollama (https://ollama.com), then `ollama pull llama3.2:3b` (Ollama serves an OpenAI-compatible API at `http://localhost:11434/v1`). Use another model with `LOCAL_MODEL=<name>`.
2. Set the hosted model in environment variables (see `.env.example`): `HOSTED_BASE_URL` (the provider's OpenAI-compatible base URL), `HOSTED_MODEL`, `HOSTED_API_KEY`, and `HOSTED_PRICE_PER_M` (US$ per 1M tokens, from the provider's pricing page).
3. `python compare_models.py`

Never paste API keys into the code. The cost column is an estimate (about 4 characters per token).
