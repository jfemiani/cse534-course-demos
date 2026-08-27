"""Shared English-French data pipeline for the module 7 RNN/LSTM/Transformer demos.

Built once and imported by 01_rnn_mt.py, 02_lstm_mt.py, and 03_transformer_mt.py
so that translation-quality differences across the three demos come only from
the architecture, not from three separately-built datasets. See
07_sequence_modeling_and_transformers/README.md for the full explanation.

Source: Hugging Face `Helsinki-NLP/opus-100` (en-fr), an OpenSubtitles-derived
corpus. It is noisy (a small fraction of pairs are misaligned or untranslated)
because it comes from real subtitle alignment, not curated sentence pairs.
That noise is left in on purpose: filtering it away would need a translation
quality signal, which is the very thing these lessons build.
"""

import random

import torch
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import Dataset

PAD, SOS, EOS, UNK = "<pad>", "<sos>", "<eos>", "<unk>"
SPECIAL_TOKENS = [PAD, SOS, EOS, UNK]

MIN_WORDS, MAX_WORDS = 3, 9  # keep sentences short enough to train in minutes on a CPU
LENGTH_RATIO_BOUNDS = (0.6, 1.8)  # drop pairs whose word counts differ too much (likely misaligned)

# Reused unchanged across all three lessons so the same sentences produce the
# module's three-way comparison table. Real opus-100 pairs, held out of
# training below. The last one is deliberately long, to show where each
# architecture starts to break.
EVAL_PAIRS = [
    ("I know my job.", "Je connais mon travail."),
    ("OK, that's it.", "Voilà, c'était tout."),
    ("Here it is.", "Le voilà."),
    ("I'll take care of the kids.", "Je m'occuperai des enfants."),
    ("Have any of your friends ever been arrested?",
     "L'une quelconque de vos amies s'est-elle jamais fait arrêter ?"),
]
EVAL_SENTENCES = [en for en, _ in EVAL_PAIRS]


def _tokenize(sentence: str) -> list[str]:
    """Lowercase, whitespace/punctuation split. Word-level on purpose: a
    from-scratch vocabulary keeps the three architectures directly
    comparable, unlike the subword tokenizer (tiktoken) used in Module 2."""
    sentence = sentence.strip().lower()
    for ch in ".,!?;:\"'":
        sentence = sentence.replace(ch, f" {ch} ")
    return sentence.split()


def load_pairs(n_pairs: int = 3000, seed: int = 42) -> list[tuple[str, str]]:
    """Stream opus-100 en-fr and keep short, length-matched pairs.

    Excludes the module's fixed EVAL_PAIRS sentences so they stay genuinely
    held out.
    """
    from datasets import load_dataset

    eval_en = {en.lower() for en, _ in EVAL_PAIRS}
    ds = load_dataset("Helsinki-NLP/opus-100", "en-fr", split="train", streaming=True)
    kept = []
    for example in ds:
        en, fr = example["translation"]["en"].strip(), example["translation"]["fr"].strip()
        if en.lower() in eval_en:
            continue
        en_words, fr_words = _tokenize(en), _tokenize(fr)
        if not (MIN_WORDS <= len(en_words) <= MAX_WORDS):
            continue
        if not (MIN_WORDS <= len(fr_words) <= MAX_WORDS):
            continue
        if en.lower() == fr.lower():
            continue
        ratio = len(fr_words) / len(en_words)
        if not (LENGTH_RATIO_BOUNDS[0] <= ratio <= LENGTH_RATIO_BOUNDS[1]):
            continue
        kept.append((en, fr))
        if len(kept) >= n_pairs:
            break
    random.Random(seed).shuffle(kept)
    return kept


class Vocab:
    def __init__(self, sentences: list[str]):
        counts: dict[str, int] = {}
        for sentence in sentences:
            for token in _tokenize(sentence):
                counts[token] = counts.get(token, 0) + 1
        self.itos = list(SPECIAL_TOKENS) + sorted(counts, key=counts.get, reverse=True)
        self.stoi = {token: i for i, token in enumerate(self.itos)}

    def __len__(self):
        return len(self.itos)

    def encode(self, sentence: str) -> list[int]:
        ids = [self.stoi.get(t, self.stoi[UNK]) for t in _tokenize(sentence)]
        return [self.stoi[SOS], *ids, self.stoi[EOS]]

    def decode(self, ids: list[int]) -> str:
        words = [self.itos[i] for i in ids if i not in (self.stoi[SOS], self.stoi[EOS], self.stoi[PAD])]
        return " ".join(words)


class TranslationDataset(Dataset):
    def __init__(self, pairs: list[tuple[str, str]], src_vocab: Vocab, tgt_vocab: Vocab):
        self.pairs = pairs
        self.src_vocab = src_vocab
        self.tgt_vocab = tgt_vocab

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        en, fr = self.pairs[idx]
        return torch.tensor(self.src_vocab.encode(en)), torch.tensor(self.tgt_vocab.encode(fr))


def collate(batch, pad_id: int):
    src, tgt = zip(*batch)
    src = pad_sequence(src, batch_first=True, padding_value=pad_id)
    tgt = pad_sequence(tgt, batch_first=True, padding_value=pad_id)
    return src, tgt


def build_dataset(n_pairs: int = 3000, val_fraction: float = 0.1, seed: int = 42):
    """Return (train_ds, val_ds, src_vocab, tgt_vocab) built once from opus-100."""
    pairs = load_pairs(n_pairs=n_pairs, seed=seed)
    src_vocab = Vocab([en for en, _ in pairs])
    tgt_vocab = Vocab([fr for _, fr in pairs])
    n_val = max(1, int(len(pairs) * val_fraction))
    val_pairs, train_pairs = pairs[:n_val], pairs[n_val:]
    train_ds = TranslationDataset(train_pairs, src_vocab, tgt_vocab)
    val_ds = TranslationDataset(val_pairs, src_vocab, tgt_vocab)
    return train_ds, val_ds, src_vocab, tgt_vocab
