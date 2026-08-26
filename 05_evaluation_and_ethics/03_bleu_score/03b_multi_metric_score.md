# 03b: The same three candidates, scored by four different metrics

Concept: `03_bleu_score.py` showed BLEU getting fooled by one reference
sentence and three candidates. This demo repeats that exact grid-search
idea, scoring the same three candidates against the same reference with
four metrics side by side: BLEU, ROUGE-L, METEOR, and BERTScore. A single
metric can be fooled in a way that looks like a fluke; four metrics
agreeing (or disagreeing) on the same candidates is more informative than
any one of them alone.

None of these needed a new package install. `nltk` (already used for
BLEU) also ships METEOR. ROUGE-L is a longest-common-subsequence
computation short enough to write by hand instead of pulling in a
library for it. BERTScore is implemented directly from its published
algorithm — greedy cosine-similarity matching between contextual token
embeddings — using `transformers` and `torch`, which are already
installed in this course's environment for other lessons. This avoids
adding `rouge_score`, `bert_score`, and `evaluate` to a shared conda
environment used by every other module.

## What the demo does

1. Reuses `03_bleu_score.py`'s reference sentence and three candidates
   (exact match, good paraphrase with low word overlap, wrong final
   answer with high word overlap).
2. Scores every candidate four ways:
   - **BLEU**: n-gram precision (same code as `03_bleu_score.py`).
   - **ROUGE-L**: longest-common-subsequence F1 between reference and
     candidate words, computed with a small dynamic-programming table.
   - **METEOR**: `nltk`'s built-in `meteor_score`, which matches stems
     and synonyms instead of requiring exact word matches.
   - **BERTScore**: contextual token embeddings from a small pretrained
     transformer (`sentence-transformers/all-MiniLM-L6-v2`, loaded as a
     plain `transformers` model), matched greedily by cosine similarity
     to get precision, recall, and F1.
3. Prints one row per candidate with all four scores.

## Reading the result

```
candidate                          BLEU  ROUGE-L   METEOR  BERTScore
exact match                       1.000    1.000    1.000      1.000
good paraphrase, low overlap      0.009    0.115    0.091      0.682
wrong answer, high overlap        0.962    0.964    0.964      0.966
```

All four metrics agree on the ranking, and that agreement is itself the
finding: every one of them still scores the wrong-answer candidate higher
than the correct paraphrase. BERTScore is supposed to be the metric best
equipped to recognize a paraphrase, since it compares meaning-bearing
embeddings instead of exact words, and it does close much of the gap —
0.682 for the paraphrase versus BLEU's 0.009. But it still ranks the
factually wrong candidate (0.966) well above the correct one, because
changing "equals 0" to "equals 6" barely moves a sentence's embeddings,
while rewording the whole derivation in different terms moves them more,
even though the second change is the one that preserves the actual fact.
Being more semantic is not the same as being correct. This is the same
lesson as the BLEU-only demo, now shown to survive across four different
automatic metrics, not just one.

## Endpoint

No API calls. Downloads one small pretrained model
(`sentence-transformers/all-MiniLM-L6-v2`, used directly through
`transformers`, not the `sentence-transformers` package) from the
Hugging Face Hub on first run, and two small `nltk` corpora
(`wordnet`, `omw-1.4`) needed for METEOR.

## Regeneration prompt

If this needs to be regenerated, ask an LLM assistant: "Reuse the
reference sentence and three candidates from `03_bleu_score.py`. Score
each candidate against the reference with BLEU (`nltk`), ROUGE-L (hand-
written longest-common-subsequence F1), METEOR (`nltk`'s
`meteor_score`), and BERTScore (hand-written greedy cosine-similarity
matching over contextual token embeddings from a small pretrained
transformer, using the `transformers` package directly rather than
installing the `bert_score` or `evaluate` packages). Print one row per
candidate with all four scores."
