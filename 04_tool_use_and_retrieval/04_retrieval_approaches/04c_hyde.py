"""04c: HyDE - embedding a hypothetical answer instead of the raw question.

See 04c_hyde.md for the full explanation.
"""

import os

import numpy as np
from openai import OpenAI

client = OpenAI()
chat_model = os.getenv("OPENAI_MODEL", "gpt-5.6")
embed_model = "text-embedding-3-small"

DOCUMENTS = [
    "Late Lab 3 submissions lose 10 percent of the grade for each day past the "
    "11:59pm deadline, with no credit given after three days.",
    "Office hours are Tuesdays 2-4pm in Laws Hall 205, no appointment needed.",
    "Exam 1 covers probability, entropy, and the normal distribution.",
    "Lab 4 submissions use assignment code LAB-4071 in Canvas.",
]
QUESTION = "docked for late lab3?"
CORRECT_INDEX = 0


def embed(texts: list[str]) -> np.ndarray:
    response = client.embeddings.create(model=embed_model, input=texts)
    return np.array([item.embedding for item in response.data])


def cosine_similarity(document_vectors: np.ndarray, query_vector: np.ndarray) -> np.ndarray:
    document_norm = document_vectors / np.linalg.norm(document_vectors, axis=1, keepdims=True)
    query_norm = query_vector / np.linalg.norm(query_vector)
    return document_norm @ query_norm


def hypothetical_answer(question: str) -> str:
    response = client.responses.create(
        model=chat_model,
        input=(
            "Write a short, plausible one-paragraph answer to this question, "
            f"even if you are not sure it is correct: {question}"
        ),
    )
    return response.output_text


document_vectors = embed(DOCUMENTS)

raw_query_vector = embed([QUESTION])[0]
raw_scores = cosine_similarity(document_vectors, raw_query_vector)

hyde_answer = hypothetical_answer(QUESTION)
hyde_vector = embed([hyde_answer])[0]
hyde_scores = cosine_similarity(document_vectors, hyde_vector)

print(f"Question: {QUESTION}")
print(f"Hypothetical answer used for HyDE: {hyde_answer}\n")
print(f"{'document':75s} {'raw query':>10s} {'HyDE':>10s}")
for i, document in enumerate(DOCUMENTS):
    marker = "  <-- correct" if i == CORRECT_INDEX else ""
    print(f"{document[:75]:75s} {raw_scores[i]:10.3f} {hyde_scores[i]:10.3f}{marker}")
