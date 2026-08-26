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
2. For each held-out block long enough to use (at least 60 characters),
   splits it into a 20-character prompt and the 40 real characters that
   actually follow it (the reference continuation).
3. Samples 30 of these blocks once, with a fixed random seed, so every
   order is evaluated on the exact same prompts.
4. For each order, trains fresh n-gram counts (identical to
   `01_ngram_eval.py`), then for every sampled block: generates a
   40-character continuation by sampling character-by-character from
   the trained distribution (falling back to the single most common
   training character on an unseen context), and scores that generated
   continuation against the real continuation with BLEU, ROUGE-L,
   METEOR, and BERTScore.
5. Averages all four metrics per order, printed alongside the same
   cross-entropy and perplexity Table 1 already reported.
6. At order 3 (the cross-entropy winner) and again at order 7 (the
   BLEU/ROUGE-L/METEOR winner), sorts the 30 generated continuations by
   ROUGE-L and prints the 5 highest (cherries), 5 near the median
   (apples), and 5 lowest (lemons), each with its prompt, generated
   candidate, true reference, and ROUGE-L score.

## Reading the result

```
order  contexts  miss rate  cross-ent  perplexity    BLEU  ROUGE-L  METEOR  BERTScore
    2      1408      1.79%      3.009        8.05   0.005    0.027   0.013      0.203
    3     11347      4.66%      2.791        6.92   0.009    0.045   0.028      0.205
    4     48846     10.49%      3.082        8.47   0.009    0.060   0.026      0.202
    5    132958     20.65%      4.005       16.06   0.009    0.068   0.026      0.201
    6    261305     33.90%      5.394       42.05   0.009    0.057   0.032      0.192
    7    406576     48.13%      6.984      126.57   0.010    0.073   0.034      0.184
    8    548803     61.35%      8.517      366.28   0.009    0.063   0.027      0.166
```

Order 3 is still the cross-entropy winner, exactly as in Table 1 (same
code, same corpus, same split — the numbers match to three decimals).
But BLEU, ROUGE-L, and METEOR all peak at order 7 instead, the same
order whose perplexity was nearly the worst in the entire sweep.
BERTScore nominally still favors order 3, but every value in that
column sits in a narrow band (0.166 to 0.205), tight enough that a
single win there is easy to mistake for signal when it may just be
noise — and both the prompt and the reference are cut off mid-word
rather than at a sentence boundary, so BERTScore is comparing two
fragments neither of which looks like anything in BERT's own training
data. The contrast worth taking seriously is order 3 (the
cross-entropy winner) against order 7 (the word-overlap winner). A
likely reason for order 7's win is exposure bias, a known limitation of
sequence models: cross-entropy tests the model on the true previous
characters at every step, but generating text lets the model's own
output feed into its own next prediction, and a higher-order model has
memorized long enough verbatim stretches of training text that it can
occasionally reproduce a run of words overlapping the reference by
chance, even while the passage as a whole stays nonsense.

Sorting order 3's and order 7's own continuations by ROUGE-L shows what
that word-overlap win actually looks like as text. Order 7's best row
genuinely reuses a real phrase from training almost verbatim ("loves a
caitiff wretched Clarence") — that is where its higher ROUGE-L average
comes from. But several of order 7's apples and lemons are not
generated text at all: order 7's 48% miss rate (see Table 1) means the
model runs out of a matching context partway through and falls back to
repeating a single filler character for the rest of the continuation.
Order 3's own best row tops out at a ROUGE-L of only 0.190 and is not
real English either. Word overlap can go up either by getting luckier
at reusing a memorized phrase, or by failing outright and producing
filler that happens to share zero words with anything — neither is
"better writing."

## Endpoint

No API calls. Downloads the public corpus and one small pretrained
model (`sentence-transformers/all-MiniLM-L6-v2`, used directly through
`transformers`) from the Hugging Face Hub on first run, plus two small
`nltk` corpora (`wordnet`, `omw-1.4`) for METEOR.

## Regeneration prompt

If this needs to be regenerated, ask an LLM assistant: "Reuse
`01_ngram_eval.py`'s corpus, train/held-out split, training, and
cross-entropy logic. For each order, on a fixed random sample of
held-out blocks long enough to split into a 20-character prompt and a
40-character reference continuation, generate a 40-character
continuation by sampling character-by-character from the trained
n-gram distribution (falling back to the single most common training
character on an unseen context), and score it against the reference
with BLEU, ROUGE-L, METEOR, and BERTScore (reusing the hand-written
implementations from `03b_multi_metric_score.py`). Print the average of
all four metrics per order alongside cross-entropy and perplexity. At
order 3 (the cross-entropy winner) and at order 7 (the BLEU/ROUGE-L/
METEOR winner), sort that order's own sampled continuations by ROUGE-L
and print the 5 highest, 5 near the median, and 5 lowest, each with its
prompt, generated candidate, true reference, and ROUGE-L score."
