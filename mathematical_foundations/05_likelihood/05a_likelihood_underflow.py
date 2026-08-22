"""Part A: Likelihood underflow - why we need log-likelihood"""

import numpy as np

# Generate Bernoulli data
rng = np.random.default_rng(seed=42)
num = 100_000
true_mu = 0.7
data = rng.binomial(1, true_mu, num)

print("Numerical stability: Likelihood vs Log-Likelihood")
print("=" * 50)

# Test candidates
candidates = [0.5, 0.6, 0.7, 0.8]

for mu in candidates:
    # Likelihood (product of probabilities)
    likelihood = np.prod([mu if x == 1 else (1 - mu) for x in data])

    # Log-likelihood (sum of log probabilities)
    log_likelihood = np.sum([np.log(mu) if x == 1 else np.log(1 - mu) for x in data])

    print(f"\nCandidate mu = {mu:.1f}:")
    print(f"  L(mu)    = {likelihood:.2e}")
    print(f"  log L(mu) = {log_likelihood:.2f}")

print("\n-> Likelihood underflows to 0.00e+00")
print("-> Log-likelihood stays finite and comparable")
