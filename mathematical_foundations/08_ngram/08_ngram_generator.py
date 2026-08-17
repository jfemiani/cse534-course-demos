"""
N-Gram Language Model
Train, generate, and evaluate with NLL and perplexity.
"""
import numpy as np
from urllib.request import urlopen

ORDER = 4  # context length (ORDER=4 means 5-gram)
ALPHA = 1.0  # add-alpha smoothing

# Fetch corpus
url = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
with urlopen(url) as r:
    corpus = r.read().decode('utf-8')[:50000]

vocab = sorted(set(corpus))
V = len(vocab)

print(f"ORDER={ORDER} (context length), vocab size={V}, corpus length={len(corpus)}")
print()

# Build count dict: count[ctx_string] = {char: count}
count = {}
for i in range(len(corpus) - ORDER):
    ctx = corpus[i:i+ORDER]
    next_char = corpus[i+ORDER]
    if ctx not in count:
        count[ctx] = {}
    count[ctx][next_char] = count[ctx].get(next_char, 0) + 1

print(f"Unique contexts: {len(count)}")
print()

# Generate
gen = corpus[:ORDER]
np.random.seed(42)
for _ in range(200):
    ctx = gen[-ORDER:]
    # P(next|ctx) with add-alpha smoothing: (count + alpha) / (total + alpha*V)
    ctx_counts = count.get(ctx, {})
    probs = np.array([(ctx_counts.get(c, 0) + ALPHA) for c in vocab])
    probs = probs / probs.sum()
    gen += np.random.choice(vocab, p=probs)

print("Generated:")
print(gen)
print()

# Evaluate on held-out text
test = corpus[40000:45000]
nll = 0
for i in range(len(test) - ORDER):
    ctx = test[i:i+ORDER]
    next_char = test[i+ORDER]
    ctx_counts = count.get(ctx, {})
    probs = np.array([(ctx_counts.get(c, 0) + ALPHA) for c in vocab])
    probs = probs / probs.sum()
    char_idx = vocab.index(next_char)
    nll += -np.log(probs[char_idx])

avg_nll = nll / (len(test) - ORDER)
perplexity = np.exp(avg_nll)

print(f"Held-out NLL: {avg_nll:.4f}")
print(f"Perplexity: {perplexity:.2f}")
print("Lower perplexity = model assigns higher probability to held-out text")
