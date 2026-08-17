"""
Transform Standard Normal with Scale, Rotate, Translate
Shows x = mu + R * S * z where z ~ N(0, I) gives correlated Gaussian.
"""
import numpy as np

rng = np.random.default_rng(42)

# Standard normal samples (mean 0, identity covariance)
n = 500
Z = rng.standard_normal((n, 2))

print("Standard normal Z ~ N(0, I):")
print(f"  Empirical mean: {Z.mean(axis=0)}")
print(f"  Empirical covariance:")
print(np.cov(Z.T))
print()

# Scale matrix (stretch by different amounts)
S = np.array([[2.0, 0.0],
              [0.0, 1.0]])

print("Scale matrix S (stretches dimension 1 by 2x):")
print(S)
print()

# Rotation matrix (45 degrees = pi/4 radians)
theta = np.pi / 4
R = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta),  np.cos(theta)]])

print(f"Rotation matrix R (theta = 45 degrees):")
print(R)
print()

# Translation vector
mu = np.array([5.0, 3.0])

print(f"Translation vector mu: {mu}")
print()

# Apply transformations: X = mu + R @ S @ Z.T
X = (R @ S @ Z.T).T + mu

print("Transformed X = mu + R * S * Z:")
print(f"  Empirical mean: {X.mean(axis=0)}")
print(f"  Empirical covariance:")
Sigma_empirical = np.cov(X.T)
print(Sigma_empirical)
print()

# Theoretical covariance: Sigma = R S S^T R^T
Sigma_theoretical = R @ S @ S.T @ R.T
print("Theoretical covariance Sigma = R S S^T R^T:")
print(Sigma_theoretical)
print()

print("Interpretation:")
print("  S: Scales along coordinate axes")
print("  R: Rotates the scaled ellipse")
print("  mu: Translates the center")
print("  Result: Elliptical Gaussian with chosen center, scale, and orientation")
