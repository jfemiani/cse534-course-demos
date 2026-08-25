"""
Sampling new faces: fit the same mean/covariance Gaussian as
13.1_eigenfaces_plot.py, keep only the top-k eigenfaces (largest variance),
and draw z ~ N(0, I) to synthesize new faces via x = mu + R @ (S * z) --
equation (7.9) applied to images, with A = R @ diag(S) built from the
eigendecomposition of Sigma (equation 7.12).

z is drawn from a *truncated* standard normal (clipped to +/- TRUNC std
devs) rather than a full N(0, I). A small fraction of z's land far out in
the tails, and those draws produce faces that look noisy/unrealistic --
truncating keeps every sample in the dense, high-probability part of the
distribution at the cost of slightly less variety. This is the same
"truncation trick" used in GANs (e.g. BigGAN, StyleGAN) to trade diversity
for sample quality.

Saves the fitted basis (mu, top-k eigenfaces R, top-k std devs S) to
outputs/eigenfaces_basis.npz so other scripts can sample without
recomputing the eigendecomposition, and produces a 3x3 sampled-faces grid
next to a 3x3 grid of real faces for comparison.

Set PLOT_THEME=dark for a slide-friendly dark background (default is light, for Canvas).
"""
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
from eigenfaces_common import load_faces
from scipy.stats import truncnorm
from torchvision.utils import make_grid

dark = os.environ.get("PLOT_THEME", "light").lower() == "dark"
plt.style.use("dark_background" if dark else "default")
suffix = "_dark" if dark else ""

K = 150  # keep the top-k eigenfaces; the rest mostly capture noise
N_SHOW = 9  # 3x3 grid
TRUNC = 0.8  # clip z to +/- this many std devs -- keeps samples in the dense part of N(0, I)

X, h, w = load_faces()
n_samples = X.shape[0]

mu = X.mean(axis=0)
V = X - mu
Sigma = (V.T @ V) / n_samples

print(f"Computing the top {K} eigenfaces...")
eigenvalues, eigenvectors = np.linalg.eigh(Sigma)
order = np.argsort(eigenvalues)[::-1][:K]
R = eigenvectors[:, order]  # (n_pixels, K): top-k eigenfaces, columns of R
S = np.sqrt(np.clip(eigenvalues[order], 0, None))  # (K,): std dev along each eigenface

output_dir = Path(__file__).resolve().parent / "outputs"
output_dir.mkdir(exist_ok=True)
np.savez(output_dir / "eigenfaces_basis.npz", mu=mu, R=R, S=S, h=h, w=w)
print(f"Saved fitted basis (mu, R, S) to {output_dir / 'eigenfaces_basis.npz'}")

rng = np.random.default_rng(42)
z = truncnorm.rvs(-TRUNC, TRUNC, size=(N_SHOW, K), random_state=rng)
sampled = mu + (z * S) @ R.T  # x = mu + A z, with A = R diag(S)

real = X[rng.choice(n_samples, N_SHOW, replace=False)]


def to_grid(faces):
    imgs = faces.reshape(-1, 1, h, w).copy()
    imgs_t = torch.from_numpy(imgs).float()
    p_min = imgs_t.amin(dim=(2, 3), keepdim=True)
    p_max = imgs_t.amax(dim=(2, 3), keepdim=True)
    imgs_t = (imgs_t - p_min) / (p_max - p_min + 1e-8)
    return make_grid(imgs_t, nrow=3, padding=2, pad_value=1.0)[0].numpy()


fig, (ax_sampled, ax_real) = plt.subplots(
    1, 2, figsize=(8, 4.3), constrained_layout=True,
)
ax_sampled.imshow(to_grid(sampled), cmap="gray")
ax_sampled.set_title(f"Sampled faces (top {K} eigenfaces)")
ax_sampled.axis("off")

ax_real.imshow(to_grid(real), cmap="gray")
ax_real.set_title("Real faces")
ax_real.axis("off")

out_path = output_dir / f"sampled_faces_grid{suffix}.png"
fig.savefig(out_path, dpi=200)
plt.close(fig)
print(f"Saved figure to {out_path}")
