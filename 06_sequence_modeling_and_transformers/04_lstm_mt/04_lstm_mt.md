# 02: An LSTM encoder-decoder, same task, same data, one line changed

Concept: gating. Compare this file line-by-line against `03_rnn_mt.py` --
the data pipeline, the training loop, the evaluation sentences, and even
the validation-based checkpoint selection are identical. The only change is
`nn.RNN` → `nn.LSTM`, which adds a separate cell state that travels
alongside the hidden state and is protected by learned forget/input/output
gates.

## What the demo does

Exactly what `03_rnn_mt.py` does, with one architectural change. See that
file's `.md` for the full explanation of the data pipeline, the training
loop, and why reference loss (not just the greedy guess) is reported.

## Why this is worth reading closely

Gating does not remove the fixed-size bottleneck -- the decoder still
starts from a single vector the encoder hands it. What changes is that the
network can now learn *what's worth protecting* inside that vector instead
of being forced to overwrite everything at every step. Compare this file's
final validation loss and its reference-loss numbers directly against
`03_rnn_mt.output.txt`: every one of the five evaluation sentences scores a
lower (better) reference loss here, including the deliberately long one --
the same task, same data, one architectural change.

## Honest caveats

Same caveats as `03_rnn_mt.md` apply: this is a small, from-scratch model on
noisy data, not a production translator, and any single sentence's
reference loss is noisier evidence than the averaged validation loss.
