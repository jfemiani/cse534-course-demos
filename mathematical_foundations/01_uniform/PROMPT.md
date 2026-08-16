# Optional regeneration and explanation prompt

Statistics is unlikely to change as quickly as an API, but this prompt can still be useful. Paste it into an AI coding assistant if you want to regenerate the demonstration, ask for a line-by-line explanation, or compare another implementation with the reviewed Python file beside this prompt.

Generated code and explanations can contain mistakes. Compare the result with the reviewed course file and with the lesson's equations.

## Prompt

Create a short, commented Python demonstration of continuous uniform sampling. Use NumPy with a fixed seed to draw 10,000 values from Uniform(0, 1). Put every value in a pandas DataFrame and print its first five rows. Divide the interval into ten equal-width bins, print a table containing each bin's count, observed probability, and expected probability, and save a clearly labeled Matplotlib histogram. Keep constants such as sample size and bin count near the top so a student can change them. Save the graph in an outputs folder. After the code, explain what should change when the sample size is reduced from 10,000 to 100.
