# run_evals.py: run every case on both prompt versions, then compare.
# A regression = a case that passed before, and fails now.
from app import answer
from checks import CHECKS
from dataset import CASES
from judge import judge

def run(version):
    results = {}
    for case in CASES:
        got = answer(version, case)
        if case["check"] == "judge":
            ok, detail = judge(case, got)
            note = f"judge {detail['score']}/5"
        else:
            ok = CHECKS[case["check"]](got, case["want"])
            note = case["check"]
        results[case["id"]] = (ok, note)
    return results

old, new = run("v1"), run("v2")
print("case  check        v1     v2")
for case in CASES:
    i = case["id"]
    mark = lambda r: "pass" if r[0] else "FAIL"
    flag = "  <- REGRESSION" if old[i][0] and not new[i][0] else ""
    print(f"{i:4}  {new[i][1]:11}  {mark(old[i]):5}  {mark(new[i]):5}{flag}")

score = lambda r: sum(ok for ok, _ in r.values())
broke = [i for i in old if old[i][0] and not new[i][0]]
print(f"\nscore: v1 {score(old)}/{len(CASES)}   v2 {score(new)}/{len(CASES)}")
print(f"regressions: {broke or 'none'}")
print("GATE:", "FAIL, do not ship v2 yet" if broke else "pass, safe to ship")
