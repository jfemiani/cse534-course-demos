"""
Generate a box diagram showing why (RS)^T = S^T R^T, not R^T S^T.

Style follows the classic "matrix decomposition dimensions diagram" convention
(https://tex.stackexchange.com/questions/168035/matrix-decomposition-dimensions-diagram):
each matrix is drawn as a box whose height is its row count and whose width is
its column count, with the shape labeled below the box.

Uses R (m x n) and S (n x p) with m=7, n=4, p=5, matching the R/S notation
already used for the rotation and scale matrices earlier in the lesson.

Set PLOT_THEME=dark for a slide-friendly dark background (default is light, for Canvas).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from plot_theme import apply_theme

theme = apply_theme()

UNIT = 0.22  # inches per row/column, so boxes are drawn to scale


def box(ax, x, y_top, rows, cols, label, color, dashed=False):
    """Draw a matrix box with top-left corner (x, y_top). Returns (width, height)."""
    w, h = cols * UNIT, rows * UNIT
    ax.add_patch(Rectangle((x, y_top - h), w, h, facecolor=color, edgecolor=theme["fg"],
                            linewidth=1.5, alpha=0.25,
                            linestyle="--" if dashed else "-"))
    ax.text(x + w / 2, y_top - h / 2, label, ha="center", va="center",
            fontsize=13, color=theme["fg"], fontweight="bold")
    ax.text(x + w / 2, y_top - h - 0.14, f"{rows}\u00d7{cols}", ha="center", va="top",
            fontsize=10, color=theme["fg"])
    return w, h


def symbol(ax, x, y_top, row_h, text, color=None, fontsize=18, ha="center"):
    ax.text(x, y_top - row_h / 2, text, ha=ha, va="center", fontsize=fontsize,
            color=color or theme["fg"], fontweight="bold")


m, n, p = 7, 4, 5  # R is m x n, S is n x p

fig, ax = plt.subplots(figsize=(9.5, 6.2), facecolor=theme["bg"])
ax.set_facecolor(theme["bg"])
ax.axis("off")

accent = theme["accent"]
ok_color = "#2e7d32" if theme["fg"] == "black" else "#66d17a"
bad_color = "#c62828" if theme["fg"] == "black" else "#ff6b6b"

title_gap = 0.28   # space from title text down to box top
dim_label_gap = 0.3  # space reserved below a row for the "rows x cols" labels
row_gap = 0.25     # extra space between one row's labels and the next row's title

cursor = 0.0  # running top-of-content y, decreases as rows are added

# --- Row 1: R S = RS, then transpose it ---------------------------------
cursor -= title_gap
ax.text(0.0, cursor, "R S and its transpose", fontsize=12,
        color=theme["fg"], fontweight="bold", va="top")
cursor -= title_gap
row_top = cursor
x = 0.0
w, h = box(ax, x, row_top, m, n, "R", accent)
x += w + 0.2
symbol(ax, x, row_top, m * UNIT, "\u00d7")
x += 0.3
w2, h2 = box(ax, x, row_top, n, p, "S", accent)
x += w2 + 0.2
symbol(ax, x, row_top, m * UNIT, "=")
x += 0.3
w3, h3 = box(ax, x, row_top, m, p, "RS", ok_color)
x += w3 + 0.55
symbol(ax, x, row_top, m * UNIT, "\u27f6 transpose \u27f6", fontsize=11)
x += 1.3
box(ax, x, row_top, p, m, "(RS)\u1d40", ok_color)
cursor = row_top - m * UNIT - dim_label_gap - row_gap

# --- Row 2: R^T S^T does not fit (wrong order) --------------------------
cursor -= title_gap
ax.text(0.0, cursor, "R\u1d40 S\u1d40 \u2014 wrong order: shapes do not agree",
        fontsize=12, color=theme["fg"], fontweight="bold", va="top")
cursor -= title_gap
row_top = cursor
row_h = max(n, p) * UNIT
x = 0.0
w, h = box(ax, x, row_top, n, m, "R\u1d40", accent, dashed=True)
x += w + 0.2
symbol(ax, x, row_top, row_h, "\u00d7", color=bad_color)
x += 0.3
w2, h2 = box(ax, x, row_top, p, n, "S\u1d40", accent, dashed=True)
x += w2 + 0.55
symbol(ax, x, row_top, row_h, "\u2717", color=bad_color, fontsize=22)
x += 0.5
ax.text(x, row_top - row_h / 2, f"{m} cols \u2260 {p} rows", fontsize=11,
        color=bad_color, va="center", ha="left")
cursor = row_top - row_h - dim_label_gap - row_gap

# --- Row 3: S^T R^T fits (correct order) --------------------------------
cursor -= title_gap
ax.text(0.0, cursor, "S\u1d40 R\u1d40 \u2014 correct order: matches (RS)\u1d40",
        fontsize=12, color=theme["fg"], fontweight="bold", va="top")
cursor -= title_gap
row_top = cursor
row_h = max(p, n) * UNIT
x = 0.0
w, h = box(ax, x, row_top, p, n, "S\u1d40", accent)
x += w + 0.2
symbol(ax, x, row_top, row_h, "\u00d7")
x += 0.3
w2, h2 = box(ax, x, row_top, n, m, "R\u1d40", accent)
x += w2 + 0.2
symbol(ax, x, row_top, row_h, "=")
x += 0.3
box(ax, x, row_top, p, m, "(RS)\u1d40", ok_color)
cursor = row_top - row_h - dim_label_gap

ax.set_xlim(-0.3, 6.5)
ax.set_ylim(cursor - 0.1, 0.1)
ax.set_aspect("equal")

fig.tight_layout()

output_dir = Path(__file__).resolve().parent / "outputs"
output_dir.mkdir(exist_ok=True)
fig.savefig(output_dir / f"transpose_shapes{theme['suffix']}.png", dpi=200,
            facecolor=theme["bg"])
print(f"Saved transpose_shapes{theme['suffix']}.png")
