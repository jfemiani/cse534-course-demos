"""RNN encoder-decoder for English-to-French translation (7.2).

Trains a plain recurrent encoder-decoder on the shared opus-100 corpus built
by mt_data.py, then greedily translates the module's fixed evaluation
sentences -- including one deliberately long one. Watch the last sentence:
the encoder squeezes the entire source sentence into one fixed-size hidden
vector (the "context vector"), and that single vector is all the decoder
gets to work with. As the source sentence gets longer, there's more to
squeeze into the same fixed-size vector, and translation quality drops.

Compare this file's output with 02_lstm_mt.py (same data, same training
loop, only nn.RNN -> nn.LSTM changes) and 03_transformer_mt.py (attention
removes the fixed-size bottleneck entirely).

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
EMBED_DIM, HIDDEN_DIM = 128, 256
BATCH_SIZE, EPOCHS, LEARNING_RATE = 64, 25, 1e-3
MAX_DECODE_LEN = 20
N_PAIRS = 12000


class Encoder(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, EMBED_DIM)
        self.rnn = nn.RNN(EMBED_DIM, HIDDEN_DIM, batch_first=True)

    def forward(self, src):
        _, hidden = self.rnn(self.embed(src))
        return hidden  # the single fixed-size context vector


class Decoder(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, EMBED_DIM)
        self.rnn = nn.RNN(EMBED_DIM, HIDDEN_DIM, batch_first=True)
        self.out = nn.Linear(HIDDEN_DIM, vocab_size)

    def forward(self, tgt_in, hidden):
        output, hidden = self.rnn(self.embed(tgt_in), hidden)
        return self.out(output), hidden

    def step(self, token, hidden):
        output, hidden = self.rnn(self.embed(token), hidden)
        return self.out(output), hidden


def train_epoch(encoder, decoder, loader, optimizer, criterion):
    encoder.train(), decoder.train()
    total_loss = 0.0
    for src, tgt in loader:
        optimizer.zero_grad()
        hidden = encoder(src)
        logits, _ = decoder(tgt[:, :-1], hidden)  # teacher forcing: feed the true previous word
        loss = criterion(logits.reshape(-1, logits.size(-1)), tgt[:, 1:].reshape(-1))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(loader)


@torch.no_grad()
def val_epoch(encoder, decoder, loader, criterion):
    encoder.eval(), decoder.eval()
    total_loss = 0.0
    for src, tgt in loader:
        hidden = encoder(src)
        logits, _ = decoder(tgt[:, :-1], hidden)
        loss = criterion(logits.reshape(-1, logits.size(-1)), tgt[:, 1:].reshape(-1))
        total_loss += loss.item()
    return total_loss / len(loader)


@torch.no_grad()
def translate(sentence, encoder, decoder, src_vocab, tgt_vocab):
    encoder.eval(), decoder.eval()
    src = torch.tensor([src_vocab.encode(sentence)])
    hidden = encoder(src)
    token = torch.tensor([[tgt_vocab.stoi["<sos>"]]])
    output_ids = []
    for _ in range(MAX_DECODE_LEN):
        logits, hidden = decoder.step(token, hidden)
        token = logits.argmax(dim=-1)
        next_id = token.item()
        if next_id == tgt_vocab.stoi["<eos>"]:
            break
        output_ids.append(next_id)
    return tgt_vocab.decode(output_ids)


@torch.no_grad()
def reference_loss(en, fr, encoder, decoder, src_vocab, tgt_vocab, criterion):
    """Teacher-forced loss on the TRUE French reference. Unlike greedy
    translation, this works even when the model's own guess is nonsense --
    it directly measures how surprised the model is by the correct answer,
    so it stays a fair comparison across sentence lengths."""
    encoder.eval(), decoder.eval()
    src = torch.tensor([src_vocab.encode(en)])
    tgt = torch.tensor([tgt_vocab.encode(fr)])
    hidden = encoder(src)
    logits, _ = decoder(tgt[:, :-1], hidden)
    return criterion(logits.reshape(-1, logits.size(-1)), tgt[:, 1:].reshape(-1)).item()


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
        train_loss = train_epoch(encoder, decoder, loader, optimizer, criterion)
        val_loss = val_epoch(encoder, decoder, val_loader, criterion)
        print(f"epoch {epoch:2d}  train_loss {train_loss:.3f}  val_loss {val_loss:.3f}")
        if val_loss < best_val_loss:  # same early-stopping idea as Module 5's grid search
            best_val_loss = val_loss
            best_state = (encoder.state_dict(), decoder.state_dict())
    encoder.load_state_dict(best_state[0])
    decoder.load_state_dict(best_state[1])
    print(f"\n(using the checkpoint with the lowest validation loss: {best_val_loss:.3f})")

    print("\nGreedy translations and reference loss on the module's fixed evaluation sentences")
    print("(reference loss = how surprised the model is by the TRUE translation; lower is better;")
    print(" watch it climb as the sentence gets longer):\n")
    for en, fr in EVAL_PAIRS:
        loss = reference_loss(en, fr, encoder, decoder, src_vocab, tgt_vocab, criterion)
        guess = translate(en, encoder, decoder, src_vocab, tgt_vocab)
        print(f"  en:  {en}")
        print(f"  fr (reference): {fr}")
        print(f"  fr (model's greedy guess): {guess}")
        print(f"  reference loss: {loss:.3f}  ({len(en.split())} source words)\n")


if __name__ == "__main__":
    main()
