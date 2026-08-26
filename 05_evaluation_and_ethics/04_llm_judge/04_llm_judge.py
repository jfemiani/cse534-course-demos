"""Demo: ask a model to judge something no formula can score at all.

See 04_llm_judge.md for the full explanation.
"""

import os

from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()
model = os.getenv("OPENAI_MODEL", "gpt-5.6")

# Real MT-Bench question 151 (humanities category), a two-turn conversation
# with no reference answer at all. Zheng et al., "Judging LLM-as-a-Judge
# with MT-Bench and Chatbot Arena," 2023. https://github.com/lm-sys/FastChat
QUESTION = (
    "Provide insights into the correlation between economic indicators such "
    "as GDP, inflation, and unemployment rates. Explain how fiscal and "
    "monetary policies affect those indicators."
)
FOLLOW_UP = "Now, explain them again like I'm five."


class Judgment(BaseModel):
    appropriate_for_a_five_year_old: bool
    reason: str


def answer_eli5(question: str, follow_up: str) -> tuple[str, str]:
    first_turn = client.responses.create(model=model, input=question).output_text.strip()
    second_prompt = f"Question: {question}\nYour answer: {first_turn}\n\n{follow_up}"
    second_turn = client.responses.create(model=model, input=second_prompt).output_text.strip()
    return first_turn, second_turn


def judge(explanation: str) -> Judgment:
    prompt = (
        f"Explanation given in response to 'explain it again like I'm five': "
        f"{explanation!r}\n\n"
        "Judge whether this explanation actually reads as something a "
        "five-year-old could follow: short sentences, concrete images, no "
        "jargon like 'GDP' or 'monetary policy' left unexplained. There is "
        "no fixed rule for this; use your own judgment."
    )
    response = client.responses.parse(
        model=model,
        input=prompt,
        text_format=Judgment,
    )
    assert response.output_parsed is not None
    return response.output_parsed


first_turn, eli5_answer = answer_eli5(QUESTION, FOLLOW_UP)
result = judge(eli5_answer)
print(f"first-turn answer:\n{first_turn}\n")
print(f"eli5 answer:\n{eli5_answer}\n")
print(f"appropriate for a five-year-old: {result.appropriate_for_a_five_year_old}")
print(f"reason: {result.reason}")


