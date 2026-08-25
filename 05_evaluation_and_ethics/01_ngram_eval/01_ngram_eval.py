"""Demo: evaluating the module 3 n-gram model on text it never saw.

See 01_ngram_eval.md for the full explanation.
"""

import math
from urllib.request import urlopen

CORPUS_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
PAD = "^"  # padding character at the start of a sequence
END = "$"  # end-of-sequence marker
ORDERS = [2, 4, 8]  # context lengths to compare
HELD_OUT_FRACTION = 0.1  # last 10% of blocks are never trained on
FLOOR_PROBABILITY = 1e-4  # assigned when a context or character was never seen in training


def load_blocks() -> list[str]:
    with urlopen(CORPUS_URL) as response:
        text = response.read().decode("utf-8")
    return [block.strip() for block in text.split("\n\n") if block.strip()]


def train_counts(blocks: list[str], order: int) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for block in blocks:
        sequence = PAD * order + block + END
        for i in range(len(sequence) - order):
            context = sequence[i:i + order]
            next_char = sequence[i + order]
            counts.setdefault(context, {})
            counts[context][next_char] = counts[context].get(next_char, 0) + 1
    return counts


def probability(counts: dict[str, dict[str, int]], context: str, next_char: str) -> tuple[float, bool]:
    """Return (probability, was_a_miss). A miss means we fell back to the floor probability."""
    context_counts = counts.get(context)
    if not context_counts or next_char not in context_counts:
        return FLOOR_PROBABILITY, True
    total = sum(context_counts.values())
    return context_counts[next_char] / total, False


def evaluate(counts: dict[str, dict[str, int]], blocks: list[str], order: int) -> tuple[float, float]:
    """Return (cross-entropy in bits per character, miss rate) on held-out blocks."""
    total_bits = 0.0
    total_chars = 0
    misses = 0
    for block in blocks:
        sequence = PAD * order + block + END
        for i in range(len(sequence) - order):
            context = sequence[i:i + order]
            next_char = sequence[i + order]
            p, was_miss = probability(counts, context, next_char)
            total_bits += -math.log2(p)
            total_chars += 1
            misses += was_miss
    cross_entropy = total_bits / total_chars
    miss_rate = misses / total_chars
    return cross_entropy, miss_rate


blocks = load_blocks()
split = int(len(blocks) * (1 - HELD_OUT_FRACTION))
train_blocks, held_out_blocks = blocks[:split], blocks[split:]
print(f"{len(train_blocks)} training blocks, {len(held_out_blocks)} held-out blocks\n")

print(f"{'order':>5s} {'contexts':>9s} {'miss rate':>10s} {'cross-ent (bits) v':>19s} {'perplexity v':>13s}")
for order in ORDERS:
    counts = train_counts(train_blocks, order)
    cross_entropy, miss_rate = evaluate(counts, held_out_blocks, order)
    perplexity = 2 ** cross_entropy
    print(f"{order:5d} {len(counts):9d} {miss_rate:10.2%} {cross_entropy:19.3f} {perplexity:13.2f}")
