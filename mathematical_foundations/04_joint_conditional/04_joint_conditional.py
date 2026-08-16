"""Autoregressive generation: P(next | context) computed at each step."""

import numpy as np

# Load word list
with open("words.txt") as f:
    words = [line.strip() for line in f]

# Generate a word letter by letter
rng = np.random.default_rng(seed=None) # I dont want reproducibility, I want variety!
generated = ""  # Start with empty string

print("Generating word autoregressively...")
print("=" * 50)

for step in range(5):
    # Find all words matching current prefix
    if generated:
        matching = [w for w in words if w.startswith(generated) and len(w) > len(generated)]
    else:
        matching = words
    
    if not matching:
        break
    
    # Compute P(all_previous) - probability of current context
    p_context = len(matching) / len(words)
    
    # Count next letters
    next_counts = {}
    for word in matching:
        if len(word) > len(generated):
            next_letter = word[len(generated)]
            next_counts[next_letter] = next_counts.get(next_letter, 0) + 1
    
    # Compute P(next | context)
    total = sum(next_counts.values())
    probs = {letter: count / total for letter, count in next_counts.items()}
    sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)
    
    # Show all possibilities
    print(f"\nStep {step + 1}: context='{generated}' ({len(matching)} words match)")
    print(f"P('{generated}') = {p_context:.3f}")
    print(f"\nP(next | '{generated}'):")
    for letter, prob in sorted_probs:
        print(f"  '{letter}': {prob:.3f}")
    
    # Sample next letter
    letters = list(probs.keys())
    ps = list(probs.values())
    next_letter = rng.choice(letters, p=ps)
    
    # Compute joint P(context, sampled)
    new_context = generated + next_letter
    matching_new = [w for w in words if w.startswith(new_context)]
    p_joint = len(matching_new) / len(words)
    
    print(f"\n→ Sampled: '{next_letter}'")
    print(f"P('{new_context}') = {p_joint:.3f}")
    
    generated += next_letter
    
    response = input("\nPress Enter to continue (or 'q' to quit)...")
    if response.lower() == 'q':
        break

print(f"\n{'=' * 50}")
print(f"Generated word: '{generated}'")
print("This is how LLMs generate text token-by-token!")
