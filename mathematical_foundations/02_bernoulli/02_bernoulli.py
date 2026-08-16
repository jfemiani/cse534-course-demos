"""Sample a Bernoulli distribution and compare observed and expected results."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SEED = 7
SAMPLE_SIZE = 10_000

# For a Bernoulli random variable, MU is the probability of outcome 1.
# Outcome 0 therefore has probability 1 - MU.
MU = 0.75

rng = np.random.default_rng(seed=SEED)

# binomial(n=1, p=MU) is a Bernoulli sample: every draw is either 0 or 1.
samples = rng.binomial(n=1, p=MU, size=SAMPLE_SIZE)

# Store the generated results in a DataFrame so that students can inspect the
# individual trials before reducing them to a single observed proportion.
sample_df = pd.DataFrame(
    {
        "trial": np.arange(1, SAMPLE_SIZE + 1),
        "outcome": samples,
    }
)
sample_df["meaning"] = sample_df["outcome"].map({0: "failure", 1: "success"})

print("First ten Bernoulli trials:")
print(sample_df.head(10).to_string(index=False))

# Compute observed proportions from the generated rows. Reindexing guarantees
# that both outcomes appear in the summary even for a very small sample.
observed = (
    sample_df["outcome"]
    .value_counts(normalize=True)
    .reindex([0, 1], fill_value=0.0)
)

summary_df = pd.DataFrame(
    {
        "outcome": [0, 1],
        "meaning": ["failure", "success"],
        "expected_probability": [1 - MU, MU],
        "observed_probability": observed.to_numpy(),
    }
)

print("\nExpected and observed Bernoulli probabilities:")
print(summary_df.to_string(index=False))

output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)
output_path = output_dir / "02_bernoulli.png"

# A two-bin histogram shows the observed fraction of 0s and 1s. The red X
# markers show the theoretical probabilities specified by MU.
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.hist(
    sample_df["outcome"],
    bins=[-0.5, 0.5, 1.5],
    weights=np.ones(SAMPLE_SIZE) / SAMPLE_SIZE,
    rwidth=0.65,
    color="#9CC3E6",
    edgecolor="black",
    label="Observed proportion",
)
ax.scatter(
    [0, 1],
    [1 - MU, MU],
    color="#C00000",
    marker="x",
    s=110,
    linewidths=3,
    label="Expected probability",
    zorder=3,
)
ax.set(
    xticks=[0, 1],
    xlabel="Bernoulli outcome",
    ylabel="Probability / observed proportion",
    title=f"Bernoulli samples with mu = {MU}",
)
ax.set_ylim(0, 1)
ax.legend()
fig.tight_layout()
fig.savefig(output_path, dpi=160)
plt.close(fig)

print(f"\nSaved histogram to {output_path}")
