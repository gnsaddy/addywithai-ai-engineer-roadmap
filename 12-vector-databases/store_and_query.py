# store_and_query.py: chunk two documents, store them in Chroma, then search.
#   pip install chromadb        python store_and_query.py --demo
import os, chromadb
from chunker import chunk
from embedder import embed

client = chromadb.PersistentClient(path="./vector_db")   # saved on disk
col = client.get_or_create_collection("handbook", metadata={"hnsw:space": "cosine"})

ids, docs, metas = [], [], []
for name in sorted(os.listdir("docs")):                   # 1. load + chunk
    for i, c in enumerate(chunk(open("docs/" + name).read())):
        ids.append(f"{name}#{i}"); docs.append(c); metas.append({"source": name})
col.upsert(ids=ids, documents=docs, metadatas=metas,     # 2. embed + store
           embeddings=embed(docs))
print(f"stored {col.count()} chunks")

def search(question, k=2, where=None):                    # 3. search
    r = col.query(query_embeddings=embed([question]), n_results=k, where=where)
    print(f"\nQ: {question}" + (f"   filter={where}" if where else ""))
    for doc, meta, dist in zip(r["documents"][0], r["metadatas"][0], r["distances"][0]):
        print(f"  {1 - dist:.2f}  [{meta['source']}] {doc[:58]}...")

search("How many vacation days do I get?")
search("My computer is slow", where={"source": "it-help.txt"})
