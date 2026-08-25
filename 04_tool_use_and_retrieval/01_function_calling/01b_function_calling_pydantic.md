# 01b: Tool use with a Pydantic-generated argument schema

Concept: tool use, also called function calling. The model does not run code.
It emits a structured request naming a function and arguments; our code runs
the real function and sends the result back as a `function_call_output` item.
This demo asks the same letter-counting question as 01a, so the only thing
that changes is how the tool's argument schema is produced.

Tool arguments are defined once, as a Pydantic model, the same way Demo 6
(`06_structured_output`) defined its output schema. The tool's JSON schema
comes from `CountLetterArgs.model_json_schema()`; the model's arguments come
back validated through `CountLetterArgs.model_validate_json(...)` instead of
a raw `json.loads()`.

This is **not** the `openai.pydantic_function_tool()` helper: that helper
builds the nested Chat Completions tool shape
(`{"type": "function", "function": {...}}`), not the flat shape the
Responses API expects (`{"type": "function", "name": ..., "parameters": ...}`),
so this demo builds the flat dict directly from the Pydantic schema instead.

## Compare with

- `01a_function_calling_json.py` — the same schema hand-typed as a JSON dict.
- `01c_function_calling_agents_sdk.py` — the schema generated automatically
  from the function's own signature via the Agents SDK, with no manual
  dispatch loop at all.

## Endpoint

OpenAI Responses API (`client.responses.create`), `tools=[...]` with
`tool_choice="required"` so the demo reliably calls the tool.

## Regeneration prompt

If OpenAI changes this API, ask an LLM assistant: "Update this script to
match the current OpenAI Responses API function-calling format. Keep the
Pydantic argument model, the single tool, the single round trip, and the
letter-counting question."
