# 03b: Three ways to cut plain text into chunks

Concept: before anything can be embedded, a document has to be cut into
chunks, and how it gets cut changes what retrieval can find. This demo runs
one short syllabus excerpt through three strategies and prints the resulting
chunks so the difference is visible, not just described:

1. **Fixed-size, no overlap** — cut every N characters, ignoring sentence or
   paragraph boundaries. Simple, but a chunk boundary can land in the middle
   of a sentence, splitting a fact from the words that explain it.
2. **Fixed-size with overlap** — the same blind cut, but each chunk repeats
   the last few characters of the one before it, so a fact split across a
   boundary still appears whole in at least one chunk.
3. **Recursive / structure-aware** — try to cut at a paragraph break first,
   merging pieces back up to the target size; only split a too-long piece
   further on the next separator (sentence break, then word, then a hard
   character cut). This is the idea behind LangChain's
   `RecursiveCharacterTextSplitter`: prefer the biggest natural boundary
   that still fits, implemented here with nothing but the standard library
   so the mechanism is visible.

No embedding or API calls happen in this demo. It is about the cut itself.
Chunks from any of these three strategies are what would get embedded in
`03a_manual_rag_pipeline.py`, or uploaded to a `file_search` vector store.

## Where this fits with the built-in tool

OpenAI's `file_search` tool defaults to an `auto` chunking strategy that is a
fixed-size cut much like strategy 2 above: 800-token chunks with 400 tokens
of overlap. A `static` chunking_strategy lets you override both numbers when
uploading a file, but the tool does not offer paragraph- or sentence-aware
cutting. That is still something you would build yourself, the way
strategy 3 does here, before the file ever reaches OpenAI.

## Compare with

- `03a_manual_rag_pipeline.py` — what happens after chunks exist: embedding,
  ranking, and answering.
- `03c_chunking_strategies_code.py` — the same cutting problem, but for
  source code, where the natural boundary is a function or class, not a
  sentence.

## Endpoint

None. Pure Python standard library — no API calls.

## Regeneration prompt

If asked to change this demo, keep the same three strategies, the same
syllabus excerpt, and the printed chunks that show a fixed-size cut landing
inside a sentence. The explanation of what to notice in the output belongs
on the Canvas page, not in a trailing `print()` in this script.
