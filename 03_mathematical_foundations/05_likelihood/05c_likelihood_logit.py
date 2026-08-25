"""Part C: Direct mu optimization with log-likelihood"""

import numpy as np
import torch

# Generate Bernoulli data
rng = np.random.default_rng(seed=42)
num = 100_000
true_mu = 0.7
data = rng.binomial(1, true_mu, num)

# Convert data to torch tensor
x = torch.tensor(data, dtype=torch.float32)

print("Direct mu optimization (with clamping)")
print("=" * 50)

mu1 = torch.tensor([0.3], requires_grad=True)
print(f"Initial mu = {mu1.item():.4f}")
print(f"Target (observed fraction) = {data.mean():.4f}\n")

for step in range(50):
    # Log-likelihood
    ll = torch.sum(x * torch.log(mu1) + (1 - x) * torch.log(1 - mu1))
    ll.backward()

    with torch.no_grad():
        mu1 += 0.000001 * mu1.grad  # maximize ll
        mu1.clamp_(0.001, 0.999)  # constrain to (0,1)
        mu1.grad.zero_()

    print(f"Step {step:2d}: mu = {mu1.item():.4f}")

print(f"\nFinal mu = {mu1.item():.4f}")
print(f"Target   = {data.mean():.4f}")
print("-> Works, but requires manual clamping to keep mu in (0,1)")
