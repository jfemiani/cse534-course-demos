"""Demo 3c: fixed-line chunking vs. AST-aware chunking for source code.

See 03c_chunking_strategies_code.md for the full explanation.
"""

import ast
import textwrap

SAMPLE_CODE = textwrap.dedent(
    '''\
    """A tiny grade-book module, used only as chunking material."""


    def letter_grade(score: float) -> str:
        """Convert a numeric score to a letter grade."""
        if score >= 90:
            return "A"
        if score >= 80:
            return "B"
        if score >= 70:
            return "C"
        return "F"


    def class_average(scores: list[float]) -> float:
        """Return the mean of a list of scores, or 0.0 if empty."""
        if not scores:
            return 0.0
        return sum(scores) / len(scores)


    class GradeBook:
        """Tracks scores for one class section."""

        def __init__(self, section: str) -> None:
            self.section = section
            self.scores: list[float] = []

        def record(self, score: float) -> None:
            self.scores.append(score)
    '''
)


def fixed_line_chunks(source: str, lines_per_chunk: int) -> list[str]:
    """Cut source code every N lines, with no regard for function or class
    boundaries."""
    lines = source.splitlines()
    return [
        "\n".join(lines[i : i + lines_per_chunk])
        for i in range(0, len(lines), lines_per_chunk)
    ]


def ast_aware_chunks(source: str) -> list[str]:
    """Parse the source and return one chunk per top-level function or
    class, each a complete, independently-readable unit."""
    tree = ast.parse(source)
    chunks = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            chunks.append(ast.get_source_segment(source, node))
    return chunks


def show(label: str, chunks: list[str]) -> None:
    print(f"\n{label} ({len(chunks)} chunks):")
    for i, chunk in enumerate(chunks):
        print(f"  --- chunk {i} ---")
        print(textwrap.indent(chunk, "  "))


LINES_PER_CHUNK = 6
show("1. Fixed-size, 6 lines per chunk", fixed_line_chunks(SAMPLE_CODE, LINES_PER_CHUNK))
show("2. AST-aware, one function/class per chunk", ast_aware_chunks(SAMPLE_CODE))

print(
    "\nIn strategy 1, look at chunk 2 and chunk 3: `class_average`'s "
    "signature, docstring, and empty-list check end up in chunk 2, while "
    "its final `return` statement lands alone in chunk 3. Either half on "
    "its own would embed and retrieve poorly. Strategy 2 never splits a "
    "function or class, because it cuts on the source's own syntax tree "
    "instead of a line count.\n"
    "\nOpenAI's file_search auto-chunking strategy has no idea a .py file is "
    "code; it applies the same token-count-and-overlap rule it would use on "
    "a novel. For a codebase, an AST-aware pass like strategy 2 - or a "
    "purpose-built code splitter such as LangChain's "
    "RecursiveCharacterTextSplitter.from_language(Language.PYTHON) - should "
    "happen before the files ever reach an embedding call."
)
