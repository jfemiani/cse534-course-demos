"""
Generate the scale/rotate/translate figure for the transform-normal lesson page.
Shows the progression from Z ~ N(0, I) to X = mu + R @ S @ Z.
Points are colored by their angle and distance from the origin in the original
standard-normal cloud, so the same point can be tracked through each stage.

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

n = 400
Z = rng.standard_normal((n, 2))

S = np.array([[2.0, 0.0],
              [0.0, 1.0]])

theta = np.pi / 4
R = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta), np.cos(theta)]])

mu = np.array([-2.5, 2.5])  # anti-diagonal translation, so the shifted cloud still fits in view

scaled = (S @ Z.T).T
rotated = (R @ S @ Z.T).T
translated = rotated + mu

# Color each point by its angle and distance from the origin in the ORIGINAL
# standard-normal cloud, so the same point keeps the same color at every stage.
colors_rgb = point_colors(Z, center=(0.0, 0.0))

output_dir = Path(__file__).resolve().parent / "outputs"
output_dir.mkdir(exist_ok=True)

fig, axes = plt.subplots(1, 4, figsize=(16, 4.2), constrained_layout=True)

stages = [
    (Z, "1. Standard normal\nZ ~ N(0, I)"),
    (scaled, "2. Scale by S\nX = S Z"),
    (rotated, "3. Rotate by R\nX = R S Z"),
    (translated, "4. Translate by mu\nX = mu + R S Z"),
]

for ax, (points, title) in zip(axes, stages):
    ax.scatter(points[:, 0], points[:, 1], s=14, alpha=0.85, c=colors_rgb)
    ax.axhline(0, color=theme["fg"], linewidth=0.5, alpha=0.4)
    ax.axvline(0, color=theme["fg"], linewidth=0.5, alpha=0.4)
    ax.set_title(title, fontsize=10)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect("equal")

fig.suptitle("Same points, colored by original angle and distance, tracked through each stage", fontsize=11)
out_path = output_dir / f"transform_normal{theme['suffix']}.png"
fig.savefig(out_path, dpi=200, facecolor=theme["bg"])
plt.close(fig)
print(f"Saved figure to {out_path}")

