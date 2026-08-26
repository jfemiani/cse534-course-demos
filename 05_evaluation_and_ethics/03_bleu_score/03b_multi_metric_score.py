"""Demo: the grid-search table from 01_ngram_eval.py, repeated with BLEU,
ROUGE-L, METEOR, and BERTScore as columns instead of just cross-entropy.

See 03b_multi_metric_score.md for the full explanation.
Reuses the same reference sentence and three candidates as 03_bleu_score.py.
"""

import nltk
import torch
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
from nltk.translate.meteor_score import meteor_score
from transformers import AutoModel, AutoTokenizer

nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

# Real MT-Bench question 120 (math category) and its reference answer.
# Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena,"
# 2023. https://github.com/lm-sys/FastChat
REFERENCE = (
    "Substituting x equals 2 gives f(2) equals 4 times 2 cubed minus 9 "
    "times 2 minus 14, which equals 32 minus 18 minus 14, so f(2) equals 0."
)

CANDIDATES = {
    "exact match": REFERENCE,
    "good paraphrase, low overlap": (
        "When x is 2, the cubic term works out to 32, and subtracting 18 "
        "then 14 leaves nothing, so the function's output is zero."
    ),
    "wrong answer, high overlap": (
        "Substituting x equals 2 gives f(2) equals 4 times 2 cubed minus 9 "
        "times 2 minus 14, which equals 32 minus 18 minus 14, so f(2) equals 6."
    ),
}

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME).eval()


def bleu(reference, candidate):
    smoothing = SmoothingFunction().method1
    return sentence_bleu([reference.lower().split()], candidate.lower().split(), smoothing_function=smoothing)


def rouge_l(reference, candidate):
    """Longest-common-subsequence F1 between reference and candidate words."""
    ref_words, cand_words = reference.lower().split(), candidate.lower().split()
    dp = [[0] * (len(cand_words) + 1) for _ in range(len(ref_words) + 1)]
    for i, r in enumerate(ref_words, 1):
        for j, c in enumerate(cand_words, 1):
            dp[i][j] = dp[i - 1][j - 1] + 1 if r == c else max(dp[i - 1][j], dp[i][j - 1])
    lcs = dp[len(ref_words)][len(cand_words)]
    precision, recall = lcs / len(cand_words), lcs / len(ref_words)
    return 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)


def meteor(reference, candidate):
    return meteor_score([reference.lower().split()], candidate.lower().split())


def token_embeddings(text):
    """Contextual embedding for every real token in text (special tokens dropped)."""
    encoded = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        hidden = model(**encoded).last_hidden_state[0]
    mask = torch.tensor([tok not in tokenizer.all_special_ids for tok in encoded["input_ids"][0]])
    return torch.nn.functional.normalize(hidden[mask], dim=-1)


def bertscore(reference, candidate):
    """Hand-rolled BERTScore: greedy cosine-similarity matching, precision/recall/F1.

    This is the same idea as the `bert_score` package, computed directly from an
    already-installed transformer model instead of adding a new dependency.
    """
    ref_emb, cand_emb = token_embeddings(reference), token_embeddings(candidate)
    similarity = cand_emb @ ref_emb.T
    precision = similarity.max(dim=1).values.mean().item()
    recall = similarity.max(dim=0).values.mean().item()
    return 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)


print(f"{'candidate':30s} {'BLEU':>8s} {'ROUGE-L':>8s} {'METEOR':>8s} {'BERTScore':>10s}")
for label, candidate in CANDIDATES.items():
    scores = (bleu(REFERENCE, candidate), rouge_l(REFERENCE, candidate), meteor(REFERENCE, candidate), bertscore(REFERENCE, candidate))
    print(f"{label:30s} {scores[0]:8.3f} {scores[1]:8.3f} {scores[2]:8.3f} {scores[3]:10.3f}")
