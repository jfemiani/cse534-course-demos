"""
Bigram Counts to Conditional Probabilities
Shows how character counts become P(next|context).
"""
import numpy as np

text = "banana"
chars = sorted(set(text))
char_to_idx = {c: i for i, c in enumerate(chars)}

print(f"Text: {text}")
print(f"Vocabulary: {chars}")
print()

# Count bigrams: bigram_counts[i,j] = count(chars[i] -> chars[j])
codes = np.array([char_to_idx[c] for c in text])
bigram_counts = np.zeros((len(chars), len(chars)), dtype=int)
bigram_counts[codes[:-1], codes[1:]] += 1

print("Bigram counts (context -> next):")
for i, c in enumerate(chars):
    for j, n in enumerate(chars):
        if bigram_counts[i, j] > 0:
            print(f"  {c} -> {n}: {bigram_counts[i, j]}")
print()

# P(next|context) = count(context, next) / count(context)
context_counts = bigram_counts.sum(axis=1, keepdims=True)
probs = bigram_counts / np.clip(context_counts, 1, None)

print("Conditional probabilities P(next|context):")
for i, c in enumerate(chars):
    if context_counts[i, 0] > 0:
        print(f"  After '{c}':")
        for j, n in enumerate(chars):
            if probs[i, j] > 0:
                print(f"    P('{n}'|'{c}') = {bigram_counts[i,j]}/{context_counts[i,0]} = {probs[i,j]:.3f}")
print()

# Generate one character after 'b'
b_idx = char_to_idx['b']
next_idx = np.random.choice(len(chars), p=probs[b_idx])
print(f"Sample after 'b': '{chars[next_idx]}' (prob={probs[b_idx, next_idx]:.3f})")
