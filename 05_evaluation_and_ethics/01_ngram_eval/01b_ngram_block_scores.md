# 01b: A single average hides what individual blocks look like

Concept: `01_ngram_eval.py`'s table reports one cross-entropy number per
order, averaged over 723 held-out blocks. That number is real, but it is
also a fog. This demo un-averages it: it scores every held-out block on
its own, sorts the blocks by their individual cross-entropy, and prints
the 5 lowest-scoring (cherries), the 5 closest to the median (apples),
and the 5 highest-scoring (lemons) — with the actual text, not just a
number. Showing 5 of each, instead of just 1, is what reveals that
several blocks are exact duplicates.

This reuses `01_ngram_eval.py`'s exact training and probability logic,
applied to order 3, the best-performing order in the original table.
There is no "margin" here — cross-entropy is already an absolute score
for a single block, so sorting blocks by that score directly is enough.

## What the demo does

1. Trains the same order-3 model on the same held-out split as
   `01_ngram_eval.py`.
2. For every held-out block, computes that one block's own cross-entropy
   (bits per character), instead of only the corpus-wide average.
3. Sorts the blocks by cross-entropy and prints the 5 lowest, the 5
   closest to the median, and the 5 highest, each with its actual text.

## Reading the result

Three of the five cherries are exact duplicates: the held-out set
contains several blank-line-separated blocks that are nothing but
"PETRUCHIO:" and score identically. The same happens with "PROSPERO:"
among the lemons. Petruchio is a major, frequently-speaking character
elsewhere in the training data, so the trigrams that spell his name were
common; Prospero is a different character from a different play, and
several of the letter-to-letter transitions in his name fall back to the
floor probability. Packed into a block this short, those few misses
dominate the average and push the lemons' cross-entropy to over 11 bits
— roughly nine times the cherries', with a perplexity over 2,500. The
apples, all a full sentence or more with no bare names, sit much closer
to the corpus-wide average of 2.791 bits: most held-out text looks more
like the apples than either extreme. The lesson is not that short blocks
are bad; it is that a block's difficulty depends on exactly which
characters it contains, and a single average cannot show you that.

## Endpoint

No API. Downloads the same public-domain corpus `01_ngram_eval.py` uses
and scores it locally.

## Regeneration prompt

If this needs to be regenerated, ask an LLM assistant: "Reuse the training
and probability logic from `01_ngram_eval.py`, but instead of only
reporting the corpus-wide average cross-entropy, compute each held-out
block's own cross-entropy, sort the blocks by that score, and print the
5 lowest (cherries), 5 closest to the median (apples), and 5 highest
(lemons) blocks along with their actual text. Keep this to order 3."
