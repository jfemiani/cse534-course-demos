"""Likelihood underflow and negative log-likelihood as loss."""

import numpy as np
import torch

# Generate Bernoulli data
rng = np.random.default_rng(seed=42)
n = 1000
true_mu = 0.7
data = rng.binomial(1, true_mu, n)

print("Part 1: Numerical stability")
print("=" * 50)

# Test candidates
candidates = [0.5, 0.6, 0.7, 0.8]

for mu in candidates:
    # Likelihood (product of probabilities)
    likelihood = np.prod([mu if x == 1 else (1 - mu) for x in data])
    
    # Log-likelihood (sum of log probabilities)
    log_likelihood = np.sum([np.log(mu) if x == 1 else np.log(1 - mu) for x in data])
    
    print(f"\nmu = {mu:.1f}:")
    print(f"  L(mu)  = {likelihood:.2e}")
    print(f"  ell(mu)  = {log_likelihood:.2f}")

print("\n-> Likelihood underflows to 0, log-likelihood stays computable")

response = input("\nPress Enter to continue (or 'q' to quit)...")
if response.lower() == 'q':
    exit()

print("\nPart 2: Why we use log-likelihood for optimization")
print("=" * 50)

# Convert data to torch tensor
x = torch.tensor(data, dtype=torch.float32)

# Try gradient descent on raw likelihood (will fail)
print("\nAttempt 1: Gradient descent on likelihood L(mu)")
mu1 = torch.tensor([0.3], requires_grad=True)
print(f"Initial mu = {mu1.item():.3f}")

for step in range(50):
    # Compute likelihood (product)
    L = torch.prod(torch.where(x == 1, mu1, 1 - mu1))
    L.backward()
    
    with torch.no_grad():
        mu1 += 0.01 * mu1.grad  # maximize L
        mu1.clamp_(0.01, 0.99)
        mu1.grad.zero_()

print(f"Final mu = {mu1.item():.3f}")
print("-> Fails! Gradients vanish due to underflow")

print("\nAttempt 2: Gradient descent on negative log-likelihood")
mu2 = torch.tensor([0.3], requires_grad=True)
optimizer = torch.optim.Adam([mu2], lr=0.05)
print(f"Initial mu = {mu2.item():.3f}")

for step in range(100):
    mu_safe = torch.clamp(mu2, 0.001, 0.999)
    nll = -torch.sum(x * torch.log(mu_safe) + (1 - x) * torch.log(1 - mu_safe))
    
    optimizer.zero_grad()
    nll.backward()
    optimizer.step()
    
    with torch.no_grad():
        mu2.clamp_(0.001, 0.999)

print(f"Final mu = {mu2.item():.3f}")
print(f"Observed fraction = {data.mean():.3f}")
print("-> Works! Log-likelihood enables gradient-based optimization")
