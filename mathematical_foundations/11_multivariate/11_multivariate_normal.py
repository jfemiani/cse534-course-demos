"""
Multivariate Normal Distributions
Compare diagonal (independent) vs correlated covariance matrices.
"""
import numpy as np

rng = np.random.default_rng(42)

# Mean vector
mu = np.array([5.0, 3.0])

# Diagonal covariance (independent variables)
Sigma_diag = np.array([[4.0, 0.0],
                       [0.0, 1.0]])

print("Diagonal covariance (independent):")
print(Sigma_diag)
print(f"  Variance in dimension 1: {Sigma_diag[0,0]}")
print(f"  Variance in dimension 2: {Sigma_diag[1,1]}")
print(f"  Covariance: {Sigma_diag[0,1]} (zero means independent)")
print()

# Sample from diagonal covariance
samples_diag = rng.multivariate_normal(mu, Sigma_diag, size=500)
print(f"Diagonal samples empirical covariance:")
print(np.cov(samples_diag.T))
print()

# Correlated covariance
Sigma_corr = np.array([[4.0, 1.8],
                       [1.8, 1.0]])

print("Correlated covariance:")
print(Sigma_corr)
print(f"  Variance in dimension 1: {Sigma_corr[0,0]}")
print(f"  Variance in dimension 2: {Sigma_corr[1,1]}")
print(f"  Covariance: {Sigma_corr[0,1]} (positive means tend to increase together)")
print()

# Sample from correlated covariance
samples_corr = rng.multivariate_normal(mu, Sigma_corr, size=500)
print(f"Correlated samples empirical covariance:")
print(np.cov(samples_corr.T))
print()

print("Visualization as ellipse:")
print("  Diagonal covariance: Axis-aligned ellipse")
print("  Correlated covariance: Rotated ellipse (principal axes not aligned with coordinates)")
