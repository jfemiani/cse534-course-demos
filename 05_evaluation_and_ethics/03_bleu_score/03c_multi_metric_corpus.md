# 03c: Table 1's order sweep, extended with generation-quality metrics over real corpus text

Concept: `03b_multi_metric_score.py` scored BLEU, ROUGE-L, METEOR, and
BERTScore on three hand-picked toy sentences. That is useful for seeing
how the four metrics disagree, but it says nothing about the n-gram
model this page actually built. This demo asks the more useful question:
does the order that wins on cross-entropy (`01_ngram_eval.py`'s Table 1,
order 3) also produce the best *generated* text, judged by the same four
metrics, over real held-out corpus text instead of three sentences?

Cross-entropy and BLEU/ROUGE/METEOR/BERTScore measure genuinely different
things. Cross-entropy is a **teacher-forced** measurement: at every
position, the model is shown the true preceding characters and asked
only "how surprised are you by the next one?" It never has to live with
its own mistakes. BLEU/ROUGE/METEOR/BERTScore need something the model
actually *generated* to compare against a reference, which means
**free-running generation**: the model predicts one character, that
character becomes part of the context for the next prediction, and so
on for many steps. A model can be excellent at the first job and much
worse at the second, because small next-character errors compound over
a full generated passage in a way a single-step cross-entropy number
never has to account for.

## What the demo does

1. Reuses `01_ngram_eval.py`'s exact corpus, training/held-out split, and
   cross-entropy measurement, so the cross-entropy and perplexity
   columns are directly comparable to Table 1.
2. For each held-out block long enough to use, splits it into roughly a
   20-character prompt and the roughly-40 real characters that follow
   it (the reference continuation), snapping both cuts out to the
   nearest word boundary so neither one ends mid-word.
3. Samples 30 of these blocks once, with a fixed random seed, so every
   order is evaluated on the exact same prompts.
4. For each order, trains fresh n-gram counts (identical to
   `01_ngram_eval.py`), then for every sampled block: generates a
   continuation, matched to the same length as that block's snapped
   reference, by sampling character-by-character from the trained
   distribution (falling back to the single most common training
   character on an unseen context), and scores that generated
   continuation against the real continuation with BLEU, ROUGE-L,
   METEOR, and BERTScore.
5. Averages all four metrics per order, printed alongside the same
   cross-entropy and perplexity Table 1 already reported.
6. At order 3 (the cross-entropy winner) and again at order 7 (the
   BERTScore winner), sorts the 30 generated continuations by
   BERTScore and prints the 5 highest (cherries), 5 near the median
   (apples), and 5 lowest (lemons), each with its prompt, generated
   candidate, true reference, and BERTScore.

## Reading the result

```
order  contexts  miss rate  cross-ent  perplexity    BLEU  ROUGE-L  METEOR  BERTScore
    2      1408      1.79%      3.009        8.05   0.006    0.034   0.019      0.170
    3     11347      4.66%      2.791        6.92   0.011    0.057   0.038      0.191
    4     48846     10.49%      3.082        8.47   0.006    0.038   0.032      0.169
    5    132958     20.65%      4.005       16.06   0.007    0.037   0.027      0.181
    6    261305     33.90%      5.394       42.05   0.006    0.039   0.017      0.175
    7    406576     48.13%      6.984      126.57   0.007    0.051   0.029      0.205
    8    548803     61.35%      8.517      366.28   0.005    0.024   0.012      0.135
```

Order 3 is still the cross-entropy winner, exactly as in Table 1 (same
code, same corpus, same split — the numbers match to three decimals),
and this time BLEU, ROUGE-L, and METEOR agree with it too. That is a
change from an earlier version of this demo, which split the prompt
and reference at a fixed character count with no regard for word
boundaries: cutting either one off mid-word starved every word-overlap
metric of anything to actually match, producing noisy, nearly-flat
scores that made a higher order look like the word-overlap winner by
coincidence. Snapping both cuts to the nearest word boundary gives
BLEU/ROUGE-L/METEOR a fair comparison, and once they get one, they
side with cross-entropy. The one metric that still disagrees is
BERTScore, which peaks at order 7 instead. BERTScore compares sentence
embeddings rather than counting matching words, so a continuation can
score well by reading as similar in meaning or structure to the
reference even without sharing its words. A higher-order model has
memorized longer verbatim stretches of the training text, so on the
sampled blocks where it still has a matching context to draw from, it
can produce a passage that reads as more plausible English than a
lower-order model's output.

Sorting order 3's and order 7's own continuations by BERTScore shows
that pattern directly, alongside the failure mode it trades for.
Order 7's best row (BERTScore 0.471) genuinely reads as more coherent
English than order 3's own best row (0.283). But three of order 7's
five lowest-scoring rows are not generated text at all — order 7's 48%
miss rate (see Table 1) means the model runs out of a matching context
partway through and falls back to repeating a single filler character
for the rest of the continuation. Order 3 never produces a blank row
in this sample; even its worst case (BERTScore 0.117) is still real,
if unconvincing, character-by-character output. A higher order can win
on embedding similarity when it has enough training data to draw on
for a given prompt, but it fails outright, not just badly, whenever it
does not.

## Endpoint

No API calls. Downloads the public corpus and one small pretrained
model (`sentence-transformers/all-MiniLM-L6-v2`, used directly through
`transformers`) from the Hugging Face Hub on first run, plus two small
`nltk` corpora (`wordnet`, `omw-1.4`) for METEOR.

## Regeneration prompt

If this needs to be regenerated, ask an LLM assistant: "Reuse
`01_ngram_eval.py`'s corpus, train/held-out split, training, and
cross-entropy logic. For each order, on a fixed random sample of
held-out blocks long enough to split into roughly a 20-character
prompt and a roughly-40-character reference continuation (each cut
snapped out to the nearest word boundary so neither one ends mid-word),
generate a continuation matched to the reference's exact length by
sampling character-by-character from the trained n-gram distribution
(falling back to the single most common training character on an
unseen context), and score it against the reference with BLEU,
ROUGE-L, METEOR, and BERTScore (reusing the hand-written
implementations from `03b_multi_metric_score.py`). Print the average of
all four metrics per order alongside cross-entropy and perplexity. At
order 3 (the cross-entropy winner) and at order 7 (the BERTScore
winner), sort that order's own sampled continuations by BERTScore and
print the 5 highest, 5 near the median, and 5 lowest, each with its
prompt, generated candidate, true reference, and BERTScore."
