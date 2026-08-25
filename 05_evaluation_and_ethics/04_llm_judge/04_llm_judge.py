"""Demo: ask a model to judge answers instead of scoring word overlap.

See 04_llm_judge.md for the full explanation.
"""

import os

from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()
model = os.getenv("OPENAI_MODEL", "gpt-5.6")

QUESTION = "When are office hours and where do I go?"
REFERENCE = "Office hours are Tuesdays from 2 to 4 pm in Laws Hall room 205."

# The same three candidates 03_bleu_score.py scored with BLEU.
CANDIDATES = {
    "exact match": "Office hours are Tuesdays from 2 to 4 pm in Laws Hall room 205.",
    "good paraphrase, low overlap": "You can stop by on Tuesday afternoons between 2 and 4 in Laws Hall 205.",
    "wrong room, high overlap": "Office hours are Tuesdays from 2 to 4 pm in Laws Hall room 305.",
}


class Judgment(BaseModel):
    correct: bool
    quality: int  # 1 (bad) to 5 (excellent)
    reason: str


def judge(question: str, reference: str, candidate: str) -> Judgment:
    prompt = (
        f"Question: {question}\n"
        f"Reference answer: {reference}\n"
        f"Student answer: {candidate}\n\n"
        "Judge the student answer against the reference. Be strict about "
        "factual details such as room numbers, days, and times."
    )
    response = client.responses.parse(
        model=model,
        input=prompt,
        text_format=Judgment,
    )
    return response.output_parsed


for label, candidate in CANDIDATES.items():
    result = judge(QUESTION, REFERENCE, candidate)
    print(f"{label:30s} correct={result.correct!s:5s} quality={result.quality}/5")
    print(f"{'':30s} reason: {result.reason}")
    print()
