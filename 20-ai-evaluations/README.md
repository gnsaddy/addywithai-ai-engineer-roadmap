# AI Engineer Roadmap, Episode 20: AI Evaluations (code)

A small eval suite: deterministic checks plus an LLM-as-judge, run on two prompt versions, with a regression gate. Python 3.9+, standard library only.

| File | What it does |
|---|---|
| `dataset.py` | The test set: 8 cases. Each has an input (`ask`), a check type (`exact`, `contains`, `json` or `judge`) and what we want. |
| `checks.py` | Deterministic evals in plain code: exact match, contains, valid JSON with the right keys. |
| `judge.py` | Model-based eval: a rubric prompt asks a model to score the answer 1 to 5 against a reference and reply as JSON. Pass = 4 or more. |
| `app.py` | The app under test: a policy helper with two prompt versions, `v1` and `v2`. |
| `run_evals.py` | Runs every case on both versions, prints pass/fail side by side, the scores, the regressions (passed before, fails now) and a ship / do-not-ship gate. |
| `models.py` | `chat(system, user)` through any OpenAI-compatible API, for real runs. |
| `stand_in.py` | DEMO ONLY: fixed answers for the two prompt versions, and a fake judge that scores by counting shared key words. Nothing in it thinks. A real judge reads the meaning. |

## Demo (no model needed)
```
python run_evals.py --demo
```
Expected output:
```
case  check        v1     v2
   1  exact        FAIL   pass
   2  exact        pass   pass
   3  exact        pass   pass
   4  contains     FAIL   pass
   5  json         FAIL   pass
   6  judge 5/5    pass   pass
   7  judge 1/5    pass   FAIL   <- REGRESSION
   8  judge 5/5    pass   pass

score: v1 5/8   v2 7/8
regressions: [7]
GATE: FAIL, do not ship v2 yet
```
The lesson: v2 has the higher score, but it broke a case that used to pass. The total score alone would have hidden that.

## Real run
1. Install [Ollama](https://ollama.com), then `ollama pull llama3.2` (or point `BASE_URL` at any OpenAI-compatible API; see `.env.example`).
2. Give the app the policy text in its prompt (or plug in your RAG app from Episode 13) so it can answer.
3. `python run_evals.py`

## Notes
- Use a stronger model for the judge than for the app when you can, keep its temperature at 0, and check the judge against human grades on a sample before you trust it.
- Model answers change from run to run. Run important evals more than once.
- For bigger projects, look at tools like DeepEval and RAGAS (ready-made metrics) and run the suite in CI on every prompt or model change.
