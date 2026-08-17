"""
N-Gram Language Model - Prediction
Load counts and generate text.
"""
import json
import numpy as np

ORDER = 8  # must match training
ALPHA = 0.0001
PAD = "^"
END = "$"
MAX_LEN = 500
NUM_SENTENCES = 5

# Load counts
with open("ngram_counts.json") as f:
    count = json.load(f)

# Reconstruct vocab from counts
vocab = sorted(set(c for ctx in count for c in count[ctx]))
V = len(vocab)

print(f"Loaded {len(count)} contexts, vocab size={V}")
print(f"\nGenerating {NUM_SENTENCES} sentences:\n")

np.random.seed(42)

for _ in range(NUM_SENTENCES):
    # Start each sentence with padding
    gen = PAD * ORDER
    
    for _ in range(MAX_LEN):
        ctx = gen[-ORDER:]
        # P(next|ctx) with add-alpha smoothing
        ctx_counts = count.get(ctx, {})
        probs = np.array([(ctx_counts.get(c, 0) + ALPHA) for c in vocab])
        probs = probs / probs.sum()
        next_char = np.random.choice(vocab, p=probs)
        gen += next_char
        if next_char == END:
            break
    
    # Strip padding and end marker
    sentence = gen[ORDER:].replace(END, "")
    print(sentence)
