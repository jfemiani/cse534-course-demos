# 01c: Tool use via the OpenAI Agents SDK's @function_tool decorator

Concept: 01a and 01b both hand-wrote the tool schema and the call/response
loop. The **OpenAI Agents SDK** automates both. Decorate a plain function
with `@function_tool` and it generates the JSON schema from the function's
own type hints and docstring — no `CountLetterArgs` class, no
`model_json_schema()` call. Give that tool to an `Agent` and run it with
`Runner.run_sync(...)`, and the SDK handles calling the tool, feeding the
result back to the model, and returning the final answer — no manual
`function_call_output` round trip.

This is a genuine framework, not just a convenience helper: `Agent` and
`Runner` sit on top of the Responses API rather than calling
`client.responses.create` directly. It's the natural next step once
students have seen 01a (bare JSON) and 01b (Pydantic schema) and want to
see what disappears when a framework takes over both jobs.

## Compare with

- `01a_function_calling_json.py` — hand-typed schema, manual dispatch.
- `01b_function_calling_pydantic.py` — Pydantic-generated schema, manual
  dispatch, same plain `client.responses.create` calls as 01a.

## Endpoint

OpenAI Agents SDK (`agents.Agent`, `agents.Runner`, `agents.function_tool`),
which wraps the Responses API.

## Troubleshooting

If you see `TypeError: process() takes no keyword arguments` from `httpx2`
when running this demo, your environment has the plain `Brotli` package
installed instead of `brotlicffi`. Fix with:

```
pip uninstall -y Brotli
pip install brotlicffi
```

## Regeneration prompt

If the Agents SDK changes, ask an LLM assistant: "Update this script to
match the current OpenAI Agents SDK. Keep the `@function_tool`-decorated
`count_letter` function, the single `Agent`, and the letter-counting
question."
