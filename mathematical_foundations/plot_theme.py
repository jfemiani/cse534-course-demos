"""
Shared plotting theme helper for course demo figures.

Controlled by the PLOT_THEME environment variable:
    PLOT_THEME=light (default) -- white background, for Canvas pages
    PLOT_THEME=dark            -- black background, for slides

Usage:
    from plot_theme import apply_theme, point_colors
    colors = apply_theme()
    ...
    fig.savefig(output_dir / f"myplot{colors['suffix']}.png", dpi=200, facecolor=colors['bg'])
"""
import os

import matplotlib.pyplot as plt
import numpy as np


def theme_name():
    """Return 'light' or 'dark' based on the PLOT_THEME environment variable."""
    return os.environ.get("PLOT_THEME", "light").lower()


def apply_theme():
    """Apply the matplotlib style for the current theme.

    Returns a dict with:
        fg      -- foreground color for text/axes
        accent  -- accent color for highlighted elements (curves, ellipses)
        bg      -- figure/axes background color
        suffix  -- filename suffix to use when saving ("" for light, "_dark" for dark)
    """
    if theme_name() == "dark":
        plt.style.use("dark_background")
        return {"fg": "white", "accent": "#ff6b6b", "bg": "black", "suffix": "_dark"}

    plt.style.use("default")
    return {"fg": "black", "accent": "#941728", "bg": "white", "suffix": ""}


def point_colors(points, center=(0.0, 0.0)):
    """Color points by polar position around `center` so the same point keeps
    the same color across multiple plots/transformation stages.

    Hue encodes the angle from `center` (so opposite directions look distinct).
    Saturation encodes distance from `center` (closer points are paler).

    Returns an (N, 3) array of RGB values suitable for `scatter(..., c=...)`.
    """
    from matplotlib.colors import hsv_to_rgb

    dx = points[:, 0] - center[0]
    dy = points[:, 1] - center[1]
    angle = np.arctan2(dy, dx)
    hue = (angle + np.pi) / (2 * np.pi)

    dist = np.sqrt(dx**2 + dy**2)
    d_max = dist.max() if dist.max() > 0 else 1.0
    saturation = 0.35 + 0.65 * (dist / d_max)

    value = np.ones_like(hue)
    hsv = np.stack([hue, saturation, value], axis=1)
    return hsv_to_rgb(hsv)
