"""
t-SNE: another nonlinear alternative to PCA, popular for revealing clusters
in high-dimensional data. Like UMAP, it preserves local neighborhoods rather
than the global straight-line structure PCA relies on.

Same face dataset and same 15x15 grid-of-nearest-face visualization as
13c_eigenfaces_pca_grid_plot.py, but the 2D coordinates come from t-SNE
instead of the top 2 principal components.

Set PLOT_THEME=dark for a slide-friendly dark background (default is light, for Canvas).
"""
import os
from pathlib import Path

import matplotlib.pyplot as plt
from eigenfaces_common import grid_mosaic, load_faces, scatter_with_grid_panel
from sklearn.manifold import TSNE

dark = os.environ.get("PLOT_THEME", "light").lower() == "dark"
plt.style.use("dark_background" if dark else "default")
accent = "#ff6b6b" if dark else "#941728"
fg = "white" if dark else "black"
suffix = "_dark" if dark else ""

X, h, w = load_faces()

print("Computing t-SNE embedding (this takes a little while)...")
scores = TSNE(n_components=2, init="pca", random_state=42).fit_transform(X)

n_grid = 15
grid_img, chosen_x, chosen_y = grid_mosaic(scores, X, h, w, n_grid=n_grid)

output_dir = Path(__file__).resolve().parent / "outputs"
output_dir.mkdir(exist_ok=True)

fig, (ax_scatter, ax_grid) = plt.subplots(
    1, 2, figsize=(11, 5.2), constrained_layout=True,
    gridspec_kw={"width_ratios": [1, 1.15]},
)
scatter_with_grid_panel(
    ax_scatter, ax_grid, scores, grid_img, chosen_x, chosen_y, fg, accent, n_grid,
    xlabel="t-SNE dimension 1", ylabel="t-SNE dimension 2",
    scatter_title="Every face, embedded by t-SNE",
    grid_title=f"{n_grid}x{n_grid} grid: nearest face per cell",
)

out_path = output_dir / f"tsne_face_grid{suffix}.png"
fig.savefig(out_path, dpi=200)
plt.close(fig)
print(f"Saved figure to {out_path}")
