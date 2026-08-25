"""
Generate the independent-measurements figure for the multivariate normal lesson:
a joint scatter of two independent Gaussians (equal-aspect, so shape and scale
are directly comparable) flanked by its two 1D marginal density curves, so
students can see the joint density IS the product of the two marginals
(equation 7.1), not just an axis-aligned blob.

Set PLOT_THEME=dark for a slide-friendly dark background (default is light, for Canvas).
"""
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

dark = os.environ.get("PLOT_THEME", "light").lower() == "dark"
plt.style.use("dark_background" if dark else "default")
accent = "#ff6b6b" if dark else "#941728"
suffix = "_dark" if dark else ""

rng = np.random.default_rng(42)


mu = np.array([5.0, 3.0])
Sigma_diag = np.array([[4.0, 0.0],
                       [0.0, 1.0]])
sigma1, sigma2 = np.sqrt(Sigma_diag[0, 0]), np.sqrt(Sigma_diag[1, 1])


def normal_pdf(x, mean, sigma):
    return np.exp(-0.5 * ((x - mean) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))


samples = rng.multivariate_normal(mu, Sigma_diag, size=400)

max_sigma = max(sigma1, sigma2)
x1_grid = np.linspace(mu[0] - 3 * max_sigma, mu[0] + 3 * max_sigma, 200)
x2_grid = np.linspace(mu[1] - 3 * max_sigma, mu[1] + 3 * max_sigma, 200)

output_dir = Path(__file__).resolve().parent / "outputs"
output_dir.mkdir(exist_ok=True)

fig = plt.figure(figsize=(7, 7), constrained_layout=True)
gs = fig.add_gridspec(2, 2, width_ratios=(4, 1), height_ratios=(1, 4),
                       wspace=0.05, hspace=0.05)

ax_main = fig.add_subplot(gs[1, 0])
ax_top = fig.add_subplot(gs[0, 0], sharex=ax_main)
ax_right = fig.add_subplot(gs[1, 1], sharey=ax_main)

# Filled contours of the joint density -- since the measurements are
# independent, this is just the product of the two marginal curves plotted
# above/beside it. More levels make the elliptical shape easier to read than
# a handful of line contours would.
X1, X2 = np.meshgrid(x1_grid, x2_grid)
joint_density = normal_pdf(X1, mu[0], sigma1) * normal_pdf(X2, mu[1], sigma2)
bg_color = "black" if dark else "white"
density_cmap = LinearSegmentedColormap.from_list("density_cmap", [bg_color, accent])
levels = np.linspace(0, joint_density.max(), 12)
ax_main.contourf(X1, X2, joint_density, levels=levels, cmap=density_cmap, alpha=0.75, zorder=1)
ax_main.contour(X1, X2, joint_density, levels=levels, colors=accent, linewidths=0.4, alpha=0.5, zorder=2)
ax_main.scatter(samples[:, 0], samples[:, 1], s=14, alpha=0.85, color=accent,
                edgecolors=bg_color, linewidths=0.3, zorder=3)
ax_main.plot(*mu, marker="+", markersize=14, markeredgewidth=2, color=accent, zorder=4)

ax_main.set_xlabel("x1 (height)")
ax_main.set_ylabel("x2 (diameter)")
# Set the y-limits of the main scatter plot to match the x-limits, so the aspect ratio is equal
ax_main.set_xlim(x1_grid.min(), x1_grid.max())
ax_main.set_ylim(x2_grid.min(), x2_grid.max())
ax_main.set_aspect("equal")

ax_top.plot(x1_grid, normal_pdf(x1_grid, mu[0], sigma1), linewidth=2, color=accent)
ax_top.fill_between(x1_grid, normal_pdf(x1_grid, mu[0], sigma1), alpha=0.2, color=accent)
ax_top.set_ylabel("p(x1)")
ax_top.tick_params(axis="x", labelbottom=False)
ax_top.set_title("Independent measurements: the joint density is the\nproduct of two 1D marginal densities", fontsize=10)

ax_right.plot(normal_pdf(x2_grid, mu[1], sigma2), x2_grid, linewidth=2, color=accent)
ax_right.fill_betweenx(x2_grid, normal_pdf(x2_grid, mu[1], sigma2), alpha=0.2, color=accent)
ax_right.set_xlabel("p(x2)")
ax_right.tick_params(axis="y", labelleft=False)

out_path = output_dir / f"diagonal_density_contours{suffix}.png"
fig.savefig(out_path, dpi=200)
plt.close(fig)
print(f"Saved figure to {out_path}")

