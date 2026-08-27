# 01: An RNN encoder-decoder, translating English to French

Concept: a recurrent neural network keeps a hidden state that updates at
every input step, instead of the fixed-size window a Module 3 n-gram model
uses. This is the module's baseline architecture -- read this file before
`04_lstm_mt.py` and `05_transformer_mt.py`, since both of those are written
as direct, minimal-diff comparisons against this one.

## What the demo does

1. Builds a shared English-French dataset from `Helsinki-NLP/opus-100`
   (see `../mt_data.py`), filtered to short sentence pairs so training
   finishes in a few minutes on a laptop CPU.
2. Trains an encoder (`nn.RNN`) and a decoder (`nn.RNN`) end to end: the
   encoder reads the whole English sentence and produces a single fixed-size
   hidden vector; the decoder starts from that one vector and generates the
   French sentence one word at a time.
3. Tracks validation loss every epoch and keeps the checkpoint with the
   lowest validation loss, the same idea Module 5 used to pick the best
   n-gram order instead of just training as long as possible.
4. Reports two kinds of evidence on five fixed evaluation sentences (the
   same five sentences `04_lstm_mt.py` and `05_transformer_mt.py` use):
   the model's own greedy-decoded guess, and a **reference loss** --
   how surprised the model is by the *correct* French translation, even
   when its own guess is wrong. Reference loss is the fairer comparison
   across sentences, since it does not depend on the model happening to
   guess the right words.

## Why this is worth reading closely

The encoder's entire understanding of the source sentence has to survive
being squeezed into one fixed-size vector before the decoder ever sees it.
Look at the reference-loss column across the five evaluation sentences: the
model is generally less surprised by short, common sentences and more
surprised by the longest one -- there simply isn't room in that one vector
to preserve everything a long sentence needs. `04_lstm_mt.py` changes
exactly one thing (the cell type) and the same evaluation improves.

## Honest caveats (read before treating any single number as gospel)

- This is a from-scratch, word-level model trained on a few thousand noisy,
  subtitle-derived sentence pairs -- not a production translator. Some
  individual greedy translations will be wrong or nonsensical; that is
  expected at this scale.
- Reference loss on a *single* sentence is noisy: an idiomatic phrase (e.g.
  "Here it is" → "Le voilà", a big surface-form jump) can score worse than a
  longer but more literal sentence. The clean, reliable comparison is the
  **average validation loss** reported each epoch -- not any one sentence in
  isolation. This is the same lesson Module 5 taught with cherries/apples/
  lemons: an averaged number and an individual example can disagree.
