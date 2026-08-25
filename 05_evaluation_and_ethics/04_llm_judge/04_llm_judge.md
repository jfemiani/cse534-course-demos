# 04: Ask a model to judge, instead of counting overlapping words

Concept: BLEU (`03_bleu_score.py`) scored the same three candidates by
counting overlapping words with a reference answer, and got fooled: the
factually wrong answer scored almost as high as the correct one, and the
correct paraphrase scored the lowest of all three. This demo asks a model
to judge the same three candidates directly, using structured output
(the same `client.responses.parse` pattern from
`02_prompt_engineering_api/06_structured_output/06_structured_output.py`)
so the judgment comes back as a validated `correct` / `quality` / `reason`
object instead of free text.

## What the demo does

1. Reuses the exact reference sentence and three candidates from
   `03_bleu_score.py`.
2. Defines a small `Judgment` model (`correct: bool`, `quality: int` 1-5,
   `reason: str`) and asks the model to fill it in for each candidate,
   told explicitly to be strict about factual details like room numbers.
3. Prints each candidate's judgment next to its label.

## Reading the result

The judge calls both the exact match and the good paraphrase correct,
quality 4 out of 5 — it recognizes that "stop by on Tuesday afternoons
between 2 and 4" means the same thing as "Tuesdays from 2 to 4 pm," which
BLEU could not do. The judge calls the wrong-room candidate incorrect,
quality 2 out of 5, and names the exact reason: the room number does not
match. That is the reverse of BLEU's ranking, which scored the wrong-room
candidate at 0.919 (nearly a perfect match) and the good paraphrase at
0.078 (barely related). A judge that reads for meaning catches exactly the
mistake a word-overlap metric is built to miss.

This is not free. Every judgment here is a full model call: slower and
more expensive than a formula, and only as good as the model doing the
judging — a weaker judge model, or a vaguer prompt, can miss the same
mistake a strong judge catches here. That tradeoff is why word-overlap
metrics like BLEU still exist alongside LLM-as-judge rather than being
replaced by it.

## Endpoint

OpenAI Responses API with structured output
(`client.responses.parse`, `text_format=Judgment`).

## Regeneration prompt

If this API changes, ask an LLM assistant: "Update this script to match
the current OpenAI Responses API structured-output pattern. Keep the
same reference sentence and three candidates as `03_bleu_score.py`, and
keep the `Judgment` model with `correct`, `quality` (1-5), and `reason`
fields."
