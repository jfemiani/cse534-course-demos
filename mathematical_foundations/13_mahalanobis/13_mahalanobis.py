"""
Mahalanobis Distance
Shows how covariance-aware distance differs from Euclidean distance.
"""
import numpy as np

# Mean and covariance
mu = np.array([0.0, 0.0])
Sigma = np.array([[4.0, 0.0],   # high variance in x
                  [0.0, 0.25]])  # low variance in y

print("Distribution: mean =", mu, ", covariance =")
print(Sigma)
print(f"  Variance in x: {Sigma[0,0]} (high)")
print(f"  Variance in y: {Sigma[1,1]} (low)")
print()

# Two points with same Euclidean distance from mean
point_x = np.array([2.0, 0.0])  # displacement along high-variance axis
point_y = np.array([0.0, 0.5])  # displacement along low-variance axis

print("Point A (along high-variance x-axis):", point_x)
print("Point B (along low-variance y-axis):", point_y)
print()

# Euclidean distances
euclidean_x = np.sqrt(((point_x - mu)**2).sum())
euclidean_y = np.sqrt(((point_y - mu)**2).sum())

print("Euclidean distances from mean:")
print(f"  Point A: {euclidean_x:.4f}")
print(f"  Point B: {euclidean_y:.4f}")
print()

# Mahalanobis distances
Sigma_inv = np.linalg.inv(Sigma)
mahalanobis_x = np.sqrt((point_x - mu) @ Sigma_inv @ (point_x - mu))
mahalanobis_y = np.sqrt((point_y - mu) @ Sigma_inv @ (point_y - mu))

print("Mahalanobis distances from mean:")
print(f"  Point A: {mahalanobis_x:.4f} (smaller -- displacement along high-variance direction)")
print(f"  Point B: {mahalanobis_y:.4f} (larger -- displacement along low-variance direction)")
print()

print("Interpretation:")
print("  Euclidean distance treats all directions equally.")
print("  Mahalanobis distance accounts for variance in each direction.")
print("  A 2-unit shift in x is less unusual than a 0.5-unit shift in y")
print("  because x naturally varies more.")
