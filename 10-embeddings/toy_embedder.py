# toy_embedder.py: a TOY embedder for the demo, so you can see every number.
# 4 dimensions: [food, sport, tech, money]. Real models LEARN hundreds or
# thousands of dimensions from data; nobody writes them by hand.
WORDS = {
    "pizza": [9, 0, 0, 1], "pasta": [9, 0, 0, 0], "recipe": [8, 0, 1, 0],
    "cook": [8, 0, 0, 0], "dinner": [8, 0, 0, 1], "hungry": [7, 1, 0, 0],
    "football": [0, 9, 0, 0], "match": [0, 8, 0, 0], "goal": [0, 8, 0, 1],
    "team": [0, 7, 1, 0], "running": [1, 8, 0, 0], "gym": [1, 8, 0, 0],
    "laptop": [0, 0, 9, 1], "battery": [0, 1, 7, 1], "slow": [0, 2, 6, 0], "fast": [1, 3, 4, 0],
    "phone": [0, 0, 8, 1], "app": [0, 0, 8, 1], "computer": [0, 0, 9, 0],
    "salary": [0, 0, 1, 9], "budget": [1, 0, 0, 9], "save": [1, 0, 1, 7],
    "money": [0, 0, 0, 9], "price": [1, 0, 1, 8], "bank": [0, 0, 1, 9],
    "cheap": [2, 0, 1, 6], "quick": [2, 2, 2, 0], "crashes": [0, 1, 8, 0],
}

def embed(texts):
    out = []
    for text in texts:
        v = [0.0, 0.0, 0.0, 0.0]
        for word in text.lower().replace("?", "").replace(".", "").split():
            word = word if word in WORDS else word.rstrip("s")  # notes -> note
            for i, x in enumerate(WORDS.get(word, [0, 0, 0, 0])):
                v[i] += x  # add up the meaning of every known word
        out.append(v)
    return out
