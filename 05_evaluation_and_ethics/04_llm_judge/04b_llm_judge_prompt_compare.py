"""Demo: use an LLM judge to compare two prompts, not two candidate answers.

See 04b_llm_judge_prompt_compare.md for the full explanation.
"""

import os
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel

client = OpenAI()
model = os.getenv("OPENAI_MODEL", "gpt-5.6")

CONTEXT = (
    "Office hours are Tuesdays from 2 to 4 pm in Laws Hall room 205. "
    "Homework is submitted through Canvas and is due by 11:59 pm on the day listed "
    "in the syllabus. Late homework loses 10% per day, up to three days late; after "
    "that it earns no credit. The final exam is cumulative and closed-book."
)

QUESTIONS = [
    "When and where are office hours?",
    "How much credit do I lose if my homework is two days late?",
    "Can I use my notes during the final exam?",
    "Is the final exam cumulative?",
    "What time zone are the office hours in?",  # not covered by CONTEXT
]

PROMPT_A = "Context: {context}\nQuestion: {question}\nAnswer the question."
PROMPT_B = (
    "Context: {context}\nQuestion: {question}\n"
    "Answer in one sentence, using only facts stated in the context. "
    "If the context does not say, respond exactly: \"The context doesn't say.\""
)


class Verdict(BaseModel):
    winner: Literal["A", "B", "tie"]
    reason: str


def answer(prompt_template: str, question: str) -> str:
    prompt = prompt_template.format(context=CONTEXT, question=question)
    response = client.responses.create(model=model, input=prompt)
    return response.output_text.strip()


def judge(question: str, answer_a: str, answer_b: str) -> Verdict:
    prompt = (
        f"Context: {CONTEXT}\n"
        f"Question: {question}\n"
        f"Answer A: {answer_a}\n"
        f"Answer B: {answer_b}\n\n"
        "Judge which answer is better for this question and context. Prefer the "
        "answer that is more accurate and complete relative to the context, and "
        "that correctly says the context doesn't say instead of guessing. Pick "
        "'tie' only if both answers are equally good."
    )
    response = client.responses.parse(model=model, input=prompt, text_format=Verdict)
    return response.output_parsed


tally = {"A": 0, "B": 0, "tie": 0}
for question in QUESTIONS:
    answer_a = answer(PROMPT_A, question)
    answer_b = answer(PROMPT_B, question)
    verdict = judge(question, answer_a, answer_b)
    tally[verdict.winner] += 1

    print(f"Q: {question}")
    print(f"  A: {answer_a}")
    print(f"  B: {answer_b}")
    print(f"  winner: {verdict.winner}   reason: {verdict.reason}")
    print()

print(f"tally over {len(QUESTIONS)} questions: A={tally['A']}  B={tally['B']}  tie={tally['tie']}")
