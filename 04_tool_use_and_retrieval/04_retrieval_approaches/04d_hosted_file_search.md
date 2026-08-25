# 04d: Pointing at a folder of documents with OpenAI's hosted file_search tool

Concept: this is the realistic version of "I have a folder of documents (or
PDFs, or code) and I want to ask questions about it." Instead of writing
your own chunk/embed/rank pipeline like `03a_manual_rag_pipeline.py`, upload
the files once to a vector store and attach that vector store to a
`file_search` tool. The model decides when to search it, the same
tool-calling mechanism from `01_function_calling` and `02_agent_loop`,
just aimed at a hosted retrieval tool instead of a hand-written one, so
chunking, embedding, and ranking all happen on OpenAI's side. This demo
uploads three small sample files, asks a question, and prints which file
the model's search actually matched before printing the answer.

A dedicated vector database (Pinecone, Weaviate, Chroma, pgvector, and
others) is the self-hosted or multi-vendor equivalent of the vector store
this demo creates: same underlying idea (store embeddings, search by
similarity), but you run and pay for the infrastructure yourself instead of
OpenAI hosting it as one tool call away.

## Compare with

- `03a_manual_rag_pipeline.py` — the same idea built by hand, useful for
  seeing every step; this demo is the version to actually use.

## Endpoint

OpenAI Files API (`client.files.create`, via
`client.vector_stores.files.upload_and_poll`), Vector Stores API
(`client.vector_stores.create`), and the Responses API's `file_search` tool.

## Regeneration prompt

If OpenAI changes these APIs, ask an LLM assistant: "Update this script to
match the current OpenAI vector store and file_search tool API. Keep the
same three sample documents, one vector store, printing which file matched
the search, and the cleanup step that deletes the files and vector store at
the end."
