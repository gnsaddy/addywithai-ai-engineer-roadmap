# Context Engineering: build a small, focused context.
import re
from data import INSTRUCTIONS, DOCS, HISTORY, QUESTION

def count_tokens(text):
    return round(len(text) / 4)   # 1 token ~ 4 characters

def words(text):
    return set(re.findall(r"[a-z]+", text.lower()))

def retrieve(question, docs, k=2):
    # score each document by shared words, keep the best k
    score = lambda d: len(words(question) & words(d))
    return sorted(docs, key=score, reverse=True)[:k]

def build_context(question, history, docs, keep_last=2):
    parts = [("INSTRUCTIONS", INSTRUCTIONS)]
    for doc in retrieve(question, docs):
        parts.append(("DOCUMENT", doc))
    older = len(history) - keep_last
    if older > 0:
        note = f"{older} older messages: order, delivery, charger"
        parts.append(("SUMMARY", note))
    for msg in history[-keep_last:]:
        parts.append(("HISTORY", msg))
    parts.append(("QUESTION", question))   # question goes last
    return parts

def total(parts):
    return sum(count_tokens(text) for _, text in parts)

if __name__ == "__main__":
    naive = [("INSTRUCTIONS", INSTRUCTIONS)]
    naive += [("DOCUMENT", d) for d in DOCS]
    naive += [("HISTORY", m) for m in HISTORY]
    naive += [("QUESTION", QUESTION)]
    smart = build_context(QUESTION, HISTORY, DOCS)
    print("Naive:", total(naive), "tokens,", len(naive), "parts")
    print("Smart:", total(smart), "tokens,", len(smart), "parts")
    for label, text in smart:
        print(f"[{label}] {text[:40]}...")
