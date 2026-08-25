# 2a: The agent loop, done by the OpenAI Agents SDK

Concept: what OpenAI's docs call the "agent loop" and what the research
literature calls the ReAct pattern (Yao et al. 2022, arXiv:2210.03629):
reason, act, observe, repeat, until the model decides it has enough to
answer. This variant lets the **OpenAI Agents SDK** run that loop. Two
tools are decorated with `@function_tool`, handed to an `Agent`, and
`Runner.run_sync(...)` drives the whole multi-step exchange: it calls
whichever tools the model asks for, feeds the results back, and keeps
going until the model has a final answer — all in one call.

This is the version to reach for by default. Hand-rolling the loop (see
`02b_agent_loop_manual.py`) is worth doing once, to see the mechanism the
SDK is automating, but production code should prefer the Agents SDK, or
the Responses API's own built-in tools (`web_search`, `file_search`,
`code_interpreter`), which run an equivalent loop internally.

## Compare with

- `02b_agent_loop_manual.py` — the same two tools and question, with the
  turn-by-turn loop, argument parsing, and `function_call_output` messages
  all written out by hand.

## Endpoint

OpenAI Agents SDK (`agents.Agent`, `agents.Runner`, `agents.function_tool`),
which wraps the Responses API.

## Regeneration prompt

If the Agents SDK changes, ask an LLM assistant: "Update this script to
match the current OpenAI Agents SDK. Keep both tools
(`lookup_office_hours`, `lookup_room_number`) and the single question about
meeting an instructor in person."
