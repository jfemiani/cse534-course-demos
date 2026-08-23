# CSE 534 Working Outline (Planning Document)

This file is **hand-maintained**, not downloaded from Canvas. It starts from
`remote_pages/outline_original.md` (the last downloaded snapshot) and records
how we intend to restructure the course from this point forward. Update this
file as decisions change; re-sync `remote_pages/outline_original.md` from Canvas
whenever you want to check what's actually live.

Status key: ✅ built and uploaded · 🚧 planned, not yet written · ⏳ existing Canvas stub (PEGA-book based, to be replaced)

---

## Modules 1-3 (unchanged, already built)

1. ✅ Introduction to Generative AI and its Applications
2. ✅ Prompt Engineering API Integration (demos 1-6: hello call, chat, streaming, rich formatting, structured output)
3. ✅ Mathematical Foundations (lessons 1-8: distributions → likelihood → entropy → n-grams → normal → multivariate → Mahalanobis/PCA)

## Module 4 (NEW — replaces old modules 4 "LangChain Fundamentals, Function Calling" and 5 "Vector Databases, RAG")

**Working title: "Tool Use, Retrieval, and Agentic Loops"**

Rationale: the old two modules were scoped around the PEGA textbook (LangChain framework mechanics, FAISS/Pinecone specifics). We're moving away from teaching a specific framework and back toward what the **OpenAI API itself** now provides natively — tool calling, an agent loop, and hosted retrieval — since that's converged a lot since this course was last taught. LangChain gets one line of context (it's *a* way to orchestrate this, not *the* way).

This lands right after Mathematical Foundations and returns to the same Responses API groundwork from Module 2, so it should feel like "week one, but deeper" rather than a brand-new framework.

### 4.1 Module Overview ✅ (first cut)

### 4.2 Tool Use: Function Calling with the Responses API ✅ (first cut)
- What "tool use" / "function calling" means: the model doesn't run code, it emits a structured request; your code executes it and sends the result back.
- Minimal demo: one custom function tool (e.g., a simple calculator or "read this local file" tool), single round trip.
- Contrast with Module 2 demo 6 (structured output): structured output shapes the model's *final* answer; tool calling lets the model *ask for data* mid-conversation.
- Short aside (optional, don't overbuild): images/PDFs can also be attached as input content, not just returned by tools — one paragraph, one small example, not a full lesson. This repo does not yet have a base64-image demo; add one only if it stays this small.

### 4.3 The Agent Loop: Multi-Step Tool Use ✅ (first cut)
- Name the pattern explicitly: this is usually called the **agent loop** (OpenAI's own term for the Responses API's internal behavior) and academically traces back to **ReAct** (Reason + Act), Yao et al. 2022 — thought → action → observation, repeated until the model decides it's done.
- Demo: drive the loop across 2-3 tool calls (e.g., a "search my notes" tool + a "read file" tool) so students see the model choosing *which* tool and *when* to stop.
- Explicitly point out: OpenAI's Responses API now runs this loop **for you** when you use built-in tools (web search, file search, code interpreter, shell). Hand-rolling the loop is for understanding; production code should prefer the built-in loop or the Agents SDK.
- Mention the OpenAI **Agents SDK** (multi-agent orchestration, handoffs, guardrails) as the "if you outgrow a single loop" pointer — not a full lesson, just orientation.

### 4.4 Chunking and Retrieval (Manual RAG) ✅ (first cut)
- Why context windows force chunking: documents and source code get split into pieces small enough to embed and retrieve individually.
- Demo: chunk a short text/markdown doc, embed chunks with the OpenAI embeddings endpoint, cosine-similarity search, stuff top-k chunks into the prompt, answer a question grounded in them.
- Explicitly call out: this manual pipeline is for building intuition. In practice, prefer the Responses API's built-in **file_search** / vector store tool, which does chunking + embedding + retrieval for you.

### 4.5 Retrieval Approaches: Vector vs. Keyword vs. Graph ✅ (first cut)
- Theory/comparison lesson, small or no new demo (can reuse 4.4's chunks and add one keyword-match comparison — e.g., simple term overlap vs. embedding similarity on the same query — to make the contrast concrete).
- Vector RAG: dense embeddings, semantic similarity, current default.
- Keyword RAG: exact/lexical match (BM25/TF-IDF-style); still wins for exact terms, IDs, code identifiers.
- Hybrid retrieval: combine both; increasingly the practical default.
- **GraphRAG**: mention only as further reading, not taught in depth — it's evolving fast and has real cost/complexity tradeoffs. Point students to Microsoft's GraphRAG project page/paper if curious.

### 4.6 Reusable Agent Instructions: AGENTS.md and SKILL.md ✅ (first cut)
- A different idea from tool use: not code the model calls, but **guidance the model reads** — detailed, task-specific instructions saved to a file with light metadata, loaded when relevant instead of stuffed into every prompt.
- `AGENTS.md` (or legacy equivalents like `CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md`): project-wide, always loaded — "here's how this repo works."
- `SKILL.md`: a specific capability, loaded on demand based on its description — "here's how to do this one task well." Uses progressive disclosure: name+description always loaded, full body loaded only when triggered, linked scripts/references loaded only if needed.
- This course repo is a live example — the assistant building these pages literally uses skill files under `~/.copilot/skills/`. Good self-referential demo: show one real `SKILL.md`, point out the frontmatter/description trigger mechanism.
- Frame it as an engineering convention, not a theoretical result — cite it as such rather than dressing it up with false rigor.

---

## Later modules (unchanged for now)

6. Ethics Evaluation Responsible AI
7. Tutorial 1: Advanced Prompting Tools Explorer
8. Trigrams Simplest Generation
9. Exam 1
10. RNNs, LSTMs, Transformers, VAEs, GANs, Diffusion, etc. (unchanged)

---

## Reading list decision (this session)

- Confirmed via grep across all downloaded Canvas pages: the PEGA book
  ("Prompt Engineering for Generative AI") is cited **only** in the two old
  modules being replaced here (LangChain Fundamentals, Vector Databases/RAG).
  No other module depends on it - GDL ("Generative Deep Learning") is the
  textbook for GANs/VAEs/Transformers/RNNs/LSTMs/ethics and is untouched.
- PEGA is too dated for this module: it's locked to a LangChain/FAISS/Pinecone
  snapshot of the ecosystem that has since been substantially superseded by
  native OpenAI tool calling and hosted retrieval. **Drop it entirely for
  Module 4** - no assigned textbook chapters.
- Replace the "Reading" section on each Module 4 page with links to current
  official docs (OpenAI's function calling / Responses API / Agents SDK
  guides, plus the AGENTS.md and agentskills.io spec pages) instead of a
  textbook citation. This matches the evergreen-page / fast-moving-links
  split already decided below - readings are exactly the kind of thing that
  should point at a live doc rather than a fixed book edition.

## Production conventions for Module 4 (decided this session)

- **No `PROMPT.md` files for these demos.** The previous PROMPT.md files were poor quality. Instead, put a clear docstring at the top of each demo `.py` file: what it demonstrates, which API/endpoint it depends on, and a note that an LLM can be asked to update the code if the API has changed. That docstring *is* the regeneration prompt.
- **Evergreen vs. fast-moving split**: HTML pages get the durable material only — concepts, tradeoffs, named patterns (agent loop, ReAct, vector/keyword/graph retrieval, AGENTS.md/SKILL.md). API specifics (exact parameter names, SDK method names) stay in the code + docstrings, and pages link out to current docs rather than reproducing details likely to drift within a year or two.
- Each page should link to the current official docs it's based on (OpenAI first; Anthropic/Google Gemini equivalents where a useful comparison exists) so students can check for drift themselves.
- Demo sizing target: same scale as `prompt_engineering_api/01_hello` through `06_structured_output` — one clear idea per file, no more than needed to see it work.

## Research notes (what's changed since this course was last taught)

- **OpenAI Responses API** (released March 2025) now unifies chat, tool calling, and stateful conversation, and runs an internal **agent loop**: the model can call tools repeatedly in one request until it decides to stop. Built-in tools include web search, file search (hosted RAG), code interpreter, and a shell tool. Chat Completions still works but is no longer the recommended starting point for tool-using code. The Assistants API is deprecated (EOL announced for August 2026) — don't build new material on it.
- **OpenAI Agents SDK** (Python + TypeScript): a lightweight open-source orchestration layer on top of the Responses API for multi-agent handoffs, guardrails, and tracing — positioned as a lighter alternative to full frameworks like LangChain/LangGraph when a single agent loop isn't enough.
- **"The agent loop" name**: OpenAI's own docs use "agent loop" / "agentic loop." The older academic name for the same think→act→observe cycle is **ReAct** (Yao et al., 2022, arXiv:2210.03629) — worth naming both so students recognize the idea across vendors and papers.
- **RAG alternatives/variants**: hybrid vector+keyword retrieval is now common practice; **GraphRAG** (Microsoft) models entities/relationships as a graph and can outperform vector RAG on queries needing broad synthesis across a corpus, at real indexing cost and complexity. Treat as "worth knowing exists," not "worth building."
- **AGENTS.md / SKILL.md**: `AGENTS.md` (agents.md) has emerged as a cross-tool standard for project-level agent instructions (adopted by Cursor, Claude Code, Copilot, Codex, etc.), replacing tool-specific files like `.cursorrules`/`CLAUDE.md`. `SKILL.md` (see agentskills.io's spec) is the complementary per-capability format with progressive disclosure. Framed as an engineering/tooling convention, not an academic result.

## Status: first cut complete (this session)
- Local skeleton built under `tool_use_and_retrieval/` (5 demo folders plus `pages/` with 6 HTML files), committed and pushed.
- 4.5 got its own dedicated demo file (`04_retrieval_approaches/04_retrieval_approaches.py`) rather than an inline snippet, resolving that open question.
- 4.6 got a small no-API-cost demo (`05_agent_instructions/05_agent_instructions.py`) that dispatches between two real SKILL.md-style files by keyword overlap with their description, resolving that open question.
- All 6 pages reviewed by the educational-reviewer subagent; feedback applied (token/chunk vocabulary collision fixed in 4.2, cosine similarity tied back to the multivariate-normal lesson's dot-product material in 4.4, loop safety-net note added to 4.3, self-referential aside softened in 4.6, inside-reference to the old modules removed from 4.1's opening).
- Checked against the avoid-ai-writing skill's banned-word and pattern list: no hits.
- Canvas: module 4 renamed to "4. Tool Use, Retrieval, and Agentic Loops"; the 6 new pages uploaded and linked as items 1-6; module 5 deleted after moving its quiz/discussion/lab items into module 4 under a second "Legacy Assessments (under review)" subheader (module 4's original Activities subheader and items were left as-is). The 4 now-superseded old pages (old 4.1, old 4.2, old 5.1, old 5.2) were unpublished and prefixed [Superseded] rather than deleted, for reversibility.
- Not yet done: reviewing/rewriting the 7 legacy quiz/discussion/lab items so they match the new material instead of LangChain/FAISS/Pinecone specifics; slides for the 6 new lessons.

## Open questions / still open
- The two Activities subheaders in module 4 (original 3 items plus the newly moved 4 items) could be consolidated into one section later; left separate this session to avoid reordering risk.
- Legacy quizzes still ask about LangChain and specific vector database products by name - review question by question before removing the "under review" label.
