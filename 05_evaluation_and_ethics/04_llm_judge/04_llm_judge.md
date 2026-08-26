# 04: Ask a model to judge something no formula can score

Concept: word-overlap metrics like BLEU (`03_bleu_score.py`) only work
when there is a reference answer to compare against. Some qualities have
no reference at all — "is this explanation actually simple enough for a
five-year-old?" has no single correct wording to count overlap against.
This demo asks a model to make that kind of judgment call directly, using
structured output (the same `client.responses.parse` pattern from
`02_prompt_engineering_api/06_structured_output/06_structured_output.py`)
so the judgment comes back as a validated `appropriate_for_a_five_year_old`
/ `reason` object instead of free text.

The conversation being judged is real MT-Bench question 151 (humanities
category), not an invented scenario: Zheng et al., "Judging LLM-as-a-Judge
with MT-Bench and Chatbot Arena," 2023. https://github.com/lm-sys/FastChat

## What the demo does

1. Sends the real MT-Bench first-turn question (explain the relationship
   between GDP, inflation, unemployment, and fiscal/monetary policy) to
   the model, then sends the real second-turn follow-up, "explain them
   again like I'm five," in the same conversation.
2. Defines a small `Judgment` model (`appropriate_for_a_five_year_old:
   bool`, `reason: str`) and asks a judge to fill it in for the second
   turn's answer.
3. Prints both turns and the judgment.

## Reading the result

The model's ELI5 answer uses a concrete lemonade-stand analogy, which is
the right instinct, but the judge still calls it not appropriate for a
five-year-old: terms like "interest rates," "central bank," and "taxes"
get brief definitions instead of being replaced with something a young
child already understands, and the explanation runs long enough that a
five-year-old's attention would have wandered well before the end. That
verdict is itself the point — a good analogy is not the same thing as a
successful simplification, and there is no formula that can check that;
only a reader (here, a judge model) making a call about whether the
explanation actually lands for its stated audience.

This is not free. Every judgment here is a full model call: slower and
more expensive than a formula, and only as good as the model doing the
judging — a weaker judge model, or a vaguer prompt, can miss the same
thing a stronger judge catches. That tradeoff is why word-overlap metrics
like BLEU still exist alongside LLM-as-judge rather than being replaced
by it.

## Endpoint

OpenAI Responses API with structured output
(`client.responses.parse`, `text_format=Judgment`).

## Regeneration prompt

If this API changes, ask an LLM assistant: "Update this script to match
the current OpenAI Responses API structured-output pattern. Keep the
real MT-Bench question 151 two-turn conversation (economic indicators,
then 'explain them again like I'm five') and the `Judgment` model with
`appropriate_for_a_five_year_old` (bool) and `reason` (str) fields."

