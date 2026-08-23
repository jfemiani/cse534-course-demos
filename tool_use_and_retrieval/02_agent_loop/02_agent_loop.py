"""Demo: the agent loop - the model calling tools repeatedly on its own.

Concept: what OpenAI's docs call the "agent loop" and what the research
literature calls the ReAct pattern (Yao et al. 2022, arXiv:2210.03629):
reason, act, observe, repeat, until the model decides it has enough to
answer. The loop below is hand-written so every step stays visible. In
production, prefer the Responses API's built-in tools (web_search,
file_search, code_interpreter), which run this same loop internally, or the
OpenAI Agents SDK if the task needs more than one agent.

Endpoint: OpenAI Responses API (client.responses.create), tools=[...],
looping while response.output still contains a function_call item.

If OpenAI changes this API, ask an LLM assistant: "Update this script to
match the current OpenAI Responses API tool-calling loop. Keep both tools
(lookup_office_hours, lookup_room_number) and keep every loop step printed."
"""

import json
import os

from openai import OpenAI

client = OpenAI()
model = os.getenv("OPENAI_MODEL", "gpt-5.6")

OFFICE_HOURS = {"femiani": "Tuesdays 2-4pm"}
ROOM_NUMBERS = {"femiani": "Laws Hall 205"}


def lookup_office_hours(instructor: str) -> str:
    return OFFICE_HOURS.get(instructor.lower(), "unknown")


def lookup_room_number(instructor: str) -> str:
    return ROOM_NUMBERS.get(instructor.lower(), "unknown")


TOOL_FUNCTIONS = {
    "lookup_office_hours": lookup_office_hours,
    "lookup_room_number": lookup_room_number,
}

tool_schema = [
    # TOOL_FUNCTIONS is a dict, so this loops over its two keys, building one
    # tool description per function.
    {
        "type": "function",
        "name": name,
        "description": f"Look up {name.replace('_', ' ')} for an instructor.",
        "parameters": {
            "type": "object",
            "properties": {"instructor": {"type": "string"}},
            "required": ["instructor"],
        },
    }
    for name in TOOL_FUNCTIONS
]

question = "When and where can I meet Professor Femiani in person this week?"
response = client.responses.create(model=model, input=question, tools=tool_schema)

step = 1
while any(item.type == "function_call" for item in response.output):
    tool_outputs = []
    for item in response.output:
        if item.type != "function_call":
            continue
        args = json.loads(item.arguments)
        result = TOOL_FUNCTIONS[item.name](**args)
        print(f"Step {step}: model called {item.name}({args}) -> {result}")
        tool_outputs.append(
            {"type": "function_call_output", "call_id": item.call_id, "output": str(result)}
        )
    response = client.responses.create(
        model=model, previous_response_id=response.id, input=tool_outputs
    )
    step += 1

print(f"Final answer: {response.output_text}")
