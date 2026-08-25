# 5: SKILL.md instructions, dispatched into an agent-as-tool

Concept: a SKILL.md is not a tool call. Only its short front-matter
description is read up front; the full body loads only once a task matches
it. This demo models that dispatch step with keyword-overlap scoring (the
same idea as the keyword retrieval in the chunking lesson), then does
something with the result: the winning skill's full body is appended to a
specialist agent's `instructions=` string, that specialist is wrapped with
`Agent.as_tool()`, and a manager agent calls it, the same agents-as-tools
pattern the agent-loop lessons used for a lookup function, applied here to a
block of prose instructions instead.

The three example skills (`tldr_summary`, `add_hashtags`,
`flag_unsupported_claims`) are generic, publicly recognizable writing tasks,
not this course's own production tooling, so the demo stands on its own
outside this repo.

This is a teaching simplification: real coding assistants pick a skill using
the model's own judgement together with the description field, not a fixed
word-overlap score.

## Endpoint

OpenAI Agents SDK (`agents.Agent`, `agents.Runner`, `Agent.as_tool`), which
wraps the Responses API. Requires `OPENAI_API_KEY`; makes one real model
call.

## Regeneration prompt

If this demo needs updating, ask an LLM assistant: "Update this script to
reflect how SKILL.md dispatch actually works in `<tool name>`, if it differs
from simple keyword matching." Keep the scoring step and the `as_tool()`
wiring visible.
