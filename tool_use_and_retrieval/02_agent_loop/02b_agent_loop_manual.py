# pip install openai pydantic

"""Demo 2b: the agent loop, hand-rolled - what the Agents SDK does for you.

See 02b_agent_loop_manual.md for the full explanation.
"""

import os

from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()
model = os.getenv("OPENAI_MODEL", "gpt-5.6")

OFFICE_HOURS = {"femiani": "Tuesdays 2-4pm"}
ROOM_NUMBERS = {"femiani": "Laws Hall 205"}


def _lookup(table: dict[str, str], instructor: str) -> str:
    name = instructor.lower()
    for key, value in table.items():
        if key in name:
            return value
    return "unknown"


def lookup_office_hours(instructor: str) -> str:
    return _lookup(OFFICE_HOURS, instructor)


def lookup_room_number(instructor: str) -> str:
    return _lookup(ROOM_NUMBERS, instructor)


TOOL_FUNCTIONS = {
    "lookup_office_hours": lookup_office_hours,
    "lookup_room_number": lookup_room_number,
}


class InstructorArgs(BaseModel):
    instructor: str


tool_schema = [
    {
        "type": "function",
        "name": "lookup_office_hours",
        "description": "Look up office hours for an instructor.",
        "parameters": InstructorArgs.model_json_schema(),
    },
    {
        "type": "function",
        "name": "lookup_room_number",
        "description": "Look up room number for an instructor.",
        "parameters": InstructorArgs.model_json_schema(),
    },
]

question = "When and where can I meet Professor Femiani in person this week?"
response = client.responses.create(model=model, input=question, tools=tool_schema)

step = 1
while any(item.type == "function_call" for item in response.output):
    tool_outputs = []
    for item in response.output:
        if item.type != "function_call":
            continue
        args = InstructorArgs.model_validate_json(item.arguments)
        result = TOOL_FUNCTIONS[item.name](args.instructor)
        print(f"Step {step}: model called {item.name}({args}) -> {result}")
        tool_outputs.append(
            {"type": "function_call_output", "call_id": item.call_id, "output": str(result)}
        )
    response = client.responses.create(
        model=model, previous_response_id=response.id, input=tool_outputs
    )
    step += 1

print(f"Final answer: {response.output_text}")
