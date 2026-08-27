"""Why subword tokenization exists, how BPE builds one, and where to get one (6.2).

mt_data.py (this module's shared data pipeline) builds a closed, word-level
vocabulary and falls back to <unk> for anything it hasn't seen -- its own
docstring calls this "a deliberate simplification." This demo shows what
production systems do instead: byte-pair encoding (BPE) builds a vocabulary
of subword pieces bottom-up, so no input string is ever truly out-of-vocabulary.

Three parts:
1. The OOV problem: mt_data.py's word-level Vocab chokes on a novel word.
2. A from-scratch BPE trainer on a tiny toy corpus, merge table shown step by
   step, then applied to a held-out word.
3. Two production tokenizers (tiktoken for OpenAI models, Hugging Face
   AutoTokenizer for open models) run on the same real sentence, plus why
   LLMs struggle to count letters -- callback to the Module 4.2 "strawberry"
   example.

pip install tiktoken transformers
"""

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import tiktoken
from transformers import AutoTokenizer

from mt_data import Vocab

# --- Part 1: the OOV problem -------------------------------------------

TOY_TRAIN_SENTENCES = ["the cat sat", "the dog ran", "a cat and a dog"]
NOVEL_WORD = "supercalifragilisticexpialidocious"


def demo_oov_problem():
    vocab = Vocab(TOY_TRAIN_SENTENCES)  # same class mt_data.py uses for the RNN/LSTM/Transformer demos

    known_id = vocab.encode("cat")[1]  # index 0 is <sos>
    unk_id = vocab.encode(NOVEL_WORD)[1]
    print(f"'cat'                                 -> id {known_id} (a real vocabulary entry)")
    print(f"'{NOVEL_WORD}' -> id {unk_id} (the SAME id every unknown word gets)")
    print("A word-level vocabulary has exactly one bucket for 'everything I've never seen.'")


# --- Part 2: from-scratch BPE, worked step by step ----------------------

BPE_TOY_CORPUS = ["low", "lower", "lowest", "newer", "wider"]
N_MERGES = 8


def word_to_symbols(word):
    return list(word) + ["</w>"]  # end-of-word marker so merges don't cross words


def get_pair_counts(corpus_symbols):
    counts = Counter()
    for symbols in corpus_symbols:
        for a, b in zip(symbols, symbols[1:]):
            counts[(a, b)] += 1
    return counts


def merge_pair(pair, corpus_symbols):
    merged = "".join(pair)
    new_corpus = []
    for symbols in corpus_symbols:
        new_symbols, i = [], 0
        while i < len(symbols):
            if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == pair:
                new_symbols.append(merged)
                i += 2
            else:
                new_symbols.append(symbols[i])
                i += 1
        new_corpus.append(new_symbols)
    return new_corpus


def train_bpe(corpus, n_merges):
    corpus_symbols = [word_to_symbols(w) for w in corpus]
    merges = []
    for step in range(n_merges):
        counts = get_pair_counts(corpus_symbols)
        if not counts:
            break
        best_pair, freq = counts.most_common(1)[0]
        corpus_symbols = merge_pair(best_pair, corpus_symbols)
        merges.append(best_pair)
        segmented = ["-".join(s) for s in corpus_symbols]
        print(f"merge {step + 1}: {best_pair} (frequency {freq}) -> {segmented}")
    return merges


def apply_bpe(word, merges):
    symbols = word_to_symbols(word)
    for pair in merges:
        symbols = merge_pair(pair, [symbols])[0]
    return symbols


def demo_bpe_training():
    print(f"Training BPE on toy corpus {BPE_TOY_CORPUS} for {N_MERGES} merges:\n")
    merges = train_bpe(BPE_TOY_CORPUS, N_MERGES)
    held_out = "lowering"
    pieces = apply_bpe(held_out, merges)
    print(f"\nApplying the learned merges to an unseen word, '{held_out}':")
    print(f"  -> {pieces}")
    print("A word the trainer never saw still gets tokenized -- worst case, "
          "one piece per character, never a single <unk> symbol.")


# --- Part 3: real tokenizers, and why letter-counting fails --------------

REAL_SENTENCE = "The cse534 students are tokenizing sentences."


def demo_real_tokenizers():
    enc = tiktoken.get_encoding("cl100k_base")  # used by GPT-4-family models
    tt_ids = enc.encode(REAL_SENTENCE)
    tt_pieces = [enc.decode([i]) for i in tt_ids]
    print(f"tiktoken (cl100k_base, GPT-4 family): {len(tt_ids)} tokens")
    print(f"  pieces: {tt_pieces}")

    hf_tok = AutoTokenizer.from_pretrained("gpt2")
    hf_pieces = hf_tok.tokenize(REAL_SENTENCE)
    print(f"\nHugging Face AutoTokenizer ('gpt2'): {len(hf_pieces)} tokens")
    print(f"  pieces: {hf_pieces}")

    print(f"\nPredict-before-reveal: how many tiktoken tokens for "
          f"'{NOVEL_WORD}'?")
    long_word_ids = enc.encode(NOVEL_WORD)
    print(f"  -> {len(long_word_ids)} tokens: {[enc.decode([i]) for i in long_word_ids]}")

    strawberry_ids = enc.encode("strawberry")
    strawberry_pieces = [enc.decode([i]) for i in strawberry_ids]
    print(f"\n'strawberry' -> {strawberry_pieces} ({len(strawberry_ids)} tokens)")
    print("The model never sees individual letters, only these pieces -- that's "
          "why asking it to count the letter 'r' in 'strawberry' is asking it "
          "to do something its input representation doesn't directly support.")


if __name__ == "__main__":
    print("=== Part 1: the out-of-vocabulary problem ===")
    demo_oov_problem()

    print("\n=== Part 2: training BPE from scratch on a tiny corpus ===")
    demo_bpe_training()

    print("\n=== Part 3: real tokenizers on the same sentence ===")
    demo_real_tokenizers()
