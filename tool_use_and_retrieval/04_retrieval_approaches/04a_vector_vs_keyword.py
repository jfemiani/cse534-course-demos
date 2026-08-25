"""Demo: vector retrieval and keyword retrieval do not agree on everything.

Concept: comparing two retrieval strategies on the same small set of
documents and the same question. Vector search (embeddings and cosine
similarity) ranks by semantic similarity; keyword search ranks by exact
token overlap. Vector search is the current default and wins on paraphrase
and meaning, but two different ID-like strings can embed close together
even though they name different things. This demo picks a question that
exposes the gap: keyword search finds the exact assignment code instantly,
while vector search has to tell two similar-looking codes apart.

Endpoint: OpenAI Embeddings API (client.embeddings.create,
text-embedding-3-small).

If OpenAI changes this API, ask an LLM assistant: "Update this script to
match the current OpenAI embeddings API. Keep the same four documents, the
same question, and both rankings printed side by side."
"""

import numpy as np
from openai import OpenAI

client = OpenAI()
embed_model = "text-embedding-3-small"

DOCUMENTS = [
    "Lab 3 submissions use assignment code LAB-3042 in Canvas.",
    "Lab 4 submissions use assignment code LAB-4071 in Canvas.",
    "Office hours are Tuesdays 2-4pm in Laws Hall 205.",
    "Exam 1 covers probability, entropy, and the normal distribution.",
]
QUESTION = "What is the assignment code for LAB-4071?"


def keyword_score(query: str, document: str) -> int:
    query_tokens = set(query.lower().split())
    document_tokens = set(document.lower().split())
    return len(query_tokens & document_tokens)


def embed(texts: list[str]) -> np.ndarray:
    response = client.embeddings.create(model=embed_model, input=texts)
    return np.array([item.embedding for item in response.data])


def cosine_similarity(document_vectors: np.ndarray, query_vector: np.ndarray) -> np.ndarray:
    document_norm = document_vectors / np.linalg.norm(document_vectors, axis=1, keepdims=True)
    query_norm = query_vector / np.linalg.norm(query_vector)
    return document_norm @ query_norm


keyword_scores = [keyword_score(QUESTION, document) for document in DOCUMENTS]
document_vectors = embed(DOCUMENTS)
question_vector = embed([QUESTION])[0]
vector_scores = cosine_similarity(document_vectors, question_vector)

print(f"Question: {QUESTION}\n")
print(f"{'document':55s} {'keyword':>8s} {'vector':>8s}")
for document, k_score, v_score in zip(DOCUMENTS, keyword_scores, vector_scores):
    print(f"{document[:55]:55s} {k_score:8d} {v_score:8.3f}")
