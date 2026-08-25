"""Meet Rich before using it in an AI program."""

from rich.console import Console
from rich.markdown import Markdown
from rich.progress import track

console = Console()
console.print("[bold cyan]Styled terminal text[/]")
console.print(Markdown("## Markdown\nRich can render **emphasis** and `code`."))

for step in track(range(3), description="Three quick steps..."):
    console.print(f"finished step {step + 1}")
