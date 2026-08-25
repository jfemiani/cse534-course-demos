"""Likelihood underflow and negative log-likelihood as loss"""

import numpy as np
import torch

# Generate Bernoulli data
rng = np.random.default_rng(seed=42)
num = 100_000
true_mu = 0.7
data = rng.binomial(1, true_mu, num)

print("Part 1: Numerical stability")
print("=" * 50)

# Test candidates
candidates = [0.5, 0.6, 0.7, 0.8]

for mu in candidates:
    # Likelihood (product of probabilities)
    likelihood = np.prod([mu if x == 1 else (1 - mu) for x in data])

    # Log-likelihood (sum of log probabilities)
    log_likelihood = np.sum([np.log(mu) if x == 1 else np.log(1 - mu) for x in data])

    print(f"\n candidate mu = {mu:.1f}:")
    print(f"  L(mu)  = {likelihood:.2e}")
    print(f"  LogL(mu)  = {log_likelihood:.2f}")

response = input("\nPress Enter to continue (or 'q' to quit)...")
if response.lower() == "q":
    exit()

print("\nPart 2: Why we use log-likelihood for optimization")
print("=" * 50)

# Convert data to torch tensor
x = torch.tensor(data, dtype=torch.float32)

print("\nAttempt 1: Gradient ascent on raw likelihood L(mu)")
mu1 = torch.tensor([0.3], requires_grad=True)
print(f"Initial mu = {mu1.item():.4f}")

for step in range(50):
    # Compute likelihood (product)
    L = torch.prod(mu1**x * (1 - mu1)**(1-x))
    L.backward()

    with torch.no_grad():
        mu1 += 0.01 * mu1.grad  # maximize L
        mu1.clamp_(0.01, 0.99)
        mu1.grad.zero_()

    if step % 5 == 0:
        print(f"  {step:3} : mu={mu1.item():.4f}")

print(f"\nFinal mu = {mu1.item():.4f}")
print(f"Observed fraction = {data.mean():.4f}")
print("-> Fails! Gradients vanish due to underflow")

response = input("\nPress Enter to continue (or 'q' to quit)...")
if response.lower() == "q":
    exit()

print("\nAttempt 2: Gradient ascent on log-likelihood (direct mu optimization)")
mu2 = torch.tensor([0.3], requires_grad=True)
print(f"Initial mu = {mu2.item():.4f}")

for step in range(50):
    # Log-likelihood
    ll = torch.sum(x * torch.log(mu2) + (1 - x) * torch.log(1 - mu2))
    ll.backward()

    with torch.no_grad():
        mu2 += 0.000001 * mu2.grad  # maximize ll
        mu2.clamp_(0.001, 0.999)  # constrain to (0,1)
        mu2.grad.zero_()

    if step % 5 == 0:
        print(f"  {step:3} : mu={mu2.item():.4f}")

print(f"\nFinal mu = {mu2.item():.4f}")
print(f"Observed fraction = {data.mean():.4f}")
print("-> Works, but requires manual clamping to keep mu in (0,1)")

response = input("\nPress Enter to continue (or 'q' to quit)...")
if response.lower() == "q":
    exit()

print("\nAttempt 3: Logit parameterization (unconstrained optimization)")
logit = torch.tensor(
    [np.log(0.3 / 0.7)], requires_grad=True
)  # log(mu/(1-mu)) for mu=0.3
print(f"Initial mu = {torch.sigmoid(logit).item():.4f}, logit = {logit.item():.3f}")

for step in range(50):
    mu = torch.sigmoid(logit)  # mu = 1/(1+exp(-logit))
    ll = torch.sum(x * torch.log(mu) + (1 - x) * torch.log(1 - mu))
    ll.backward()

    with torch.no_grad():
        logit += 0.01 * logit.grad  # maximize ll (no clamping needed!)
        logit.grad.zero_()

    if step % 5 == 0:
        print(f"  {step:3} : mu={mu.item():.4f}, logit={logit.item():.3f}")

mu_final = torch.sigmoid(logit).item()
print(f"\nFinal mu = {mu_final:.4f}, logit = {logit.item():.3f}")
print(f"Observed fraction = {data.mean():.4f}")
print("-> Best! Logit is unconstrained (-∞,+∞), no clamping needed")
