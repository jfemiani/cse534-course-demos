# Optional regeneration and explanation prompt

Statistics is unlikely to change as quickly as an API, but this prompt can still be useful. Paste it into an AI coding assistant if you want to regenerate the demonstration, ask for a line-by-line explanation, or compare another implementation with the reviewed Python file beside this prompt.

Generated code and explanations can contain mistakes. Compare the result with the reviewed course file and with the lesson's equations.

## Prompt

Create a short, commented Python demonstration of a Bernoulli distribution. Use NumPy's binomial sampler with n=1, a fixed seed, 10,000 samples, and a clearly named MU constant that represents the probability of outcome 1. Put trial number, outcome, and a success/failure label in a pandas DataFrame and print its first ten rows. Print expected and observed probabilities for outcomes 0 and 1. Save a two-bin Matplotlib histogram of observed proportions and overlay visible markers for the two expected probabilities. Keep MU easy to change. After the code, explain what should happen when MU changes from 0.75 to 0.25.
