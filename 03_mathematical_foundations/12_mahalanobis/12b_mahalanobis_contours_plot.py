"""
Side-by-side comparison of Euclidean vs. Mahalanobis distance contours,
overlaid on samples from a diagonal-covariance Gaussian.

Euclidean contours are circles -- they treat every direction as equally
likely. Mahalanobis contours are ellipses that match the data's spread,
so a contour line passes through equally "typical" points of the
distribution, not just equally distant ones.

Set PLOT_THEME=dark for a slide-friendly dark background (default is light, for Canvas).
"""
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

dark = os.environ.get("PLOT_THEME", "light").lower() == "dark"
plt.style.use("dark_background" if dark else "default")
accent = "#ff6b6b" if dark else "#941728"
suffix = "_dark" if dark else ""

rng = np.random.default_rng(42)

mu = np.array([0.0, 0.0])
sigma1, sigma2 = 2.0, 0.5  # high variance in x, low variance in y

samples = rng.multivariate_normal(mu, np.diag([sigma1**2, sigma2**2]), size=300)

lim = 3 * sigma1
grid = np.linspace(-lim, lim, 200)
X, Y = np.meshgrid(grid, grid)
euclidean = np.sqrt((X - mu[0])**2 + (Y - mu[1])**2)
mahalanobis = np.sqrt(((X - mu[0]) / sigma1)**2 + ((Y - mu[1]) / sigma2)**2)

levels = [1, 2, 3]

output_dir = Path(__file__).resolve().parent / "outputs"
output_dir.mkdir(exist_ok=True)

fig, (ax_euclid, ax_maha) = plt.subplots(1, 2, figsize=(9, 4.5), constrained_layout=True)

for ax, dist, title in (
    (ax_euclid, euclidean, "Euclidean distance"),
    (ax_maha, mahalanobis, "Mahalanobis distance"),
):
    ax.scatter(samples[:, 0], samples[:, 1], s=10, alpha=0.4, color=accent)
    cs = ax.contour(X, Y, dist, levels=levels, colors=accent, linewidths=1.5)
    ax.clabel(cs, levels, fmt="%d")
    ax.plot(*mu, marker="+", markersize=12, markeredgewidth=2, color=accent)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_title(title)
    ax.set_xlabel("x1")

ax_euclid.set_ylabel("x2")

out_path = output_dir / f"mahalanobis_contours{suffix}.png"
fig.savefig(out_path, dpi=200)
plt.close(fig)
print(f"Saved figure to {out_path}")
