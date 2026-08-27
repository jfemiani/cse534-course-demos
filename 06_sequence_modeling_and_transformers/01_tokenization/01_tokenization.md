# 01: Tokenization -- from a closed vocabulary to BPE, and two real tokenizers

Concept: `../mt_data.py`'s `Vocab` class -- used by every demo in this
module -- builds a closed, word-level vocabulary and falls back to a single
`<unk>` id for anything it hasn't seen. This demo opens up what production
systems do instead: byte-pair encoding (BPE) builds a vocabulary of
subword pieces from the bottom up, so there is no such thing as an
unrepresentable string, and shows two real tokenizer libraries doing
exactly that on real text.

## What the demo does

1. Builds a tiny word-level `Vocab` (the same class `mt_data.py` uses) and
   shows that an invented, never-seen word gets the exact same id as every
   other unknown word -- the out-of-vocabulary problem in one line.
2. Trains BPE from scratch on a five-word toy corpus, printing the merge
   table one merge at a time: start from individual characters, find the
   most frequent adjacent pair, merge it, repeat. Then applies the learned
   merges to a held-out word the trainer never saw.
3. Runs `tiktoken` (`cl100k_base`, the encoding behind GPT-4-family models)
   and Hugging Face's `AutoTokenizer` (`gpt2`) on the same real sentence,
   side by side, to show real production vocabularies (tens of thousands of
   merges) instead of the toy demo's eight.
4. Tokenizes `"strawberry"` and explains, using the actual pieces `tiktoken`
   produces, why an LLM struggles to count individual letters in a word: it
   never sees individual letters, only these multi-letter pieces.

## Why this is worth reading closely

The merge table in part 2 is the whole algorithm: at every step, count how
often each adjacent pair of symbols occurs across the corpus, and merge the
single most frequent pair into a new symbol. Nothing else is happening.
Watch the held-out word at the end: `"lowering"` was never in the training
corpus, but the learned merges still produce a reasonable segmentation of
it -- worst case, one piece per character, never a single `<unk>` symbol.

Part 3's real-tokenizer comparison is the payoff: production tokenizers run
the identical algorithm (or a close cousin -- see the module notes on
SentencePiece) at a scale of tens of thousands of merges instead of eight,
which is why `tiktoken` and Hugging Face's tokenizer split the same
sentence into slightly different, non-obvious pieces.

## Where to get a tokenizer

- **OpenAI models** -- `tiktoken` (`pip install tiktoken`).
- **Open Hugging Face models** -- `transformers.AutoTokenizer.from_pretrained(model_name)`
  or the standalone `tokenizers` library.
- **Llama- and T5-style models** -- SentencePiece
  (Kudo & Richardson, 2018), usually loaded via that same
  `AutoTokenizer.from_pretrained` call; the underlying format differs from
  `tiktoken`'s, but the workflow of "ask for the tokenizer that matches the
  model" is the same across all three.

## Honest caveats

- The toy BPE trainer is a teaching implementation: no special handling for
  unicode, rare bytes, or the pretokenization rules real BPE
  implementations use. It is meant to make the merge algorithm visible, not
  to be production code.
- `tiktoken`'s `cl100k_base` and Hugging Face's `gpt2` encoding are trained
  on different corpora with different merge counts, so their token counts
  on the same sentence are expected to differ -- that difference is the
  point, not a bug.
