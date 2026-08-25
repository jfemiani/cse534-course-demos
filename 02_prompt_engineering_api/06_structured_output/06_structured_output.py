"""Turn natural language into a validated Python object."""

import os

from openai import OpenAI
from pydantic import BaseModel


class CourseTask(BaseModel):
    title: str
    due_date: str | None
    estimated_minutes: int
    deliverables: list[str]


client = OpenAI()
model = os.getenv("OPENAI_MODEL", "gpt-5.6")

response = client.responses.parse(
    model=model,
    input="Read chapter 3 by Friday and submit a one-page critique.",
    text_format=CourseTask,
)

task = response.output_parsed
print(task.model_dump_json(indent=2))
