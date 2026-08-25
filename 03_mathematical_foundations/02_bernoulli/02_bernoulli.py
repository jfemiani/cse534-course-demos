"""Demo sampling a bernoulli trial"""

import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(seed=42)

FILENAME='02_bernoulli.png'
MU=0.2
samples = rng.choice(['cat', 'dog'], size=10_000, p=[MU, (1-MU)])

print("First 10 samples:")
print(samples[:10])

num_cats = np.sum(samples=='cat')
num_dogs = np.sum(samples=='dog')

p_hat_cat = num_cats/len(samples)
p_hat_dog = num_dogs/len(samples)

print("Expected fraction of cats:", MU, "and of dogs:", (1-MU))
print("Number of 'cat' samples:", num_cats, " fraction:", p_hat_cat)
print("Number of 'dog' samples:", num_dogs, " fraction:", p_hat_dog)


# Show a histogram....

plt.hist(samples)
plt.xlabel('Outcome')
plt.ylabel('Count')
plt.title('Bernoulli Samples')
plt.savefig(FILENAME)
plt.close()
print("Figure saved to", FILENAME)

