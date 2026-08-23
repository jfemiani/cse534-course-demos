"""Demo: how a coding assistant decides which SKILL.md file to read.

Concept: SKILL.md files are not tools the model calls. They are instructions
the model reads on demand, based on the file's short description, instead of
being stuffed into every prompt. This script models that dispatch step: given
a task, score each skill's description against the task by keyword overlap
(the same idea as the keyword retrieval in the previous lesson), and load
the body of whichever skill scores highest.

This is a teaching simplification. Real coding assistants match a task to a
skill using the model's own judgement together with the description field,
not a fixed keyword-overlap formula. The point here is to make the *idea* of
progressive disclosure visible: only the name and description are read up
front, and the full instructions load only once a skill is selected.

No external API is called by this script.

If this demo needs updating, ask an LLM assistant: "Update this script to
reflect how SKILL.md dispatch actually works in <tool name>, if it differs
from simple keyword matching." Keep the two example skill files and the
scoring step visible.
"""

from pathlib import Path

SKILLS_DIR = Path(__file__).parent / "sample_skills"


def read_frontmatter(path: Path) -> dict[str, str]:
    """Pull name/description out of a SKILL.md file's YAML frontmatter."""
    lines = path.read_text().splitlines()
    fields = {}
    for line in lines[1:]:  # skip the opening ---
        if line.strip() == "---":
            break
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"')
    return fields


def keyword_score(task: str, description: str) -> int:
    task_tokens = set(task.lower().split())
    description_tokens = set(description.lower().split())
    return len(task_tokens & description_tokens)


task = "The OpenAI Responses API changed and this demo script no longer runs."

skills = [
    (path, read_frontmatter(path)) for path in sorted(SKILLS_DIR.glob("*.SKILL.md"))
]

print(f"Task: {task}\n")
for path, frontmatter in skills:
    score = keyword_score(task, frontmatter["description"])
    print(f"{path.name:30s} score={score}  {frontmatter['description'][:60]}")

best_path, _ = max(skills, key=lambda entry: keyword_score(task, entry[1]["description"]))
print(f"\nWould load in full: {best_path.name}")
