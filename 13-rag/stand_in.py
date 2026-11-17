# stand_in.py: DEMO ONLY. A toy embedder + a fake "LLM", so rag.py needs no model.
# The fake LLM does NOT think: it quotes the source sentence that shares the
# most words with the question, or says "I don't know". A real LLM writes
# its own answer.
import re

IDEAS = ["hotel night tokyo london york city",      # toy embedder: 6 ideas
         "flight flights fly economy premium class",
         "meals food alcohol",
         "claim expense expenses receipt submit paid salary",
         "approved approval manager book",
         "train trains trip trips travel travelling"]
def words(t): return re.findall(r"[a-z0-9]+", t.lower())
def toy_embed(texts):
    return [[float(sum(w in idea.split() for w in words(t))) for idea in IDEAS]
            for t in texts]

STOP = set("""a an the is are i my me can how much what when where do does
              to of in on for and or be""".split())
def fake_llm(messages):
    user = messages[-1]["content"]
    question = set(words(user.split("Question:")[1])) - STOP
    best, best_n, src = "", 0, 0
    for n, line in re.findall(r"\[(\d+)\] \(page \d+\) (.*)", user):
        for sentence in re.split(r"(?<=[.!?])\s+", line):
            hits = len(question & set(words(sentence)))
            if hits > best_n:
                best, best_n, src = sentence, hits, n
    if best_n < 2:
        return "I don't know. It is not in the sources."
    return f"{best} [{src}]"
