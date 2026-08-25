# 02b: Look at individual examples, not just the aggregate hit-rate

Concept: a single hit-rate number (like `02a_retrieval_eval_hitrate.py`'s
"vector: 0.83") already tells you vector search beat keyword search on this
test set. It does not tell you what a *typical* retrieval looked like, or
what the *worst* one looked like. This demo picks out three concrete
examples instead: the best margin, the median margin, and the worst margin,
labeled cherry, apple, and lemon.

## What the demo does

1. Reuses the same six documents and six labeled test questions as
   `02a_retrieval_eval_hitrate.py`.
2. For each question, scores every document against it with the OpenAI
   Embeddings API and computes a **margin**: the correct document's cosine
   similarity minus the best-scoring *wrong* document's similarity. A large
   positive margin is a clean win; a negative margin means vector search
   actually preferred a wrong document over the right one.
3. Sorts the six questions by margin and prints the top one (cherry), the
   middle one (apple), and the bottom one (lemon), including the correct
   document's actual rank and whether it counted as a hit at `K = 2`.

## Reading the result

The cherry example is a clean win: the correct document is a near-exact
paraphrase of the question, and it wins by a wide margin. The apple example
still wins, but barely — this is what most of the "hits" in the aggregate
table actually look like: a close call, not a landslide. The lemon example
is a real *miss*: for "Do I need to sign in to class?" vector search's top
pick was a document about a lab assignment code, and the document that
actually answers the question ranked third. A hit-rate of 0.83 sounds
strong; the lemon is a reminder that "won 5 of 6" still means something
went visibly, obviously wrong once — and an aggregate number alone would
never show you which time, or how.

## Endpoint

OpenAI Embeddings API (`client.embeddings.create`, `text-embedding-3-small`).

## Regeneration prompt

If OpenAI changes this API, ask an LLM assistant: "Update this script to
match the current OpenAI embeddings API. Keep the same six documents and
six test questions as `02a_retrieval_eval_hitrate.py`, keep the margin
calculation (correct document's score minus the best wrong document's
score), and keep printing the cherry (best margin), apple (median margin),
and lemon (worst margin) examples with their rank and hit/miss status."
