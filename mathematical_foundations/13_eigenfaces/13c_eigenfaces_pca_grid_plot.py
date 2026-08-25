"""
PCA for dimension reduction: project each face onto its top 2 principal
components, then tile a 15x15 grid over that 2D space, showing the face
closest to each cell's center.

This is the same eigenface basis from 13b_eigenfaces_plot.py, but instead of
looking at the eigenfaces themselves, it shows what the first two principal
component scores actually encode -- moving across the grid should trace out
a smooth change in some visual attribute (lighting, pose, expression).

Set PLOT_THEME=dark for a slide-friendly dark background (default is light, for Canvas).
"""
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from eigenfaces_common import grid_mosaic, load_faces, scatter_with_grid_panel

dark = os.environ.get("PLOT_THEME", "light").lower() == "dark"
plt.style.use("dark_background" if dark else "default")
accent = "#ff6b6b" if dark else "#941728"
fg = "white" if dark else "black"
suffix = "_dark" if dark else ""

X, h, w = load_faces()
n_samples = X.shape[0]

mu = X.mean(axis=0)
V = X - mu
Sigma = (V.T @ V) / n_samples

print("Computing the top 2 principal components...")
eigenvalues, eigenvectors = np.linalg.eigh(Sigma)
order = np.argsort(eigenvalues)[::-1]
top2 = eigenvectors[:, order[:2]]
scores = V @ top2  # (n_samples, 2): PCA dimension reduction, pixels -> 2 numbers

n_grid = 15
grid_img, chosen_x, chosen_y = grid_mosaic(scores, X, h, w, n_grid=n_grid)

output_dir = Path(__file__).resolve().parent / "outputs"
output_dir.mkdir(exist_ok=True)

fig, (ax_scatter, ax_grid) = plt.subplots(
    1, 2, figsize=(11, 5.2), constrained_layout=True,
    gridspec_kw={"width_ratios": [1, 1.15]},
)
scatter_with_grid_panel(
    ax_scatter, ax_grid, scores, grid_img, chosen_x, chosen_y, fg, accent, n_grid,
    xlabel="PC1 score", ylabel="PC2 score",
    scatter_title="Every face, projected to 2 dimensions",
    grid_title=f"{n_grid}x{n_grid} grid: nearest face per cell",
)

out_path = output_dir / f"pca_face_grid{suffix}.png"
fig.savefig(out_path, dpi=200)
plt.close(fig)
print(f"Saved figure to {out_path}")
