"""Demo: measuring which retrieval strategy actually works, instead of guessing.

See 02_retrieval_eval.md for the full explanation.
"""

import numpy as np
from openai import OpenAI

client = OpenAI()
embed_model = "text-embedding-3-small"

DOCUMENTS = [
    "CSE 534 meets Tuesdays and Thursdays. Attendance is not graded.",
    "Exam 1 covers mathematical foundations: probability, entropy, and the normal distribution.",
    "Labs are submitted through Canvas as a single Python file, due by 11:59pm.",
    "Office hours are Tuesdays 2-4pm in Laws Hall 205, no appointment needed.",
    "Lab 3 submissions use assignment code LAB-3042 in Canvas.",
    "Lab 4 submissions use assignment code LAB-4071 in Canvas.",
]

# Each test question names the index of the one document that answers it.
TEST_QUESTIONS = [
    ("Do I need to sign in to class?", 0),
    ("What does the first exam cover?", 1),
    ("How do I turn in a lab?", 2),
    ("When can I stop by without an appointment?", 3),
    ("What is the assignment code for LAB-3042?", 4),
    ("What is the assignment code for LAB-4071?", 5),
]

K = 2  # a "hit" means the right document appears in the top K results


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


def top_k_indices(scores: np.ndarray, k: int) -> set[int]:
    return set(np.argsort(scores)[::-1][:k].tolist())


document_vectors = embed(DOCUMENTS)
hits = {"vector": 0, "keyword": 0, "hybrid": 0}

for question, correct_index in TEST_QUESTIONS:
    question_vector = embed([question])[0]
    vector_scores = cosine_similarity(document_vectors, question_vector)
    keyword_scores = np.array([keyword_score(question, doc) for doc in DOCUMENTS])
    keyword_norm = keyword_scores / keyword_scores.max() if keyword_scores.max() > 0 else keyword_scores
    hybrid_scores = (vector_scores + keyword_norm) / 2

    for name, scores in [("vector", vector_scores), ("keyword", keyword_scores), ("hybrid", hybrid_scores)]:
        if correct_index in top_k_indices(scores, K):
            hits[name] += 1

print(f"Hit-rate@{K} on {len(TEST_QUESTIONS)} test questions (higher is better)\n")
best_rate = max(hits.values())
for name, count in hits.items():
    rate = count / len(TEST_QUESTIONS)
    marker = " <- best" if count == best_rate else ""
    print(f"{name:10s} {rate:.2f}{marker}")
