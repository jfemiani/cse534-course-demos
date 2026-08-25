# Evaluation and Ethics demonstrations

These demos ask a simple question about everything the course has built so
far: how do you know if any of it is any good? The first demo measures a
model. The second demo measures a choice you make when you build something
on top of a model.

Work through these in order.

## Demos

1. [N-gram evaluation](01_ngram_eval) — the module 3 n-gram model, scored on
   text it never trained on. Cross-entropy, perplexity, and a grid search
   over context length (`ORDER = 2, 4, 8`), showing the tradeoff between a
   short context that has seen almost everything and a long context that
   often has not.
2. [Retrieval evaluation](02_retrieval_eval) — an ablation study on a small
   RAG pipeline: vector search, keyword search, and a hybrid, each measured
   by hit-rate against a labeled set of test questions, instead of guessed.

Each demo folder contains one Python file. The file's docstring points to a
companion `.md` file of the same name, which carries the full concept, any
API it depends on, and a regeneration prompt an LLM assistant can use if
the underlying API changes.

Demo 1 makes no API calls; it downloads a public text file and does the
counting locally. Demo 2 calls the OpenAI Embeddings API.

Follow the Canvas lesson for setup, exact run instructions, and links to
the benchmarks, leaderboards, and evaluation tools this module points to.
