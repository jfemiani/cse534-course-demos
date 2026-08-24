# pip install openai-agents

"""Demo 2c: mixing a hosted (cloud-run) tool with a function tool in one Agent.

See 02c_agent_loop_hosted_tools.md for the full explanation.
"""

import os

from agents import Agent, Runner, WebSearchTool, function_tool
from agents.items import ToolCallItem, ToolCallOutputItem

model = os.getenv("OPENAI_MODEL", "gpt-5.6")

ROOM_NUMBERS = {"femiani": "Laws Hall 205"}


@function_tool
def lookup_room_number(instructor: str) -> str:
    """Look up room number for an instructor."""
    name = instructor.lower()
    for key, value in ROOM_NUMBERS.items():
        if key in name:
            return value
    return "unknown"


agent = Agent(
    name="Course Assistant",
    instructions=(
        "Answer questions about instructors and current events. "
        "Use lookup_room_number for room numbers. Use web search for anything "
        "that needs current, real-world information you were not trained on."
    ),
    tools=[lookup_room_number, WebSearchTool()],
    model=model,
)

question = (
    "What room is Professor Femiani in, and what is one real news story "
    "from today?"
)
result = Runner.run_sync(agent, question)

for item in result.new_items:
    if isinstance(item, ToolCallItem):
        print(f"Tool call: {type(item.raw_item).__name__}")
    elif isinstance(item, ToolCallOutputItem):
        print(f"Tool output: {str(item.output)[:120]}")

print(f"Final answer: {result.final_output}")
