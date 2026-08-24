# 2c: Mixing a hosted tool with a function tool

Concept: an `Agent` can hold both kinds of tools in one `tools=[...]` list.
`lookup_room_number` is an ordinary `@function_tool` running our own Python
code. `WebSearchTool()` is a **hosted (cloud-run) tool** — OpenAI runs the
search itself; no code on our side executes for that call. The Agents SDK's
loop doesn't care which kind of tool it dispatches to: it calls whichever
tool the model asks for, feeds back the result, and repeats until the model
has a final answer, exactly as in `02a_agent_loop_agents_sdk.py`.

The one demo question ("What room is Professor Femiani in, and what is one
real news story from today?") forces both tools to fire in the same run, so
the printed trace shows one local tool call and one hosted tool call side
by side.

## Compare with

- `02a_agent_loop_agents_sdk.py` — two local `@function_tool`s only, no
  hosted tool.
- `02b_agent_loop_manual.py` — the same loop hand-rolled with the Responses
  API, no Agents SDK.

## Endpoint

OpenAI Agents SDK (`agents.Agent`, `agents.Runner`, `agents.function_tool`,
`agents.WebSearchTool`).

## Regeneration prompt

If the Agents SDK changes, ask an LLM assistant: "Update this script to
match the current OpenAI Agents SDK. Keep `lookup_room_number` as a local
function tool and `WebSearchTool()` as the hosted tool, and keep the single
question that requires both."
