# pip install openai-agents

"""Demo 2d: calling a real, external MCP server with HostedMCPTool.

See 02d_agent_loop_mcp.md for the full explanation.
"""

import os

from agents import Agent, HostedMCPTool, Runner
from agents.items import ToolCallItem, ToolCallOutputItem

model = os.getenv("OPENAI_MODEL", "gpt-5.6")

deepwiki = HostedMCPTool(
    tool_config={
        "type": "mcp",
        "server_label": "deepwiki",
        "server_url": "https://mcp.deepwiki.com/mcp",
        "require_approval": "never",
    }
)

agent = Agent(
    name="Repo Assistant",
    instructions=(
        "Answer questions about public GitHub repositories using the "
        "deepwiki MCP server's tools."
    ),
    tools=[deepwiki],
    model=model,
)

question = (
    "Using the openai/openai-agents-python repo, what is the Agents SDK's "
    "main loop actually doing when it runs an agent?"
)
result = Runner.run_sync(agent, question)

for item in result.new_items:
    if isinstance(item, ToolCallItem):
        print(f"Tool call: {type(item.raw_item).__name__}")
    elif isinstance(item, ToolCallOutputItem):
        print(f"Tool output: {str(item.output)[:120]}")

print(f"Final answer: {result.final_output}")
