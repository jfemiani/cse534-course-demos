"""
Transform Standard Normal Samples
Shows X = mu + sigma * Z where Z ~ N(0,1) gives X ~ N(mu, sigma^2).
"""
import numpy as np

rng = np.random.default_rng(42)

# Sample from standard normal
Z = rng.standard_normal(1000)

print("Standard normal samples Z ~ N(0, 1):")
print(f"  Mean: {Z.mean():.4f} (should be ~0)")
print(f"  Variance: {Z.var():.4f} (should be ~1)")
print(f"  Std dev: {Z.std():.4f} (should be ~1)")
print()

# Transform to N(5, 4) -- mean=5, variance=4, std=2
mu = 5.0
sigma = 2.0  # std dev, so variance = 4

X = mu + sigma * Z

print(f"Transformed samples X = {mu} + {sigma} * Z:")
print(f"  Mean: {X.mean():.4f} (should be ~{mu})")
print(f"  Variance: {X.var():.4f} (should be ~{sigma**2})")
print(f"  Std dev: {X.std():.4f} (should be ~{sigma})")
print()

print("The transformation X = mu + sigma * Z:")
print("  - Multiplying by sigma scales the spread")
print("  - Adding mu shifts the center")
print("  - Works because normal distributions are closed under linear transformations")
