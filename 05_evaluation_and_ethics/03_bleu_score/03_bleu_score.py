"""Demo: BLEU rewards word overlap, not correctness. Watch it get fooled.

See 03_bleu_score.md for the full explanation.
"""

from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu

REFERENCE = "Office hours are Tuesdays from 2 to 4 pm in Laws Hall room 205."

CANDIDATES = {
    "exact match": "Office hours are Tuesdays from 2 to 4 pm in Laws Hall room 205.",
    "good paraphrase, low overlap": "You can stop by on Tuesday afternoons between 2 and 4 in Laws Hall 205.",
    "wrong room, high overlap": "Office hours are Tuesdays from 2 to 4 pm in Laws Hall room 305.",
}

reference_tokens = REFERENCE.lower().split()
smoothing = SmoothingFunction().method1

for label, candidate in CANDIDATES.items():
    candidate_tokens = candidate.lower().split()
    score = sentence_bleu([reference_tokens], candidate_tokens, smoothing_function=smoothing)
    print(f"{label:30s} BLEU={score:.3f}  {candidate!r}")
