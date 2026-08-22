"""
Generate the regression figure for the Gaussian regression lesson page.
This script is separate from the simple demo used for teaching the core idea.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(42)

b_true = 2.0
m_true = 3.0
sigma_true = 1.5
n = 50
X = rng.uniform(0, 10, n)
epsilon = rng.normal(0, sigma_true, n)
Y = b_true + m_true * X + epsilon

X_mean = X.mean()
Y_mean = Y.mean()

m_hat = ((X - X_mean) * (Y - Y_mean)).sum() / ((X - X_mean)**2).sum()
b_hat = Y_mean - m_hat * X_mean

x_grid = np.linspace(0, 10, 200)
y_true = b_true + m_true * x_grid
y_hat = b_hat + m_hat * x_grid

x_vis = np.arange(0.5, 10, 0.5)

output_dir = Path(__file__).resolve().parent / "outputs"
output_dir.mkdir(exist_ok=True)

fig, ax = plt.subplots(figsize=(9, 5.5), constrained_layout=True)
ax.scatter(X, Y, s=30, alpha=0.8, color="#941728", label="observations")
ax.plot(x_grid, y_true, color="black", linestyle="--", linewidth=2, label="true mean")
ax.plot(x_grid, y_hat, color="#1f77b4", linewidth=2.5, label="least-squares fit")

for x0 in x_vis:
    mu = b_true + m_true * x0
    z = np.linspace(mu - 4 * sigma_true, mu + 4 * sigma_true, 500)
    density = np.exp(-0.5 * ((z - mu) / sigma_true) ** 2) / (sigma_true * np.sqrt(2 * np.pi))
    scale = 0.35
    ax.plot(np.full_like(z, x0), z, color="#1f77b4", alpha=0.35, linewidth=1.5)
    ax.plot(x0 + scale * density, z, color="#1f77b4", alpha=0.8, linewidth=1.5)

ax.set_title("Gaussian regression: mean line + vertical Gaussian slices")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend(loc="upper left")

ax2 = ax.twinx()
ax2.set_ylim(ax.get_ylim())
ax2.set_ylabel("z")
ax2.set_yticklabels([])

fig.savefig(output_dir / "gaussian_regression.png", dpi=200)
plt.close(fig)
