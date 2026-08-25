# Demo: Entropy, Cross-Entropy, and KL Divergence

This demo compares letter frequency distributions from two different text samples.

## What it demonstrates

1. **Entropy H(p)**: Average surprise in bits when sampling from distribution p
2. **Cross-entropy H(p,q)**: Average surprise when using model q to predict data from p  
3. **KL divergence D_KL(p||q)**: Extra surprise from using q instead of p
4. **Mathematical identity**: D_KL(p||q) = H(p,q) - H(p)

## How it works

The demo:
- Counts letter frequencies in two text samples
- Converts counts to probability distributions
- Calculates all three information measures
- Verifies the mathematical relationship between them

## Connection to GenAI

Language models minimize cross-entropy during training. When evaluating models, lower cross-entropy on test data means the model assigns higher probability to real sequences.

In RLHF, KL divergence keeps the fine-tuned model close to the base model, preventing it from drifting too far while optimizing for human preferences.
