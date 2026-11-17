# How LLMs Work: code (AI Engineer Roadmap, Episode 3)

Two small Python files. **No API key, no GPU, no install**: they use only the Python standard library (Python 3.8+).

| File | What it shows |
|---|---|
| `mini_bpe.py` | Tokenization. Builds a tiny BPE (byte pair encoding) tokenizer: start from letters, merge the most common pair, repeat. Then splits new words, even one it never saw ("slowest"). |
| `sampling.py` | How the next token is picked. Turns example scores (logits) into probabilities with softmax, then shows temperature, top-k, top-p and a repetition penalty, and samples 6 picks at three temperatures. |

## Run

```
python mini_bpe.py
python sampling.py
```

## Expected output

`mini_bpe.py`
```
merge  1: l + o -> lo  (seen 5x)
...
merge 10: ne + w -> new  (seen 3x)
lowest   -> ['low', 'est_']
newer    -> ['new', 'er_']
slowest  -> ['s', 'low', 'est_']
```

`sampling.py`
```
temp 0.2    | tea 88%  coffee 12%  chai 0%  water 0%
temp 1.0    | tea 48%  coffee 32%  chai 12%  water 5%
temp 1.5    | tea 40%  coffee 30%  chai 16%  water 9%
top-k 2     | tea 60%  coffee 40%
top-p 0.9   | tea 52%  coffee 35%  chai 13%
penalty tea | coffee 51%  tea 20%  chai 19%  water 8%
T=0.2: tea tea tea tea tea tea
T=1.0: coffee coffee tea tea chai tea
T=1.5: chai tea coffee chai tea water
```

## Notes
* The scores in `sampling.py` are made-up example logits, so the numbers are for learning, not from a real model.
* Real tokenizers (for GPT, Llama, Gemini and others) work on bytes, learn tens of thousands of merges from huge text, and handle spaces differently. The idea is the same.
* Real APIs call these settings `temperature`, `top_p`, `top_k`, `frequency_penalty`, `presence_penalty` or `repetition_penalty`. Which ones exist depends on the provider and model; check its docs.
