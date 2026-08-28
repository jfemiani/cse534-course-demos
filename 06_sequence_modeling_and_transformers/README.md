# Sequence Modeling and Transformers demonstrations

This module has two parts. First, two prerequisite lessons on tokenization
and word embeddings -- every architecture below depends on both. Then: one
task, three architectures. Every translation demo in this module trains an
English-to-French translation model on the identical dataset (built once by
`mt_data.py`, from `Helsinki-NLP/opus-100` on Hugging Face) and evaluates on
the identical five held-out sentences, so the only thing that changes
across `03_rnn_mt`, `04_lstm_mt`, and `05_transformer_mt` is the
architecture. All three use PyTorch (not the Keras/TensorFlow code in the
GDL textbook) and the Hugging Face `datasets` library, per this course's
framework choice going forward.

Work through these in order -- `04_lstm_mt.py` and `05_transformer_mt.py`
are written as direct, minimal-diff comparisons against `03_rnn_mt.py`, not
as standalone demos.

Install this module's dependencies once:
`pip install -r requirements-sequence-modeling-and-transformers.txt`.

## Demos

1. [Tokenization](01_tokenization) — `01_tokenization.py` shows the
   out-of-vocabulary problem this module's own word-level `Vocab` has,
   trains byte-pair encoding (BPE) from scratch on a tiny corpus, then runs
   `tiktoken` and Hugging Face's `AutoTokenizer` on the same real sentence.
2. [Word embeddings](02_word_embeddings) — `02_word_embeddings.py`
   contrasts WordNet's hand-built synsets against a GloVe vector's nearest
   neighbors for the ambiguous word "bank," then uses PCA (the same call as
   Module 3's eigenfaces demo) to visualize a small set of word vectors.
3. [RNN](03_rnn_mt) — `03_rnn_mt.py` trains a plain recurrent
   encoder-decoder. The encoder squeezes the whole source sentence into one
   fixed-size hidden vector; the decoder generates French one word at a
   time starting from that single vector.
4. [LSTM](04_lstm_mt) — `04_lstm_mt.py` changes exactly one thing versus
   `03_rnn_mt.py`: `nn.RNN` → `nn.LSTM`. Same data, same training loop, same
   evaluation sentences. Gating doesn't remove the fixed-size bottleneck,
   it lets the network learn what's worth protecting inside it.
5. [Transformer](05_transformer_mt) — `05_transformer_mt.py` removes
   recurrence entirely. Self-attention and cross-attention (via PyTorch's
   `nn.MultiheadAttention`) let the decoder look directly at every source
   position at every step; the demo also visualizes which source word each
   output word attends to most.

Each demo folder has a companion `.md` file with the full explanation and
an `.output.txt` file with a real captured run -- read the `.md` before the
`.py`.

## Data pipeline

`mt_data.py` (module root) builds the shared corpus once: it streams
`Helsinki-NLP/opus-100` (en-fr), keeps short (3-9 word) length-matched
pairs, builds a word-level vocabulary from scratch (not the subword/BPE
tokenizer this module's own 6.2 lesson covers -- a deliberate simplification
so the vocabulary stays small and the three architectures stay directly
comparable), and holds out five fixed sentences (`EVAL_PAIRS`) from training
so the same sentences can be used for evaluation across all three demos.

This corpus is real, noisy, subtitle-derived data -- not a curated
textbook dataset. A small fraction of pairs are misaligned or literal
subtitle artifacts. That noise is intentional context, not a bug to hide:
it's why every demo tracks validation loss and reports the checkpoint with
the lowest validation loss, instead of just training for a fixed number of
epochs and hoping for the best (the same evaluation discipline Module 5
taught with the n-gram order sweep).

## Canvas pages and activities

`pages/` holds the working copies of the seven Canvas lesson pages (6.1
Module Overview, 6.2 Tokenization, 6.3 Word Embeddings, 6.4 RNNs, 6.5
LSTMs, 6.6 Transformers and Attention, 6.7 Fine-Tuning and RLHF), built
from this module's real, captured demo output. `quizzes/` holds the
working copy of the single combined 6.8 quiz (text2qti format, 25
questions, weighted toward Transformers/Attention/RLHF as the module's
main payoff); it replaced three legacy per-architecture pretest quizzes
(RNN, LSTM, Transformer), which were unpublished rather than deleted for
reversibility. `assignments/` holds the working copy of the 6.9 lab
("Reproduce and Extend a Transformer Demo"), following the same
reproduce-and-extend format as the labs in modules 2 and 4. `discussion/`
still holds the local copies of the original 6.8/6.9 discussion prompts,
but both were retired from the live module (unpublished, prefixed
`[Retired]`, and removed from the module) rather than kept active,
since the module already carries seven pages, a quiz, and a lab. See
`DESIGN-module-6.md` for the design brief 6.1/6.4-6.6 were authored from
(written when this module was still numbered 7; renumbered to 6 to close
a numbering gap; 6.6 was later split into 6.6 Transformers/Attention and
6.7 Fine-Tuning and RLHF); 6.2 and 6.3 were added in a later pass to
cover tokenization and word embeddings as prerequisites for the rest of
the module.
