# Episode 23 code: AI Development Tools (AI Engineer Roadmap)

A tiny bill-splitter project to practise the workflow every AI coding tool uses
(Claude Code, Cursor, Windsurf, Codex, Gemini CLI, and app builders like Replit, Bolt, Lovable):
**rules file → clear prompt → plan → diff → tests → review**.

| File | What it is |
|---|---|
| `AGENTS.md` | Project rules most coding agents read first (commands, rules, "never edit tests") |
| `CLAUDE.md` | One line that points Claude Code to AGENTS.md |
| `prompt.txt` | A good task prompt: goal, context, constraints, done-when |
| `split.py` | The code (already fixed) |
| `test_split.py` | The tests. Before the fix, `test_shares_add_up_to_the_bill` failed (999.99 != 1000.0) |
| `fix.diff` | The change the AI coding agent proposed (work in whole paise, spread the extra paisa) |
| `risky.diff` | A careless "vibe-coded" change, made up for the demo (fake key, new library, deleted test) |
| `review_diff.py` | Hand-written safety check for any diff before you accept it |

## Run it
```
pip install pytest
python -m pytest -q                 # 4 passed
git apply -R fix.diff && python -m pytest -q   # (inside a git repo) see the original bug: 1 failed
python review_diff.py fix.diff      # verdict: OK to review by eye
python review_diff.py risky.diff    # verdict: BLOCK
```
The key in `risky.diff` is fake. Never put a real key in code.
`review_diff.py` is a small first filter, not a full security scan. Always read the diff yourself too.
