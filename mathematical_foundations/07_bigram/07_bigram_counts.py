"""
Bigram Counts to Conditional Probabilities
Shows how character counts become P(next|context) for a simple string.
"""

text = "banana"

print("Training text:", text)
print()

# Count bigrams (context, next_char) pairs
bigram_counts = {}
for i in range(len(text) - 1):
    context = text[i]
    next_char = text[i + 1]
    pair = (context, next_char)
    bigram_counts[pair] = bigram_counts.get(pair, 0) + 1

print("Bigram counts:")
for pair, count in sorted(bigram_counts.items()):
    print(f"  ('{pair[0]}', '{pair[1]}'): {count}")
print()

# Count contexts
context_counts = {}
for i in range(len(text) - 1):
    context = text[i]
    context_counts[context] = context_counts.get(context, 0) + 1

print("Context counts:")
for context, count in sorted(context_counts.items()):
    print(f"  '{context}': {count}")
print()

# Calculate conditional probabilities
print("Conditional probabilities P(next|context):")
for context in sorted(set(context_counts.keys())):
    print(f"\n  After '{context}':")
    for next_char in sorted(set(n for c, n in bigram_counts.keys() if c == context)):
        count_cx = bigram_counts.get((context, next_char), 0)
        count_c = context_counts[context]
        prob = count_cx / count_c
        print(f"    P('{next_char}'|'{context}') = {count_cx}/{count_c} = {prob:.3f}")

print("\n\nGenerating one step from context 'b':")
print("  Sample from: P('a'|'b') = 1.000")
print("  Generated: 'ba'")
