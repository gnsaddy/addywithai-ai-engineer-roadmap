# compare_models.py: the SAME search task on two embedding models.
# Scores: recall@1, recall@3 (is the right note in the top 1 / top 3?) and MRR.
#   python compare_models.py --demo                       (two toy models)
#   python compare_models.py nomic-embed-text all-minilm  (real, BASE_URL set)
import math, sys
from testset import DOCS, TESTS
from models import api_model, toy_word_match, toy_meaning

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0

def ranks(embed):                     # rank of the right note for each question
    doc_vecs = embed(DOCS)            # embed the notes once
    out = []
    for question, right in TESTS:
        q = embed([question])[0]
        order = sorted(range(len(DOCS)), key=lambda i: -cosine(q, doc_vecs[i]))
        out.append(order.index(right) + 1)   # 1 = first place
    return out

if "--demo" in sys.argv:
    MODELS = [("word-match", toy_word_match), ("meaning", toy_meaning)]
else:
    MODELS = [(m, api_model(m)) for m in sys.argv[1:3]]

R = {name: ranks(fn) for name, fn in MODELS}
names = list(R)
print(f"{'question':<30}" + "".join(f"{n:>12}" for n in names))
for i, (question, _) in enumerate(TESTS):
    print(f"{question:<30}" + "".join(f"{R[n][i]:>12}" for n in names))
n = len(TESTS)
for label, score in [("recall@1", lambda r: sum(x == 1 for x in r) / n),
                     ("recall@3", lambda r: sum(x <= 3 for x in r) / n),
                     ("MRR",      lambda r: sum(1 / x for x in r) / n)]:
    print(f"{label:<30}" + "".join(f"{score(R[m]):>12.2f}" for m in names))
