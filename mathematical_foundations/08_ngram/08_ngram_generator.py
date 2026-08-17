"""
N-Gram Language Model
Train a character-level model, generate text, and evaluate with perplexity.
"""
import numpy as np
from collections import defaultdict

# Configuration
ORDER = 2  # context length (ORDER=2 means trigram, N=3)
SMOOTHING = 1  # add-one smoothing

# Training corpus
corpus = """To be or not to be that is the question
Whether tis nobler in the mind to suffer
The slings and arrows of outrageous fortune"""

print(f"Context length (ORDER): {ORDER}")
print(f"Training on {len(corpus)} characters")
print()

# Build counts
counts = defaultdict(lambda: defaultdict(int))
for i in range(len(corpus) - ORDER):
    context = corpus[i:i + ORDER]
    next_char = corpus[i + ORDER]
    counts[context][next_char] += 1

print(f"Learned {len(counts)} unique contexts")
print()

# Generation
def sample_next(context, counts, vocab):
    """Sample next character given context with smoothing."""
    options = counts[context]
    chars = list(vocab)
    probs = np.array([options[c] + SMOOTHING for c in chars])
    probs = probs / probs.sum()
    return np.random.choice(chars, p=probs)

vocab = set(corpus)
seed = corpus[:ORDER]
generated = seed
for _ in range(50):
    context = generated[-ORDER:]
    next_char = sample_next(context, counts, vocab)
    generated += next_char

print("Generated sample:")
print(generated)
print()

# Evaluation on held-out text
test_text = "not to be"
nll = 0
for i in range(len(test_text) - ORDER):
    context = test_text[i:i + ORDER]
    next_char = test_text[i + ORDER]
    
    # Get smoothed probability
    count_next = counts[context][next_char] + SMOOTHING
    count_total = sum(counts[context].values()) + SMOOTHING * len(vocab)
    prob = count_next / count_total
    
    nll += -np.log(prob)

avg_nll = nll / (len(test_text) - ORDER)
perplexity = np.exp(avg_nll)

print(f"Test text: '{test_text}'")
print(f"Average NLL: {avg_nll:.4f}")
print(f"Perplexity: {perplexity:.4f}")
print()
print("Lower perplexity means the model assigns higher probability to the text.")
