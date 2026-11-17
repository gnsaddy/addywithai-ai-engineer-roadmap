# rag.py: chat with your PDF. RAG from scratch: retrieve, augment, generate.
#   pip install pypdf      python rag.py travel-policy.pdf --demo
import math, sys
from ingest import load_pdf, chunk_pages
from models import embed, chat

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0

# 1. INGEST (once): load, chunk, embed. In memory here (or a vector DB).
chunks = chunk_pages(load_pdf(sys.argv[1]))
vectors = embed([c["text"] for c in chunks])
print(f"indexed {len(chunks)} chunks from {sys.argv[1]}")

# 2. RETRIEVE: the k chunks closest to the question
def retrieve(question, k=3):
    q = embed([question])[0]
    ranked = sorted(zip(vectors, chunks), key=lambda v: -cosine(q, v[0]))
    return [c for _, c in ranked[:k]]

# 3. AUGMENT: put the chunks in the prompt, numbered, so answers can cite
SYSTEM = ("Answer ONLY from the sources. Cite them like [1]. "
          "If the answer is not in the sources, say: I don't know.")
def build_prompt(question, found):
    sources = "\n".join(f"[{i}] (page {c['page']}) {c['text']}"
                        for i, c in enumerate(found, 1))
    user = f"Sources:\n{sources}\n\nQuestion: {question}"
    return [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": user}]

# 4. GENERATE: the LLM answers from the sources
for question in ["How much can I spend on a hotel in Tokyo?",
                 "When must I submit my expense claim?",
                 "What is the office wifi password?"]:
    found = retrieve(question)
    pages = [c["page"] for c in found]
    print(f"\nQ: {question}   (retrieved pages {pages})")
    print("A: " + chat(build_prompt(question, found)))
