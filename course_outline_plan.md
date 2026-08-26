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

### 4.5 Retrieval Approaches: Vector vs. Keyword ✅ (revised)
- Dropped GraphRAG entirely — title, content, and reading link. Not worth the engineering-cost caveat for a technique this course doesn't teach or demo.
- Vector RAG: dense embeddings, semantic similarity, current default.
- Keyword RAG: exact/lexical match; still wins for exact terms, IDs, code identifiers.
- Hybrid retrieval: combine both; increasingly the practical default.
- Reranking and query rewriting (HyDE) now each have a real demo (`04b_reranking.py`, `04c_hyde.py`), not just prose.
- Added a "retrieval in production" section: hosted `file_search`/vector stores vs. dedicated vector databases (Pinecone, Weaviate, Chroma, pgvector) — answers "what would I actually use for a folder of documents," and is where Pinecone/vector databases now get named explicitly.
- New demo `04d_hosted_file_search.py`: uploads a small folder of sample files to a hosted vector store and asks a question through the `file_search` tool, printing which file matched — the realistic answer to "I have a folder of docs and want to ask questions."
- Page reordered: no leading header, concept sections first, all four demos grouped in one "The demos" section placed last, right before Reading.

### 4.6 Reusable Agent Instructions: AGENTS.md and SKILL.md ✅ (first cut)
- A different idea from tool use: not code the model calls, but **guidance the model reads** — detailed, task-specific instructions saved to a file with light metadata, loaded when relevant instead of stuffed into every prompt.
- `AGENTS.md` (or legacy equivalents like `CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md`): project-wide, always loaded — "here's how this repo works."
- `SKILL.md`: a specific capability, loaded on demand based on its description — "here's how to do this one task well." Uses progressive disclosure: name+description always loaded, full body loaded only when triggered, linked scripts/references loaded only if needed.
- This course repo is a live example — the assistant building these pages literally uses skill files under `~/.copilot/skills/`. Good self-referential demo: show one real `SKILL.md`, point out the frontmatter/description trigger mechanism.
- Frame it as an engineering convention, not a theoretical result — cite it as such rather than dressing it up with false rigor.

---

## Module 5 (built this session — was mislabeled "6" on Canvas)

**Working title: "Evaluation, Ethics, and Responsible AI"**

Rationale: the module numbering note below was stale. When old modules 4
and 5 were merged into the new Module 4 ("Tool Use, Retrieval, and Agentic
Loops") and the old module 5 was deleted, every later module should have
shifted up by one position. The Canvas module that used to be "6. Ethics,
Evaluation, and Responsible AI" kept its old internal `position` value (8)
and its old display number ("6.") even after the merge freed up position 7.
Fixed this session: the module's Canvas `position` field was corrected
from 8 to 7 via the Canvas API (`module.edit(module={'position': 7})`),
and its name was updated to "5. Evaluation, Ethics, and Responsible AI" —
evaluation first, since the lesson order was also reversed (see below).

### 5.1 Module Overview ✅ (first cut)

### 5.2 Evaluating LLMs ✅ (second cut)
- Two threads under one "evaluation" umbrella: evaluating a model's raw
  capability (benchmarks) and evaluating your own design choices when
  building on top of a model (ablation studies, grid search).
- Reuses the module 3 n-gram model and cross-entropy lesson: a demo
  (`01_ngram_eval`) holds out text, sweeps context length (orders 2
  through 8), and reports cross-entropy and perplexity — the course's
  first concrete grid search, and a real illustration of overfitting and
  the bias-variance tradeoff (order 3 wins; order 8 memorizes and fails to
  generalize).
- Immediately un-averages that table with a companion demo
  (`01b_ngram_block_scores`): the 5 lowest-scoring, 5 median, and 5
  highest-scoring individual blocks of held-out text (cherries, apples,
  lemons), showing what a single averaged cross-entropy number hides, and
  naming Goodhart's Law — a model (or a report) can look better by
  favoring short, low-information text, since fewer characters means
  fewer chances to be surprised.
- Covers reading a results table like a research paper (arrow convention,
  bold-best/italic-second-best, and the real limitation that a lot of
  published tables are a single run with no significance testing).
- Introduces the zoo of automatic text-generation metrics right after that,
  with a demo (`03_bleu_score`) showing BLEU reward a factually wrong,
  high-overlap answer over a correct paraphrase, then a bulleted tour of
  ROUGE, METEOR, exact-match/F1, and BERTScore, followed by a second demo
  (`03b_multi_metric_score`) that scores the same three candidates with
  BLEU, ROUGE-L, METEOR, and BERTScore side by side — all four still rank
  the wrong-room answer above the correct paraphrase, showing that even an
  embedding-based metric is not the same as a correctness check. All four
  metrics are computed without adding new packages to the shared
  environment (`nltk` for BLEU/METEOR, a hand-written longest-common-
  subsequence for ROUGE-L, and a hand-written greedy cosine-similarity
  match over `transformers`/`torch` embeddings for BERTScore). A third
  demo (`03c_multi_metric_corpus`) reruns all four metrics at the scale of
  the order sweep itself: for each order, it generates a continuation of
  real held-out text and scores it against the true continuation, showing
  that the order cross-entropy already favors (order 3) does not also win
  on generation-quality metrics — a real instance of exposure bias, the
  gap between an easy teacher-forced training signal and the harder
  free-running generation task.
- Gives LLM-as-judge its own section (`04_llm_judge`), collapsed to a
  single minimal demo: a model judges whether a hand-written email reply
  reads as friendly, across three replies varying only in tone. No BLEU
  comparison and no fixed reference answer — the point is a quality with
  no reference wording to count overlap against at all, paired with the
  cost/reliability tradeoff of judging with a model and the honest
  instability of a judge's call on a genuine borderline case.
- Covers evaluating your own work: ablation studies (framed as working
  backwards from a baseline-then-educated-guesses build process, to prove
  each kept change mattered) and grid search (framed around combinatorial
  explosion and a hierarchical/greedy alternative, with an early pointer to
  hyperparameter-optimization tooling like Optuna/Ray Tune/W&B Sweeps).
  Worked example: a demo pair (`02a_retrieval_eval_hitrate`,
  `02b_retrieval_eval_examples`) measures hit-rate for vector, keyword, and
  hybrid retrieval on a small labeled test set built from the module 4
  chunking/retrieval demos; `02b` is available for anyone who wants the
  same cherry/apple/lemon-by-margin idea applied to retrieval, but the page
  itself does not repeat that explanation a second time (it is already
  taught in full using the n-gram demo above).
- Names real benchmark families (MMLU/MMLU-Pro, GSM8K/AIME, HumanEval/
  SWE-bench, GPQA) without hardcoding scores, after the ablation/grid-search
  section, and links out to live leaderboards (SWE-bench, and "MMLU
  leaderboard"/"livebench" as search starting points) instead.
- Covers LMArena (human head-to-head preference, Elo-style rating) as a
  different kind of measurement from a correctness benchmark.
- Covers benchmark contamination, citing Xu et al. 2024 (arXiv:2406.04244)
  as a real survey of the problem, and LiveBench as one response to it.
- Closes with links to OpenAI Evals, Anthropic's evaluation docs, and
  promptfoo/Langfuse as tools that automate this instead of hand-building
  it every time, including an illustrative (non-executed) promptfoo config
  showing how much of the hand-rolled retrieval hit-rate demo a library
  absorbs.
- Adds a section on verifiers as a third kind of "scoring": when a task has
  a precise, checkable specification, a program can decide correct/
  incorrect directly, with no metric formula and no second model forming
  an opinion. Demo (`05_math_verifier`) extracts a final numeric answer
  from four candidate solutions to one math problem and checks it against
  a known ground truth, contrasting a format check against an accuracy
  check (echoing DeepSeek-R1's dual reward design) and showing the
  verifier is immune to the wording-vs-value confusion BLEU fell into
  earlier on the page. Companion demo (`05b_floorplan_verifier`) applies
  the same idea to a non-numeric, spatial output — no room overlaps, every
  room has a door — via plain rectangle geometry, showing a verifier
  generalizes past math. Ties this to Reinforcement Learning with
  Verifiable Rewards (RLVR), citing DeepSeek-R1 (arXiv:2501.12948) and
  AlphaProof (Nature, s41586-025-09833-y) as real, citable examples, and
  names the boundary (no specification precise enough to check
  automatically means no verifier, which is why the earlier metrics and
  LLM-as-judge still matter) plus the Goodhart's-Law risk of a
  non-airtight verifier. No new packages: both demos are pure Python.

### 5.3 Ethics and Responsible AI ✅ (first cut)
- Hard constraint followed throughout: every section poses an open
  question and does not answer it. No verdicts on what is or isn't
  ethical anywhere on this page.
- Covers the visible costs (data center electricity/water use, job
  displacement), using AI to build a skill vs. to skip learning one, and
  "the pipeline problem" (where future senior engineers' judgment comes
  from if AI increasingly does junior-level work).
- Case studies, each posed as a question: AI-written personal messages,
  real likenesses used without consent, the real and documented January
  2024 New Hampshire AI-robocall incident, and video's higher believability
  compared to faked text or images.
- Explicitly points students to the new discussion assignment and quiz as
  where these questions get worked through, not the page itself.

### Activities (new this session)
- New discussion assignment (`05_evaluation_and_ethics/discussion/`): an
  open-ended prompt built around three of the ethics case studies above.
  Students pick one, take a position, and respond to a classmate.
- New quiz (`05_evaluation_and_ethics/quizzes/`), text2qti format, validated
  with `text2qti` and exported to a zip alongside the `.txt` source. The
  evaluation-lesson questions are ordinary fact/concept questions. The
  ethics questions are situational-judgment questions that test whether a
  student can identify which concern a scenario raises, not what the
  "right" ethical answer is — no question asserts a moral verdict.
- The pre-existing "Discussion: AI Evaluation in the Wild" discussion and
  "Lab 5: AI Evaluation Methods" assignment were left as-is; they already
  fit the evaluation lesson and were out of scope for this session.

---

## Later modules (unchanged for now)

6. Tutorial 1: Advanced Prompting Tools Explorer
7. Trigrams Simplest Generation
8. Exam 1
9. RNNs, LSTMs, Transformers, VAEs, GANs, Diffusion, etc. (unchanged)

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
  - **Exception, added later this session:** when a lesson has multiple side-by-side variants of the same demo (e.g. `01_function_calling`'s 01a/01b/01c — bare JSON, Pydantic schema, Agents SDK `@function_tool`), a full docstring in each variant is too long to embed cleanly on a Canvas page. For these, each `.py` file keeps a one-line docstring pointing at a companion Markdown file of the same name (`01a_function_calling_json.py` -> `01a_function_calling_json.md`), and the full concept/endpoint/regeneration-prompt content lives in that `.md` file instead. Single-variant demos (03-05) keep the original full-docstring convention.
  - Lesson 4.2 now demonstrates tool argument definition three ways: `01a_function_calling_json.py` (hand-typed JSON schema), `01b_function_calling_pydantic.py` (schema from a Pydantic model), `01c_function_calling_agents_sdk.py` (schema and dispatch loop both generated by the OpenAI Agents SDK's `@function_tool` decorator).
  - Lesson 4.3 now has two variants: `02a_agent_loop_agents_sdk.py` (the Agents SDK runs the loop) and `02b_agent_loop_manual.py` (the same loop hand-rolled against the plain Responses API). `02a` is presented first/as the default; `02b` is explicitly framed as "seeing the mechanism," not an equally-valid alternative.
- **Agents-SDK-first policy (decided this session, applies going forward):** for any demo that calls tools or runs a multi-step loop, default to the OpenAI Agents SDK (`Agent`, `Runner`, `@function_tool`). Only write a hand-rolled `client.responses.create` / Chat Completions version when the explicit teaching goal is to show the underlying mechanism the SDK is automating — and in that case, label it clearly as the "manual" or "under the hood" variant, not the default. This does not apply to demos that don't involve tool-calling loops (e.g. `03_chunking_retrieval`, `04_retrieval_approaches` — plain embeddings calls, no agent loop to automate).
- **Evergreen vs. fast-moving split**: HTML pages get the durable material only — concepts, tradeoffs, named patterns (agent loop, ReAct, vector/keyword/graph retrieval, AGENTS.md/SKILL.md). API specifics (exact parameter names, SDK method names) stay in the code + docstrings, and pages link out to current docs rather than reproducing details likely to drift within a year or two.
- Each page should link to the current official docs it's based on (OpenAI first; Anthropic/Google Gemini equivalents where a useful comparison exists) so students can check for drift themselves.
- Demo sizing target: same scale as `02_prompt_engineering_api/01_hello` through `06_structured_output` — one clear idea per file, no more than needed to see it work.
- Each demo `.py` file starts with a `# pip install ...` comment naming its extra dependencies, so students can tell what to install without opening the requirements file.

## Research notes (what's changed since this course was last taught)

- **OpenAI Responses API** (released March 2025) now unifies chat, tool calling, and stateful conversation, and runs an internal **agent loop**: the model can call tools repeatedly in one request until it decides to stop. Built-in tools include web search, file search (hosted RAG), code interpreter, and a shell tool. Chat Completions still works but is no longer the recommended starting point for tool-using code. The Assistants API is deprecated (EOL announced for August 2026) — don't build new material on it.
- **OpenAI Agents SDK** (Python + TypeScript): a lightweight open-source orchestration layer on top of the Responses API for multi-agent handoffs, guardrails, and tracing — positioned as a lighter alternative to full frameworks like LangChain/LangGraph when a single agent loop isn't enough. Confirmed working in `01c_function_calling_agents_sdk.py`; requires `openai-agents` in requirements. Environment note: installing `openai-agents` upgraded `openai` to 3.3.1 in the shared `cse434` conda environment and exposed a pre-existing `Brotli`/`brotlicffi` incompatibility with the bundled `httpx2` (fix: uninstall `Brotli`, install `brotlicffi`).
- **"The agent loop" name**: OpenAI's own docs use "agent loop" / "agentic loop." The older academic name for the same think→act→observe cycle is **ReAct** (Yao et al., 2022, arXiv:2210.03629) — worth naming both so students recognize the idea across vendors and papers.
- **RAG alternatives/variants**: hybrid vector+keyword retrieval is now common practice; **GraphRAG** (Microsoft) models entities/relationships as a graph and can outperform vector RAG on queries needing broad synthesis across a corpus, at real indexing cost and complexity. Treat as "worth knowing exists," not "worth building."
- **AGENTS.md / SKILL.md**: `AGENTS.md` (agents.md) has emerged as a cross-tool standard for project-level agent instructions (adopted by Cursor, Claude Code, Copilot, Codex, etc.), replacing tool-specific files like `.cursorrules`/`CLAUDE.md`. `SKILL.md` (see agentskills.io's spec) is the complementary per-capability format with progressive disclosure. Framed as an engineering/tooling convention, not an academic result.

## Status: first cut complete (this session)
- Local skeleton built under `04_tool_use_and_retrieval/` (5 demo folders plus `pages/` with 6 HTML files), committed and pushed.
- 4.5 got its own dedicated demo file (`04_retrieval_approaches/04_retrieval_approaches.py`) rather than an inline snippet, resolving that open question.
- 4.6 got a small no-API-cost demo (`05_agent_instructions/05_agent_instructions.py`) that dispatches between two real SKILL.md-style files by keyword overlap with their description, resolving that open question.
- All 6 pages reviewed by the educational-reviewer subagent; feedback applied (token/chunk vocabulary collision fixed in 4.2, cosine similarity tied back to the multivariate-normal lesson's dot-product material in 4.4, loop safety-net note added to 4.3, self-referential aside softened in 4.6, inside-reference to the old modules removed from 4.1's opening).
- Checked against the avoid-ai-writing skill's banned-word and pattern list: no hits.
- Canvas: module 4 renamed to "4. Tool Use, Retrieval, and Agentic Loops"; the 6 new pages uploaded and linked as items 1-6; module 5 deleted after moving its quiz/discussion/lab items into module 4 under a second "Legacy Assessments (under review)" subheader (module 4's original Activities subheader and items were left as-is). The 4 now-superseded old pages (old 4.1, old 4.2, old 5.1, old 5.2) were unpublished and prefixed [Superseded] rather than deleted, for reversibility.
- Not yet done: reviewing/rewriting the 7 legacy quiz/discussion/lab items so they match the new material instead of LangChain/FAISS/Pinecone specifics; slides for the 6 new lessons.

## Open questions / still open
- The two Activities subheaders in module 4 (original 3 items plus the newly moved 4 items) could be consolidated into one section later; left separate this session to avoid reordering risk.
- Legacy quizzes still ask about LangChain and specific vector database products by name - review question by question before removing the "under review" label.
