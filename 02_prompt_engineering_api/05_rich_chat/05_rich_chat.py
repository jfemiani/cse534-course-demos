"""Render model Markdown cleanly in a terminal with Rich."""

import os

from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

client = OpenAI()
console = Console()
model = os.getenv("OPENAI_MODEL", "gpt-5.6")
previous_id = None

while True:
    user_text = console.input("[bold cyan]You:[/] ").strip()
    if user_text.lower() in {"quit", "exit"}:
        break

    response = client.responses.create(
        model=model,
        input=user_text,
        previous_response_id=previous_id,
    )
    console.print("[bold green]Assistant:[/]")
    console.print(Markdown(response.output_text))
    previous_id = response.id
