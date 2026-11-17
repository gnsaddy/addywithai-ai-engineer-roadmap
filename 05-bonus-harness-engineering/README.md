# Harness Engineering: mini harness (Python)
Code from the @addywithai video "Learn Harness Engineering" (AI Engineer Roadmap, bonus episode).

A tiny agent harness in about 50 lines: tools, permissions (allow / ask), a stop rule (MAX_STEPS), a log file, and the agent loop.
The "model" is a stand-in (`fake_model.py`) so it runs with **no API key and no installs**. Swap `fake_model` for a real LLM call later; the harness stays the same.

## Run (Python 3.9+)
```
python mini_harness.py           # asks before delete_file: type n (no) or y (yes)
python mini_harness.py --stuck   # a model that loops forever: the harness stops it at 5 steps
type harness_log.jsonl           # every step, one JSON line each (cat on Mac/Linux)
```

## Files
- `mini_harness.py`: tools, guardrails (ALLOW / ASK / MAX_STEPS), `run_tool()`, `log()`, `run_agent()` loop
- `fake_model.py`: `fake_model` (weather, then delete) and `stuck_model` (repeats one tool forever)

Tested 2026-10-30 with Python 3. Output of `echo n | python mini_harness.py`:
```
[step 1] get_weather {'city': 'Bengaluru'}
[step 2] delete_file {'path': 'notes.txt'}
  Allow delete_file({'path': 'notes.txt'})? [y/N] n
Answer: Bengaluru: 31°C, sunny. I did not delete notes.txt (the user said no).
```
