"""
N-Gram Language Model - Prediction
Load counts and generate text.
"""
import json
import numpy as np

ORDER = 8  # must match training
PAD = "^"
END = "$"
MAX_LEN = 500
NUM_SENTENCES = 5

# Load counts
with open("ngram_counts.json") as f:
    count = json.load(f)

print(f"Loaded {len(count)} contexts")
print(f"\nGenerating {NUM_SENTENCES} sentences:\n")

rng = np.random.default_rng(None)

for _ in range(NUM_SENTENCES):
    # Start each sentence with padding
    gen = PAD * ORDER
    
    for _ in range(MAX_LEN):
        ctx = gen[-ORDER:]
        ctx_counts = count.get(ctx, {})
        if not ctx_counts:  # unseen context, stop
            break
        # Sample from observed next chars only
        chars = list(ctx_counts.keys())
        probs = np.array([ctx_counts[c] for c in chars])
        probs = probs / probs.sum()
        next_char = rng.choice(chars, p=probs)
        gen += next_char
        if next_char == END:
            break
    
    # Strip padding and end marker
    sentence = gen[ORDER:].replace(END, "")
    print(sentence)
