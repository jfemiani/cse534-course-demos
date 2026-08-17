"""Autoregressive generation: P(next | context) computed at each step."""

import numpy as np
import pandas as pd

# Load word list with probabilities
df = pd.read_csv("words.csv")
words = df["word"].tolist()
probs = df["prob"].values

# Generate a word letter by letter
rng = np.random.default_rng(seed=None) # I dont want reproducibility, I want variety!
generated = ""  # Start with empty string

print("Generating word autoregressively...")
print("=" * 50)

for step in range(5):
    # Find all words matching current prefix
    matching = [w for w in words if w.startswith(generated)]
    
    # Compute P(context) - sum of probabilities of matching words
    matching_idx = [i for i, w in enumerate(words) if w.startswith(generated)]
    p_context = probs[matching_idx].sum()
    
    # Count next letters weighted by word probabilities
    next_probs = {}
    for idx in matching_idx:
        word = words[idx]
        next_letter = word[len(generated)]
        next_probs[next_letter] = next_probs.get(next_letter, 0) + probs[idx]
    
    # Compute P(next | context) by normalizing
    conditional_probs = {letter: p / p_context for letter, p in next_probs.items()}
    sorted_probs = sorted(conditional_probs.items(), key=lambda x: x[1], reverse=True)
    
    # Show all possibilities
    print(f"\nStep {step + 1}: context='{generated}' ({len(matching)} words match)")
    print(f"P('{generated}') = {p_context:.3f}")
    print(f"\nP(next | '{generated}'):")
    for letter, prob in sorted_probs:
        print(f"  '{letter}': {prob:.3f}")
    
    # Sample next letter
    letters = list(conditional_probs.keys())
    ps = list(conditional_probs.values())
    next_letter = rng.choice(letters, p=ps)
    
    # Compute joint P(context, sampled) - already computed in next_probs!
    p_joint = next_probs[next_letter]
    
    print(f"\n→ Sampled: '{next_letter}'")
    print(f"P('{generated}{next_letter}') = {p_joint:.3f}")
    
    generated += next_letter
    
    response = input("\nPress Enter to continue (or 'q' to quit)...")
    if response.lower() == 'q':
        break

print(f"\n{'=' * 50}")
print(f"Generated word: '{generated}'")
print("This is how LLMs generate text token-by-token!")
