# How LLMs Work: turn next-token scores into a choice. Stdlib only.
import math, random

# Example scores (logits) for the next token after "I'd like a cup of"
logits = {"tea": 4.0, "coffee": 3.6, "chai": 2.6, "water": 1.8,
          "soup": 0.6, "rocks": -2.0}

def softmax(scores, temperature=1.0):
    t = max(temperature, 1e-6)                # never divide by 0
    exps = {k: math.exp(v / t) for k, v in scores.items()}
    total = sum(exps.values())
    return {k: e / total for k, e in exps.items()}

def ranked(probs):
    return sorted(probs.items(), key=lambda x: -x[1])

def renorm(keep):
    total = sum(keep.values())
    return {k: p / total for k, p in keep.items()}

def top_k(probs, k):
    return renorm(dict(ranked(probs)[:k]))     # keep the k best

def top_p(probs, p):
    keep, running = {}, 0.0
    for tok, pr in ranked(probs):
        keep[tok] = pr
        running += pr
        if running >= p:                       # stop at p of the total
            break
    return renorm(keep)

def penalize(scores, used, penalty=1.5):
    # tokens already used get a lower score (CTRL-style penalty)
    return {k: (v / penalty if v > 0 else v * penalty) if k in used else v
            for k, v in scores.items()}

def show(label, probs):
    best = "  ".join(f"{k} {p:.0%}" for k, p in ranked(probs)[:4])
    print(f"{label:<12}| {best}")

show("temp 0.2", softmax(logits, 0.2))
show("temp 1.0", softmax(logits, 1.0))
show("temp 1.5", softmax(logits, 1.5))
show("top-k 2", top_k(softmax(logits), 2))
show("top-p 0.9", top_p(softmax(logits), 0.9))
show("penalty tea", softmax(penalize(logits, {"tea"})))

random.seed(1)                    # same picks every run
for temp in (0.2, 1.0, 1.5):
    probs = softmax(logits, temp)
    picks = random.choices(list(probs), weights=list(probs.values()), k=6)
    print(f"T={temp}: " + " ".join(picks))
