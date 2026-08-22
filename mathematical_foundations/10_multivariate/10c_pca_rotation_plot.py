"""
Generate the "rotate into alignment, scale, rotate back" figure that motivates
eigendecomposition / PCA: Sigma = R D R^T.

Starting from a correlated Gaussian (its ellipse tilted at 45 degrees), this
shows the sequence:
    1. Correlated samples (as given)
    2. Rotate by -theta: aligns the principal axes with the coordinate axes
       (the covariance becomes diagonal in this frame)
    3. Scale along the now axis-aligned principal directions
    4. Rotate by +theta: back to the original orientation, with the new shape

Points are colored by their angle and distance from the mean in the ORIGINAL
(panel 1) frame, so the same point can be tracked through every stage.

Set PLOT_THEME=dark for a slide-friendly dark background (default is light, for Canvas).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt
import numpy as np

from plot_theme import apply_theme, point_colors

theme = apply_theme()

rng = np.random.default_rng(42)

mu = np.array([5.0, 3.0])

# Correlated covariance: eigenvectors at +/- 45 degrees from the axes.
Sigma_corr = np.array([[4.0, 1.8],
                       [1.8, 1.0]])

eigenvalues, eigenvectors = np.linalg.eigh(Sigma_corr)
order = np.argsort(eigenvalues)[::-1]
eigenvalues, eigenvectors = eigenvalues[order], eigenvectors[:, order]
theta = np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0])
R = eigenvectors  # columns are the principal-axis directions

n = 400
samples = rng.multivariate_normal(mu, Sigma_corr, size=n)
centered = samples - mu

# Stage 2: rotate by -theta (i.e., multiply by R^T) to align principal axes with x/y.
aligned = (R.T @ centered.T).T

# Stage 3: scale further along the now axis-aligned principal directions
# (here: stretch the first principal axis, shrink the second, to show that
# scaling only makes clean sense once you're in the aligned frame).
extra_scale = np.array([1.6, 0.5])
scaled = aligned * extra_scale

# Stage 4: rotate back by +theta (multiply by R) to restore the original orientation.
rotated_back = (R @ scaled.T).T + mu

colors_rgb = point_colors(centered, center=(0.0, 0.0))

output_dir = Path(__file__).resolve().parent / "outputs"
output_dir.mkdir(exist_ok=True)

fig, axes = plt.subplots(1, 4, figsize=(16, 4.8), constrained_layout=True)

stages = [
    (centered, f"1. Correlated samples\n(tilted ~{np.degrees(theta):.0f} deg)"),
    (aligned, "2. Rotate by -theta\naligns principal axes"),
    (scaled, "3. Scale along\nprincipal axes"),
    (rotated_back - mu, "4. Rotate by +theta\nback to original orientation"),
]

lim = 8
for ax, (points, title) in zip(axes, stages):
    ax.scatter(points[:, 0], points[:, 1], s=14, alpha=0.85, c=colors_rgb)
    ax.axhline(0, color=theme["fg"], linewidth=0.5, alpha=0.4)
    ax.axvline(0, color=theme["fg"], linewidth=0.5, alpha=0.4)
    ax.set_title(title, fontsize=10)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")

fig.suptitle("Rotate to align, scale, rotate back: the idea behind Sigma = R D R^T", fontsize=11)
out_path = output_dir / f"pca_rotation{theme['suffix']}.png"
fig.savefig(out_path, dpi=200, facecolor=theme["bg"])
plt.close(fig)
print(f"Saved figure to {out_path}")
