"""Demo: BLEU rewards word overlap, not correctness. Watch it get fooled.

See 03_bleu_score.md for the full explanation.
Compare with 04_llm_judge.py, which asks a model to judge a quality BLEU
can't score at all: whether an explanation actually reads as simple enough
for a five-year-old, where there is no reference wording to count overlap
against.
"""

from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu

# Real MT-Bench question 120 (math category) and its reference answer,
# worked out in full sentences. Zheng et al., "Judging LLM-as-a-Judge with
# MT-Bench and Chatbot Arena," 2023. https://github.com/lm-sys/FastChat
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

reference_tokens = REFERENCE.lower().split()
smoothing = SmoothingFunction().method1

for label, candidate in CANDIDATES.items():
    candidate_tokens = candidate.lower().split()
    score = sentence_bleu([reference_tokens], candidate_tokens, smoothing_function=smoothing)
    print(f"{label:30s} BLEU={score:.3f}  {candidate!r}")
