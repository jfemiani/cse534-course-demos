"""Sample a continuous uniform distribution and inspect the samples."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Keeping the seed fixed makes the demonstration reproducible. Students who
# change the seed will see different individual samples but the same pattern.
SEED = 7
SAMPLE_SIZE = 10_000
LOWER_BOUND = 0.0
UPPER_BOUND = 1.0
BIN_COUNT = 10

# NumPy's generator produces the random values used in this demonstration.
rng = np.random.default_rng(seed=SEED)
samples = rng.uniform(LOWER_BOUND, UPPER_BOUND, size=SAMPLE_SIZE)

# A DataFrame gives every generated value a row. This is the same tabular form
# we will use later when generated results have several columns to inspect.
sample_df = pd.DataFrame({"sample": samples})

print("First five generated values:")
print(sample_df.head().to_string(index=False))

# Divide [0, 1) into ten intervals. A uniform distribution assigns the same
# theoretical probability, 1 / BIN_COUNT, to every equal-width interval.
bin_edges = np.linspace(LOWER_BOUND, UPPER_BOUND, BIN_COUNT + 1)
sample_df["interval"] = pd.cut(
    sample_df["sample"],
    bins=bin_edges,
    include_lowest=True,
    right=False,
)

interval_summary = (
    sample_df["interval"]
    .value_counts(sort=False)
    .rename_axis("interval")
    .reset_index(name="count")
)
interval_summary["observed_probability"] = (
    interval_summary["count"] / SAMPLE_SIZE
)
interval_summary["expected_probability"] = 1 / BIN_COUNT

print("\nCounts and probabilities for the ten equal-width intervals:")
print(interval_summary.to_string(index=False))

# Save the plot instead of requiring a graphical window to remain open.
output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)
output_path = output_dir / "01_uniform.png"

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(
    sample_df["sample"],
    bins=bin_edges,
    edgecolor="black",
    color="#9CC3E6",
)
ax.set(
    xlabel="Generated value",
    ylabel="Count",
    title="10,000 samples from Uniform(0, 1)",
)
fig.tight_layout()
fig.savefig(output_path, dpi=160)
plt.close(fig)

print(f"\nSaved histogram to {output_path}")
