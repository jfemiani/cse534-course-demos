import os
import numpy as np
import matplotlib.pyplot as plt

SAMPLE_SIZE = 10_000
BIN_COUNT = 10
SEED = 42

np.random.seed(SEED)
samples = np.random.uniform(0, 1, SAMPLE_SIZE)

print("First five samples:")
print(samples[:5])

os.makedirs("outputs", exist_ok=True)

# Plot the samples in 10 equal-width bins
plt.hist(samples, bins=BIN_COUNT, range=(0, 1),   edgecolor="black")
plt.xlabel("Value")
plt.ylabel("Count")
plt.title("Uniform(0, 1)")
plt.savefig("outputs/uniform_histogram.png")
plt.close()

