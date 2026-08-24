# 01a: Tool use with a hand-typed JSON schema

Concept: tool use, also called function calling. The model does not run code.
It emits a structured request naming a function and arguments; our code runs
the real function and sends the result back as a `function_call_output` item.
This demo asks a question language models are famous for getting wrong on
their own (counting letters in a word), so the tool's answer is visibly
better than a guess would be.

This is the bare-metal version: the tool's JSON schema is a hand-typed dict,
and the model's returned arguments are parsed with `json.loads()`.

## Compare with

- `01b_function_calling_pydantic.py` — the same schema generated from a
  Pydantic model instead of hand-typed, with the arguments validated instead
  of just parsed.
- `01c_function_calling_agents_sdk.py` — the OpenAI Agents SDK's
  `@function_tool` decorator, which generates this same schema from the
  function's own signature and docstring, and runs the call/response loop
  for you.

## Endpoint

OpenAI Responses API (`client.responses.create`), `tools=[...]` with
`tool_choice="required"` so the demo reliably calls the tool.

## Regeneration prompt

If OpenAI changes this API, ask an LLM assistant: "Update this script to
match the current OpenAI Responses API function-calling format. Keep the
hand-typed JSON schema, the single tool, the single round trip, and the
letter-counting question."
