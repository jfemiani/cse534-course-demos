# Prompt Engineering and API Integration demonstrations

Work through these demonstrations in the order used by the Canvas module. The first three build one idea at a time: a single API request, remembered conversation state, and streaming output. Demos 4 and 5 are optional presentation enhancements. Demo 6 returns data that Python can validate and use reliably.

## Demos

1. [Your first Responses API call](01_hello)
2. [A non-streaming terminal chat](02_chat)
3. [A streaming terminal chat](03_chat_streaming)
4. [Rich terminal formatting basics](04_rich_basics) — optional presentation tangent
5. [Rich formatting applied to chat](05_rich_chat) — optional presentation tangent
6. [Structured output with Pydantic](06_structured_output)

Each folder contains:

- the reviewed Python file shown in the course; and
- PROMPT.md, containing the complete regeneration prompt.

In this module, a regeneration prompt is called evergreen because it tells the AI coding assistant to check current official documentation before writing code. That makes it useful when an API or SDK changes. It does not guarantee correct code: compare any generated result with the reviewed Python file and the current documentation.

Follow the Canvas lesson for API-access setup, safe key storage, exact run instructions, and what to change in each demonstration.
