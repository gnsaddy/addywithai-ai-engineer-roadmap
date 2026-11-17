# stand_in.py: DEMO ONLY. A toy embedder + a fake "LLM", so every version runs with no model.
# The fake LLM does NOT think: it quotes the source sentence that shares the most words
# with the question and names its source, or says "I don't know". A real LLM writes its own answer.
import re

IDEAS = ["hotel night tokyo london york city",      # toy embedder: 6 ideas
         "flight flights fly economy premium class",
         "meals food alcohol",
         "claim expense expenses receipt submit paid salary",
         "approved approval manager book",
         "train trains trip trips travel travelling"]
def words(t): return re.findall(r"[a-z0-9]+", t.lower())
def toy_embed(texts):   # + a tiny constant, so no vector is all zeros
    return [[float(sum(w in idea.split() for w in words(t))) for idea in IDEAS] + [0.1] for t in texts]

STOP = set("a an the is are i my me can how much what when where do does to of in on for and or be".split())
def fake_llm(messages):
    text = messages[-1]["content"]
    sources, question = text.rsplit("Question:", 1)
    q = set(words(question)) - STOP
    best, best_n, label, cur = "", 0, "", ""
    for line in sources.splitlines():
        m = re.match(r"\s*(\[\d+\])|.*page[_ a-z]*:? ?(\d+)", line)
        if m: cur = m.group(1) or f"[page {m.group(2)}]"
        for sentence in re.split(r"(?<=[.!?])\s+", line):
            hits = len(q & set(words(sentence)))
            if hits > best_n:
                best, best_n, label = re.sub(r"^\s*\[\d+\] \(page \d+\) ", "", sentence), hits, cur
    return f"{best} {label}" if best_n >= 2 else "I don't know. It is not in the sources."
