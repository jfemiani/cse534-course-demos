# 01b: A single average hides what individual blocks look like

Concept: `01_ngram_eval.py`'s table reports one cross-entropy number per
order, averaged over 723 held-out blocks. That number is real, but it is
also a fog. This demo un-averages it: it scores every held-out block on
its own, sorts the blocks by their individual cross-entropy, and prints
the lowest (cherry), the middle (apple), and the highest (lemon) — with
the actual text, not just a number.

This reuses `01_ngram_eval.py`'s exact training and probability logic,
applied to order 8, the order whose *average* cross-entropy was worst in
the original table. Unlike the retrieval demo's cherries/apples/lemons
(`02b_retrieval_eval_examples.py`), there is no "margin" here — cross-
entropy is already an absolute score for a single block, so sorting
blocks by that score directly is enough.

## What the demo does

1. Trains the same order-8 model on the same held-out split as
   `01_ngram_eval.py`.
2. For every held-out block, computes that one block's own cross-entropy
   (bits per character), instead of only the corpus-wide average.
3. Sorts the blocks by cross-entropy and prints the lowest, the median,
   and the highest, each with its actual text.

## Reading the result

The cherry is a short, formulaic line of dialogue ("PETRUCHIO: What is
his name?") built almost entirely out of common two-to-eight-character
sequences the model saw constantly during training — this is the order-8
model at its best, and it looks nothing like the corpus-wide average.
The apple is a longer, less formulaic sentence, and its cross-entropy is
already far higher: most real text is closer to the apple than the
cherry. The lemon is a short line too, but it names "Dido," a proper noun
the model's training data barely uses in this context; the model has to
fall back to the floor probability again and again inside those eight
characters, and the resulting cross-entropy is more than ten times the
cherry's. This is the same "expensive wrong guess" mechanism `01_ngram_eval.py`'s
table already named — a rare token inside a long context — but seeing the
actual sentence makes it concrete instead of abstract: the failure is not
a statistical artifact, it is one specific name the model had barely seen.

## Endpoint

No API. Downloads the same public-domain corpus `01_ngram_eval.py` uses
and scores it locally.

## Regeneration prompt

If this needs to be regenerated, ask an LLM assistant: "Reuse the training
and probability logic from `01_ngram_eval.py`, but instead of only
reporting the corpus-wide average cross-entropy, compute each held-out
block's own cross-entropy, sort the blocks by that score, and print the
lowest (cherry), median (apple), and highest (lemon) block along with
its actual text. Keep this to order 8."
