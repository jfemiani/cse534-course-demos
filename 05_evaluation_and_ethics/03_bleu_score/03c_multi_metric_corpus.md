# 03c: A real summarization benchmark, scored with four metrics at once

Concept: `03b_multi_metric_score.py` scored BLEU, ROUGE-L, METEOR, and
BERTScore on three hand-picked toy sentences. That is useful for seeing
how the four metrics disagree, but every sentence in it was invented
for the demo. This demo asks the same four-metric question about a real
extrinsic task instead: given a real Congressional bill, does ChatGPT's
summary of it agree with a real human-written reference summary, by
BLEU, ROUGE-L, METEOR, and BERTScore?

The bills and their reference summaries come from BillSum (Kornilova
and Eidelman, "BillSum: A Corpus for Automatic Summarization of US
Legislation," 2019,
https://huggingface.co/datasets/FiscalNote/billsum), a real
summarization benchmark built from public-domain US Congressional and
California legislation. Two short bills from BillSum's test split are
used here as a tiny slice of that benchmark: the Merchant Marine of
World War II Congressional Gold Medal Act, and the Prescription Drug
Monitoring Act of 2016.

## What the demo does

1. For each of the two real bills, sends the bill's full text to
   ChatGPT with a prompt asking for a one-paragraph summary "the way a
   legislative summary service would" write one.
2. Scores that generated summary against BillSum's own human-written
   reference summary for the same bill, using the same BLEU, ROUGE-L,
   METEOR, and BERTScore implementations from `03b_multi_metric_score.py`.
3. Prints all four scores per bill, followed by the reference summary
   and ChatGPT's summary side by side, so you can read what each metric
   is actually scoring.

## Reading the result

```
bill                                             BLEU  ROUGE-L  METEOR  BERTScore
Merchant Marine of World War II Congressional   0.233    0.395   0.383      0.736
Prescription Drug Monitoring Act of 2016        0.162    0.424   0.487      0.763
```

Read the two summaries next to their references and the low BLEU
scores make immediate sense: ChatGPT's summaries are correct and
complete, but they are original writing, not a near-copy of BillSum's
phrasing. "This bill awards a Congressional Gold Medal to the U.S.
Merchant Marine of World War II in recognition of its vital and
dedicated wartime service" says the same thing as the reference's "This
bill requires the Speaker of the House of Representatives and the
President pro tempore of the Senate to arrange for the award...of a
single gold medal," but shares few of its words. BLEU, built to reward
matching runs of words, barely credits that agreement. ROUGE-L and
METEOR, which give partial credit for shorter shared spans and for
stems and synonyms, score both summaries meaningfully higher. BERTScore
scores highest of all on both bills, because it compares what the two
summaries mean rather than which words they use.

This is the same lesson Table 1's order sweep taught about
cross-entropy and generation-quality metrics, but sharper: a summary
can be substantively correct and still score low on a metric built for
a different kind of similarity. BLEU was built for machine translation,
where a correct translation really is expected to share most of its
words with a reference. A good summary is not that kind of task at
all &mdash; there is no one correct wording, only a correct set of
facts stated some reasonable way &mdash; which is exactly why the
"best for" column in the metrics table above lists summarization next
to ROUGE-L, not BLEU.

## Endpoint

OpenAI Responses API (`client.responses.create`) for the summaries.

## Regeneration prompt

If this needs to be regenerated, ask an LLM assistant: "Keep the two
real BillSum bills (Merchant Marine of World War II Congressional Gold
Medal Act, Prescription Drug Monitoring Act of 2016) and their real
BillSum reference summaries. For each bill, ask ChatGPT via the OpenAI
Responses API to write a one-paragraph summary, then score it against
the reference with BLEU, ROUGE-L, METEOR, and BERTScore (reusing the
hand-written implementations from `03b_multi_metric_score.py`). Print
all four scores per bill plus the reference and generated summaries."
