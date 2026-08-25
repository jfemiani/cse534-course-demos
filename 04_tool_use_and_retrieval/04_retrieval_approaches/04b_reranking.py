"""04b: reranking a vector-search shortlist with a cross-encoder.

See 04b_reranking.md for the full explanation.
"""

# pip install sentence-transformers

import numpy as np
from openai import OpenAI
from sentence_transformers import CrossEncoder

client = OpenAI()
embed_model = "text-embedding-3-small"
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

DOCUMENTS = [
    "If a Canvas submission is rejected as late, email the instructor with a "
    "screenshot of the timestamp; a regrade may be granted case by case.",
    "Lab 3 submissions use assignment code LAB-3042 in Canvas, are due at "
    "11:59pm, and late submissions are penalized 10% per day up to three days.",
    "Office hours are Tuesdays 2-4pm in Laws Hall 205, no appointment needed.",
    "Canvas sometimes rejects a submission if the file type does not match the "
    "assignment's allowed formats, such as submitting a .docx instead of a .py file.",
]
QUESTION = "What do I do if my Lab 3 submission gets rejected by Canvas for being late?"


def embed(texts: list[str]) -> np.ndarray:
    response = client.embeddings.create(model=embed_model, input=texts)
    return np.array([item.embedding for item in response.data])


def cosine_similarity(document_vectors: np.ndarray, query_vector: np.ndarray) -> np.ndarray:
    document_norm = document_vectors / np.linalg.norm(document_vectors, axis=1, keepdims=True)
    query_norm = query_vector / np.linalg.norm(query_vector)
    return document_norm @ query_norm


# Stage 1: fast bi-encoder search over the whole collection.
document_vectors = embed(DOCUMENTS)
question_vector = embed([QUESTION])[0]
vector_scores = cosine_similarity(document_vectors, question_vector)
shortlist = list(np.argsort(-vector_scores))

print(f"Question: {QUESTION}\n")
print("Stage 1 - vector search order (whole collection):")
for rank, i in enumerate(shortlist, start=1):
    print(f"  {rank}. (score={vector_scores[i]:.3f}) {DOCUMENTS[i]}")

# Stage 2: slow cross-encoder reranks only that shortlist, scoring the
# question and each candidate together instead of comparing two separately
# computed vectors.
pairs = [(QUESTION, DOCUMENTS[i]) for i in shortlist]
rerank_scores = reranker.predict(pairs)
reranked = [i for _, i in sorted(zip(rerank_scores, shortlist), reverse=True)]

print("\nStage 2 - cross-encoder reranked order (same shortlist):")
for rank, i in enumerate(reranked, start=1):
    score = rerank_scores[shortlist.index(i)]
    print(f"  {rank}. (score={score:.3f}) {DOCUMENTS[i]}")
