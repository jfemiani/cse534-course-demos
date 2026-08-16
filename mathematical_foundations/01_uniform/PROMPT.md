# Optional regeneration and explanation prompt

Statistics is unlikely to change as quickly as an API, but this prompt can still be useful. Paste it into an AI coding assistant if you want to regenerate the demonstration, ask for a line-by-line explanation, or compare another implementation with the reviewed Python file beside this prompt.

Generated code and explanations can contain mistakes. Compare the result with the reviewed course file and with the lesson's equations.

## Prompt

Create a very short Python demonstration of continuous uniform sampling for teaching probability distributions.

Use NumPy with a fixed seed to draw 10,000 samples from Uniform(0, 1), print the first five values, and plot a Matplotlib histogram with 10 equal-width bins over [0, 1]. Save the histogram as outputs/uniform_histogram.png.

Keep SAMPLE_SIZE, BIN_COUNT, and SEED near the top so students can easily change them.

Keep the code minimal. Do not use pandas, do not manually compute bin counts or bin edges, and do not add anything beyond what is needed to generate, inspect, and plot the samples.

After the code, briefly explain what students should observe if SAMPLE_SIZE is changed from 10,000 to 100.
