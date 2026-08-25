# 03a: The smallest visible RAG pipeline

Concept: retrieval-augmented generation (RAG), built by hand so every step
is visible: split source text into chunks, embed each chunk, embed the
question, rank chunks by cosine similarity, and paste the closest chunk into
the prompt before asking the model to answer. The chunks here are already
short, complete sentences, chosen by hand, so this demo can focus on the
embed-rank-answer steps rather than on how the chunks were cut.

This manual pipeline is for building intuition. In production, prefer the
Responses API's built-in `file_search` tool, a hosted vector store that
chunks, embeds, and retrieves documents for you.

## Compare with

- `03b_chunking_strategies_text.py` — the harder problem this demo skips:
  cutting ordinary paragraphs into chunks in the first place.
- `03c_chunking_strategies_code.py` — the same cutting problem, but for
  source code, where a naive chunk boundary can split a function in two.

## Endpoint

OpenAI Embeddings API (`client.embeddings.create`, `text-embedding-3-small`)
and the Responses API (`client.responses.create`).

## Regeneration prompt

If OpenAI changes these APIs, ask an LLM assistant: "Update this script to
match the current OpenAI embeddings and Responses API. Keep the same four
document chunks, the cosine-similarity ranking, and the single retrieved
chunk pasted into the final prompt."
