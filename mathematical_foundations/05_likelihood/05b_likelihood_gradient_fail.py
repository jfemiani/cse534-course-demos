"""Part B: Gradient ascent on raw likelihood fails due to underflow"""

import numpy as np
import torch

# Generate Bernoulli data
rng = np.random.default_rng(seed=42)
num = 100_000
true_mu = 0.7
data = rng.binomial(1, true_mu, num)

print("Gradient ascent on raw likelihood L(mu)")
print("=" * 50)

# Convert data to torch tensor
x = torch.tensor(data, dtype=torch.float32)

print(f"{x.data=}, {x.grad=}, {x.grad_fn}")

mu = torch.tensor([0.3], requires_grad=True)
print(f"Initial mu = {mu.item():.4f}")
print(f"Target (observed fraction) = {data.mean():.4f}\n")

for step in range(50):
    # Compute likelihood (product)
    L = torch.prod(mu**x * (1 - mu)**(1-x))
    L.backward()
    assert mu.grad is not None, "Gradient should not be None"

    with torch.no_grad():
        print(f"Step {step:2d}: mu = {mu.item():.4f}, grad = {mu.grad.item():.6f}")
        mu.data += 0.01 * mu.grad  # maximize L
        mu.clamp_(0.01, 0.99)
        mu.grad.zero_()

print(f"\nFinal mu = {mu.item():.4f}")
print(f"Target   = {data.mean():.4f}")
print("\n-> Fails! Gradients vanish due to underflow")
print("-> mu doesn't move from initial value")
