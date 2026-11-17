# How LLMs Work: a mini BPE tokenizer. Python stdlib only.
from collections import Counter

def merge(w, a, b):               # glue every "a b" pair into "ab"
    i = 0
    while i < len(w) - 1:
        if w[i] == a and w[i + 1] == b:
            w[i:i + 2] = [a + b]
        else:
            i += 1
    return w

text = "low low low lower lowest new newer newest wide wider widest"
words = [list(w) + ["_"] for w in text.split()]   # "_" = word end
merges = []

for step in range(10):
    pairs = Counter()
    for w in words:
        for a, b in zip(w, w[1:]):
            pairs[a, b] += 1
    (a, b), n = pairs.most_common(1)[0]       # most common pair
    merges.append((a, b))
    print(f"merge {step + 1:>2}: {a} + {b} -> {a + b}  (seen {n}x)")
    for w in words:
        merge(w, a, b)

def tokenize(word):
    w = list(word) + ["_"]
    for a, b in merges:                       # same merges, same order
        merge(w, a, b)
    return w

for word in ["lowest", "newer", "slowest"]:
    print(f"{word:<8} -> {tokenize(word)}")
