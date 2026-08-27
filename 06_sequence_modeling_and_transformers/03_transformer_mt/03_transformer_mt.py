"""Transformer encoder-decoder for English-to-French translation (6.4).

Same corpus, same training loop, same evaluation sentences as 01_rnn_mt.py
and 02_lstm_mt.py. What changes: there is no hidden state carried step by
step, and no single fixed-size bottleneck vector. Instead, at every decoding
step the decoder computes fresh attention weights over every encoder output
position -- a learned version of the same dot-product similarity used for
retrieval in Module 4. This demo prints the actual attention weights for one
sentence so you can see which source word the decoder is "looking at" while
producing each output word.

The encoder uses PyTorch's built-in nn.TransformerEncoderLayer. The decoder
is assembled from PyTorch's built-in nn.MultiheadAttention blocks (self-
attention, then cross-attention, then a feedforward layer) instead of the
built-in nn.TransformerDecoderLayer, only so the cross-attention weights are
easy to pull out for the visualization above -- the attention math itself is
still entirely PyTorch's, nothing here is hand-rolled.

pip install torch datasets
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from mt_data import EVAL_PAIRS, build_dataset, collate

DEVICE = torch.device("cpu")
D_MODEL, N_HEAD, FF_DIM, MAX_LEN = 128, 4, 256, 32
BATCH_SIZE, EPOCHS, LEARNING_RATE = 64, 25, 1e-3
MAX_DECODE_LEN = 20
N_PAIRS = 12000


class PositionalEmbedding(nn.Module):
    """A learned position vector added to each token embedding, since a
    Transformer has no recurrence to tell it word order on its own."""

    def __init__(self, vocab_size):
        super().__init__()
        self.token_embed = nn.Embedding(vocab_size, D_MODEL)
        self.pos_embed = nn.Embedding(MAX_LEN, D_MODEL)

    def forward(self, tokens):
        positions = torch.arange(tokens.size(1), device=tokens.device).unsqueeze(0)
        return self.token_embed(tokens) + self.pos_embed(positions)


class Encoder(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()
        self.embed = PositionalEmbedding(vocab_size)
        layer = nn.TransformerEncoderLayer(D_MODEL, N_HEAD, FF_DIM, batch_first=True)
        self.transformer = nn.TransformerEncoder(layer, num_layers=2)

    def forward(self, src, pad_mask):
        return self.transformer(self.embed(src), src_key_padding_mask=pad_mask)


class DecoderLayer(nn.Module):
    """One decoder block: causal self-attention over the target so far, then
    cross-attention over every encoder output position, then a feedforward
    layer. Built from nn.MultiheadAttention directly (rather than
    nn.TransformerDecoderLayer) so the cross-attention weights can be
    returned for the visualization at the bottom of this file."""

    def __init__(self):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(D_MODEL, N_HEAD, batch_first=True)
        self.cross_attn = nn.MultiheadAttention(D_MODEL, N_HEAD, batch_first=True)
        self.ff = nn.Sequential(nn.Linear(D_MODEL, FF_DIM), nn.ReLU(), nn.Linear(FF_DIM, D_MODEL))
        self.norm1, self.norm2, self.norm3 = (nn.LayerNorm(D_MODEL) for _ in range(3))

    def forward(self, tgt, memory, causal_mask, memory_pad_mask):
        attended, _ = self.self_attn(tgt, tgt, tgt, attn_mask=causal_mask, need_weights=False)
        tgt = self.norm1(tgt + attended)
        attended, cross_weights = self.cross_attn(
            tgt, memory, memory, key_padding_mask=memory_pad_mask, need_weights=True)
        tgt = self.norm2(tgt + attended)
        tgt = self.norm3(tgt + self.ff(tgt))
        return tgt, cross_weights  # cross_weights: [batch, tgt_len, src_len]


class Decoder(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()
        self.embed = PositionalEmbedding(vocab_size)
        self.layer = DecoderLayer()
        self.out = nn.Linear(D_MODEL, vocab_size)

    def forward(self, tgt_in, memory, memory_pad_mask):
        causal_mask = nn.Transformer.generate_square_subsequent_mask(tgt_in.size(1))
        hidden, cross_weights = self.layer(self.embed(tgt_in), memory, causal_mask, memory_pad_mask)
        return self.out(hidden), cross_weights


def train_epoch(encoder, decoder, loader, optimizer, criterion, pad_id):
    encoder.train(), decoder.train()
    total_loss = 0.0
    for src, tgt in loader:
        optimizer.zero_grad()
        src_pad_mask = src == pad_id
        memory = encoder(src, src_pad_mask)
        logits, _ = decoder(tgt[:, :-1], memory, src_pad_mask)  # teacher forcing
        loss = criterion(logits.reshape(-1, logits.size(-1)), tgt[:, 1:].reshape(-1))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(loader)


@torch.no_grad()
def val_epoch(encoder, decoder, loader, criterion, pad_id):
    encoder.eval(), decoder.eval()
    total_loss = 0.0
    for src, tgt in loader:
        src_pad_mask = src == pad_id
        memory = encoder(src, src_pad_mask)
        logits, _ = decoder(tgt[:, :-1], memory, src_pad_mask)
        loss = criterion(logits.reshape(-1, logits.size(-1)), tgt[:, 1:].reshape(-1))
        total_loss += loss.item()
    return total_loss / len(loader)


@torch.no_grad()
def translate(sentence, encoder, decoder, src_vocab, tgt_vocab):
    encoder.eval(), decoder.eval()
    src = torch.tensor([src_vocab.encode(sentence)])
    memory = encoder(src, pad_mask=None)
    ids = [tgt_vocab.stoi["<sos>"]]
    for _ in range(MAX_DECODE_LEN):
        logits, _ = decoder(torch.tensor([ids]), memory, memory_pad_mask=None)
        next_id = logits[0, -1].argmax().item()
        if next_id == tgt_vocab.stoi["<eos>"]:
            break
        ids.append(next_id)
    return tgt_vocab.decode(ids[1:])


@torch.no_grad()
def reference_loss(en, fr, encoder, decoder, src_vocab, tgt_vocab, criterion):
    """Teacher-forced loss on the TRUE French reference -- see 01_rnn_mt.py
    for why this is a fairer cross-length comparison than greedy output."""
    encoder.eval(), decoder.eval()
    src = torch.tensor([src_vocab.encode(en)])
    tgt = torch.tensor([tgt_vocab.encode(fr)])
    memory = encoder(src, pad_mask=None)
    logits, _ = decoder(tgt[:, :-1], memory, memory_pad_mask=None)
    return criterion(logits.reshape(-1, logits.size(-1)), tgt[:, 1:].reshape(-1)).item()


@torch.no_grad()
def show_attention(en, fr, encoder, decoder, src_vocab, tgt_vocab):
    """Print the decoder's cross-attention weights: which source word each
    output word was 'looking at' most while it was generated."""
    encoder.eval(), decoder.eval()
    src_tokens = src_vocab.encode(en)[1:-1]  # drop <sos>/<eos> for a readable header
    src = torch.tensor([src_vocab.encode(en)])
    tgt = torch.tensor([tgt_vocab.encode(fr)])
    memory = encoder(src, pad_mask=None)
    _, cross_weights = decoder(tgt[:, :-1], memory, memory_pad_mask=None)
    tgt_words = [tgt_vocab.itos[i] for i in tgt[0, 1:-1].tolist()]
    src_words = [src_vocab.itos[i] for i in src_tokens]
    print(f"  source words: {src_words}")
    for i, word in enumerate(tgt_words):
        weights = cross_weights[0, i, 1:1 + len(src_words)]
        top = src_words[weights.argmax().item()]
        print(f"    \"{word}\" attends most to \"{top}\"")


def main():
    train_ds, val_ds, src_vocab, tgt_vocab = build_dataset(n_pairs=N_PAIRS)
    pad_id = src_vocab.stoi["<pad>"]
    loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,
                         collate_fn=lambda b: collate(b, pad_id))
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, collate_fn=lambda b: collate(b, pad_id))

    encoder = Encoder(len(src_vocab)).to(DEVICE)
    decoder = Decoder(len(tgt_vocab)).to(DEVICE)
    optimizer = torch.optim.Adam(list(encoder.parameters()) + list(decoder.parameters()), lr=LEARNING_RATE)
    criterion = nn.CrossEntropyLoss(ignore_index=pad_id)

    best_val_loss, best_state = float("inf"), None
    for epoch in range(1, EPOCHS + 1):
        train_loss = train_epoch(encoder, decoder, loader, optimizer, criterion, pad_id)
        val_loss = val_epoch(encoder, decoder, val_loader, criterion, pad_id)
        print(f"epoch {epoch:2d}  train_loss {train_loss:.3f}  val_loss {val_loss:.3f}")
        if val_loss < best_val_loss:  # same early-stopping idea as Module 5's grid search
            best_val_loss = val_loss
            best_state = (encoder.state_dict(), decoder.state_dict())
    encoder.load_state_dict(best_state[0])
    decoder.load_state_dict(best_state[1])
    print(f"\n(using the checkpoint with the lowest validation loss: {best_val_loss:.3f})")

    print("\nGreedy translations and reference loss on the module's fixed evaluation sentences")
    print("(same sentences, same corpus, same training loop as 01_rnn_mt.py and")
    print(" 02_lstm_mt.py -- recurrence is gone entirely, replaced by attention):\n")
    for en, fr in EVAL_PAIRS:
        loss = reference_loss(en, fr, encoder, decoder, src_vocab, tgt_vocab, criterion)
        guess = translate(en, encoder, decoder, src_vocab, tgt_vocab)
        print(f"  en:  {en}")
        print(f"  fr (reference): {fr}")
        print(f"  fr (model's greedy guess): {guess}")
        print(f"  reference loss: {loss:.3f}  ({len(en.split())} source words)\n")

    print("Attention: which source word does each output word look at?")
    en, fr = EVAL_PAIRS[-1]  # the deliberately long sentence
    print(f"  en: {en}\n  fr (reference): {fr}")
    show_attention(en, fr, encoder, decoder, src_vocab, tgt_vocab)


if __name__ == "__main__":
    main()
