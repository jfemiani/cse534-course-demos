"""Demo: a hit-rate hides individual examples. Look at the best, the
median, and the worst one instead.

See 02b_retrieval_eval_examples.md for the full explanation.
Compare with 02a_retrieval_eval_hitrate.py, which reports only the
aggregate hit-rate across all six questions.
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

TEST_QUESTIONS = [
    ("Do I need to sign in to class?", 0),
    ("What does the first exam cover?", 1),
    ("How do I turn in a lab?", 2),
    ("When can I stop by without an appointment?", 3),
    ("What is the assignment code for LAB-3042?", 4),
    ("What is the assignment code for LAB-4071?", 5),
]


def embed(texts: list[str]) -> np.ndarray:
    response = client.embeddings.create(model=embed_model, input=texts)
    return np.array([item.embedding for item in response.data])


def cosine_similarity(document_vectors: np.ndarray, query_vector: np.ndarray) -> np.ndarray:
    document_norm = document_vectors / np.linalg.norm(document_vectors, axis=1, keepdims=True)
    query_norm = query_vector / np.linalg.norm(query_vector)
    return document_norm @ query_norm


document_vectors = embed(DOCUMENTS)

# margin: how far ahead the correct document's score is over the best wrong
# document. A large positive margin is a clean win. A negative margin means
# vector search actually preferred at least one wrong document.
examples = []
for question, correct_index in TEST_QUESTIONS:
    question_vector = embed([question])[0]
    scores = cosine_similarity(document_vectors, question_vector)
    wrong_scores = [scores[i] for i in range(len(DOCUMENTS)) if i != correct_index]
    margin = scores[correct_index] - max(wrong_scores)
    top_index = int(np.argmax(scores))
    rank = int((scores > scores[correct_index]).sum()) + 1  # 1 = top pick
    examples.append((margin, question, correct_index, top_index, rank, scores))

examples.sort(key=lambda e: e[0], reverse=True)
cherry = examples[0]
apple = examples[len(examples) // 2]
lemon = examples[-1]

for label, (margin, question, correct_index, top_index, rank, scores) in [
    ("CHERRY (best margin)", cherry),
    ("APPLE (median margin)", apple),
    ("LEMON (worst margin)", lemon),
]:
    print(f"--- {label} ---")
    print(f"question:           {question}")
    print(f"correct document:   {DOCUMENTS[correct_index]!r}")
    print(f"top-ranked document: {DOCUMENTS[top_index]!r}")
    print(f"margin (correct score - best wrong score): {margin:+.3f}")
    print(f"correct document's rank by vector score: {rank} of {len(DOCUMENTS)}")
    print(f"a hit at K=2: {rank <= 2}")
    print()
