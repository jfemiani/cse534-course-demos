# CSE 534 Course Demos — Copilot Instructions

## What this repo is

Source code demos and lecture slides for **CSE 534: Generative Artificial
Intelligence** at Miami University (instructor: John Femiani). It does **not**
contain the live Canvas course; it contains the material that gets built here
and then pushed/linked into Canvas.

Three related repos exist under the `jfemiani` GitHub account:
- **`cse534-course-demos`** (this repo) — demo code, slides, and working
  copies of Canvas pages.
- **`cse434-instructor`** — a separate repo; check its own instructions before
  assuming conventions carry over.
- **`canvas-tools`** — a separate repo that holds the Canvas API upload
  tooling. This repo does not talk to the Canvas API directly; if a task
  needs to push HTML/quizzes to Canvas, that tooling lives there, not here.

## The course plan

`course_outline_plan.md` (repo root) is the **hand-maintained, working plan**
for how the course is being restructured. It is not downloaded from Canvas —
update it directly as decisions change (new module structure, production
conventions, research notes on what's changed in the underlying APIs, etc.).
Read it before planning any module-level change.

## The canonical Canvas reference

`remote_pages/` holds the **last downloaded snapshot** of the live Canvas
pages (one folder per Canvas module, exported HTML).
`remote_pages/outline_original.md` is the last downloaded Canvas outline.

- Treat `remote_pages/` as read-only reference for "what was live before we started editing" — use it to check for drift between this repo's working copies
  and our starting point, not as a place to author new content.
- Re-sync it from Canvas (via the `canvas-tools` repo, or the Canvas MCP
  server if configured) when you need to confirm current state before a
  restructuring task.

## Working copies of Canvas pages

Each module keeps its own **working version** of each page at:

```
modulename/pages/N. Some Topic.html
```

The number and title in the filename mirror the live Canvas item order and
title — keep them in sync when reordering or renaming.

These HTML files reference this GitHub repo directly for two things:
- **Images**: `<img>` tags point at
  `https://raw.githubusercontent.com/jfemiani/cse534-course-demos/master/...`
  (module output PNGs, etc.). Do not change these paths unless explicitly
  asked to move the underlying file.  When an image is updated, the new PNG must be committed and pushed before the Canvas page will show the change.
- **Source code embeds**: demo `.py` files are embedded via
  [emgithub.com](https://emgithub.com) iframes pointing at
  `https://github.com/jfemiani/cse534-course-demos/blob/master/...`. Because
  these reference the `master` branch, **a demo change is not visible on a
  Canvas page until it is committed and pushed** — flag this to whoever is
  driving the session before assuming an edit is "done."

> Note: this is the verified GitHub setup (confirmed via `git remote -v` and
> the embed URLs actually used in `pages/*.html`).

### Code-embed conventions for Canvas pages

When a page embeds a demo `.py` file via emgithub, follow this pattern
(established while revising
`04_tool_use_and_retrieval/pages/4.2 Tool Use - Function Calling with the Responses API.html`):

- **Introduce the source with a sentence, never a bare link line.** Before
  the first embed, write a sentence that both points at the full file and
  tells the reader what's about to happen, e.g. "The code below is
  available in full on GitHub at
  [`01a_function_calling_json.py`](...); we'll walk through the parts that
  matter." A link sitting alone on its own line, with no lead-in sentence
  (e.g. just `01a_function_calling_json.py (full source on GitHub)`), reads
  as an abrupt drop-in and must not be used.
- **Show several small, selective snippets, not the whole file.** Pick out
  the lines relevant to a specific idea (the function definition, the
  schema, the request/dispatch, sending the result back) as separate
  embeds, each with its own line range, instead of one embed covering
  nearly the whole file. Never lump two unrelated concepts (e.g. a class
  definition and an unrelated function) into a single line range. Skip
  boilerplate: imports, argument-parsing, print formatting, and any pattern
  any working programmer would already recognize don't need their own
  embed or their own explanation — spend the reader's attention on the
  lines that carry the lesson's actual idea.
- **Never embed a snippet's leading module docstring.** Course demo files
  open with a `"""..."""` docstring pointing at the companion `.md` file;
  it duplicates what the surrounding page prose already says. Start line
  ranges at the first import or the first line of real code, not at line 1
  of the file.
- **Line ranges use `#L<start>-L<end>` inside the encoded `target=` URL**,
  not appended after it:
  ```html
  <iframe
    src="https://emgithub.com/iframe.html?target=https%3A%2F%2Fgithub.com%2Fjfemiani%2Fcse534-course-demos%2Fblob%2Fmaster%2F04_tool_use_and_retrieval%2F01_function_calling%2F01a_function_calling_json.py%23L17-L19&style=codepen-embed&type=code&showBorder=on&showLineNumbers=on&showFileMeta=on&showFullPath=on&showCopy=on"
    style="width: min(100%, 750px); height: 120px; border: 0;"
    frameborder="0">
  </iframe>
  ```
- **Iframes must not be full-width.** Always use
  `style="width: min(100%, 750px); height: <N>px; border: 0;"` (plus the
  `frameborder="0"` attribute) — never `width: 100%` alone. Pick `height` to
  fit the snippet's line count plus the emgithub header.
- **Interleave prose with snippets, not a separate bullet list.** Put a short
  explanation directly above each snippet as flowing prose ("what to look
  for" folded into the sentence), not a bulleted list before/after the
  embeds and not a mechanical `<strong>Label:</strong> sentence` (or even
  unbolded `Label: sentence`) template repeated before every snippet — both
  read as a list dressed as prose. Vary sentence openers instead. Snippets
  that are just "ordinary code, nothing special" (e.g. the real function
  itself) need only a one-line caption; snippets central to the lesson
  (e.g. the tool schema) deserve more discussion.
- **Every snippet needs prose that earns its place, not just a caption.**
  A one-line caption is a minimum, not a target: explain *why* the code is
  written this way, what the reader should notice in it, and — if the
  logic is at all tricky (a normalization step, a fallback branch, an
  off-by-one in a range) — what it actually does and why. If you cannot
  say anything beyond "here is the code," the snippet is boilerplate and
  should be cut per the point above, not embedded with a filler caption.
- **Run every demo and show its output on the page.** Before a demo goes
  on a Canvas page, run it (e.g. `conda run -n cse434 dotenv run --
  python3 <script>.py`) and save the captured stdout as
  `<script_name>.output.txt` next to the `.py` file. Show that output on
  the page as a `<pre>` block (or a hand-built HTML table when the output
  is naturally tabular) — either once immediately after the full set of
  code snippets, or split alongside the snippet it corresponds to when a
  demo is broken into multiple embeds. Never claim or imply a demo
  produced a result without having actually run it and captured that
  output.

## Slides

Beamer/LaTeX slides live in `modulename/slides/N. Some Topic Slides.{tex,pdf}`
(plus LaTeX build artifacts), numbered and titled to match the same lesson's
page and demos. A few older decks are Marp-based (`.md` files alongside the
`.tex`); check what already exists in a module's `slides/` folder before
picking a format for a new deck.

## Demos

Convention: `modulename/NN_topic/NN_topic.py`, one runnable script per
concept, small enough to read in one sitting (see
`02_prompt_engineering_api/01_hello` through `06_structured_output` for the
target scale).

- **No `PROMPT.md` files.** Create a Markdown with the prompt named after the demo -- e.g. 06_structured_output.py would have 06_structured_output.md. This documents what
  it demonstrates, which API/endpoint it depends on, and a note that an LLM
  assistant can be asked to update the code if the API has changed. That
  Markdown file *is* the regeneration prompt.  We do not want to use PROMPT.md because we may have several variants of the same demo, and we want to keep the prompt with the code it documents.
- **Exception — multi-variant lessons.** When a lesson has several
  side-by-side variants of the same demo (see `04_tool_use_and_retrieval/01_function_calling`'s
  `01a_/01b_/01c_...py`).  The full concept/endpoint/regeneration-prompt content lives in the `.md` file.
- Each demo `.py` file starts with a `# pip install ...`  comment (if needed) naming its
  extra dependencies, so a reader can tell what to install without opening
  the requirements file.
- Every module folder has one `requirements-<module>.txt` (e.g.
  `requirements-tool-use-and-retrieval.txt`). Install it before running that
  module's demos.
- Preserve the teaching scenario when editing an existing demo; instructors
  run these live. Prefer minimal, surgical edits over rewrites unless asked
  to redesign the demo.
- As of the `04_tool_use_and_retrieval` module: for any demo involving tool
  calls or a multi-step loop, default to the **OpenAI Agents SDK**
  (`Agent`, `Runner`, `@function_tool`). Only write a hand-rolled
  `client.responses.create` loop when the explicit teaching goal is to show
  the mechanism the SDK automates, and label that variant clearly
  (`..._manual.py`), never as the default.

## Skills and agents to use

This workspace has domain-specific skills and agents. Use them rather than
improvising equivalent content by hand:

- **`beamer-slide-template`** skill — templates and review guidance for
  Beamer/LaTeX lecture slides: Miami-red dark theme, frame patterns, and the
  hard constraint that this is an **online** course (no live whiteboard —
  anything "worked through carefully" must be built into the slides with
  incremental reveals, not deferred to speaker notes).
- **`cse534-page-template`** skill — HTML/CSS templates for Canvas pages:
  Miami-red section headers, numbered-equation MathML blocks, code-embed
  patterns. Use this before hand-rolling new page markup.
- **`mathml-notation`** skill — writing/reviewing MathML equations
  (stretchy fences, bold vector/matrix notation, consistent bracket style,
  a pre-flight checklist). Use whenever a page or note needs new equations.
- **`canvas-page-editor`** agent — revising or creating Canvas pages,
  checking links/accessibility, merging local and Canvas content, embedding
  code demos, reviewing page quality.
- **`educational-reviewer`** agent — reviews slides/notes/HTML for
  accessibility to new learners (jargon, unexplained assumptions,
  pedagogical clarity). Run this on new or substantially revised lesson
  content before considering it finished.
- **`avoid-ai-writing`** skill — audits and cleans written content (pages,
  notes, READMEs) for AI-writing tells before finalizing. Run in `detect` or
  `edit` mode on any new prose-heavy content.

## Environment

- Demos run in the conda environment **`cse434`**
  (`conda run -n cse434 python3 ...` or `conda activate cse434`). Do not use
  `trace` or `trace-mamba` here — those belong to an unrelated project.
- `.env` in the repo root holds API keys for local runs; never commit
  secrets. Use a local, gitignored `.env` per the existing pattern.
- The `cse434` environment is shared across all modules. If a task needs a
  new package (e.g. `openai-agents`), installing it can upgrade shared
  dependencies (e.g. `openai` itself) — re-run demos from other modules
  afterward to confirm nothing broke, rather than assuming isolation.
- Known environment gotcha: a broken `pip install --force-reinstall --no-deps`
  on a package (e.g. `idna`) can corrupt its dist-info metadata and make
  *every* subsequent `pip` command fail with a confusing error. If `pip`
  itself starts erroring, check for missing/corrupt `.dist-info/METADATA` or
  `RECORD` files before assuming the target package is the problem.

## General workflow rules

- Don't rename or move module folders casually — filenames and numbering are
  load-bearing for Canvas links (page embeds, slide links, module ordering).
- When adding a new demo, keep numeric ordering and update the module's
  `README.md` demo list to match.
- Keep evergreen concept material in HTML pages; keep fast-moving API/SDK
  specifics (exact parameter names, method names) in code + docstrings, and
  link pages out to current official docs instead of reproducing details
  likely to drift within a year or two.
