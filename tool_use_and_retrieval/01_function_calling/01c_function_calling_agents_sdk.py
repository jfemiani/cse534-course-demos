# pip install openai-agents
import os

from agents import Agent, Runner, function_tool
from agents.items import ToolCallItem, ToolCallOutputItem

model = os.getenv("OPENAI_MODEL", "gpt-5.6")


@function_tool
def count_letter(word: str, letter: str) -> int:
    """Count how many times a letter appears in a word."""
    return word.lower().count(letter.lower())


agent = Agent(
    name="Letter Counter",
    instructions="Answer letter-counting questions using the count_letter tool.",
    tools=[count_letter],
    model=model,
)

result = Runner.run_sync(agent, "How many times does the letter 'r' appear in 'strawberry'?")

for item in result.new_items:
    if isinstance(item, ToolCallItem):
        print(f"Tool call: {item.raw_item}")
    if isinstance(item, ToolCallOutputItem):
        print(f"Tool output: {item.output}")

print(f"Final answer: {result.final_output}")
