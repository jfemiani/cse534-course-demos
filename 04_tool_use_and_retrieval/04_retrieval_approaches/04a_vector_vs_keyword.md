# 04a: Vector search and keyword search do not agree on everything

Concept: comparing two retrieval strategies on the same small set of
documents and the same question. Vector search (embeddings and cosine
similarity) ranks by semantic similarity; keyword search ranks by exact
token overlap. Vector search is the current default and wins on paraphrase
and meaning, but two different ID-like strings can embed close together
even though they name different things. This demo picks a question that
exposes the gap: keyword search finds the exact assignment code instantly,
while vector search has to tell two similar-looking codes apart.

## Compare with

- `04b_reranking.py` — takes a vector-search shortlist like this one and
  runs a slower, more accurate cross-encoder over just those candidates.
- `04c_hyde.py` — rewrites the query itself before embedding it, instead of
  changing how the documents are ranked.
- `04d_hosted_file_search.py` — the same idea at production scale: a hosted
  vector store instead of four hand-picked strings.

## Endpoint

OpenAI Embeddings API (`client.embeddings.create`, `text-embedding-3-small`).

## Regeneration prompt

If OpenAI changes this API, ask an LLM assistant: "Update this script to
match the current OpenAI embeddings API. Keep the same four documents, the
same question, and both rankings printed side by side."
