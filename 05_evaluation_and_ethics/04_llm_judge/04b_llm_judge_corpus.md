# 04b: Table 1's order sweep, extended with an LLM-as-judge column over real corpus text

Concept: `04_llm_judge.py` asked a model to judge three hand-picked
candidates instead of counting overlapping words. This demo asks the
same kind of question at the same scale as `03c_multi_metric_corpus.py`:
across every order in Table 1's sweep, is a generated continuation of
real held-out text actually good, according to a model that reads for
meaning instead of a formula that counts word overlap?

This reuses `03c_multi_metric_corpus.py`'s exact generation setup
(same corpus, same prompt/reference split, same character-by-character
sampling from the trained n-gram distribution) but replaces
BLEU/ROUGE-L/METEOR/BERTScore with one real judgment per generated
continuation. The sample size drops to 10 blocks per order on purpose:
this demo makes one real API call per block per order (70 calls total
for the full sweep), instead of a free local computation.

## What the demo does

1. Reuses `01_ngram_eval.py`'s corpus, split, training, and cross-entropy
   logic, and `03c_multi_metric_corpus.py`'s character-by-character
   generation, to produce one 40-character generated continuation per
   sampled held-out block, per order.
2. For each generated continuation, asks the same kind of judge
   `04_llm_judge.py` used — a structured `Judgment` (`correct: bool`,
   `quality: 1-5`, `reason: str`) — but with a prompt written for this
   task: judge whether the candidate is a plausible continuation of the
   prompt, compared against the real reference continuation.
3. Averages the judge's correct-rate and quality score per order, printed
   alongside the same cross-entropy and perplexity Table 1 reported.
4. At order 3, sorts the 10 judged continuations by quality score and
   prints the 5 highest, 5 near the median, and 5 lowest, each with the
   judge's verdict, reason, prompt, candidate, and reference.

## Reading the result

```
order  contexts  miss rate  cross-ent  perplexity  judge: correct  judge: quality
    2      1408      1.79%      3.009        8.05            0.0%            0.00
    3     11347      4.66%      2.791        6.92            0.0%            0.80
    4     48846     10.49%      3.082        8.47           10.0%            0.80
    5    132958     20.65%      4.005       16.06            0.0%            1.00
    6    261305     33.90%      5.394       42.05            0.0%            0.80
    7    406576     48.13%      6.984      126.57            0.0%            0.80
    8    548803     61.35%      8.517      366.28            0.0%            0.50
```

Cross-entropy still peaks at order 3. The judge does not agree that
order 3 generates the best text — because, unlike the automatic metrics
in `03c_multi_metric_corpus.py`, which at least gave BERTScore a visible
downward trend across orders, the judge marks nearly every generated
continuation as flatly incorrect, at every order, with an average
quality around 1 out of 5 almost everywhere. Reading the actual
judgments makes it clear why: a 40-character continuation sampled
character-by-character from an n-gram model, at any order this page
tested, produces text with Shakespearean-looking word fragments but no
real grammar or meaning — "his hear of lovely,\nAnd by thereford" is the
kind of thing the judge rejects instantly, and it does not read
meaningfully differently at order 2 than at order 8. Where the automatic
metrics could be partly fooled by incidental word overlap (as Table 4
and Table 3 both showed earlier on this page), the judge is not fooled
at all here — it is, if anything, a stricter and more decisive check
than BLEU, ROUGE-L, or METEOR, precisely because it reads for whether
the text means something rather than whether it overlaps with something.

The cherries, apples, and lemons at order 3 confirm there is no real
"good" tier to find: even the highest-quality-rated continuations still
score 1 out of 5, with reasons like "does not form plausible
Shakespearean syntax." This is a different, more useful result than a
demo engineered to show the judge finding a clear winner would have
been: it shows a real limit of what a tiny character-level n-gram model
can generate, at any order, and shows that an LLM judge and a battery of
automatic metrics can agree on that limit even when they disagree with
each other about the details.

## Endpoint

Calls the OpenAI API once per sampled block per order (70 calls for the
full sweep across 7 orders), using `OPENAI_MODEL` from the environment
(same convention as `04_llm_judge.py`).

## Regeneration prompt

If this needs to be regenerated, ask an LLM assistant: "Reuse
`01_ngram_eval.py`'s corpus, split, training, and cross-entropy logic,
and `03c_multi_metric_corpus.py`'s character-by-character generation
from a fixed random sample of held-out blocks. For each order, generate
one continuation per sampled block (use a small sample, e.g. 10, since
this makes one real API call per block per order) and ask an LLM judge
— the same `Judgment` structured-output pattern as `04_llm_judge.py`
(`correct: bool`, `quality: 1-5`, `reason: str`) — whether the generated
continuation plausibly continues the prompt, compared to the real
reference continuation. Print the average correct-rate and quality per
order alongside cross-entropy and perplexity. At order 3, sort the
judged continuations by quality and print the 5 highest, 5 near the
median, and 5 lowest, each with the verdict, reason, prompt, candidate,
and reference."
