# mini_vector_db.py: what a vector database does, in a few lines (a FLAT index:
# compare the question with EVERY vector). Real databases add fast indexes (HNSW),
# saving to disk, filters at scale, and many users at once.
import math, os, sys
from chunker import chunk
from embedder import embed

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0

class MiniVectorDB:
    def __init__(self):
        self.rows = {}                                  # id -> (vector, metadata, text)
    def upsert(self, id, vector, meta, text):
        self.rows[id] = (vector, meta, text)
    def search(self, q, k=2, where=None):
        hits = [(cosine(q, v), m["source"], t) for v, m, t in self.rows.values()
                if not where or all(m.get(f) == x for f, x in where.items())]
        return sorted(hits, reverse=True)[:k]          # top k by similarity

db = MiniVectorDB()
for name in sorted(os.listdir("docs")):
    chunks = chunk(open("docs/" + name).read())
    for i, (c, v) in enumerate(zip(chunks, embed(chunks))):
        db.upsert(f"{name}#{i}", v, {"source": name}, c)
for score, src, text in db.search(embed(["How many vacation days do I get?"])[0]):
    print(f"{score:.2f}  [{src}] {text[:58]}...")
