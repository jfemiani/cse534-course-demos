# 04b: Ask a judge to compare two prompts, not two candidate answers

Concept: `04_llm_judge.py` judged three hand-picked candidates against one
reference answer — a good fit when there is a single correct answer to
check against. Comparing prompts is a different, equally common use of
LLM-as-judge: instead of asking "is this answer correct," it asks "which
of two prompts gets better answers out of the same model," which has no
single reference answer to score against at all. The earlier version of
this demo reused the n-gram order sweep from `03c_multi_metric_corpus.py`
and asked a judge to grade free-running character generation as
`correct`/`incorrect`, but a generated Shakespeare continuation has no one
right answer to be correct against, so that criterion never fit the task.
This version drops the n-gram sweep and judges something a pairwise
verdict actually fits: two competing prompts, answering the same
questions.

## What the demo does

1. Defines one short context paragraph (an office-hours/homework policy,
   continuing the running example from `04_llm_judge.py`) and five
   questions about it, one of which the context does not actually answer.
2. Defines two prompt templates: `PROMPT_A`, a bare "answer the question"
   instruction, and `PROMPT_B`, which adds explicit instructions to
   answer in one sentence, use only facts stated in the context, and say
   so plainly when the context doesn't say.
3. For each question, calls the same underlying model once with each
   prompt template to get `answer_a` and `answer_b`.
4. Asks a judge — a structured `Verdict` (`winner: "A" | "B" | "tie"`,
   `reason: str`) — which answer is better for that question and context,
   told to prefer accuracy, completeness, and correctly saying "the
   context doesn't say" over guessing.
5. Tallies how many questions each prompt wins.

## Reading the result

```
tally over 5 questions: A=3  B=0  tie=2
```

The engineered prompt (B) does not win a single question here. On the
one question the context does not cover, both prompts correctly decline
to guess, so the judge calls it a tie: A's "not specified in the provided
information" and B's "the context doesn't say" are functionally the same
answer. On the questions the context does answer, the judge repeatedly
prefers A's slightly more explicit phrasing (spelling out that a two-day
late penalty is "10% for each day," or that closed-book means notes
are not allowed) over B's shorter, more constrained one-sentence answers.
The instruction that was supposed to make B better, forcing a single
terse sentence, is exactly what cost it the comparison: this model
already answers these questions well without much steering, so adding a
tighter format constraint only threw away detail the judge counted in
A's favor.

That is the actual value of comparing prompts with a judge instead of
assuming: a plausible-sounding prompt-engineering idea (be concise, cite
only the context) did not produce a better prompt here, and the only way
to find that out was to run both prompts and ask something to compare
the results, since neither answer is simply "correct" or "incorrect" on
its own.

## Endpoint

Calls the OpenAI API three times per question (one `responses.create` per
prompt variant, plus one `responses.parse` for the judge), using
`OPENAI_MODEL` from the environment (same convention as `04_llm_judge.py`).

## Regeneration prompt

If this needs to be regenerated, ask an LLM assistant: "Write a demo that
uses an LLM judge to compare two *prompts* rather than two candidate
answers. Define one short context paragraph and a handful of questions
about it, including at least one question the context does not answer.
Define two prompt templates that both answer a question from the
context, e.g. a bare instruction versus one with explicit formatting and
grounding instructions. For each question, call the same model once per
prompt template, then ask a judge — a structured `Verdict` with a
`winner: \"A\" | \"B\" | \"tie\"` field and a `reason` field — which
answer is better, preferring accuracy, completeness, and correctly
declining to guess when the context doesn't say. Tally how often each
prompt wins and report the result honestly, even if the more
'engineered' prompt does not win."
