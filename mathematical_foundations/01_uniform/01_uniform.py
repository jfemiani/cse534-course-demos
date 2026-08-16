import os
import numpy as np
import matplotlib.pyplot as plt

SAMPLE_SIZE = 10_000
BIN_COUNT = 10
SEED = 43
OUTPUT="01_uniform.png"

np.random.seed(SEED)  # seed' = (C1*seed + C2)% C3 (maybe)
samples = np.random.uniform(0, 1, SAMPLE_SIZE)
# 1000 like [0.2, 0.4, 0.17897897, 0.789... ]

print("First five samples:")
print(samples[:5])

# Plot the samples in 10 equal-width bins
plt.hist(samples, bins=BIN_COUNT, range=(0, 1), edgecolor="black")
plt.xlabel("Value")
plt.ylabel("Count")
plt.title("Uniform(0, 1), $U(0,1)$")
plt.savefig(OUTPUT)
plt.close()
print(f"Plot saved to: {OUTPUT}")
