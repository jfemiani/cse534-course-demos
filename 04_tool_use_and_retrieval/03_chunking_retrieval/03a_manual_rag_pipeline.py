"""Demo 3a: the smallest visible RAG pipeline - chunk, embed, retrieve, answer.

See 03a_manual_rag_pipeline.md for the full explanation.
"""

import os

import numpy as np
from openai import OpenAI

client = OpenAI()
model = os.getenv("OPENAI_MODEL", "gpt-5.6")
embed_model = "text-embedding-3-small"

CHUNKS = [
    "CSE 534 meets Tuesdays and Thursdays. Attendance is not graded.",
    "Exam 1 covers mathematical foundations: probability, entropy, and the normal distribution.",
    "Labs are submitted through Canvas as a single Python file, due by 11:59pm.",
    "Office hours are Tuesdays 2-4pm in Laws Hall 205, no appointment needed.",
]


def embed(texts: list[str]) -> np.ndarray:
    response = client.embeddings.create(model=embed_model, input=texts)
    return np.array([item.embedding for item in response.data])


def cosine_similarity(chunk_vectors: np.ndarray, query_vector: np.ndarray) -> np.ndarray:
    chunk_norm = chunk_vectors / np.linalg.norm(chunk_vectors, axis=1, keepdims=True)
    query_norm = query_vector / np.linalg.norm(query_vector)
    return chunk_norm @ query_norm


question = "Do I need to sign in to class?"
chunk_vectors = embed(CHUNKS)
question_vector = embed([question])[0]

scores = cosine_similarity(chunk_vectors, question_vector)
best_index = int(np.argmax(scores))
best_chunk = CHUNKS[best_index]
print(f"Retrieved chunk (score={scores[best_index]:.3f}): {best_chunk}")

prompt = f"Context: {best_chunk}\n\nQuestion: {question}\nAnswer using only the context."
response = client.responses.create(model=model, input=prompt)
print(f"Assistant: {response.output_text}")
