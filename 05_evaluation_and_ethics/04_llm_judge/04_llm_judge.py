"""Demo: ask a model to judge something no formula can score at all.

See 04_llm_judge.md for the full explanation.
"""

import os

from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()
model = os.getenv("OPENAI_MODEL", "gpt-5.6")

# Three replies a TA might send to the same student email. There is no
# single "correct" reply to compare these against, so a word-overlap
# metric has nothing to score them against. "Friendly" is a judgment call.
REPLIES = {
    "warm": "Hi Sam! No problem at all, take the extra day and let me know if you need anything else.",
    "curt": "Extension granted. Submit by Friday.",
    "cold_but_polite": "Your request has been reviewed. An extension until Friday is approved.",
}


class Judgment(BaseModel):
    friendly: bool
    reason: str


def judge(reply: str) -> Judgment:
    prompt = (
        f"Email reply: {reply!r}\n\n"
        "Judge whether this reply reads as friendly, the way one person would "
        "describe another person's tone in conversation. There is no fixed "
        "rule for this; use your own sense of tone."
    )
    response = client.responses.parse(
        model=model,
        input=prompt,
        text_format=Judgment,
    )
    return response.output_parsed


for label, reply in REPLIES.items():
    result = judge(reply)
    print(f"{label:15s} friendly={result.friendly!s:5s} {reply!r}")
    print(f"{'':15s} reason: {result.reason}")
    print()

