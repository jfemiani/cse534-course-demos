# 04c: HyDE - embedding a hypothetical answer instead of the raw question

Concept: what someone actually types is not always a good search query - it
can be short, vague, or worded differently than the documents that would
answer it. HyDE (Hypothetical Document Embeddings) has the model write a
plausible-looking answer to the question first, then embeds that
hypothetical answer instead of the question itself. A fabricated answer
tends to share more wording and vocabulary with a real matching document
than the original, terse question does, so searching with it can retrieve
better matches, even though the hypothetical answer is never shown to the
user. This demo asks a short, jargon-heavy question, generates a
hypothetical answer with a chat model, embeds both the raw question and the
hypothetical answer, and prints how each one scores the correct document.

## Compare with

- `04a_vector_vs_keyword.py` and `04b_reranking.py` — both improve how
  documents are ranked; HyDE instead improves what gets embedded on the
  query side, before ranking starts.

## Endpoint

OpenAI Responses API (`client.responses.create`) to generate the
hypothetical answer, and OpenAI Embeddings API
(`client.embeddings.create`, `text-embedding-3-small`) to embed it.

## Regeneration prompt

If OpenAI changes these APIs, ask an LLM assistant: "Update this script to
match the current OpenAI Responses API and embeddings API. Keep the same
four documents, the same terse question, and print the correct document's
score under both the raw-query embedding and the HyDE embedding."
