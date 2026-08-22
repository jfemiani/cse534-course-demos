"""
Generate the diagonal-covariance density figure for the multivariate normal lesson.
Left: 2D contour plot (equal-probability ellipses, axis-aligned) with sample scatter.
Right: the same density as a 3D surface.
Both panels use a DIAGONAL covariance matrix (independent X1, X2).

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


def diagonal_normal_pdf(x1, x2, mu, Sigma):
    var1, var2 = Sigma[0, 0], Sigma[1, 1]
    norm_const = 1.0 / (2 * np.pi * np.sqrt(var1 * var2))
    exponent = -0.5 * (((x1 - mu[0]) ** 2) / var1 + ((x2 - mu[1]) ** 2) / var2)
    return norm_const * np.exp(exponent)


samples = rng.multivariate_normal(mu, Sigma_diag, size=400)

x1_grid = np.linspace(mu[0] - 4, mu[0] + 4, 200)
x2_grid = np.linspace(mu[1] - 4, mu[1] + 4, 200)
X1, X2 = np.meshgrid(x1_grid, x2_grid)
Z = diagonal_normal_pdf(X1, X2, mu, Sigma_diag)

output_dir = Path(__file__).resolve().parent / "outputs"
output_dir.mkdir(exist_ok=True)

fig = plt.figure(figsize=(11, 5), constrained_layout=True)

ax1 = fig.add_subplot(1, 2, 1)
ax1.scatter(samples[:, 0], samples[:, 1], s=12, alpha=0.8, c=point_colors(samples, center=mu))
contours = ax1.contour(X1, X2, Z, levels=6, colors=colors["accent"], linewidths=1.5)
ax1.plot(*mu, marker="+", color=colors["fg"], markersize=14, markeredgewidth=2)
ax1.set_title("Contours: equal-probability ellipses\n(axis-aligned, diagonal covariance)", fontsize=10)
ax1.set_xlabel("x1")
ax1.set_ylabel("x2")
ax1.set_aspect("equal")

ax2 = fig.add_subplot(1, 2, 2, projection="3d")
ax2.plot_surface(X1, X2, Z, cmap="Reds", linewidth=0, antialiased=True, alpha=0.9)
ax2.set_title("Density surface p(x1, x2)", fontsize=10)
ax2.set_xlabel("x1")
ax2.set_ylabel("x2")
ax2.set_zlabel("density")

out_path = output_dir / f"diagonal_density_contours{colors['suffix']}.png"
fig.savefig(out_path, dpi=200, facecolor=colors["bg"])
plt.close(fig)
print(f"Saved figure to {out_path}")
