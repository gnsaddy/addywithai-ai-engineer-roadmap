# review_diff.py: a quick safety check on a diff from an AI coding tool, before you accept it.
# Usage: python review_diff.py fix.diff
import re
import sys

CHECKS = [
    ("secret",     r"(sk-[A-Za-z0-9]{16,}|api_key\s*=\s*['\"])", "a key is written in the code"),
    ("test-skip",  r"pytest\.mark\.skip|@unittest\.skip",        "a test was switched off"),
    ("danger",     r"rm -rf|DROP TABLE|os\.system\(",            "a dangerous command"),
    ("new-lib",    r"^(import|from) (requests|numpy|pandas)\b",  "a new library (ask first)"),
]

def review(diff_text):
    added = [l[1:] for l in diff_text.splitlines() if l.startswith("+") and not l.startswith("+++")]
    removed = [l[1:] for l in diff_text.splitlines() if l.startswith("-") and not l.startswith("---")]
    found = []
    for name, pattern, why in CHECKS:
        for line in added:
            if re.search(pattern, line.strip()):
                found.append((name, why, line.strip()[:48]))
    for line in removed:                     # deleting a test is never a fix
        if line.strip().startswith("def test_"):
            found.append(("test-deleted", "a test was deleted", line.strip()[:48]))
    return len(added), len(removed), found

if __name__ == "__main__":
    plus, minus, found = review(open(sys.argv[1], encoding="utf-8").read())
    print(f"{sys.argv[1]}: +{plus} -{minus} lines")
    for name, why, line in found:
        print(f"  ! {name:12} {why:28} | {line}")
    print("verdict: BLOCK, fix these first" if found else "verdict: OK to review by eye")
