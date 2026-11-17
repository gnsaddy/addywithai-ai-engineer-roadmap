# search.py: semantic search. Find notes by MEANING, not by matching words.
from embed import embed, cosine

NOTES = [
    "Easy pasta recipe for a quick dinner",
    "How to save money on a small salary",
    "My laptop battery dies too fast",
    "Football team training before the match",
    "Make your phone app run less slow",
    "Cheap pizza night with the bank budget",
]
QUERY = "my computer is slow"

note_vecs = embed(NOTES)              # embed once, store, reuse
query_vec = embed([QUERY])[0]         # embed the question at search time
scores = [(cosine(query_vec, v), n) for v, n in zip(note_vecs, NOTES)]
print("Query:", QUERY)
for score, note in sorted(scores, reverse=True)[:3]:   # top 3
    print(f"  {score:.2f}  {note}")
