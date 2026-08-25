# 04b: Reranking a vector-search shortlist with a cross-encoder

Concept: vector and keyword search both score every chunk on its own, one
number per chunk, computed by comparing it to the question in isolation.
Reranking adds a second pass: the initial search still runs first and
returns a short list of candidates, then a slower cross-encoder model reads
the question and each candidate together, one pair at a time, and scores
that pair directly instead of comparing two separately computed vectors.
This demo picks a question with two "dense distractor" documents that share
a lot of surface vocabulary with the question (Canvas, Lab 3, late) without
actually answering it, and one document that answers it in different words.
Vector search can be pulled toward the lexically dense distractors; the
cross-encoder reads the actual question-document pair and can tell the
difference.

Fast-and-broad, then slow-and-precise, is the two-stage pattern most
production retrieval systems use: the cross-encoder is far more accurate at
telling close candidates apart, but too slow to run against an entire
collection, which is why it only reranks the shortlist the first search
already narrowed down.

## Compare with

- `04a_vector_vs_keyword.py` — the first-pass search this demo reranks.
- `04c_hyde.py` — improves the query going into that first pass instead of
  adding a second pass after it.

## Endpoint

OpenAI Embeddings API (`client.embeddings.create`, `text-embedding-3-small`)
for stage 1, and a local `sentence-transformers` cross-encoder
(`cross-encoder/ms-marco-MiniLM-L-6-v2`) for stage 2. The cross-encoder runs
on-device, no API call and no cost.

## Regeneration prompt

If OpenAI or sentence-transformers changes these APIs, ask an LLM assistant:
"Update this script to match the current OpenAI embeddings API and the
current sentence-transformers CrossEncoder API. Keep the same four
documents, the same question, and print both the vector-search order and
the cross-encoder-reranked order."
