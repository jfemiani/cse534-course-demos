"""
Generate the "whitening" figure for the Mahalanobis distance lesson: the
exact reverse of the scale/rotate/translate sampling recipe in
11_transform/11_transform_plot.py.

Starting from a correlated Gaussian X = mu + R S Z, this undoes each step in
turn -- subtract mu, un-rotate by R^T, un-scale by S^-1 -- ending back at an
isotropic standard normal. Each panel draws the covariance ellipse of the
Gaussian at that stage (not just the scatter), so the "unstretching" of the
distribution itself is visible, matching the same R, S, mu used in the
forward recipe figure.

This whitening transform, z = S^-1 R^T (x - mu), is exactly what makes
Mahalanobis distance in the original space equal to ordinary Euclidean
distance in this standardized space.

Set PLOT_THEME=dark for a slide-friendly dark background (default is light, for Canvas).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

from plot_theme import apply_theme, point_colors

theme = apply_theme()

rng = np.random.default_rng(42)

n = 400
Z = rng.standard_normal((n, 2))

# Same S, R, mu as 11_transform/11_transform_plot.py, so this figure is
# recognizably the reverse of that one.
S = np.array([[2.0, 0.0],
              [0.0, 1.0]])

theta = np.pi / 4
R = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta), np.cos(theta)]])

mu = np.array([-2.5, 2.5])

# Forward recipe: X = mu + R S Z
X = (R @ S @ Z.T).T + mu

# Reverse recipe, one step undone at a time:
centered = X - mu                              # = R S Z
unrotated = (R.T @ centered.T).T               # = S Z
unscaled = (np.linalg.inv(S) @ unrotated.T).T  # = Z

# Color by angle and distance in the original standard-normal cloud Z, so the
# same point can be tracked backward through the undoing.
colors_rgb = point_colors(Z, center=(0.0, 0.0))


def covariance_ellipse(ax, mean, cov, n_std=2.0, **kwargs):
    """Draw an ellipse showing the n_std confidence region of a 2D Gaussian."""
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues, eigenvectors = eigenvalues[order], eigenvectors[:, order]
    angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))
    width, height = 2 * n_std * np.sqrt(eigenvalues)
    ellipse = Ellipse(xy=mean, width=width, height=height, angle=angle, **kwargs)
    ax.add_patch(ellipse)


Sigma_full = R @ S @ S.T @ R.T  # covariance of X and of "centered"
Sigma_scaled = S @ S.T          # covariance of "unrotated" -- axis-aligned
Sigma_iso = np.eye(2)           # covariance of "unscaled" -- isotropic

output_dir = Path(__file__).resolve().parent / "outputs"
output_dir.mkdir(exist_ok=True)

fig, axes = plt.subplots(1, 4, figsize=(16, 4.2), constrained_layout=True)

origin = np.zeros(2)
stages = [
    (X, mu, Sigma_full, "1. Correlated X\nX = mu + R S Z"),
    (centered, origin, Sigma_full, "2. Undo translate\nX - mu = R S Z"),
    (unrotated, origin, Sigma_scaled, "3. Undo rotate: $R^T(X-\\mu)$\n= S Z"),
    (unscaled, origin, Sigma_iso, "4. Undo scale: $S^{-1}R^T(X-\\mu)$\n= Z ~ N(0, I)"),
]

for ax, (points, mean, cov, title) in zip(axes, stages):
    covariance_ellipse(ax, mean, cov, n_std=2.0, facecolor="none",
                        edgecolor=theme["accent"], linewidth=2, zorder=2)
    ax.scatter(points[:, 0], points[:, 1], s=14, alpha=0.85, c=colors_rgb, zorder=3)
    ax.plot(*mean, marker="+", markersize=14, markeredgewidth=2, color=theme["fg"], zorder=4)
    ax.axhline(0, color=theme["fg"], linewidth=0.5, alpha=0.3)
    ax.axvline(0, color=theme["fg"], linewidth=0.5, alpha=0.3)
    ax.set_title(title, fontsize=10)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect("equal")

fig.suptitle("Undoing the recipe: each step removes one transformation, ending at an isotropic Gaussian",
             fontsize=11)
out_path = output_dir / f"whitening_recipe{theme['suffix']}.png"
fig.savefig(out_path, dpi=200, facecolor=theme["bg"])
plt.close(fig)
print(f"Saved figure to {out_path}")
