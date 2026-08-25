# Evaluation and Ethics demonstrations

These demos ask a simple question about everything the course has built so
far: how do you know if any of it is any good? The first demo measures a
model. The second pair measures a choice you make when you build something
on top of a model. The third demo looks at one of the automatic metrics
used to score generated text.

Work through these in order.

## Demos

1. [N-gram evaluation](01_ngram_eval) — the module 3 n-gram model, scored on
   text it never trained on. `01_ngram_eval.py` computes cross-entropy,
   perplexity, and a grid search over context length
   (`ORDERS = 2` through `8`), showing the tradeoff between a short context
   that underfits and a long context that overfits and memorizes training
   data instead of generalizing. `01b_ngram_block_scores.py` un-averages
   that table down to individual blocks of held-out text: the 5
   lowest-scoring, 5 median, and 5 highest-scoring blocks (cherries,
   apples, and lemons), showing what a single averaged cross-entropy
   number hides — and how a metric can be gamed by short, low-information
   text (Goodhart's Law).
2. [Retrieval evaluation](02_retrieval_eval) — an ablation study on a small
   RAG pipeline. `02a_retrieval_eval_hitrate.py` measures vector search,
   keyword search, and a hybrid against a labeled set of test questions,
   instead of guessed. `02b_retrieval_eval_examples.py` looks past the
   aggregate hit-rate at individual questions by margin, for anyone who
   wants to see the same cherry/apple/lemon idea applied to retrieval.
3. [BLEU score](03_bleu_score) — scores a correct paraphrase and a
   factually wrong near-copy against a reference sentence with the BLEU
   metric, showing how a word-overlap metric can reward the wrong answer
   over the right one. `03b_multi_metric_score.py` repeats the same
   three candidates through ROUGE-L, METEOR, and BERTScore alongside
   BLEU, showing that even an embedding-based metric like BERTScore still
   ranks the factually wrong candidate above the correct paraphrase.
4. [LLM-as-judge](04_llm_judge) — asks a model to judge the same three
   candidates BLEU just scored, directly, instead of counting overlapping
   words. The judge reverses BLEU's ranking, catching the factually wrong
   candidate and crediting the correct paraphrase.
5. [Verifiable rewards](05_verifiable_rewards) — instead of a metric or a
   second model, a short program checks the output directly.
   `05_math_verifier.py` extracts a final numeric answer from four
   candidate solutions and checks it against a known ground truth,
   contrasting a format check with an accuracy check. `05b_floorplan_verifier.py`
   applies the same idea to a non-numeric, spatial output: a geometric
   check confirms no two rooms overlap and every room has a door. Both tie
   into Reinforcement Learning with Verifiable Rewards (RLVR), the training
   approach behind DeepSeek-R1 and AlphaProof.

Each demo folder contains one Python file. The file's docstring points to a
companion `.md` file of the same name, which carries the full concept, any
API it depends on, and a regeneration prompt an LLM assistant can use if
the underlying API changes.

Demo 1 makes no API calls; it downloads a public text file and does the
counting locally, including its block-level companion. Demos 2a and 2b call
the OpenAI Embeddings API. Demo 3 makes no API calls; `03_bleu_score.py`
uses `nltk`'s BLEU implementation locally, and `03b_multi_metric_score.py`
adds ROUGE-L, METEOR, and BERTScore, all computed locally with `nltk`,
`transformers`, and `torch` (no new packages beyond what this course's
environment already installs for other lessons). Demo 4 calls the OpenAI
API for structured-output judgments. Demo 5 makes no API calls; both
scripts are pure Python (`re` and plain rectangle geometry) with no new
dependencies.

Follow the Canvas lesson for setup, exact run instructions, and links to
the benchmarks, leaderboards, and evaluation tools this module points to.
