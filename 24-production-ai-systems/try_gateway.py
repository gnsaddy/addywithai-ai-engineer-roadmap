# try_gateway.py: send real HTTP requests to gateway.py (in-process, no server needed)
import time
from fastapi.testclient import TestClient
import fake_llm, gateway

c = TestClient(gateway.app)
ASHA, RAVI = {"X-API-Key": "demo-key-asha"}, {"X-API-Key": "demo-key-ravi"}

def show(label, r):
    b = r.json()
    if r.status_code >= 400:
        print(f"{label:<20} {r.status_code}  {b['detail']}")
    elif "job_id" in b or "status" in b:
        print(f"{label:<20} {r.status_code}  {b}")
    else:
        print(f"{label:<20} {r.status_code}  {b['model']:<11} retries={b['retries']} "
              f"cached={b['cached']!s:<5} cost=Rs {b['cost']}")

show("no key", c.post("/ask", json={"prompt": "What is RAG?"}))
show("first ask", c.post("/ask", json={"prompt": "What is RAG?"}, headers=ASHA))
show("same, new spacing", c.post("/ask", json={"prompt": "what is  RAG?"}, headers=ASHA))
time.sleep(3)                                # wait: the bucket refills to 3
for i in range(4):
    show(f"burst {i + 1}", c.post("/ask", json={"prompt": f"Explain topic {i}"}, headers=ASHA))
time.sleep(1.1)
show("over budget", c.post("/ask", json={"prompt": "One more question"}, headers=ASHA))

fake_llm.FAIL["big-model"] = 9               # big model is down
show("big model down", c.post("/ask", json={"prompt": "Summarise this ticket"}, headers=RAVI))
job = c.post("/jobs", json={"prompt": "Summarise 200 tickets"}, headers=RAVI)
show("start job", job)
show("check job", c.get(f"/jobs/{job.json()['job_id']}"))
print("health:", c.get("/health").json())
