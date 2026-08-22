"""
Generate the slide figure for the standard-normal-to-shifted-normal example.
Black background, vertical stacking, same y-limits.
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

# Dark theme for slides
plt.style.use('dark_background')

# Vertical stacking: 2 rows, 1 column
fig, axes = plt.subplots(2, 1, figsize=(6, 8), sharex=False, constrained_layout=True)

# Calculate consistent y-limit
y_max = max(standard_pdf.max(), shifted_pdf.max()) * 1.2

# Center axes on 0 and mu respectively
z_range = max(abs(Z.min()), abs(Z.max()))
x_range = max(abs(X.min() - mu), abs(X.max() - mu))

# Top plot: Standard normal
axes[0].hist(Z, bins=35, density=True, alpha=0.75, color="#941728", edgecolor="white", linewidth=0.5)
axes[0].plot(xs, standard_pdf, color="white", linewidth=2)
axes[0].set_title("Z ~ N(0, 1)", fontsize=14, color="white")
axes[0].set_xlabel("z", fontsize=12, color="white")
axes[0].set_ylabel("Density", fontsize=12, color="white")
axes[0].set_xlim(-z_range * 1.1, z_range * 1.1)
axes[0].set_ylim(0, y_max)
axes[0].axvline(0, color="white", linestyle="--", linewidth=1, alpha=0.7)
axes[0].tick_params(colors='white')
axes[0].spines['bottom'].set_color('white')
axes[0].spines['left'].set_color('white')
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)

# Bottom plot: Shifted normal
axes[1].hist(X, bins=35, density=True, alpha=0.75, color="#941728", edgecolor="white", linewidth=0.5)
axes[1].plot(xs, shifted_pdf, color="white", linewidth=2)
axes[1].set_title("X = 5 + 2Z ~ N(5, 4)", fontsize=14, color="white")
axes[1].set_xlabel("x", fontsize=12, color="white")
axes[1].set_ylabel("Density", fontsize=12, color="white")
axes[1].set_xlim(mu - x_range * 1.1, mu + x_range * 1.1)
axes[1].set_ylim(0, y_max)
axes[1].axvline(mu, color="white", linestyle="--", linewidth=1, alpha=0.7)
axes[1].tick_params(colors='white')
axes[1].spines['bottom'].set_color('white')
axes[1].spines['left'].set_color('white')
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)

fig.patch.set_facecolor('black')
for ax in axes:
    ax.set_facecolor('black')

fig.savefig(output_dir / "normal_shift_slides.png", dpi=200, facecolor='black')
plt.close(fig)
print(f"Saved: {output_dir / 'normal_shift_slides.png'}")
