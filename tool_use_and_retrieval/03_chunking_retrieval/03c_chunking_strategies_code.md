# 03c: Fixed-line chunking vs. AST-aware chunking for source code

Concept: text-oriented chunking strategies (fixed-size, sentence-aware,
paragraph-aware) do not transfer cleanly to source code. Code's natural
units are functions, classes, and blocks, not sentences and paragraphs, and
a fixed line count can, and eventually will, cut a function's signature
away from its body. This demo runs a small Python module through two
strategies:

1. **Fixed-size, N lines per chunk** — cut every N lines, ignoring function
   or class boundaries. It is exactly the code equivalent of
   `03b_chunking_strategies_text.py`'s fixed-size text chunker, and it fails
   the same way: a chunk boundary can land inside a function body.
2. **AST-aware** — parse the source with Python's built-in `ast` module and
   emit one chunk per top-level function or class definition, using
   `ast.get_source_segment` to recover the exact original text for each
   node. Every chunk is a complete, independently-readable unit.

No embedding or API calls happen in this demo. Like 03b, it is about the
cut itself, using only the Python standard library (`ast`, `textwrap`).

## Where this fits with the built-in tool

OpenAI's `file_search` tool has no special handling for code: uploading a
`.py` file gets the same fixed-size, token-count chunking it would apply to
a novel. For a codebase, an AST-aware pass like strategy 2, or a
purpose-built code splitter such as LangChain's
`RecursiveCharacterTextSplitter.from_language(Language.PYTHON)`, is worth
doing before the files ever reach an embedding call.

## Compare with

- `03b_chunking_strategies_text.py` — the same fixed-size-vs-structure-aware
  comparison, for ordinary prose instead of code.

## Endpoint

None. Pure Python standard library — no API calls.

## Regeneration prompt

If asked to change this demo, keep the same sample module (two functions and
a class), the fixed-line strategy, the AST-based strategy using
`ast.get_source_segment`, and the printed comparison that shows a fixed-line
cut landing inside a function body.
