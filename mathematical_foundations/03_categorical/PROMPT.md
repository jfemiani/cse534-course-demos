# Optional regeneration and explanation prompt

Statistics is unlikely to change as quickly as an API, but this prompt can still be useful. Paste it into an AI coding assistant if you want to regenerate the demonstration, ask for a line-by-line explanation, or compare another implementation with the reviewed Python file beside this prompt.

Generated code and explanations can contain mistakes. Compare the result with the reviewed course file and with the lesson's equations.

## Prompt

Create a short, commented Python demonstration of a categorical distribution. Define three named categories—cat, dog, and horse—with probabilities 0.50, 0.30, and 0.20. Validate that all probabilities are nonnegative and sum to one. Use NumPy with a fixed seed to draw 10,000 samples. Put draw number and category in a pandas DataFrame and print its first ten rows. Print a summary containing each expected probability, observed proportion, and their difference. Save a side-by-side Matplotlib bar chart comparing expected and observed values. Explain why bars are clearer than a continuous histogram for named categories, and show students which probability list they can safely change.
