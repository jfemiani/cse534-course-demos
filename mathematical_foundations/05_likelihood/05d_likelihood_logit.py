
"""Part D: Logit parameterization for unconstrained optimization"""

import numpy as np
import torch

# Generate Bernoulli data
rng = np.random.default_rng(seed=42)
num = 100_000
true_mu = 0.7
data = rng.binomial(1, true_mu, num)

# Convert data to torch tensor
x = torch.tensor(data, dtype=torch.float32)

print("Logit parameterization (unconstrained optimization)")
print("=" * 50)

logit = torch.tensor([np.log(0.3 / 0.7)], requires_grad=True)  # log(mu/(1-mu))
print(f"Initial mu = {torch.sigmoid(logit).item():.4f}, logit = {logit.item():.3f}")
print(f"Target (observed fraction) = {data.mean():.4f}\n")

for step in range(50):
    # Numerically stable log-likelihood using logit directly
    # Avoids computing sigmoid then log (which can underflow)
    ll = torch.sum(x * logit - torch.log(1 + torch.exp(logit)))
    ll.backward()

    with torch.no_grad():
        logit += 0.000001 * logit.grad  # maximize ll (no clamping needed!)
        logit.grad.zero_()
    
    mu = torch.sigmoid(logit)  # compute mu for display

    print(f"Step {step:2d}: mu = {mu.item():.4f}, logit = {logit.item():.3f}")

mu_final = torch.sigmoid(logit).item()
print(f"\nFinal mu = {mu_final:.4f}, logit = {logit.item():.3f}")
print(f"Target   = {data.mean():.4f}")
print("-> Best! Logit is unconstrained (-∞,+∞), no clamping needed")
print("-> This is why logistic regression uses logit parameterization")
