# pip install openai-agents python-dotenv

"""Demo 5: SKILL.md instructions, dispatched into an agent-as-tool.

See 05_agent_instructions.md for the full explanation.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from agents import Agent, Runner

load_dotenv()

SKILLS_DIR = Path(__file__).parent / "sample_skills"
model = os.getenv("OPENAI_MODEL", "gpt-5.6")


def read_skill(path: Path) -> tuple[dict[str, str], str]:
    """Split a SKILL.md file into its front matter fields and its body."""
    text = path.read_text()
    _, frontmatter_text, body = text.split("---", 2)
    fields = {}
    for line in frontmatter_text.strip().splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"')
    return fields, body.strip()


def keyword_score(task: str, description: str) -> int:
    task_tokens = set(task.lower().split())
    description_tokens = set(description.lower().split())
    return len(task_tokens & description_tokens)


task = "Can you write me a caption for this hike photo I want to post on instagram?"

skills = [read_skill(path) for path in sorted(SKILLS_DIR.glob("*.SKILL.md"))]

print(f"Task: {task}\n")
for frontmatter, _ in skills:
    score = keyword_score(task, frontmatter["description"])
    print(f"{frontmatter['name']:25s} score={score}  {frontmatter['description'][:60]}")

best_frontmatter, best_body = max(
    skills, key=lambda entry: keyword_score(task, entry[0]["description"])
)
print(f"\nLoading in full: {best_frontmatter['name']}\n")

specialist = Agent(
    name=best_frontmatter["name"],
    instructions=f"You are a writing assistant.\n\n{best_body}",
    model=model,
)

manager = Agent(
    name="Writing Manager",
    instructions="Use the writing_specialist tool to handle the user's request.",
    tools=[
        specialist.as_tool(
            tool_name="writing_specialist",
            tool_description=best_frontmatter["description"],
        )
    ],
    model=model,
)

result = Runner.run_sync(manager, task)
print(f"Final answer:\n{result.final_output}")
