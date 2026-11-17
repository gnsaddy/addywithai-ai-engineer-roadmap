# AI Engineer Roadmap, Episode 19: AI Observability (code)

Log every LLM call with tokens, cost and latency, then turn the log into a small report. Python 3.9+, standard library only.

| File | What it does |
|---|---|
| `llm_log.py` | `logged_chat(model, messages, feature, trace_id)`: wraps the model call, times it, reads the token counts from `usage`, works out the cost from a price table, and appends one JSON line per call to `llm_calls.jsonl`. Errors are logged too (`finally`). |
| `app.py` | A pretend app with three features (chat, summary, report). One `trace_id` per user request; the report feature makes two model calls that share it. |
| `report.py` | Reads the log: calls, error rate, p50 and p95 latency, tokens and cost per feature, the slowest call with its trace id, and a simple alert rule. |
| `stand_in.py` | DEMO ONLY: a fake model with made-up token counts and speed (scaled down so the demo is quick), a few timeouts and a few slow calls. It does not think. |

## Run it
```
python app.py
python report.py
```
Example output from our run (latency changes a little on every run):
```
feature   calls errors    p50    p95   tokens    cost$
chat         60    8.3%     96    138    47144   0.0123
summary      25    0.0%    102    138    21489   0.0058
report       29   17.2%    185    708    20956   0.0390
ALL         114    8.8%    103    399    89589   0.0572

slowest call: 2078 ms  feature=report  trace_id=0dda285c
ALERT: error rate 9% is above 5%
```

## Use it with a real model
In `llm_log.py`, replace `fake_chat(model, messages)` with your real client call. Any OpenAI-compatible API returns `usage.prompt_tokens` and `usage.completion_tokens`. Put your provider's real prices in `PRICES` (the numbers in the file are examples only), and add cached-token prices if you use prompt caching.

## Notes
- Prompts and answers can hold private data. This demo does not log them. If you do, mask personal data and limit who can read the logs.
- For real apps, tools like Langfuse, LangSmith, Helicone and Arize Phoenix give you tracing, dashboards and alerts, and many build on OpenTelemetry. The idea is the same as this file.
