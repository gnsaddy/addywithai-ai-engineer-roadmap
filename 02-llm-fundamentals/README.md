# LLM Fundamentals: count tokens and see the context window (AI Engineer Roadmap, Episode 2)

Two small Python files that show tokens and the context window with real Gemini API calls.

## Setup (Windows, macOS or Linux)
1. Install Python 3.10 or newer.
2. Make a folder, put these files in it, then open a terminal there:
   ```
   python -m venv .venv
   .venv\Scripts\activate        # Windows  (macOS/Linux: source .venv/bin/activate)
   pip install -r requirements.txt
   ```
3. Get a free API key at Google AI Studio (aistudio.google.com, "Get API key").
4. Copy `.env.example` to `.env` and paste your key. Never share or upload `.env`.

## Run
```
python count_tokens.py     # context window size + token counts + "will it fit?" check
python token_usage.py      # one real request + the tokens it used
```

## What you will see
- `count_tokens.py`: the model's input and output limits, how many tokens a few short texts use, and a very long text that is too big for the window.
- `token_usage.py`: a one-line answer, then the input, output and total tokens of that request, and how much of the context window the prompt used.

Notes
- `count_tokens` only counts. It does not make an answer.
- The total can be a little more than input + output, because "thinking" models also count hidden thinking tokens.
- Exact numbers change between models and versions. The model alias `gemini-flash-latest` always points to the current Flash model.
- The numbers in the video are sample output.
