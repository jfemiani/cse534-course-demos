# 04: Ask a model to judge something no formula can score

Concept: word-overlap metrics like BLEU (`03_bleu_score.py`) only work
when there is a reference answer to compare against. Some qualities have
no reference at all — "does this email sound friendly?" has no single
correct wording to count overlap against. This demo asks a model to make
that kind of judgment call directly, using structured output (the same
`client.responses.parse` pattern from
`02_prompt_engineering_api/06_structured_output/06_structured_output.py`)
so the judgment comes back as a validated `friendly` / `reason` object
instead of free text.

## What the demo does

1. Defines three hand-written email replies to the same request (an
   extension), varying only in tone: warm, curt, and cold-but-polite.
2. Defines a small `Judgment` model (`friendly: bool`, `reason: str`) and
   asks the model to fill it in for each reply.
3. Prints each reply's judgment next to its label.

## Reading the result

The judge calls the warm reply friendly and the other two not, giving a
reason grounded in specific wording each time (a cheerful greeting and an
offer to help, versus terse or overly formal phrasing). Run it again and
the borderline "cold but polite" reply can flip verdicts between runs —
that instability is the point: this is a genuine judgment call, not a
fact the model is retrieving, so don't expect a judge to be perfectly
consistent on borderline cases the way a formula would be.

This is not free. Every judgment here is a full model call: slower and
more expensive than a formula, and only as good as the model doing the
judging — a weaker judge model, or a vaguer prompt, can disagree with a
stronger judge on the same borderline case. That tradeoff is why
word-overlap metrics like BLEU still exist alongside LLM-as-judge rather
than being replaced by it.

## Endpoint

OpenAI Responses API with structured output
(`client.responses.parse`, `text_format=Judgment`).

## Regeneration prompt

If this API changes, ask an LLM assistant: "Update this script to match
the current OpenAI Responses API structured-output pattern. Keep the
three hand-written email replies (warm, curt, cold-but-polite) and the
`Judgment` model with `friendly` (bool) and `reason` (str) fields."

