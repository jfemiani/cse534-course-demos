# 03: BLEU rewards word overlap, not correctness

Concept: BLEU is the oldest and most common automatic metric for scoring
generated text against a reference, borrowed from machine translation. It
counts overlapping n-grams (runs of consecutive words) between a candidate
and a reference. It has no idea what the words mean. This demo asks BLEU to
score three candidate answers against one reference and shows how badly
that surface-level counting can diverge from human judgment.

## What the demo does

1. Defines one reference sentence and three candidates: an exact match, a
   correct paraphrase that reuses almost none of the reference's wording,
   and a near-copy of the reference with a single factual error (the wrong
   room number).
2. Scores each candidate against the reference with `nltk`'s
   `sentence_bleu`, using a smoothing function (short sentences without
   smoothing often score exactly 0, which hides useful detail).

## Reading the result

The exact match scores 1.0, as expected. The good paraphrase, which a
person would call a correct answer, scores far lower, because BLEU cannot
recognize "stop by on Tuesday afternoons" as the same fact as "office hours
are Tuesdays." The factually wrong candidate scores far higher than the
correct paraphrase, because it reuses almost every word from the reference
and only changes the room number. BLEU cannot tell that this single change
makes the answer wrong. A metric like this can reward the wrong answer
over the right one, for the same reason a hit-rate number can hide a lemon:
the aggregate number looks clean, but it is not measuring what you actually
care about.

## The zoo of automatic metrics

BLEU is one entry in a much larger set of automatic metrics that show up
constantly in papers and benchmark leaderboards. A few of the most common:

- **BLEU** (this demo): n-gram precision against one or more references.
  Standard in machine translation; still reported for other generation
  tasks despite the paraphrase problem shown above.
- **ROUGE**: n-gram and longest-common-subsequence *recall* instead of
  precision. Standard for summarization, where the question is closer to
  "did the summary keep the important parts" than "did it use the exact
  same words."
- **METEOR**: like BLEU, but matches synonyms and word stems instead of
  requiring an exact string match, specifically to reduce the paraphrase
  problem this demo shows.
- **Exact match / F1**: standard for extractive question answering
  (e.g. the SQuAD benchmark), where the answer is a short span of text
  pulled directly from a document, not a free-form generated sentence.
- **BERTScore**: replaces word overlap with embedding similarity between
  candidate and reference tokens, so a correct paraphrase scores well
  instead of being penalized like it is here.
- **LLM-as-judge**: instead of a formula, a separate (usually stronger)
  model reads the candidate and reference and scores or ranks the answer.
  Closer to human judgment, at the cost of being slower, more expensive,
  and dependent on whichever model is doing the judging.

No single one of these is "the" right metric. Each trades off cost, speed,
and how closely it tracks what a human reader would actually say counts as
a good answer.

## Endpoint

No API. Uses `nltk.translate.bleu_score`, which ships with the `nltk`
package already installed in this course's environment.

## Regeneration prompt

If `nltk`'s BLEU API changes, ask an LLM assistant: "Update this script to
match the current `nltk.translate.bleu_score` API. Keep the same reference
sentence and the same three candidates (exact match, good paraphrase, wrong
room), and keep printing each candidate's BLEU score with smoothing
enabled."
