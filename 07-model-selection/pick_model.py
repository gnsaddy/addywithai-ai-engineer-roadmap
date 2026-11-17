# pick_model.py: drop models that miss a must, then score the trade-offs.
# Example data: fill it in from YOUR eval set and your provider's pages.
CANDIDATES = [
    # name, quality %, seconds, $ per 1k calls, context (K tokens), tools?
    ("small", 71, 1.1, 0.30, 128, True),
    ("medium", 84, 2.4, 1.40, 200, True),
    ("large", 92, 6.5, 9.00, 1000, True),
    ("open-local", 76, 3.0, 0.00, 32, False),
]
MUSTS = {"min_context": 100, "tools": True}

def passes(m):
    name, quality, secs, cost, context, tools = m
    return context >= MUSTS["min_context"] and (tools or not MUSTS["tools"])

def rank(pool, weights):
    fastest = min(m[2] for m in pool)
    cheapest = min(m[3] for m in pool)
    rows = []
    for name, quality, secs, cost, *_ in pool:
        speed = fastest / secs            # 1.0 = the fastest one
        price = (cheapest + 0.01) / (cost + 0.01)  # 1.0 = the cheapest
        total = (weights["quality"] * quality / 100
                 + weights["speed"] * speed + weights["cost"] * price)
        rows.append((round(total, 2), name))
    return sorted(rows, reverse=True)

pool = [m for m in CANDIDATES if passes(m)]
print("Pass the musts:", ", ".join(m[0] for m in pool))
APPS = {  # how much each thing matters, per app (adds up to 1)
    "chat helper": {"quality": 0.6, "speed": 0.2, "cost": 0.2},
    "legal review": {"quality": 0.9, "speed": 0.05, "cost": 0.05},
}
for app, weights in APPS.items():
    best = rank(pool, weights)
    print(f"{app:<13}", "  ".join(f"{n} {s}" for s, n in best),
          "->", best[0][1])
