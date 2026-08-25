"""
Entropy, Cross-Entropy, and KL Divergence
Demonstrates how these information measures relate to distribution similarity.
"""
import numpy as np
import tiktoken
from urllib.request import urlopen

# Fetch text from different sources
url_p = "https://www.gutenberg.org/files/1342/1342-0.txt"      # Pride and Prejudice
url_same = "https://www.gutenberg.org/files/11/11-0.txt"       # Alice in Wonderland
url_diff = "https://raw.githubusercontent.com/django/django/main/django/db/models/query.py"  # Python code

with urlopen(url_p) as response:
    text_p = response.read().decode('utf-8')[:50000]
with urlopen(url_same) as response:
    text_same = response.read().decode('utf-8')[:50000]
with urlopen(url_diff) as response:
    text_diff = response.read().decode('utf-8')[:50000]

# Tokenize using GPT-4 tokenizer
enc = tiktoken.get_encoding("cl100k_base")
tokens_p = np.array(enc.encode(text_p))
tokens_same = np.array(enc.encode(text_same))
tokens_diff = np.array(enc.encode(text_diff))

# Build probability distributions p, q_same, q_diff
max_token = max(tokens_p.max(), tokens_same.max(), tokens_diff.max())
p = np.bincount(tokens_p, minlength=max_token+1) / len(tokens_p)
q_same = np.bincount(tokens_same, minlength=max_token+1) / len(tokens_same)
q_diff = np.bincount(tokens_diff, minlength=max_token+1) / len(tokens_diff)

# Individual entropies (not measuring similarity)
H_p = -np.sum(p[p > 0] * np.log2(p[p > 0]))
H_same = -np.sum(q_same[q_same > 0] * np.log2(q_same[q_same > 0]))
H_diff = -np.sum(q_diff[q_diff > 0] * np.log2(q_diff[q_diff > 0]))
print(f"H(p) = {H_p:.4f} bits")
print(f"H(q_same) = {H_same:.4f} bits")
print(f"H(q_diff) = {H_diff:.4f} bits")
print()

# Cross-entropy and KL divergence (measuring similarity)
print("Comparing p with q_same (similar sources):")
mask_same = p > 0
H_p_qsame = -np.sum(p[mask_same] * np.log2(np.clip(q_same[mask_same], 1e-10, None)))
D_kl_same = np.sum(p[mask_same] * np.log2(p[mask_same] / np.clip(q_same[mask_same], 1e-10, None)))
print(f"  H(p, q_same) = {H_p_qsame:.4f} bits")
print(f"  D_KL(p || q_same) = {D_kl_same:.4f} bits")
print()

print("Comparing p with q_diff (different sources):")
mask_diff = p > 0
H_p_qdiff = -np.sum(p[mask_diff] * np.log2(np.clip(q_diff[mask_diff], 1e-10, None)))
D_kl_diff = np.sum(p[mask_diff] * np.log2(p[mask_diff] / np.clip(q_diff[mask_diff], 1e-10, None)))
print(f"  H(p, q_diff) = {H_p_qdiff:.4f} bits")
print(f"  D_KL(p || q_diff) = {D_kl_diff:.4f} bits")
