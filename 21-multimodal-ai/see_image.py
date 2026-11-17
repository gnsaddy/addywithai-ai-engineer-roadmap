# see_image.py: how a vision model "sees" an image, and what it costs
# 1) cut the image into patches   2) count the tokens (Episode 21)
import math
import numpy as np
from PIL import Image

PATCH = 32   # a vision encoder looks at small squares (patches)

def to_patches(path, size=448):
    img = Image.open(path).convert("RGB").resize((size, size))
    a = np.asarray(img, dtype=np.float32) / 255    # (448, 448, 3)
    n = size // PATCH                               # 14 per side
    p = a.reshape(n, PATCH, n, PATCH, 3).swapaxes(1, 2)
    return p.reshape(n * n, PATCH * PATCH * 3)      # 1 row per patch

def openai_tokens(w, h, detail="high"):   # GPT-4o style tile rule
    if detail == "low":
        return 85
    s = min(1, 2048 / max(w, h)); w, h = w * s, h * s
    s = min(1, 768 / min(w, h)); w, h = w * s, h * s
    return 85 + 170 * math.ceil(w / 512) * math.ceil(h / 512)

def claude_tokens(w, h):                  # about (width x height) / 750
    s = min(1, 1568 / max(w, h), math.sqrt(1_150_000 / (w * h)))
    return round(w * s * h * s / 750)

if __name__ == "__main__":
    p = to_patches("receipt.png")
    print("patches:", p.shape[0], "| numbers per patch:", p.shape[1])
    for name, (w, h) in {"receipt 600x800": (600, 800),
                         "phone photo 4032x3024": (4032, 3024)}.items():
        print(f"{name:22} openai high {openai_tokens(w, h):5}"
              f" | low {openai_tokens(w, h, 'low'):3}"
              f" | claude {claude_tokens(w, h):5}")
    for mins in (1, 10, 60):              # Gemini: ~263 tokens per second
        print(f"video {mins:2} min  ~{mins * 60 * 263:>9,} tokens")
