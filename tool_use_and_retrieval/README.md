# Tool Use, Retrieval, and Agentic Loops demonstrations

These demos pick up where `prompt_engineering_api/` left off. That module
covered one request, one reply. This module covers what happens when the
model needs to call code, keep calling code on its own, or answer questions
about a document it was never trained on.

Work through these in order. Each one adds a single new idea to the last.

## Demos

1. [Tool use: a function the model cannot fake](01_function_calling) — the model asks for a letter count instead of guessing one.
2. [The agent loop](02_agent_loop) — the model calls two tools, one after another, deciding for itself when it has enough to answer.
3. [Chunking and retrieval](03_chunking_retrieval) — a small RAG pipeline built by hand: chunk, embed, rank, answer.
4. [Vector vs. keyword retrieval](04_retrieval_approaches) — the same question, ranked two different ways, with a case where they disagree.
5. [Agent instructions: SKILL.md dispatch](05_agent_instructions) — how a coding assistant decides which instructions file to read.

Each demo folder contains one reviewed Python file. The file's docstring
names the concept it teaches and the API it depends on. If an API changes,
ask an LLM assistant to update the file using that docstring as the brief;
it is written to be a complete regeneration prompt on its own.

Follow the Canvas lesson for setup, exact run instructions, and links to the
current official documentation each demo is based on.
