# 01: Evaluating the n-gram model on held-out text

Concept: cross-entropy and perplexity measured on text the model never
trained on, swept across a few different context lengths (the model's
"order"). This is also the course's first concrete grid search: order is
the one setting being varied, and the results table shows the tradeoff
between it.

Compare with `01b_ngram_block_scores.py`, which un-averages this table's
cross-entropy down to individual blocks of held-out text.

## What the demo does

1. Downloads the same Tiny Shakespeare corpus as
   `03_mathematical_foundations/07_ngram/07_ngram_train.py`, split into blocks
   on blank lines.
2. Holds out the last 10% of blocks. The model never sees these while
   training.
3. For each order in {2, 4, 8}, counts n-grams on the training blocks only,
   then walks through the held-out blocks computing the cross-entropy
   (in bits per character) of the real next character under the trained
   counts.
4. Converts that cross-entropy to perplexity using perplexity = 2^(cross-entropy in bits).
   This demo always uses base-2 logarithms and this exact formula; a
   model using natural logarithms (nats) would instead use perplexity =
   e^(cross-entropy in nats). Either convention is standard; state which
   one you used any time you report a perplexity number.
5. When a held-out context was never seen in training, or the actual next
   character was never seen following that context, the demo falls back to
   a small floor probability (`FLOOR_PROBABILITY`) instead of dividing by
   zero. The demo also reports the miss rate: how often that fallback fired.

## Why this is worth reading closely

A short context (order 2) has seen almost every possible context by the
time training ends, so its miss rate on new text stays low. A long context
(order 8) is very confident whenever it has seen the exact 8-character
context before, but most 8-character contexts in new text were never seen
during training, so the miss rate climbs and the model's high confidence
in the wrong direction gets punished hard by cross-entropy. This is the
same "surprise" idea from lesson 3.4, applied to a whole model instead of
one outcome.

## Endpoint

None. This demo makes no API calls; it downloads a public text file and
does the counting locally.

## Regeneration prompt

If the corpus URL stops working, ask an LLM assistant: "Update
`CORPUS_URL` in this script to point at a working plain-text copy of the
Tiny Shakespeare dataset (or a similarly sized public-domain text corpus),
keeping the block-splitting, train/held-out split, and cross-entropy and
perplexity calculations unchanged."
