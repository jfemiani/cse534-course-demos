"""Shared helpers for the eigenfaces demo scripts (13b-13e): loading the face
dataset once, and building the 15x15 "nearest face per grid cell" mosaic used
by the PCA, UMAP, and t-SNE dimension-reduction visualizations.
"""
import numpy as np
import torch
from sklearn.datasets import fetch_lfw_people
from torchvision.utils import make_grid


def load_faces():
    """Load the LFW face dataset. Returns (X, h, w): X is (n_samples, n_pixels)."""
    print("Loading face dataset (downloads ~200MB the first time)...")
    faces = fetch_lfw_people(min_faces_per_person=70, resize=0.4)
    X = faces.data
    h, w = faces.images.shape[1], faces.images.shape[2]
    print(f"{X.shape[0]} faces, {X.shape[1]} pixels each ({h}x{w})")
    return X, h, w


def grid_mosaic(scores, X, h, w, n_grid=15):
    """Tile a 2D embedding into an n_grid x n_grid mosaic, showing the face
    closest to each cell's center (blank if a cell contains no faces).

    Returns (grid_image, chosen_x, chosen_y): the mosaic as a single 2D array,
    and the embedding coordinates of the faces actually shown.
    """
    x_edges = np.linspace(scores[:, 0].min(), scores[:, 0].max(), n_grid + 1)
    y_edges = np.linspace(scores[:, 1].min(), scores[:, 1].max(), n_grid + 1)
    x_centers = (x_edges[:-1] + x_edges[1:]) / 2
    y_centers = (y_edges[:-1] + y_edges[1:]) / 2

    x_bin = np.digitize(scores[:, 0], x_edges[1:-1])
    y_bin = np.digitize(scores[:, 1], y_edges[1:-1])

    tiles = np.ones((n_grid, n_grid, h, w))
    chosen_x, chosen_y = [], []
    for xb in range(n_grid):
        for yb in range(n_grid):
            candidates = np.where((x_bin == xb) & (y_bin == yb))[0]
            if len(candidates) == 0:
                continue
            xc, yc = x_centers[xb], y_centers[yb]
            dists = np.hypot(scores[candidates, 0] - xc, scores[candidates, 1] - yc)
            best = candidates[np.argmin(dists)]
            img = X[best].reshape(h, w)
            row = n_grid - 1 - yb  # flip so high y is at the top of the mosaic
            tiles[row, xb] = (img - img.min()) / (img.max() - img.min() + 1e-8)
            chosen_x.append(scores[best, 0])
            chosen_y.append(scores[best, 1])

    tiles_t = torch.from_numpy(tiles.reshape(-1, 1, h, w)).float()
    grid_img = make_grid(tiles_t, nrow=n_grid, padding=1, pad_value=1.0)[0].numpy()
    return grid_img, np.array(chosen_x), np.array(chosen_y)


def scatter_with_grid_panel(
    ax_scatter, ax_grid, scores, grid_img, chosen_x, chosen_y, fg, accent, n_grid,
    xlabel, ylabel, scatter_title, grid_title,
):
    """Draw the standard two-panel layout: scatter + grid lines on the left,
    the resulting mosaic on the right.
    """
    x_edges = np.linspace(scores[:, 0].min(), scores[:, 0].max(), n_grid + 1)
    y_edges = np.linspace(scores[:, 1].min(), scores[:, 1].max(), n_grid + 1)

    ax_scatter.scatter(scores[:, 0], scores[:, 1], s=6, alpha=0.35, color=fg)
    # ax_scatter.scatter(chosen_x, chosen_y, s=18, color=accent, zorder=3)
    for xe in x_edges:
        ax_scatter.axvline(xe, color=fg, alpha=0.15, linewidth=0.5)
    for ye in y_edges:
        ax_scatter.axhline(ye, color=fg, alpha=0.15, linewidth=0.5)
    ax_scatter.set_xlabel(xlabel)
    ax_scatter.set_ylabel(ylabel)
    ax_scatter.set_title(scatter_title)

    ax_grid.imshow(grid_img, cmap="gray")
    ax_grid.set_title(grid_title)
    ax_grid.axis("off")
