# compare_all.py: run all three versions and show their answers side by side.
#   python compare_all.py --demo
import subprocess, sys

VERSIONS = ["rag_plain.py", "rag_langchain.py", "rag_llamaindex.py"]
answers = {}
for v in VERSIONS:
    out = subprocess.run([sys.executable, v, *sys.argv[1:]],
                         capture_output=True, text=True).stdout
    rows = [line.split("| ", 1)[1] for line in out.splitlines() if "| " in line]
    answers[v] = list(zip(rows[0::2], rows[1::2]))   # (question, answer) pairs

for i, (question, _) in enumerate(answers[VERSIONS[0]]):
    print(f"Q: {question}")
    for v in VERSIONS:
        a = answers[v][i][1]
        if len(a) > 56:                               # keep the start + the citation
            a = a[:40] + "... " + a[a.rfind("["):] if a.endswith("]") else a[:56]
        print(f"   {v:<18} {a}")
