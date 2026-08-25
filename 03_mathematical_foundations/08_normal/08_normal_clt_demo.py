"""
Central Limit Theorem Demo
Shows that sample means are approximately normal.
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

rng = np.random.default_rng(42)

NUM_TRIALS = 1000
NUM_SAMPLES_PER_TRIAL = 100

sample_means = []
for _ in range(NUM_TRIALS):
    samples = rng.uniform(0, 1, NUM_SAMPLES_PER_TRIAL)
    sample_means.append(samples.mean())

sample_means = np.array(sample_means)

print(f"Distribution of sample means (n={NUM_SAMPLES_PER_TRIAL}, trials={NUM_TRIALS}):")
print(f"  Mean: {sample_means.mean():.4f}")
print(f"  Std: {sample_means.std():.4f}")

# Create figure
output_dir = Path(__file__).resolve().parent / "outputs"
output_dir.mkdir(exist_ok=True)

plt.style.use('dark_background')
fig, ax = plt.subplots(1, 1, figsize=(8, 5), constrained_layout=True)

# Histogram of sample means
ax.hist(sample_means, bins=30, density=True, alpha=0.75, color="#941728", edgecolor="white", linewidth=0.5)

# Overlay theoretical normal
mu_true = 0.5
sigma_true = 1/np.sqrt(12) / np.sqrt(NUM_SAMPLES_PER_TRIAL)
xs = np.linspace(sample_means.min(), sample_means.max(), 200)
normal_pdf = np.exp(-0.5 * ((xs - mu_true) / sigma_true)**2) / (sigma_true * np.sqrt(2 * np.pi))
ax.plot(xs, normal_pdf, 'w-', linewidth=2, label='Normal fit')

ax.set_title(f"Sample means are approximately normal (n={NUM_SAMPLES_PER_TRIAL})", fontsize=14, color="white")
ax.set_xlabel("Sample mean", fontsize=12, color="white")
ax.set_ylabel("Density", fontsize=12, color="white")
ax.legend()
ax.tick_params(colors='white')
for spine in ax.spines.values():
    spine.set_color('white')

fig.patch.set_facecolor('black')
ax.set_facecolor('black')

fig.savefig(output_dir / "clt_demo.png", dpi=200, facecolor='black')
print(f"Saved: {output_dir / 'clt_demo.png'}")
plt.close(fig)
