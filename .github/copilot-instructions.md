Purpose

Provide concise repository guidance for Copilot sessions: how to run demos, where teaching assets live, and repository-specific conventions that matter to automated assistants.

Build, test, and lint commands

- No project-wide build/test/lint targets are defined.
- To run a single demo (recommended workflow):
  - Install the module requirements file found next to each module: 
    pip install -r requirements-<module>.txt
    Example: pip install -r requirements-math-foundations.txt
  - Run the demo script directly:
    python prompt_engineering_api/01_hello/01_hello.py
- Linting: no repository-wide linter configured. Some modules have .ruff_cache entries; if using ruff locally, run: ruff check <path>

High-level architecture

- Top-level modules: each top-level folder is a course module (e.g., prompt_engineering_api, mathematical_foundations, tool_use_and_retrieval, remote_pages).
- Each module folder:
  - contains numbered demo subfolders (01_*, 02_*, ...). Each demo is a standalone Python script illustrating a single concept.
  - includes a PROMPT.md next to each demo describing the prompt or regeneration steps for that example.
  - may include a pages/ directory (Canvas-exported HTML lesson pages) and slides/ (LaTeX sources + built PDFs).
- remote_pages/ holds exported Canvas pages used as the canonical course content.
- tool_use_and_retrieval/ contains examples for agent instruction formats (sample SKILL.md files and HTML AGENTS.md pages) used by automated assistants.

Key conventions (repository-specific)

- Demo naming: files and folders are prefixed with two-digit indices (01_, 02_, ...) to match Canvas lesson ordering. Keep numbering when adding or moving demos.
- PROMPT.md: every demo has a PROMPT.md that documents the exact prompt (or regeneration steps). Use it when updating demos or when an AI assistant needs to regenerate code.
- Requirements: per-module requirements files follow pattern requirements-<module>.txt (e.g., requirements-math-foundations.txt). Prefer installing only the needed module requirements for a demo.
- Slides and pages: filenames and numbering mirror demo indices. When editing slides or pages, keep names aligned with demos to preserve Canvas links.
- Agent instructions: agent skill files in tool_use_and_retrieval/05_agent_instructions/sample_skills use front-matter and clear step lists (SKILL.md format). New assistant skills should follow the same front-matter + section style.
- .env: present in repo root (do not commit secrets). Use a local .env (gitignored) for API keys referenced by demos.

Important places to inspect

- README.md at repo root: module overview and running-demonstration notes.
- Each module's README.md and pages/ subfolder for Canvas-exported guidance.
- PROMPT.md alongside any demo needing regeneration or explanation.
- tool_use_and_retrieval/05_agent_instructions/sample_skills for example SKILL.md files used by agents.

Notes for Copilot sessions

- When asked to modify or regenerate demos, preserve the PROMPT.md and keep the pedagogical scenario unchanged unless user asks to change it.
- Prefer minimal, surgical edits to demo scripts; instructors use these files in Canvas, and changes should not break the teaching narrative.
- If adding new demos, maintain numeric ordering and add a PROMPT.md that documents the prompt and the teaching goal.

Questions

Would you like an MCP server configured for this repo (e.g., a Playwright or other test server)?
