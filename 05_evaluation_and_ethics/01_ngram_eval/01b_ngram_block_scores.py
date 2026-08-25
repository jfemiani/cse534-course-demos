"""Demo: a single average hides what individual blocks of text actually look like.

See 01b_ngram_block_scores.md for the full explanation.
"""

import math
from urllib.request import urlopen

CORPUS_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
PAD = "^"
END = "$"
ORDER = 8  # the order that struggled most in 01_ngram_eval.py's table
HELD_OUT_FRACTION = 0.1
FLOOR_PROBABILITY = 1e-4
PREVIEW_CHARS = 160  # how much of each block to print


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


def probability(counts: dict[str, dict[str, int]], context: str, next_char: str) -> float:
    context_counts = counts.get(context)
    if not context_counts or next_char not in context_counts:
        return FLOOR_PROBABILITY
    total = sum(context_counts.values())
    return context_counts[next_char] / total


def block_cross_entropy(counts: dict[str, dict[str, int]], block: str, order: int) -> float:
    """Cross-entropy in bits per character for this one block, not averaged with any other block."""
    sequence = PAD * order + block + END
    total_bits = 0.0
    total_chars = 0
    for i in range(len(sequence) - order):
        context = sequence[i:i + order]
        next_char = sequence[i + order]
        total_bits += -math.log2(probability(counts, context, next_char))
        total_chars += 1
    return total_bits / total_chars


blocks = load_blocks()
split = int(len(blocks) * (1 - HELD_OUT_FRACTION))
train_blocks, held_out_blocks = blocks[:split], blocks[split:]
counts = train_counts(train_blocks, ORDER)

scored_blocks = [(block_cross_entropy(counts, block, ORDER), block) for block in held_out_blocks]
scored_blocks.sort(key=lambda item: item[0])

cherry = scored_blocks[0]
apple = scored_blocks[len(scored_blocks) // 2]
lemon = scored_blocks[-1]

print(f"order={ORDER}, {len(held_out_blocks)} held-out blocks\n")
for label, (cross_entropy, block) in [("CHERRY (lowest)", cherry), ("APPLE (median)", apple), ("LEMON (highest)", lemon)]:
    preview = block[:PREVIEW_CHARS].replace("\n", " ")
    print(f"--- {label} ---")
    print(f"cross-entropy: {cross_entropy:.3f} bits/char   perplexity: {2 ** cross_entropy:.2f}")
    print(f"text: {preview!r}{'...' if len(block) > PREVIEW_CHARS else ''}")
    print()
