# 05: A program checks the answer instead of a metric or a model

Concept: every evaluation demo so far on this page has one thing in
common: something inexact does the scoring. BLEU counts overlapping
words. LLM-as-judge asks another model to form an opinion. Both can be
fooled, exactly as earlier sections showed. Some outputs do not need
either. If a task has a precise, checkable specification, a short
program can verify the output directly, with no judgment call involved.
This demo builds that kind of verifier for a single grade-school math
problem, in the same style DeepSeek-R1's training used at scale: extract
the final answer, then compare it to a known-correct value.

## What the demo does

1. Poses one math word problem with a known numeric ground truth.
2. Defines four candidate "model solutions," each chosen to expose one
   specific verifier behavior: a fully correct and formatted solution, a
   correct solution missing the expected `####` marker, a confidently
   wrong arithmetic error, and a correct answer written with different
   number formatting (`$20.00` instead of `20`).
3. Runs two independent checks on each candidate: `has_format_marker`
   (did the solution use the expected answer-marking convention?) and
   `extract_answer` (what number did the solution actually land on?),
   then compares that number to the ground truth for a strict
   correct/incorrect verdict.

## Reading the result

```
candidate                       format ok  extracted  accuracy reward
correct, well-formatted              True       20.0             True
correct, no format marker           False       20.0             True
wrong arithmetic, well-formatted       True       23.0            False
correct, different formatting        True       20.0             True
```

The format check and the accuracy check disagree on the second
candidate, and that disagreement is the point: DeepSeek-R1's training
used exactly these two rewards separately, a small one for using the
expected format and a larger one for actually being correct, because
conflating them would punish a correct answer for a cosmetic reason. The
third candidate is where a verifier earns its keep: the prose reads just
as confidently as the correct solutions, and nothing about its fluency
signals the arithmetic error, but the extracted number is simply wrong,
and the check catches it without needing to "read" the reasoning at all.
The fourth candidate is the flip side of the BLEU lesson earlier on this
page: BLEU would score `"$20.00"` against a reference of `"20"` as a
near-miss because the strings do not match, while this verifier parses
both as the number 20.0 and calls it correct, because a verifier can be
built to care about the value, not the wording.

## Why this matters beyond one demo

This is not a niche trick. **Reinforcement Learning with Verifiable
Rewards (RLVR)** is the training approach behind DeepSeek-R1, OpenAI's
o-series, and most current "reasoning" models: instead of a human or a
reward model scoring every response, the training loop rewards a
response only when an automatic check passes, and that check needs no
human in the loop at all. DeepSeek-R1's own paper describes exactly this
kind of rule-based reward for math and logic problems, plus a
compiler-based check for code (Guo et al., DeepSeek-AI,
["DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via
Reinforcement Learning"](https://arxiv.org/abs/2501.12948), 2025).
DeepMind's AlphaProof pushes the same idea further: it generates formal
mathematical proofs and rewards them using the Lean theorem prover as
the verifier, since a formal proof is either accepted by Lean's kernel
or it is not, and that check was precise enough to reach silver-medal
performance at the 2024 International Mathematical Olympiad (Nature,
["Olympiad-level formal mathematical reasoning with reinforcement
learning"](https://www.nature.com/articles/s41586-025-09833-y), 2025).

The tradeoff is exactly the boundary this suggests: a verifier only
exists where a specification is precise enough to check automatically.
Math has a numeric ground truth. Code has unit tests or a compiler. A
formal proof has a proof checker. A floor plan can be checked
geometrically (the companion demo, `05b_floorplan_verifier.py`, does
exactly this). Open-ended writing, or "is this a good summary," usually
has no such program, which is why BLEU-style metrics and LLM-as-judge
still matter for everything a verifier cannot reach.

## Endpoint

No API calls. All candidates are hardcoded strings; the checks are pure
`re`-based parsing.

## Regeneration prompt

If this needs to be regenerated, ask an LLM assistant: "Pose one math
word problem with a known numeric ground truth. Define several candidate
solutions as strings: one fully correct and using a `####` final-answer
marker, one correct but missing that marker, one with a confident but
wrong arithmetic error, and one correct but using different number
formatting (e.g. `$20.00` vs `20`). Write a `has_format_marker` check and
an `extract_answer` check (parse the number after `####`, or the last
number in the text if no marker is present) that verify each candidate
independently, and print both results per candidate."
