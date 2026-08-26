"""Demo: Table 1's n-gram order sweep, scored with BLEU, ROUGE-L, METEOR,
and BERTScore (via nltk, rouge-score, and bert-score) over generated
continuations of real held-out text. Also prints, for orders 3 and 7
separately, the generated continuations sorted by ROUGE-L.

See 03c_multi_metric_corpus.md for the full explanation.
Reuses the same corpus, split, and training logic as 01_ngram_eval.py.
"""

import math
import random
from collections import Counter
from urllib.request import urlopen

import nltk
from bert_score import BERTScorer
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
from nltk.translate.meteor_score import meteor_score
from rouge_score import rouge_scorer

nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

CORPUS_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
PAD = "^"
END = "$"
ORDERS = [2, 3, 4, 5, 6, 7, 8]
HELD_OUT_FRACTION = 0.1
FLOOR_PROBABILITY = 1e-4
PROMPT_CHARS = 20  # characters of real held-out text used to seed generation
CONTINUATION_CHARS = 40  # characters generated, and compared to the true continuation
SAMPLE_SIZE = 30  # held-out blocks sampled for the generation metrics (BERTScore is not free)
GROUP_SIZE = 5
BEST_ORDER = 3  # the order Table 1 already found best by cross-entropy
WORD_OVERLAP_ORDER = 7  # the order that wins on BLEU/ROUGE-L/METEOR despite worse perplexity
RANDOM_SEED = 42

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
rouge = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
bert_scorer = BERTScorer(model_type=MODEL_NAME, num_layers=6, lang="en", rescale_with_baseline=False)


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


def evaluate(counts: dict[str, dict[str, int]], blocks: list[str], order: int) -> tuple[float, float]:
    """Cross-entropy (bits/char) and miss rate over blocks — same measurement as 01_ngram_eval.py."""
    total_bits = 0.0
    total_chars = 0
    misses = 0
    for block in blocks:
        sequence = PAD * order + block + END
        for i in range(len(sequence) - order):
            context = sequence[i:i + order]
            next_char = sequence[i + order]
            context_counts = counts.get(context)
            if not context_counts or next_char not in context_counts:
                p, miss = FLOOR_PROBABILITY, True
            else:
                p, miss = context_counts[next_char] / sum(context_counts.values()), False
            total_bits += -math.log2(p)
            total_chars += 1
            misses += miss
    return total_bits / total_chars, misses / total_chars


def generate(counts: dict[str, dict[str, int]], order: int, prompt: str, length: int, fallback_char: str) -> str:
    """Generate `length` characters after `prompt`, sampling from the trained distribution."""
    text = PAD * order + prompt
    generated = []
    for _ in range(length):
        context_counts = counts.get(text[-order:])
        if context_counts:
            chars, weights = zip(*context_counts.items())
            next_char = random.choices(chars, weights=weights)[0]
        else:
            next_char = fallback_char
        generated.append(next_char)
        text += next_char
    return "".join(generated)


def bleu(reference: str, candidate: str) -> float:
    ref_tokens, cand_tokens = reference.lower().split(), candidate.lower().split()
    if not cand_tokens:
        return 0.0
    return sentence_bleu([ref_tokens], cand_tokens, smoothing_function=SmoothingFunction().method1)


def rouge_l(reference: str, candidate: str) -> float:
    return rouge.score(reference, candidate)["rougeL"].fmeasure


def meteor(reference: str, candidate: str) -> float:
    ref_tokens, cand_tokens = reference.lower().split(), candidate.lower().split()
    if not ref_tokens or not cand_tokens:
        return 0.0
    return meteor_score([ref_tokens], cand_tokens)


def bertscore(reference: str, candidate: str) -> float:
    _, _, f1 = bert_scorer.score([candidate], [reference])
    return f1.item()


blocks = load_blocks()
split = int(len(blocks) * (1 - HELD_OUT_FRACTION))
train_blocks, held_out_blocks = blocks[:split], blocks[split:]

min_length = PROMPT_CHARS + CONTINUATION_CHARS
eligible_blocks = [block for block in held_out_blocks if len(block) >= min_length]
random.seed(RANDOM_SEED)
sample_blocks = random.sample(eligible_blocks, SAMPLE_SIZE)
fallback_char = Counter("".join(train_blocks)).most_common(1)[0][0]

print(f"{len(train_blocks)} training blocks, {len(held_out_blocks)} held-out blocks, "
      f"{len(eligible_blocks)} long enough to generate from, sampling {SAMPLE_SIZE}\n")

results_by_order: dict[int, list[tuple[float, str, str, str]]] = {}
print(f"{'order':>5s} {'contexts':>9s} {'miss rate':>10s} {'cross-ent':>10s} {'perplexity':>11s} "
      f"{'BLEU':>7s} {'ROUGE-L':>8s} {'METEOR':>7s} {'BERTScore':>10s}")
for order in ORDERS:
    counts = train_counts(train_blocks, order)
    cross_entropy, miss_rate = evaluate(counts, held_out_blocks, order)

    bleu_scores, rouge_scores, meteor_scores, bert_scores = [], [], [], []
    per_block = []
    for block in sample_blocks:
        prompt, reference = block[:PROMPT_CHARS], block[PROMPT_CHARS:PROMPT_CHARS + CONTINUATION_CHARS]
        candidate = generate(counts, order, prompt, CONTINUATION_CHARS, fallback_char)
        b, r, m, s = bleu(reference, candidate), rouge_l(reference, candidate), meteor(reference, candidate), bertscore(reference, candidate)
        bleu_scores.append(b), rouge_scores.append(r), meteor_scores.append(m), bert_scores.append(s)
        per_block.append((r, s, prompt, candidate, reference))
    results_by_order[order] = per_block

    avg = lambda values: sum(values) / len(values)
    perplexity = 2 ** cross_entropy
    print(f"{order:5d} {len(counts):9d} {miss_rate:10.2%} {cross_entropy:10.3f} {perplexity:11.2f} "
          f"{avg(bleu_scores):7.3f} {avg(rouge_scores):8.3f} {avg(meteor_scores):7.3f} {avg(bert_scores):10.3f}")

for order in (BEST_ORDER, WORD_OVERLAP_ORDER):
    per_block = sorted(results_by_order[order], key=lambda item: item[0])
    lemons, apples, cherries = per_block[:GROUP_SIZE], per_block[len(per_block) // 2 - GROUP_SIZE // 2:len(per_block) // 2 - GROUP_SIZE // 2 + GROUP_SIZE], per_block[-GROUP_SIZE:]

    print(f"\norder={order} generated continuations, sorted by ROUGE-L (higher is better)\n")
    for label, group in [("CHERRIES (highest ROUGE-L)", cherries), ("APPLES (median)", apples), ("LEMONS (lowest ROUGE-L)", lemons)]:
        print(f"--- {label} ---")
        for rouge_score, bert_score, prompt, candidate, reference in group:
            print(f"ROUGE-L: {rouge_score:.3f}  BERTScore: {bert_score:.3f}")
            print(f"  prompt:     {prompt!r}")
            print(f"  candidate:  {candidate!r}")
            print(f"  reference:  {reference!r}")
        print()
