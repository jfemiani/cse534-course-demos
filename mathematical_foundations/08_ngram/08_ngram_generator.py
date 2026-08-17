"""
N-Gram Language Model
Train, generate, and evaluate with NLL and perplexity.
"""
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from urllib.request import urlopen

ORDER = 4  # context length (ORDER=4 means 5-gram)
ALPHA = 1.0  # add-alpha smoothing

# Fetch corpus
url = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
try:
    with urlopen(url) as r:
        corpus = r.read().decode('utf-8')[:50000]
except:
    corpus = "To be or not to be that is the question\n" * 100

vocab = sorted(set(corpus))
char_to_idx = {c: i for i, c in enumerate(vocab)}
V = len(vocab)

print(f"ORDER={ORDER} (context length), vocab size={V}, corpus length={len(corpus)}")
print()

# Extract all (context, next_char) pairs with sliding window
codes = np.array([char_to_idx[c] for c in corpus])
windows = sliding_window_view(codes, ORDER+1)
contexts = [''.join(vocab[i] for i in w[:-1]) for w in windows]
next_idxs = windows[:, -1]

# Build count dict: count[ctx] = histogram over vocab
count = {}
for ctx, idx in zip(contexts, next_idxs):
    if ctx not in count:
        count[ctx] = np.zeros(V, dtype=int)
    count[ctx][idx] += 1

print(f"Unique contexts: {len(count)}")
print()

# Generate
gen = corpus[:ORDER]
np.random.seed(42)
for _ in range(200):
    ctx = gen[-ORDER:]
    # P(next|ctx) with add-alpha smoothing
    counts = count.get(ctx, np.zeros(V))
    probs = (counts + ALPHA) / (counts.sum() + ALPHA * V)
    next_idx = np.random.choice(V, p=probs)
    gen += vocab[next_idx]

print("Generated:")
print(gen)
print()

# Evaluate on held-out text
test = corpus[40000:45000]
nll = 0
for i in range(len(test) - ORDER):
    ctx = test[i:i+ORDER]
    next_idx = char_to_idx[test[i+ORDER]]
    counts = count.get(ctx, np.zeros(V))
    probs = (counts + ALPHA) / (counts.sum() + ALPHA * V)
    nll += -np.log(probs[next_idx])

avg_nll = nll / (len(test) - ORDER)
perplexity = np.exp(avg_nll)

print(f"Held-out NLL: {avg_nll:.4f}")
print(f"Perplexity: {perplexity:.2f}")
print("Lower perplexity = model assigns higher probability to held-out text")
