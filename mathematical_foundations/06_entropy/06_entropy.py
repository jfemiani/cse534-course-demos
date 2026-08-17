"""
Entropy, Cross-Entropy, and KL Divergence
Demonstrates how these information measures relate to distribution similarity.
"""
import numpy as np

# Two sample texts
text1 = "the quick brown fox jumps over the lazy dog"
text2 = "python code uses many loops and functions"

def get_letter_distribution(text):
    """Count letter frequencies and return distribution."""
    text = text.lower().replace(" ", "")
    counts = {}
    for char in text:
        counts[char] = counts.get(char, 0) + 1
    
    total = sum(counts.values())
    probs = {char: count / total for char, count in counts.items()}
    return probs

def entropy(p):
    """Calculate entropy H(p) = -sum(p(x) * log2(p(x)))"""
    return -sum(px * np.log2(px) for px in p.values() if px > 0)

def cross_entropy(p, q):
    """Calculate cross-entropy H(p,q) = -sum(p(x) * log2(q(x)))"""
    result = 0
    for x in p:
        if p[x] > 0:
            qx = q.get(x, 1e-10)  # small value if letter not in q
            result -= p[x] * np.log2(qx)
    return result

def kl_divergence(p, q):
    """Calculate KL divergence D_KL(p||q) = sum(p(x) * log2(p(x)/q(x)))"""
    result = 0
    for x in p:
        if p[x] > 0:
            qx = q.get(x, 1e-10)
            result += p[x] * np.log2(p[x] / qx)
    return result

# Get distributions
p = get_letter_distribution(text1)
q = get_letter_distribution(text2)

print("Text 1:", text1)
print("Text 2:", text2)
print()

print("Distribution p (text 1):", {k: f"{v:.3f}" for k, v in sorted(p.items())})
print("Distribution q (text 2):", {k: f"{v:.3f}" for k, v in sorted(q.items())})
print()

# Calculate measures
H_p = entropy(p)
H_q = entropy(q)
H_pq = cross_entropy(p, q)
D_kl = kl_divergence(p, q)

print(f"H(p) = {H_p:.4f} bits")
print(f"H(q) = {H_q:.4f} bits")
print(f"H(p,q) = {H_pq:.4f} bits")
print(f"D_KL(p||q) = {D_kl:.4f} bits")
print()

# Verify identity: D_KL(p||q) = H(p,q) - H(p)
identity_check = H_pq - H_p
print(f"Verifying identity D_KL(p||q) = H(p,q) - H(p):")
print(f"  H(p,q) - H(p) = {identity_check:.4f} bits")
print(f"  D_KL(p||q)    = {D_kl:.4f} bits")
print(f"  Match: {abs(identity_check - D_kl) < 0.0001}")
