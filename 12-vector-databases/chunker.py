# chunker.py: split long text into small, overlapping chunks (one idea each).
import re

def chunk(text, max_chars=120, overlap=1):
    """Pack whole sentences into chunks of up to max_chars.
    Each new chunk repeats the last `overlap` sentence(s) of the one before,
    so an idea that sits on a border is not cut in half."""
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks, cur = [], []
    for s in sentences:
        if cur and len(" ".join(cur + [s])) > max_chars:
            chunks.append(" ".join(cur))
            cur = cur[-overlap:] if overlap else []
        cur.append(s)
    if cur:
        chunks.append(" ".join(cur))
    return chunks

if __name__ == "__main__":
    text = open("docs/leave-policy.txt").read()
    for i, c in enumerate(chunk(text)):
        print(f"[{i}] {c}")
