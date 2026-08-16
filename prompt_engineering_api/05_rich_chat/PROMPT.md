# Regeneration prompt

This is an evergreen prompt: it tells an AI coding assistant to consult current official documentation before it writes the program. That matters here because APIs, SDK methods, and recommended models can change. The Python file beside this prompt is the reviewed course version; rerunning the prompt lets you compare a newly generated version with that reviewed snapshot.

## How to use it

Copy the Base contract and the Demo request below into an AI coding assistant. Review generated code before running it.

## Base contract

Create one very short, pedagogically useful Python program for an upper-level Generative AI course. Before writing code, consult the current official documentation for every API and model used. Use the current recommended API, not a deprecated compatibility API. Use the official Python SDK and read the API key from OPENAI_API_KEY. Read the primary model from OPENAI_MODEL, with a current broadly available default. Introduce only the requested new concept; do not add a web framework, classes, async code, retries, logging frameworks, or helper abstractions unless the concept requires them. Include a module docstring, clear variable names, type annotations where they clarify data, and brief comments that explain concepts rather than restating syntax. Do not hide response objects or tool loops behind a third-party framework. After the code, state the install command, run command, expected behavior, likely cost-bearing operations, and the exact official documentation pages checked. If a current API differs from the requested shape, explain the change and implement the current form. Output only one Python file plus the short run notes.

## Demo request

Filename 05_rich_chat.py. Apply the Console and Markdown ideas from demo 04 to the non-streaming chat from demo 02. Do not add panels, layouts, or live displays. Explain that Rich affects presentation, not OpenAI conversation state or the response protocol.
