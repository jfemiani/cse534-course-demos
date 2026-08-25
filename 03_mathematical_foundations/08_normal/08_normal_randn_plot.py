"""
Generate the lesson figure for the standard-normal-to-shifted-normal example.
This script is intentionally separate from the simple demo code used in class.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(42)
Z = rng.standard_normal(1000)
mu = 5.0
sigma = 2.0
X = mu + sigma * Z

xs = np.linspace(-4, 10, 500)
standard_pdf = np.exp(-0.5 * xs**2) / np.sqrt(2 * np.pi)
shifted_pdf = np.exp(-0.5 * ((xs - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))

output_dir = Path(__file__).resolve().parent / "outputs"
output_dir.mkdir(exist_ok=True)

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True, constrained_layout=True)

# Center axes on 0 and mu respectively
z_range = max(abs(Z.min()), abs(Z.max()))
x_range = max(abs(X.min() - mu), abs(X.max() - mu))

axes[0].hist(Z, bins=35, density=True, alpha=0.75, color="#941728", edgecolor="black")
axes[0].plot(xs, standard_pdf, color="black", linewidth=2)
axes[0].set_title("Standard normal: Z ~ N(0, 1)")
axes[0].set_xlabel("z")
axes[0].set_ylabel("Density")
axes[0].set_xlim(-z_range * 1.1, z_range * 1.1)
axes[0].axvline(0, color="black", linestyle="--", linewidth=1)

axes[1].hist(X, bins=35, density=True, alpha=0.75, color="#941728", edgecolor="black")
axes[1].plot(xs, shifted_pdf, color="black", linewidth=2)
axes[1].set_title("Shifted normal: X = 5 + 2Z")
axes[1].set_xlabel("x")
axes[1].set_ylabel("Density")
axes[1].set_xlim(mu - x_range * 1.1, mu + x_range * 1.1)
axes[1].axvline(mu, color="black", linestyle="--", linewidth=1)

for ax in axes:
    ax.set_ylim(0, max(standard_pdf.max(), shifted_pdf.max()) * 1.2)

fig.suptitle("Linear transformation of a Gaussian")
fig.savefig(output_dir / "normal_shift.png", dpi=200)
plt.close(fig)
