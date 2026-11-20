# courier_api.py: a stand-in for an internal HTTP API (the courier's tracking service).
# In a real company: requests.get("https://courier.internal/track/<id>", timeout=3).
# Here it is a local function with fake data, so the demo runs offline, on CPU, with no keys.
import time

_TRACKING = {
    "TRK-5521": {"status": "delivered", "where": "Bengaluru", "eta": "done"},
    "TRK-7734": {"status": "in transit", "where": "Pune hub", "eta": "2026-11-21"},
    "TRK-9000": "slow",          # pretend this one hangs, to show the timeout path
}

class ApiError(Exception):
    pass

def track(tracking_id: str, timeout_s: float = 2.0) -> dict:
    time.sleep(0.05)              # a small network delay
    data = _TRACKING.get(tracking_id)
    if data == "slow":
        raise ApiError(f"courier API timed out after {timeout_s} s")
    if data is None:
        raise ApiError(f"404: no parcel with id {tracking_id}")
    return dict(data, tracking_id=tracking_id)
