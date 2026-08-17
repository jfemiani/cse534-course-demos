"""
N-Gram Language Model - Training
Count N-grams from corpus and save model.
"""
import json
from urllib.request import urlopen
from rich.progress import track

ORDER = 8  # context length (ORDER=8 means 9-gram)
PAD = "^"  # padding character at start of sequence
END = "$"  # end of sequence marker

# Fetch corpus
url = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
with urlopen(url) as r:
    corpus = r.read().decode('utf-8')

# Split into lines (sentences)
lines = [line.strip() for line in corpus.split('\n') if line.strip()]

print(f"ORDER={ORDER}, lines={len(lines)}")

# Build count dict: count[ctx_string] = {char: count}
count = {}
for line in track(lines, description="Counting N-grams"):
    # Pad start and add end marker
    seq = PAD * ORDER + line + END
    for i in range(len(seq) - ORDER):
        ctx = seq[i:i+ORDER]
        next_char = seq[i+ORDER]
        if ctx not in count:
            count[ctx] = {}
        count[ctx][next_char] = count[ctx].get(next_char, 0) + 1

print(f"Unique contexts: {len(count)}")

# Save counts
with open("ngram_counts.json", "w") as f:
    json.dump(count, f, indent=2)

print("Counts saved to ngram_counts.json")
