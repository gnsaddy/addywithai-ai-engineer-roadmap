# report.py: read the log, and answer the four big questions.
# How many calls? How many failed? How slow? How much money?
import json
from collections import defaultdict

rows = [json.loads(line) for line in open("llm_calls.jsonl")]

def pct(values, p):                        # p50 = middle, p95 = slow tail
    values = sorted(values)
    return values[min(len(values) - 1, int(len(values) * p / 100))]

def line(name, group):
    ok = [r for r in group if r["status"] == "ok"]
    lat = [r["latency_ms"] for r in group]
    cost = sum(r["cost_usd"] for r in ok)
    errors = 100 * (len(group) - len(ok)) / len(group)
    print(f"{name:9}{len(group):6}{errors:7.1f}%{pct(lat, 50):7}{pct(lat, 95):7}"
          f"{sum(r['tokens_in'] + r['tokens_out'] for r in ok):9}{cost:9.4f}")

print("feature   calls errors    p50    p95   tokens    cost$")
by_feature = defaultdict(list)
for r in rows:
    by_feature[r["feature"]].append(r)
for name, group in by_feature.items():
    line(name, group)
line("ALL", rows)

slow = max(rows, key=lambda r: r["latency_ms"])
print(f"\nslowest call: {slow['latency_ms']} ms  feature={slow['feature']}"
      f"  trace_id={slow['trace_id']}")

error_rate = sum(r["status"] == "error" for r in rows) / len(rows)
if error_rate > 0.05:                      # a simple alert rule
    print(f"ALERT: error rate {error_rate:.0%} is above 5%")
