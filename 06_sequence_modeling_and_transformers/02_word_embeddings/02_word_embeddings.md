# 02: Word embeddings -- a hand-built lookup vs. a learned vector, then PCA

Concept: once text is tokenized (previous lesson), how do we represent what
a token *means*? This demo contrasts two fundamentally different answers --
WordNet's hand-built symbolic lookup and GloVe's learned distributional
vector -- on the same ambiguous word, then uses PCA (the identical call
from Module 3's eigenfaces demo) to actually look at a handful of GloVe
vectors.

## What the demo does

1. Looks up WordNet synsets for `"bank"`: a hand-built lexical database
   with a separate, human-written entry for each distinct sense (riverbank,
   financial institution, a row of switches, and more).
2. Loads a small, hand-picked subset of pretrained GloVe vectors
   (`glove_subset.50d.txt`, extracted once from the official 50-dimensional
   GloVe release) and finds `"bank"`'s nearest neighbors by cosine
   similarity -- the same similarity measure already used for retrieval in
   Module 4.
3. Runs `sklearn.decomposition.PCA` on ~35 of those vectors and plots them
   in 2D (`glove_pca.png`), labeled by word.

## Why this is worth reading closely

Part 1 and part 2 are a direct contrast, not two unrelated demos. WordNet
gives `"bank"` 18 separate senses because a lexicographer wrote each one
down by hand. GloVe gives it exactly one 50-number vector, learned purely
from how often `"bank"` co-occurs with other words in a huge amount of
text -- and every one of that vector's nearest neighbors (`securities`,
`banking`, `investment`, `financial`, `credit`, `finance`) is financial.
The riverbank sense doesn't surface at all: whichever sense is more common
in the training text dominates the single vector completely, because there
is only one vector to hold both meanings.

Part 3 reuses Module 3's PCA without re-deriving it: same rotation-and-scale
decomposition of a covariance matrix, same library call, only the cloud of
points changed from face pixels to word vectors. Look at `glove_pca.png`:
countries cluster together, animals cluster together, emotions cluster
together, and the finance words (`bank`, `banking`, `credit`, `loan`,
`finance`, `money`) sit in their own corner, separate from the river words
(`river`, `creek`, `stream`, `shore`) -- exactly the sense split the vector
itself couldn't make, made visible by which other words a word's vector
sits near.

## Honest caveats

- `glove_subset.50d.txt` is a ~100-word subset picked to make a legible,
  labeled scatterplot, not the full 400,000-word GloVe vocabulary -- the
  nearest-neighbor and clustering results shown here were checked against
  the full vocabulary and hold up, but a different subset could nudge
  individual distances.
- GloVe is a **static** embedding: one vector per word type, the same
  regardless of which sentence it appears in. That is exactly the
  limitation this page's final section names -- and exactly what Module
  6.6's attention mechanism fixes, by giving a word a different vector in
  every sentence it appears in.
