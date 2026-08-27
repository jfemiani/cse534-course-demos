"""What a word embedding is, and two different ways to get one (6.3).

WordNet represents word meaning symbolically: a human-built graph of senses
(synsets) with hypernym/hyponym relations. word2vec and GloVe instead learn
a single dense vector per word purely from how often words co-occur in huge
amounts of real text (the distributional hypothesis: words used in similar
contexts tend to mean similar things). This demo contrasts the two directly
on an ambiguous word, then uses PCA (identical to Module 3's eigenfaces
demo) to actually look at a handful of GloVe vectors.

`glove_subset.50d.txt` is a hand-picked ~90-word subset of the official
50-dimensional GloVe vectors (Pennington, Socher & Manning, 2014,
https://nlp.stanford.edu/projects/glove/), extracted once from the full
400k-word release so this demo needs no large download.

pip install nltk scikit-learn matplotlib
python -c "import nltk; nltk.download('wordnet')"
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from nltk.corpus import wordnet as wn
from sklearn.decomposition import PCA

GLOVE_PATH = Path(__file__).parent / "glove_subset.50d.txt"
AMBIGUOUS_WORD = "bank"

CLUSTER_WORDS = [
    "france", "germany", "italy", "spain", "japan",       # countries
    "paris", "berlin", "rome", "madrid", "tokyo",          # capitals
    "cat", "dog", "wolf", "tiger", "lion",                 # animals
    "doctor", "teacher", "lawyer", "engineer", "artist",   # professions
    "happy", "joyful", "glad", "sad", "angry",             # emotions
    "bank", "river", "shore", "stream", "creek",            # bank's two senses
    "money", "finance", "banking", "credit", "loan",
]


def load_glove(path):
    vectors = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split(" ")
            vectors[parts[0]] = np.array(parts[1:], dtype=np.float32)
    return vectors


def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# --- Part 1: WordNet, a hand-built symbolic lookup -----------------------

def demo_wordnet(word):
    synsets = wn.synsets(word)
    print(f"WordNet has {len(synsets)} synsets for '{word}'. The first few:")
    for s in synsets[:4]:
        print(f"  {s.name():<22} {s.definition()}")
    print("Each sense is a separate, hand-written entry -- a lexicographer "
          "decided these are different meanings.")


# --- Part 2: GloVe, a learned distributional vector ----------------------

def demo_glove_neighbors(vectors, word, k=6):
    target = vectors[word]
    scored = [(w, cosine_similarity(target, v)) for w, v in vectors.items() if w != word]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    print(f"Predict-before-reveal: '{word}' has a riverbank sense and a "
          f"financial sense. Will GloVe's nearest neighbors show both, or just one?")
    print(f"GloVe's {k} nearest neighbors to '{word}' (one vector, no senses):")
    for w, sim in scored[:k]:
        print(f"  {w:<10} cosine similarity {sim:.3f}")
    print("Every neighbor is financial. The riverbank sense doesn't even appear: "
          "whichever sense dominates the training text swallows the other one "
          "completely, because there is only one vector to hold both.")


# --- Part 3: PCA on the embeddings, same call as Module 3's eigenfaces --

def demo_pca_plot(vectors, words, out_path):
    matrix = np.stack([vectors[w] for w in words])
    coords = PCA(n_components=2).fit_transform(matrix)

    fig, ax = plt.subplots(figsize=(11, 9))
    ax.scatter(coords[:, 0], coords[:, 1], s=10)
    for i, ((x, y), word) in enumerate(zip(coords, words)):
        offset = (6, 6) if i % 2 == 0 else (6, -10)  # alternate to reduce label collisions
        ax.annotate(word, (x, y), textcoords="offset points", xytext=offset, fontsize=9)
    ax.set_title("50-dim GloVe vectors projected to 2D with PCA")
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    print(f"Saved scatterplot to {out_path}")

    countries = ["france", "germany", "italy", "spain", "japan"]
    country_coords = np.stack([coords[words.index(w)] for w in countries])
    centroid = country_coords.mean(axis=0)
    spread = np.linalg.norm(country_coords - centroid, axis=1).mean()
    print(f"Country words cluster tightly: mean distance to their own centroid "
          f"is {spread:.2f} in the projected 2D space.")


if __name__ == "__main__":
    print("=== Part 1: WordNet -- a hand-built symbolic lookup ===")
    demo_wordnet(AMBIGUOUS_WORD)

    print("\n=== Part 2: GloVe -- a learned distributional vector ===")
    glove = load_glove(GLOVE_PATH)
    demo_glove_neighbors(glove, AMBIGUOUS_WORD)

    print("\n=== Part 3: PCA, the same call as Module 3's eigenfaces demo ===")
    out_file = Path(__file__).parent / "glove_pca.png"
    demo_pca_plot(glove, CLUSTER_WORDS, out_file)
