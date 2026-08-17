"""
Gaussian Regression
Generate line + Gaussian noise, fit by least squares, connect to likelihood.
"""
import numpy as np

rng = np.random.default_rng(42)

# True parameters
beta0_true = 2.0  # intercept
beta1_true = 3.0  # slope
sigma_true = 1.5  # noise std dev

# Generate data: Y = beta0 + beta1 * X + epsilon
n = 50
X = rng.uniform(0, 10, n)
epsilon = rng.normal(0, sigma_true, n)  # Gaussian noise
Y = beta0_true + beta1_true * X + epsilon

print("Generated regression data:")
print(f"  True line: Y = {beta0_true} + {beta1_true} * X + noise")
print(f"  Noise std dev: {sigma_true}")
print(f"  Sample size: {n}")
print()

# Fit by least squares (minimize sum of squared residuals)
X_mean = X.mean()
Y_mean = Y.mean()

beta1_hat = ((X - X_mean) * (Y - Y_mean)).sum() / ((X - X_mean)**2).sum()
beta0_hat = Y_mean - beta1_hat * X_mean

print("Least squares fit:")
print(f"  Estimated line: Y = {beta0_hat:.4f} + {beta1_hat:.4f} * X")
print()

# Calculate residuals
Y_pred = beta0_hat + beta1_hat * X
residuals = Y - Y_pred
sse = (residuals**2).sum()

print("Residuals:")
print(f"  Sum of squared residuals: {sse:.4f}")
print(f"  Mean squared error: {sse/n:.4f}")
print()

print("Connection to Gaussian likelihood:")
print("  For Gaussian errors with fixed variance, maximizing likelihood")
print("  is equivalent to minimizing sum of squared residuals.")
print("  This is why normal errors -> least squares regression.")
