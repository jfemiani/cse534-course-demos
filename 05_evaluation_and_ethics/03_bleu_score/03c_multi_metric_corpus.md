# 03c: Zero-shot vs. one-shot prompting, scored with four metrics at once

Concept: `03b_multi_metric_score.py` scored BLEU, ROUGE-L, METEOR, and
BERTScore on three hand-picked toy sentences. That is useful for seeing
how the four metrics disagree, but every sentence in it was invented
for the demo. This demo asks the same four-metric question about a real
extrinsic task instead, and adds a second question on top of it: given a
real Congressional bill, does ChatGPT's summary of it agree with a real
human-written reference summary -- and does giving ChatGPT one worked
example before asking (one-shot prompting) change the answer, compared
to asking directly with no example (zero-shot prompting)?

The bills and their reference summaries come from BillSum (Kornilova
and Eidelman, "BillSum: A Corpus for Automatic Summarization of US
Legislation," 2019,
https://huggingface.co/datasets/FiscalNote/billsum), a real
summarization benchmark built from public-domain US Congressional and
California legislation. Two short bills from BillSum's test split are
scored here: the Merchant Marine of World War II Congressional Gold
Medal Act, and the Prescription Drug Monitoring Act of 2016. A third
BillSum bill, the Children's Bicycle Helmet Safety Act of 1993, is used
only as the worked example inside the one-shot prompt -- it is never
itself summarized or scored.

## What the demo does

1. For each of the two test bills, sends the bill's full text to
   ChatGPT twice: once with a zero-shot prompt asking directly for a
   one-paragraph summary "the way a legislative summary service would"
   write one, and once with a one-shot prompt that first shows the
   Bicycle Helmet Safety Act's text and its real BillSum summary as a
   worked example, then asks for the same kind of summary of the target
   bill.
2. Scores each generated summary against BillSum's own human-written
   reference summary for that bill, using the same BLEU, ROUGE-L,
   METEOR, and BERTScore implementations from `03b_multi_metric_score.py`.
3. Averages the four scores across the two test bills separately for
   each prompt, and prints one row per prompt -- not one row per bill --
   so the table answers "did the example help?" directly, alongside the
   reference and generated summaries for each bill.

## Reading the result

```
prompt                          BLEU  ROUGE-L  METEOR  BERTScore
zero-shot (no example)         0.196    0.419   0.442      0.752
one-shot (one example)         0.232    0.422   0.454      0.759
```

The one-shot row is a little higher on every metric, but only a
little -- ChatGPT already writes fluent, accurate legislative summaries
with no example at all, so a single worked example has limited room to
help. That itself is worth noticing: one-shot prompting is not free
(the example nearly doubles the prompt's length here) and its benefit
depends on how much the task's format was already implicit in the
instruction. A model that did not already know what a "legislative
summary" looks like would likely show a bigger gap between these two
rows.

The BLEU/ROUGE-L/METEOR/BERTScore spread within each row repeats the
same lesson as before: ChatGPT's summaries are correct and complete but
are original writing, not a near-copy of BillSum's phrasing, so BLEU
(built to reward matching runs of words) scores lowest, ROUGE-L and
METEOR give partial credit for shorter shared spans and for stems and
synonyms, and BERTScore, which compares what the two summaries mean
rather than which words they use, scores highest of all.

## Endpoint

OpenAI Responses API (`client.responses.create`) for the summaries.

## Regeneration prompt

If this needs to be regenerated, ask an LLM assistant: "Keep the two
real BillSum test bills (Merchant Marine of World War II Congressional
Gold Medal Act, Prescription Drug Monitoring Act of 2016) and their
real BillSum reference summaries, plus a third real BillSum bill
(Children's Bicycle Helmet Safety Act of 1993) used only as the
worked example. For each test bill, ask ChatGPT via the OpenAI
Responses API for a one-paragraph summary twice: once zero-shot (no
example) and once one-shot (prompt includes the example bill's text and
its real reference summary before asking). Score each generated summary
against its bill's reference with BLEU, ROUGE-L, METEOR, and BERTScore
(reusing the hand-written implementations from
`03b_multi_metric_score.py`), average the four scores across the two
test bills per prompt, and print one row per prompt plus each bill's
reference and generated summaries."

