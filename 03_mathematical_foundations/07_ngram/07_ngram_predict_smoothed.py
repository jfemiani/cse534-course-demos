"""
N-Gram Language Model - Prediction with Bayesian Smoothing
Load counts and generate text, never hitting dead ends.
"""
import json
import numpy as np

ORDER = 8  # must match training
PAD = "^"
END = "$"
MAX_LEN = 500
NUM_BLOCKS = 5
ALPHA = 0.01  # smoothing parameter (imaginary prior observations)

# Load counts
with open("ngram_counts.json") as f:
    count = json.load(f)

# Build vocabulary from all characters seen during training
vocab = list(set().union(*count.values()))

print(f"Loaded {len(count)} contexts")
print(f"Vocabulary size: {len(vocab)} characters")
print(f"Smoothing parameter α = {ALPHA}")
print(f"\nGenerating {NUM_BLOCKS} blocks of text:\n")

rng = np.random.default_rng(None)

for _ in range(NUM_BLOCKS):
    # Start each block with padding
    gen = PAD * ORDER
    
    for _ in range(MAX_LEN):
        ctx = gen[-ORDER:]
        ctx_counts = count.get(ctx, {})
        
        # Bayesian smoothing: alpha prior + observed counts
        counts = np.array([ALPHA + ctx_counts.get(c, 0) for c in vocab])
        probs = counts / counts.sum()
        
        next_char = rng.choice(vocab, p=probs)
        gen += next_char
        if next_char == END:
            break
    
    # Strip padding and end marker
    block = gen[ORDER:].replace(END, "")
    print(block)
    print()  # blank line between blocks
