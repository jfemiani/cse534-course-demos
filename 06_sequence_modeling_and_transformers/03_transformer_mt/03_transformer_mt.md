# 03: A Transformer encoder-decoder, same task, same data, attention instead of recurrence

Concept: attention removes the fixed-size bottleneck entirely. Same corpus,
same evaluation sentences, same validation-based checkpoint selection as
`01_rnn_mt.py` and `02_lstm_mt.py` -- but there is no hidden state carried
step by step anymore. At every decoding step, the decoder computes a fresh
weighted lookup over *every* encoder output position, using the same
dot-product/cosine-similarity idea already used for retrieval in Module 4,
now learned end to end instead of computed against a fixed embedding.

## What the demo does

1. Uses the identical `mt_data.py` pipeline as the RNN/LSTM demos.
2. Encoder: PyTorch's built-in `nn.TransformerEncoderLayer` (self-attention
   only -- every source word can look at every other source word in one
   pass, with no recurrence).
3. Decoder: assembled from PyTorch's built-in `nn.MultiheadAttention`
   blocks -- causal self-attention over the target so far, then
   cross-attention over the encoder's output, then a feedforward layer.
   This is deliberately built from `nn.MultiheadAttention` directly rather
   than `nn.TransformerDecoderLayer`, only so the cross-attention weights
   are easy to pull out for the visualization below. The attention math
   itself is entirely PyTorch's; nothing here is hand-rolled.
4. A learned positional embedding is added to each token embedding, since
   removing recurrence also removes the model's only built-in sense of word
   order.
5. After training, prints which source word each output word's
   cross-attention weight points at most strongly, for the deliberately
   long evaluation sentence.

## Why this is worth reading closely

Look at the final validation loss compared to `01_rnn_mt.output.txt` and
`02_lstm_mt.output.txt`: it keeps improving, RNN → LSTM → Transformer, with
no architecture-specific bottleneck vector left at all. Then look at the
attention printout: each output word is attending to a *specific* source
word, not a single compressed summary of the whole sentence. This won't be
perfectly aligned (this is still a tiny, quickly-trained model), but the
mechanism -- a fresh, learned weighted lookup at every step -- is the same
mechanism behind every modern LLM.

## Honest caveats

Same caveats as `01_rnn_mt.md`: small from-scratch model, noisy data, no
GPU. Note specifically that the **long** evaluation sentence's individual
reference loss does not always land below the RNN/LSTM's on this particular
sentence, even though the Transformer's *average* validation loss is the
best of the three. That is a real result, not a cherry-picked one -- and
it's worth pointing out to students directly: a single hard example can
disagree with an aggregate metric, which is exactly the caution Module 5
raised about trusting one averaged number.
