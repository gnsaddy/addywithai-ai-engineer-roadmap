# rag_plain.py: version 1, plain Python (the same steps as episode 13).
import math, sys
from ingest import load_pdf, chunk_pages
from models import embed, chat
from questions import QUESTIONS, SYSTEM

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0

chunks = chunk_pages(load_pdf("travel-policy.pdf"))
vectors = embed([c["text"] for c in chunks])

def answer(question, k=3):
    q = embed([question])[0]
    top = sorted(zip(vectors, chunks), key=lambda vc: -cosine(q, vc[0]))[:k]
    sources = "\n".join(f"[{i}] (page {c['page']}) {c['text']}"
                        for i, (_, c) in enumerate(top, 1))
    user = f"Sources:\n{sources}\n\nQuestion: {question}"
    return chat([{"role": "system", "content": SYSTEM},
                 {"role": "user", "content": user}])

for q in QUESTIONS:
    print(f"plain      | {q}\n           | {answer(q)}")
