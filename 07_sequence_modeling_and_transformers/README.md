# Sequence Modeling and Transformers demonstrations

One task, three architectures. Every demo in this module trains an
English-to-French translation model on the identical dataset (built once by
`mt_data.py`, from `Helsinki-NLP/opus-100` on Hugging Face) and evaluates on
the identical five held-out sentences, so the only thing that changes
across `01_rnn_mt`, `02_lstm_mt`, and `03_transformer_mt` is the
architecture. All three use PyTorch (not the Keras/TensorFlow code in the
GDL textbook) and the Hugging Face `datasets` library, per this course's
framework choice going forward.

Work through these in order -- `02_lstm_mt.py` and `03_transformer_mt.py`
are written as direct, minimal-diff comparisons against `01_rnn_mt.py`, not
as standalone demos.

Install this module's dependencies once:
`pip install -r requirements-sequence-modeling-and-transformers.txt`.

## Demos

1. [RNN](01_rnn_mt) — `01_rnn_mt.py` trains a plain recurrent
   encoder-decoder. The encoder squeezes the whole source sentence into one
   fixed-size hidden vector; the decoder generates French one word at a
   time starting from that single vector.
2. [LSTM](02_lstm_mt) — `02_lstm_mt.py` changes exactly one thing versus
   `01_rnn_mt.py`: `nn.RNN` → `nn.LSTM`. Same data, same training loop, same
   evaluation sentences. Gating doesn't remove the fixed-size bottleneck,
   it lets the network learn what's worth protecting inside it.
3. [Transformer](03_transformer_mt) — `03_transformer_mt.py` removes
   recurrence entirely. Self-attention and cross-attention (via PyTorch's
   `nn.MultiheadAttention`) let the decoder look directly at every source
   position at every step; the demo also visualizes which source word each
   output word attends to most.

Each demo folder has a companion `.md` file with the full explanation and
an `.output.txt` file with a real captured run (validation loss, greedy
translations, and reference loss on the module's fixed evaluation
sentences) -- read the `.md` before the `.py`.

## Data pipeline

`mt_data.py` (module root) builds the shared corpus once: it streams
`Helsinki-NLP/opus-100` (en-fr), keeps short (3-9 word) length-matched
pairs, builds a word-level vocabulary from scratch (not the subword
tokenizer used in Module 2 -- a deliberate simplification so the vocabulary
stays small and the three architectures stay directly comparable), and
holds out five fixed sentences (`EVAL_PAIRS`) from training so the same
sentences can be used for evaluation across all three demos.

This corpus is real, noisy, subtitle-derived data -- not a curated
textbook dataset. A small fraction of pairs are misaligned or literal
subtitle artifacts. That noise is intentional context, not a bug to hide:
it's why every demo tracks validation loss and reports the checkpoint with
the lowest validation loss, instead of just training for a fixed number of
epochs and hoping for the best (the same evaluation discipline Module 5
taught with the n-gram order sweep).

## Canvas pages and activities

`pages/` holds the working copies of the four Canvas lesson pages (7.1
Module Overview, 7.2 RNNs, 7.3 LSTMs, 7.4 Transformers/Attention/RLHF),
built from this module's real, captured demo output. `discussion/` holds
the working copies of the 7.5 and 7.6 discussion prompts, rewritten to ask
students to reason about the specific numbers and examples in 7.2/7.3's
demo output rather than generic RNN/LSTM trivia. Neither has been pushed to
Canvas yet -- see `DESIGN-module-7.md` for the design brief these were
authored from.
