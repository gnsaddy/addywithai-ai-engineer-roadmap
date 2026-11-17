# uses.py: the same vectors also classify, recommend and flag anomalies.
from embed import embed, cosine

LABELS = ["food", "sport", "tech", "money"]
label_vecs = embed(["cook dinner recipe", "gym running match",
                    "laptop phone app", "salary budget bank"])

def classify(text):                       # nearest label wins
    v = embed([text])[0]
    scores = [cosine(v, lv) for lv in label_vecs]
    return LABELS[scores.index(max(scores))]

for text in ["Quick pizza for dinner", "New phone battery"]:
    print(f"classify   {text!r:<26} -> {classify(text)}")

liked = embed(["Easy pasta recipe"])[0]   # what this user liked
posts = ["Pizza dinner tonight", "Bank salary tips", "Gym running plan"]
pick = max(posts, key=lambda p: cosine(liked, embed([p])[0]))
print(f"recommend  liked pasta -> {pick!r}")

normal = embed(["laptop battery slow", "phone app crashes",
                "computer running slow"])  # usual support tickets
for text in ["App crashes on my phone", "Pasta recipe for dinner"]:
    near = max(cosine(embed([text])[0], v) for v in normal)
    flag = "  <- anomaly" if near < 0.5 else ""
    print(f"anomaly    {text!r:<26} closest={near:.2f}{flag}")
