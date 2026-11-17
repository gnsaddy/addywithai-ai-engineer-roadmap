# AI Engineer Roadmap, Episode 18: AI Safety & Security (code)

A prompt-injection demo on our own tiny app, then three layers of guardrails, then a small red-team test. Defensive only. Python 3.9+, standard library only.

**Test only apps you own, or have written permission to test.**

| File | What it does |
|---|---|
| `app.py` | A tiny support helper: it summarises a customer email. Its system prompt holds a made-up internal note (staff refund code `RF-7731`). `summarise()` has no guardrails. |
| `guardrails.py` | Three layers: `check_input()` (known attack phrases), `wrap()` (marks the email as data inside tags and escapes `<`), `check_output()` (blocks the secret's pattern, removes card-like numbers and email addresses, checks the reply is a short summary). `safe_summarise()` uses all three. |
| `demo.py` | Runs three emails (normal, attack, private data) without and with guardrails. |
| `red_team.py` | Adversarial testing: 8 attack emails against the guarded app. Prints which layer stopped each one. |
| `stand_in.py` | DEMO ONLY: a fake, gullible "model" that obeys the newest order it finds, even one hidden in the email. It does not think. Real models resist more, but not always, which is why the guardrails matter. |

## Demo (no model needed)
```
python demo.py --demo
python red_team.py --demo
```
In the demo run, the input check stops 4 of the 8 attacks. The other 4 are worded differently and get past it, and the output check stops them. That is the lesson: no single layer is enough.

## Real run with a free local model
1. Install [Ollama](https://ollama.com), then `ollama pull llama3.2`
2. Set `BASE_URL=http://localhost:11434/v1` (see `.env.example`).
3. `python demo.py` and `python red_team.py`

A real model behaves differently on each run, so run the red-team test many times and add new attacks as you find them.

## Honest limits
- Pattern checks are easy to get around with new wording, other languages or encodings. They reduce risk; they do not remove it.
- The strongest fix is design: do not put secrets in the prompt, give the model the least access it needs, and keep risky actions behind a human approval step.
- The card and email patterns are simple examples, not a full PII detector.
