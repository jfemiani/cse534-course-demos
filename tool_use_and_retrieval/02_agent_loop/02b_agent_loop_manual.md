# 2b: The agent loop, hand-rolled

Concept: the same ReAct-style agent loop as `02a_agent_loop_agents_sdk.py`
(Yao et al. 2022, arXiv:2210.03629), but written out by hand against the
plain Responses API instead of the Agents SDK, so every step stays
visible: the model calls one or both tools, the code runs them and sends
`function_call_output` items back, and the loop repeats — checking
`response.output` for a `function_call` item — until the model stops
asking for tools and returns a final answer.

Both tools take the same one-field argument, so they share a single
Pydantic model (`InstructorArgs`), the same pattern as Demo 1b
(`01b_function_calling_pydantic.py`): schema from `model_json_schema()`,
arguments parsed back with `model_validate_json()` instead of
`json.loads()`.

This manual version exists to show the mechanism underneath 02a. Once
that mechanism is clear, prefer the Agents SDK version, or the Responses
API's own built-in tools (`web_search`, `file_search`, `code_interpreter`),
for anything beyond a teaching demo.

## Compare with

- `02a_agent_loop_agents_sdk.py` — the same two tools and question, run
  through the OpenAI Agents SDK's `Agent` / `Runner`, with no hand-written
  loop or argument parsing.

## Endpoint

OpenAI Responses API (`client.responses.create`), `tools=[...]`, looping
while `response.output` still contains a `function_call` item.

## Regeneration prompt

If OpenAI changes this API, ask an LLM assistant: "Update this script to
match the current OpenAI Responses API tool-calling loop. Keep both tools
(`lookup_office_hours`, `lookup_room_number`), the Pydantic argument model,
and keep every loop step printed."
