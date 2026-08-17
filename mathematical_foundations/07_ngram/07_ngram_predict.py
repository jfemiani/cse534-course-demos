"""
N-Gram Language Model - Prediction
Load counts and generate text.
"""
import json
import numpy as np

ORDER = 4  # must match training
ALPHA = 1.0

# Load counts
with open("ngram_counts.json") as f:
    count = json.load(f)

# Reconstruct vocab from counts
vocab = sorted(set(c for ctx in count for c in count[ctx]))
V = len(vocab)

print(f"Loaded {len(count)} contexts, vocab size={V}")

# Generate from random seed
seed = list(count.keys())[0]
gen = seed
np.random.seed(42)

for _ in range(500):
    ctx = gen[-ORDER:]
    # P(next|ctx) with add-alpha smoothing
    ctx_counts = count.get(ctx, {})
    probs = np.array([(ctx_counts.get(c, 0) + ALPHA) for c in vocab])
    probs = probs / probs.sum()
    gen += np.random.choice(vocab, p=probs)

print("\nGenerated text:")
print(gen)
