"""
Eigenfaces: fit a multivariate Gaussian (mean + covariance) to face images,
using nothing more than equations (7.6) and (7.12) from the lesson.

Produces a single three-panel figure:
  1. The mean face (mu-hat)
  2. The top 16 eigenfaces -- the principal axes of Sigma, reshaped back
     into images and laid out with torchvision.utils.make_grid
  3. Cumulative variance explained, with a line marking 90%

Each eigenface is min-max normalized to [0, 1] on its own before display,
since an eigenvector's sign and scale are arbitrary -- only the spatial
pattern of light and dark it captures is meaningful.

Set PLOT_THEME=dark for a slide-friendly dark background (default is light, for Canvas).
"""
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
from sklearn.datasets import fetch_lfw_people
from torchvision.utils import make_grid

dark = os.environ.get("PLOT_THEME", "light").lower() == "dark"
plt.style.use("dark_background" if dark else "default")
accent = "#ff6b6b" if dark else "#941728"
suffix = "_dark" if dark else ""

print("Loading face dataset (downloads ~200MB the first time)...")
faces = fetch_lfw_people(min_faces_per_person=70, resize=0.4)
X = faces.data  # (n_samples, n_pixels): rows are samples, matching V in eq (7.6)
n_samples, n_features = X.shape
h, w = faces.images.shape[1], faces.images.shape[2]
print(f"{n_samples} faces, {n_features} pixels each ({h}x{w})")

mu = X.mean(axis=0)  # eq (7.12)
V = X - mu
Sigma = (V.T @ V) / n_samples  # eq (7.6): (1/n) V^T V

print("Computing eigenfaces (eigh on the pixel covariance matrix)...")
eigenvalues, eigenvectors = np.linalg.eigh(Sigma)
order = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[order]
eigenvectors = eigenvectors[:, order]  # columns are eigenfaces, most variance first

explained = eigenvalues / eigenvalues.sum()
cumulative = np.cumsum(explained)
k90 = int(np.searchsorted(cumulative, 0.90) + 1)
print(f"90% of variance is captured by the first {k90} components")

# Top-16 eigenfaces as a 4x4 grid via torchvision
n_show = 16
patches = eigenvectors[:, :n_show].T.reshape(n_show, 1, h, w).copy()
patches_t = torch.from_numpy(patches).float()
p_min = patches_t.amin(dim=(2, 3), keepdim=True)
p_max = patches_t.amax(dim=(2, 3), keepdim=True)
patches_t = (patches_t - p_min) / (p_max - p_min + 1e-8)
grid_img = make_grid(patches_t, nrow=4, padding=2, pad_value=1.0)[0].numpy()

output_dir = Path(__file__).resolve().parent / "outputs"
output_dir.mkdir(exist_ok=True)

fig, (ax_mean, ax_grid, ax_var) = plt.subplots(
    1, 3, figsize=(11, 4), constrained_layout=True,
    gridspec_kw={"width_ratios": [1, 1.3, 1.5]},
)

ax_mean.imshow(mu.reshape(h, w), cmap="gray")
ax_mean.set_title("Mean face")
ax_mean.axis("off")

ax_grid.imshow(grid_img, cmap="gray")
ax_grid.set_title(f"Top {n_show} eigenfaces")
ax_grid.axis("off")

components = np.arange(1, len(cumulative) + 1)
ax_var.plot(components, cumulative, color=accent)
ax_var.axhline(0.90, color=accent, linestyle="--", linewidth=1)
ax_var.axvline(k90, color=accent, linestyle=":", linewidth=1)
ax_var.set_xlabel("Number of components (k)")
ax_var.set_ylabel("Cumulative variance explained")
ax_var.set_title(f"90% at k = {k90}")
ax_var.set_xlim(1, len(cumulative))
ax_var.set_ylim(0, 1.02)

out_path = output_dir / f"eigenfaces_summary{suffix}.png"
fig.savefig(out_path, dpi=200)
plt.close(fig)
print(f"Saved figure to {out_path}")
