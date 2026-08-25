# 02: Which retrieval strategy actually finds the right chunk?

Concept: an ablation study on a small RAG pipeline. Instead of guessing
whether vector search, keyword search, or a hybrid of the two is "better"
for a given collection of documents, this demo measures it directly with a
small labeled test set: a handful of questions, each with a known correct
source document, and a hit-rate that says how often each strategy actually
found it.

This reuses the documents-and-question style from
`tool_use_and_retrieval/03_chunking_retrieval/03a_manual_rag_pipeline.py`
and the vector-vs-keyword comparison from
`tool_use_and_retrieval/04_retrieval_approaches/04a_vector_vs_keyword.py`,
combined into one small evaluation.

## What the demo does

1. Defines six short documents and six test questions, each question
   paired with the index of the one document that actually answers it.
2. Scores every document against every question three ways: cosine
   similarity between embeddings (vector), token overlap (keyword), and a
   simple average of both, normalized to a comparable scale (hybrid).
3. Counts a "hit" whenever the correct document lands in the top `K = 2`
   results for a given strategy, and reports each strategy's hit-rate:
   hits divided by the number of questions.

## Reading the result

Two of these test questions ask about near-identical assignment codes
(`LAB-3042` vs. `LAB-4071`), the same exact-string problem covered in
`04a_vector_vs_keyword.py`. Watch what that does to each strategy's
hit-rate: it is exactly this kind of question that keyword search should
handle well and vector search may not, so the aggregate hit-rate is a
concrete, measured answer to "which retrieval approach should I actually
use here," rather than a guess.

## Endpoint

OpenAI Embeddings API (`client.embeddings.create`, `text-embedding-3-small`).

## Regeneration prompt

If OpenAI changes this API, ask an LLM assistant: "Update this script to
match the current OpenAI embeddings API. Keep the same six documents, the
same six test questions with their labeled correct document, and the same
vector, keyword, and hybrid hit-rate calculation."
