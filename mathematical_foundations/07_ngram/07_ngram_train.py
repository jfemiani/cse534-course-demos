"""
N-Gram Language Model - Training
Count N-grams from corpus and save model.
"""
import json
import numpy as np
from urllib.request import urlopen
from rich.progress import track

ORDER = 4  # context length (ORDER=4 means 5-gram)
ALPHA = 1.0  # add-alpha smoothing

# Fetch corpus
url = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
with urlopen(url) as r:
    corpus = r.read().decode('utf-8')[:50000]

vocab = sorted(set(corpus))
V = len(vocab)

print(f"ORDER={ORDER}, vocab size={V}, corpus length={len(corpus)}")

# Build count dict: count[ctx_string] = {char: count}
count = {}
for i in track(range(len(corpus) - ORDER), description="Counting N-grams"):
    ctx = corpus[i:i+ORDER]
    next_char = corpus[i+ORDER]
    if ctx not in count:
        count[ctx] = {}
    count[ctx][next_char] = count[ctx].get(next_char, 0) + 1

print(f"Unique contexts: {len(count)}")

# Save counts
with open("ngram_counts.json", "w") as f:
    json.dump(count, f, indent=2)

print("Counts saved to ngram_counts.json")
