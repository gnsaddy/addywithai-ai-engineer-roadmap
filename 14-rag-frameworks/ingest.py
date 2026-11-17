# ingest.py: PDF -> clean text per page -> small chunks that remember their page.
import re
from pypdf import PdfReader

def load_pdf(path):
    pages = []
    for n, page in enumerate(PdfReader(path).pages, start=1):
        text = re.sub(r"\s+", " ", page.extract_text() or "").strip()
        pages.append((n, text))
    return pages

def chunk_pages(pages, max_chars=200):
    chunks = []
    for n, text in pages:
        cur = ""
        for s in re.split(r"(?<=[.!?])\s+", text):     # whole sentences only
            if cur and len(cur) + len(s) > max_chars:
                chunks.append({"page": n, "text": cur.strip()})
                cur = ""
            cur += s + " "
        if cur.strip():
            chunks.append({"page": n, "text": cur.strip()})
    return chunks
