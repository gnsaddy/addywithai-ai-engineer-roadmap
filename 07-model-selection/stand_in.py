# stand_in.py: fake models for the --demo runs (no API key, no network).
# Fixed delays and token counts, so you can see the table work.
import time

FAKE = {  # model: (seconds, output tokens)
    "small": (0.4, 60),
    "medium": (0.9, 75),
    "large": (2.1, 110),
}

def ask(model, prompt):
    secs, n_out = FAKE[model]
    time.sleep(secs)
    n_in = len(prompt) // 4 + 4  # about 4 characters a token + chat overhead
    return "An API is like a waiter...", n_in, n_out
