# quantize_demo.py: why quantization makes models smaller. Stdlib only.
import random

def memory_gb(params_billion, bits):
    return params_billion * bits / 8  # billions of weights x bytes each

print("Memory just to hold the weights:")
print(f"{'model':>6} {'16-bit':>9} {'8-bit':>9} {'4-bit':>9}")
for size in [1, 8, 70]:
    row = [f"{memory_gb(size, b):>6.1f} GB" for b in (16, 8, 4)]
    print(f"{str(size) + 'B':>6} " + " ".join(row))

def quantize(weights, bits):
    levels = 2 ** (bits - 1) - 1  # 127 for 8-bit, 7 for 4-bit
    scale = max(abs(w) for w in weights) / levels
    return [round(w / scale) for w in weights], scale

def dequantize(q, scale):
    return [x * scale for x in q]

def avg_error(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)

random.seed(7)
weights = [random.gauss(0, 0.05) for _ in range(10_000)]
print("\nOriginal:", [round(w, 4) for w in weights[:4]])
for bits in (8, 4):
    q, scale = quantize(weights, bits)
    err = avg_error(weights, dequantize(q, scale))
    print(f"{bits}-bit: {q[:4]}  avg error {err:.4f}")

back = []
for i in range(0, len(weights), 64):  # one scale per group of 64
    q, scale = quantize(weights[i:i + 64], 4)
    back += dequantize(q, scale)
print(f"4-bit, groups of 64: avg error {avg_error(weights, back):.4f}")
