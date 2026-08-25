"""Demo: Table 1's n-gram order sweep, extended with BLEU, ROUGE-L, METEOR,
and BERTScore computed over real held-out text, instead of three
hand-picked toy sentences.

See 03c_multi_metric_corpus.md for the full explanation.
Reuses the same corpus, split, and training logic as 01_ngram_eval.py.
"""

import math
import random
from collections import Counter
from urllib.request import urlopen

import nltk
import torch
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
from nltk.translate.meteor_score import meteor_score
from transformers import AutoModel, AutoTokenizer

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
RANDOM_SEED = 42

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME).eval()


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
    ref_words, cand_words = reference.lower().split(), candidate.lower().split()
    if not ref_words or not cand_words:
        return 0.0
    dp = [[0] * (len(cand_words) + 1) for _ in range(len(ref_words) + 1)]
    for i, r in enumerate(ref_words, 1):
        for j, c in enumerate(cand_words, 1):
            dp[i][j] = dp[i - 1][j - 1] + 1 if r == c else max(dp[i - 1][j], dp[i][j - 1])
    lcs = dp[len(ref_words)][len(cand_words)]
    precision, recall = lcs / len(cand_words), lcs / len(ref_words)
    return 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)


def meteor(reference: str, candidate: str) -> float:
    ref_tokens, cand_tokens = reference.lower().split(), candidate.lower().split()
    if not ref_tokens or not cand_tokens:
        return 0.0
    return meteor_score([ref_tokens], cand_tokens)


def token_embeddings(text: str) -> torch.Tensor | None:
    encoded = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        hidden = model(**encoded).last_hidden_state[0]
    mask = torch.tensor([tok not in tokenizer.all_special_ids for tok in encoded["input_ids"][0]])
    embeddings = hidden[mask]
    return torch.nn.functional.normalize(embeddings, dim=-1) if embeddings.shape[0] else None


def bertscore(reference: str, candidate: str) -> float:
    ref_emb, cand_emb = token_embeddings(reference), token_embeddings(candidate)
    if ref_emb is None or cand_emb is None:
        return 0.0
    similarity = cand_emb @ ref_emb.T
    precision = similarity.max(dim=1).values.mean().item()
    recall = similarity.max(dim=0).values.mean().item()
    return 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)


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
        per_block.append((s, prompt, candidate, reference))
    results_by_order[order] = per_block

    avg = lambda values: sum(values) / len(values)
    perplexity = 2 ** cross_entropy
    print(f"{order:5d} {len(counts):9d} {miss_rate:10.2%} {cross_entropy:10.3f} {perplexity:11.2f} "
          f"{avg(bleu_scores):7.3f} {avg(rouge_scores):8.3f} {avg(meteor_scores):7.3f} {avg(bert_scores):10.3f}")

per_block = sorted(results_by_order[BEST_ORDER], key=lambda item: item[0])
lemons, apples, cherries = per_block[:GROUP_SIZE], per_block[len(per_block) // 2 - GROUP_SIZE // 2:len(per_block) // 2 - GROUP_SIZE // 2 + GROUP_SIZE], per_block[-GROUP_SIZE:]

print(f"\norder={BEST_ORDER} generated continuations, sorted by BERTScore (higher is better)\n")
for label, group in [("CHERRIES (highest BERTScore)", cherries), ("APPLES (median)", apples), ("LEMONS (lowest BERTScore)", lemons)]:
    print(f"--- {label} ---")
    for score, prompt, candidate, reference in group:
        print(f"BERTScore: {score:.3f}")
        print(f"  prompt:     {prompt!r}")
        print(f"  candidate:  {candidate!r}")
        print(f"  reference:  {reference!r}")
    print()
