"""
Generate the covariance ellipse figure for the multivariate normal lesson page.
Compares diagonal (independent) vs correlated covariance as ellipses.

Set PLOT_THEME=dark for a slide-friendly dark background (default is light, for Canvas).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt
import numpy as np

from plot_theme import apply_theme, point_colors

colors = apply_theme()

rng = np.random.default_rng(42)

mu = np.array([5.0, 3.0])

Sigma_diag = np.array([[4.0, 0.0],
                       [0.0, 1.0]])

Sigma_corr = np.array([[4.0, 1.8],
                       [1.8, 1.0]])


def covariance_ellipse(ax, mean, cov, n_std=2.0, **kwargs):
    """Draw an ellipse showing the n_std confidence region of a 2D Gaussian."""
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues, eigenvectors = eigenvalues[order], eigenvectors[:, order]

    angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))
    width, height = 2 * n_std * np.sqrt(eigenvalues)

    from matplotlib.patches import Ellipse
    ellipse = Ellipse(xy=mean, width=width, height=height, angle=angle, **kwargs)
    ax.add_patch(ellipse)

    # Draw principal axes
    for i in range(2):
        direction = eigenvectors[:, i] * n_std * np.sqrt(eigenvalues[i])
        ax.plot([mean[0], mean[0] + direction[0]], [mean[1], mean[1] + direction[1]],
                color=colors["fg"], linewidth=1.5)


output_dir = Path(__file__).resolve().parent / "outputs"
output_dir.mkdir(exist_ok=True)

fig, axes = plt.subplots(1, 2, figsize=(11, 5.2), constrained_layout=True)

for ax, Sigma, title in zip(
    axes,
    [Sigma_diag, Sigma_corr],
    ["Diagonal covariance: axis-aligned ellipse", "Correlated covariance: rotated ellipse"],
):
    samples = rng.multivariate_normal(mu, Sigma, size=400)
    ax.scatter(samples[:, 0], samples[:, 1], s=14, alpha=0.8, c=point_colors(samples, center=mu))
    covariance_ellipse(ax, mu, Sigma, n_std=2.0, facecolor="none", edgecolor=colors["accent"], linewidth=2.5)
    ax.plot(*mu, marker="+", color=colors["fg"], markersize=14, markeredgewidth=2)
    ax.set_title(title, fontsize=11)
    ax.set_xlabel("x1")
    ax.set_ylabel("x2")
    ax.set_xlim(-2, 12)
    ax.set_ylim(-3, 9)
    ax.set_aspect("equal")

out_path = output_dir / f"covariance_ellipses{colors['suffix']}.png"
fig.savefig(out_path, dpi=200, facecolor=colors["bg"])
plt.close(fig)
print(f"Saved figure to {out_path}")
