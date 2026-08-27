# Lesson Sources — 6.2 Tokenization, 6.3 Word Embeddings

Instructor-facing planning artifact. Not uploaded to Canvas, not
student-facing. Backs the claims made on 6.2 and 6.3, added to this module
as prerequisite pages after the original 6.1/6.4-6.6 (renumbered from
7.1/7.2-7.4) design brief. Supersedes the sources originally drafted for a
standalone "Module 7: Tokenization and Word Embeddings" plan, which was
folded into this module instead (the RNN/LSTM/Transformer lessons already
depend on tokenization and embeddings, so the content belongs alongside
them, not in its own module). That LDA/LSA aside from the earlier draft was
dropped per instructor request -- 6.3 covers only what a word embedding is
and how to compute one (WordNet vs. word2vec/GloVe), not document-topic
models.

## 6.2 Tokenization

| Source | What it backs |
|---|---|
| Sennrich, R., Haddow, B., & Birch, A. (2016). "Neural Machine Translation of Rare Words with Subword Units." *ACL 2016*. https://arxiv.org/abs/1508.07909 | BPE-for-NLP: iteratively merging the most frequent adjacent symbol pair to build a subword vocabulary. |
| Gage, P. (1994). "A New Algorithm for Data Compression." *The C Users Journal*, 12(2), 23-38. | Historical origin of the byte-pair-encoding compression algorithm Sennrich et al. adapted. |
| OpenAI `tiktoken`. https://github.com/openai/tiktoken | Tokenizer library behind GPT-family models; used directly in the demo. |
| Hugging Face `transformers` `AutoTokenizer`. https://huggingface.co/docs/transformers/main_classes/tokenizer | Tokenizer for open (non-OpenAI) model families; used directly in the demo. |
| Kudo, T., & Richardson, J. (2018). "SentencePiece." *EMNLP 2018*. https://arxiv.org/abs/1808.06226 | SentencePiece as the format used by Llama/T5-style models; backs the "where to find tokenizers" section. Not run in the demo (would require a gated/large model download); named only. |
| Internal: `mt_data.py`'s `Vocab` class and its "a deliberate simplification" docstring. | The opening tension: this module's own word-level vocabulary has an OOV problem. |
| Internal: `04_tool_use_and_retrieval/pages/4.2 Tool Use - Function Calling with the Responses API.html`, the "strawberry" example. | The failure-mode callback: why counting letters is hard once text is tokenized. |

## 6.3 Word Embeddings

| Source | What it backs |
|---|---|
| Miller, G. A. (1995). "WordNet: A Lexical Database for English." *CACM*, 38(11), 39-41. | WordNet's structure: synsets, hypernym/hyponym relations, hand-built by lexicographers. |
| Princeton WordNet project page. https://wordnet.princeton.edu/ | WordNet is a real, maintained resource, accessed here via `nltk.corpus.wordnet`. |
| Harris, Z. S. (1954). "Distributional Structure." *Word*, 10(2-3), 146-162. | Formal origin of the distributional hypothesis underlying word2vec and GloVe. |
| Firth, J. R. (1957). "A Synopsis of Linguistic Theory, 1930-1955." | Source of the popular "a word is characterized by the company it keeps" paraphrase, used only as a memorable framing line. |
| Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2013). "Efficient Estimation of Word Representations in Vector Space." https://arxiv.org/abs/1301.3781 | word2vec: predicting a word from its context. |
| Pennington, J., Socher, R., & Manning, C. D. (2014). "GloVe: Global Vectors for Word Representation." https://nlp.stanford.edu/projects/glove/ | GloVe: factorizing global co-occurrence counts into vectors. Source of the pretrained vectors used in the demo (`glove_subset.50d.txt`, a ~100-word subset extracted from the official 50-dimensional release). |
| Internal: `03_mathematical_foundations/pages/7. Multivariate Normal Distributions and Covariance Geometry.html` and `13_eigenfaces/`. | The PCA mechanism itself, reused (not re-derived) for the word-vector scatterplot; also the PCA-vs-UMAP/t-SNE tradeoff, named but not re-taught. |
| Internal: `04_tool_use_and_retrieval` retrieval lessons (cosine similarity over embeddings). | Reused directly for the GloVe nearest-neighbor computation. |
| Internal: this module's own `mt_data.py`/RNN-LSTM demos (`nn.Embedding`) and 6.6's attention mechanism. | Backs the closing "three senses of embedding" paragraph and the forward pointer to contextual embeddings as the fix for the one-vector-per-word limitation. |

## Cross-cutting notes

- Every empirical claim about GloVe's nearest neighbors for "bank" (all
  financial, no riverbank sense) was verified twice: once against this
  page's small checked-in subset, once against the full local 400k-word
  GloVe file, before writing the claim onto the page.
- No citation above is fabricated; arXiv IDs and venues are standard,
  well-known citations for these methods.
