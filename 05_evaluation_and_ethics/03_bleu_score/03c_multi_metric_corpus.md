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
6. At order 3 — Table 1's cross-entropy winner — sorts the 30 generated
   continuations by BERTScore and prints the 5 highest (cherries), 5
   near the median (apples), and 5 lowest (lemons), each with its prompt,
   generated candidate, and true reference.

## Reading the result

```
order  contexts  miss rate  cross-ent  perplexity    BLEU  ROUGE-L  METEOR  BERTScore
    2      1408      1.79%      3.009        8.05   0.005    0.023   0.013      0.201
    3     11347      4.66%      2.791        6.92   0.009    0.046   0.028      0.201
    4     48846     10.49%      3.082        8.47   0.009    0.052   0.026      0.199
    5    132958     20.65%      4.005       16.06   0.009    0.049   0.026      0.198
    6    261305     33.90%      5.394       42.05   0.009    0.050   0.032      0.189
    7    406576     48.13%      6.984      126.57   0.010    0.062   0.034      0.181
    8    548803     61.35%      8.517      366.28   0.009    0.055   0.027      0.164
```

Order 3 is still the cross-entropy winner, exactly as in Table 1 (same
code, same corpus, same split — the numbers match to three decimals).
But the generation-quality columns tell a different story than
cross-entropy did. BLEU, ROUGE-L, and METEOR are all close to zero at
every order and do not clearly favor order 3 over its neighbors —
40 characters of sampled generation rarely reproduces the same words as
the real continuation, at any order, because the n-gram model has no
notion of a sentence's overall meaning, only of what character usually
follows a short window of previous ones. BERTScore is the one column
with a clear trend, and it is not the trend cross-entropy showed: it is
essentially flat from order 2 through order 4, then declines steadily
through order 8. Free-running generation punishes a high-order model
harder than teacher-forced cross-entropy did, because once a high-order
model's own generated text drifts even slightly from anything it saw in
training, every later character is conditioned on a context that is now
partly synthetic and unfamiliar — a small early mistake compounds into a
worse one, over and over, for the rest of the 40 characters. Order 8's
first table (Table 1) already showed this model missing its context 61%
of the time on real held-out text; here that same weakness shows up as
generation quality that degrades the longer the model runs on its own
output. This mismatch between an easy-to-compute training signal
(teacher-forced cross-entropy) and the harder-to-improve thing you
actually want (good free-running generation) is a well-known failure
mode in sequence models called **exposure bias**.

The cherries, apples, and lemons at order 3 make the "generation quality
is genuinely low everywhere" point concrete: even the best-scoring
continuation ("he duke men and quin; novatier,\nLest\nMy ") is not real
English, just a sequence of English-shaped fragments; the worst-scoring
one ("his reath Tybalt true\nWhose\nUnless bushi") is further from the
reference but not obviously worse to a casual glance. Unlike Table 2's
cherries and lemons, which showed the model looking sharply better or
worse on different held-out blocks, here every block looks roughly
equally unconvincing — a reminder that a 3-character-order model was
never going to write real sentences, no matter which held-out text you
ask it to continue.

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
order 3, sort the sampled continuations by BERTScore and print the 5
highest, 5 near the median, and 5 lowest, each with its prompt,
generated candidate, and true reference."
