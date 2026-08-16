"""Sample a categorical distribution and compare observed category frequencies."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SEED = 7
SAMPLE_SIZE = 10_000

CATEGORIES = np.array(["cat", "dog", "horse"])
PROBABILITIES = np.array([0.50, 0.30, 0.20])

rng = np.random.default_rng(seed=SEED)
samples = rng.choice(CATEGORIES, size=SAMPLE_SIZE, p=PROBABILITIES)

sample_df = pd.DataFrame( { "draw": np.arange(1, SAMPLE_SIZE + 1), "category": samples, })

print("First ten categorical draws:")
print(sample_df.head(10).to_string(index=False))

# Count each category, convert the counts to proportions, and place the rows in
# the same order as CATEGORIES so expected and observed values line up.
observed = sample_df["category"].value_counts(normalize=True).reindex(CATEGORIES, fill_value=0.0)

summary_df = pd.DataFrame(
    {
        "category": CATEGORIES,
        "expected_probability": PROBABILITIES,
        "observed_probability": observed.to_numpy(),
    }
)

print("\nExpected and observed categorical probabilities:")
print(summary_df.to_string(index=False))

output_path = "03_categorical.png"

# Categories do not have meaningful numeric intervals, so side-by-side bars are
# clearer than a continuous histogram.
x_positions = np.arange(len(CATEGORIES))
bar_width = 0.38

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(
    x_positions - bar_width / 2,
    PROBABILITIES,
    width=bar_width,
    label="Expected probability",
    color="#4472C4",
)
ax.bar(
    x_positions + bar_width / 2,
    observed.to_numpy(),
    width=bar_width,
    label="Observed proportion",
    color="#A5A5A5",
)
ax.set(
    xticks=x_positions,
    xticklabels=CATEGORIES,
    xlabel="Category",
    ylabel="Probability / observed proportion",
    title="10,000 samples from a categorical distribution",
)
ax.set_ylim(0, 0.6)
ax.legend()
fig.tight_layout()
fig.savefig(output_path, dpi=160)
plt.close(fig)

print(f"\nSaved bar chart to {output_path}")
