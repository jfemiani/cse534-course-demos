"""Demo 3b: three ways to cut plain text into chunks, and what each one costs.

See 03b_chunking_strategies_text.md for the full explanation.
"""

SYLLABUS_EXCERPT = (
    "CSE 534 meets Tuesdays and Thursdays from 3:00pm to 4:20pm. "
    "Attendance is not graded, but the material moves quickly and each "
    "lecture builds on the last one, so missing a session usually costs "
    "more time than it saves.\n\n"
    "Exam 1 covers mathematical foundations: probability, entropy, and the "
    "normal distribution. It is closed-book, but a one-page formula sheet "
    "is allowed and must be handed in with the exam.\n\n"
    "Labs are submitted through Canvas as a single Python file, due by "
    "11:59pm on the posted date. Late labs lose ten percent per day and "
    "are not accepted after one week."
)


def fixed_size_chunks(text: str, chunk_size: int) -> list[str]:
    """Cut text every chunk_size characters, with no regard for word or
    sentence boundaries."""
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


def fixed_size_chunks_with_overlap(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Same blind cut as fixed_size_chunks, but each chunk after the first
    repeats the last `overlap` characters of the previous chunk."""
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start : start + chunk_size])
        start += chunk_size - overlap
    return chunks


def recursive_chunks(text: str, chunk_size: int, separators: list[str] | None = None) -> list[str]:
    """Prefer the biggest natural break that still fits: split on paragraph
    breaks first, merging pieces back together up to chunk_size; only split
    a too-long piece further on the next separator (sentence, then word,
    then a hard character cut). This is the idea behind LangChain's
    RecursiveCharacterTextSplitter."""
    if separators is None:
        separators = ["\n\n", ". ", " "]

    separator, *rest_separators = separators
    pieces = text.split(separator)

    # Recurse into any piece that is still too big, using the next
    # separator down the list (or a hard character cut if none is left).
    units: list[str] = []
    for piece in pieces:
        if len(piece) <= chunk_size:
            units.append(piece)
        elif rest_separators:
            units.extend(recursive_chunks(piece, chunk_size, rest_separators))
        else:
            units.extend(fixed_size_chunks(piece, chunk_size))

    # Re-join units with the separator that split them, packing as many as
    # possible into each chunk before starting a new one.
    chunks: list[str] = []
    current = ""
    for unit in units:
        candidate = current + separator + unit if current else unit
        if len(candidate) <= chunk_size:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = unit
    if current:
        chunks.append(current)
    return chunks


def show(label: str, chunks: list[str]) -> None:
    print(f"\n{label} ({len(chunks)} chunks):")
    for i, chunk in enumerate(chunks):
        print(f"  [{i}] {chunk!r}")


CHUNK_SIZE = 90
show("1. Fixed-size, no overlap", fixed_size_chunks(SYLLABUS_EXCERPT, CHUNK_SIZE))
show(
    "2. Fixed-size, 20-char overlap",
    fixed_size_chunks_with_overlap(SYLLABUS_EXCERPT, CHUNK_SIZE, overlap=20),
)
show("3. Recursive / structure-aware", recursive_chunks(SYLLABUS_EXCERPT, CHUNK_SIZE))
