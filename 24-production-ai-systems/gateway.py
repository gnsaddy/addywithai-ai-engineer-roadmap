# gateway.py: a small production-style AI gateway (FastAPI). Run: uvicorn gateway:app
# auth -> rate limit -> cache -> budget -> retries + fallback -> background jobs
import hashlib, random, time, uuid
from fastapi import BackgroundTasks, FastAPI, Header, HTTPException
from pydantic import BaseModel
import fake_llm

app = FastAPI()
KEYS = {hashlib.sha256(k.encode()).hexdigest(): u            # store key HASHES, never raw keys
        for k, u in [("demo-key-asha", "asha"), ("demo-key-ravi", "ravi")]}
RATE, BURST = 1.0, 3          # 1 request per second, bursts of up to 3
BUDGET = 0.40                 # rupees per user per day (demo value)
buckets, spent, cache, jobs = {}, {}, {}, {}
stats = {"requests": 0, "cache_hits": 0, "retries": 0, "fallbacks": 0, "errors": 0}


class Ask(BaseModel):
    prompt: str


def user_for(api_key):                                        # 1. authentication
    user = KEYS.get(hashlib.sha256((api_key or "").encode()).hexdigest())
    if not user:
        raise HTTPException(401, "missing or wrong API key")
    return user


def allow(user):                                              # 2. rate limit (token bucket)
    now = time.monotonic()
    tokens, last = buckets.get(user, (BURST, now))
    tokens = min(BURST, tokens + (now - last) * RATE)         # refill since last time
    if tokens < 1:
        raise HTTPException(429, "slow down", headers={"Retry-After": "1"})
    buckets[user] = (tokens - 1, now)


def ask_model(prompt):                                        # 4. retries + fallback
    for model in ("big-model", "small-model"):
        for attempt in range(3):
            try:
                return fake_llm.call(model, prompt) | {"model": model, "retries": attempt}
            except fake_llm.Overloaded:
                stats["retries"] += 1
                time.sleep(0.05 * 2 ** attempt + random.uniform(0, 0.02))  # backoff + jitter
        stats["fallbacks"] += 1
    stats["errors"] += 1
    raise HTTPException(503, "all models busy, try again soon")


@app.post("/ask")
def ask(body: Ask, x_api_key: str = Header(None)):
    user = user_for(x_api_key)
    allow(user)
    stats["requests"] += 1
    key = hashlib.sha256(" ".join(body.prompt.lower().split()).encode()).hexdigest()
    if key in cache:                                          # 3. cache: same question = free
        stats["cache_hits"] += 1
        return cache[key] | {"cached": True, "cost": 0}
    if spent.get(user, 0) >= BUDGET:                          # cost control
        raise HTTPException(402, "daily AI budget used up")
    out = ask_model(body.prompt)
    spent[user] = round(spent.get(user, 0) + out["cost"], 3)
    cache[key] = out
    return out | {"cached": False, "spent_today": spent[user]}


@app.post("/jobs", status_code=202)                           # 5. background jobs
def start_job(body: Ask, tasks: BackgroundTasks, x_api_key: str = Header(None)):
    user_for(x_api_key)
    job_id = uuid.uuid4().hex[:6]
    jobs[job_id] = {"status": "queued"}
    tasks.add_task(run_job, job_id, body.prompt)              # real apps: a queue + workers
    return {"job_id": job_id, "status": "queued"}


def run_job(job_id, prompt):
    jobs[job_id] = {"status": "running"}
    jobs[job_id] = {"status": "done", "result": ask_model(prompt)["text"]}


@app.get("/jobs/{job_id}")
def job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(404, "no such job")
    return jobs[job_id]


@app.get("/health")                                           # 6. what your alerts watch
def health():
    return {"ok": True, **stats}
