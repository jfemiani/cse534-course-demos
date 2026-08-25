# pip install openai-agents

"""Demo 2a: the agent loop, done by the OpenAI Agents SDK.

See 02a_agent_loop_agents_sdk.md for the full explanation.
"""

import os

from agents import Agent, Runner, function_tool
from agents.items import ToolCallItem, ToolCallOutputItem

model = os.getenv("OPENAI_MODEL", "gpt-5.6")

OFFICE_HOURS = {"femiani": "Tuesdays 2-4pm"}
ROOM_NUMBERS = {"femiani": "Laws Hall 205"}


def _lookup(table: dict[str, str], instructor: str) -> str:
    name = instructor.lower()
    for key, value in table.items():
        if key in name:
            return value
    return "unknown"


@function_tool
def lookup_office_hours(instructor: str) -> str:
    """Look up office hours for an instructor."""
    return _lookup(OFFICE_HOURS, instructor)


@function_tool
def lookup_room_number(instructor: str) -> str:
    """Look up room number for an instructor."""
    return _lookup(ROOM_NUMBERS, instructor)


agent = Agent(
    name="Course Assistant",
    instructions="Answer questions about instructors using the lookup tools.",
    tools=[lookup_office_hours, lookup_room_number],
    model=model,
)

question = "When and where can I meet Professor Femiani in person this week?"
result = Runner.run_sync(agent, question)

for item in result.new_items:
    if isinstance(item, ToolCallItem):
        print(f"Tool call: {item.raw_item.name}({item.raw_item.arguments})")
    elif isinstance(item, ToolCallOutputItem):
        print(f"Tool output: {item.output}")

print(f"Final answer: {result.final_output}")
