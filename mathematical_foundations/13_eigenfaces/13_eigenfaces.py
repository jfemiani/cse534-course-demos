"""
Eigenfaces with PCA
Loads face images, computes PCA, shows reconstruction from reduced dimensions.
"""
import numpy as np
from sklearn.datasets import fetch_lfw_people
from sklearn.decomposition import PCA

# Load face dataset (downloads ~200MB first time)
print("Loading face dataset...")
faces = fetch_lfw_people(min_faces_per_person=70, resize=0.4)
X = faces.data  # shape: (n_samples, n_pixels)
n_samples, n_features = X.shape
h, w = faces.images.shape[1], faces.images.shape[2]

print(f"Dataset: {n_samples} faces, {n_features} pixels each ({h}x{w})")
print()

# Fit PCA
n_components = 150
print(f"Fitting PCA with {n_components} components...")
pca = PCA(n_components=n_components, whiten=True)
pca.fit(X)

print(f"Mean face computed (centers the data)")
print(f"Computed {n_components} eigenfaces (principal components)")
print()

# Show variance explained
variance_explained = pca.explained_variance_ratio_[:10]
print("Variance explained by first 10 components:")
for i, var in enumerate(variance_explained):
    print(f"  Component {i+1}: {var:.4f} ({var*100:.2f}%)")
print()

# Cumulative variance
cumsum = pca.explained_variance_ratio_.cumsum()
print(f"Cumulative variance explained by {n_components} components: {cumsum[-1]:.4f}")
print()

# Reconstruct a face with different numbers of components
face_idx = 0
original = X[face_idx]

for k in [10, 50, 150]:
    # Project to k dimensions and reconstruct
    z = pca.transform([original])[:, :k]  # reduced coordinates
    reconstructed = pca.mean_ + z @ pca.components_[:k]
    
    error = np.mean((original - reconstructed[0])**2)
    print(f"Reconstruction with {k} components: MSE = {error:.2f}")

print()
print("PCA pipeline:")
print("  1. Center data by subtracting mean face")
print("  2. Find eigenvectors of covariance matrix (eigenfaces)")
print("  3. Project face onto first k eigenfaces -> k coordinates")
print("  4. Reconstruct: mean + sum(coordinate_i * eigenface_i)")
print()
print("More components -> better reconstruction but less compression")
