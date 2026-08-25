---
name: student-clarity-review
description: 'Use when: a lesson paragraph/page "starts strong but gets hard to read", reads as rambling, narrates a table/result instead of engaging the reader, or needs a jargon/concept transition made explicit instead of buried. Diagnoses WHY prose is hard to follow via register-shift analysis, and rewrites narrating prose into Socratic questions or explicit callouts. Triggers: "why is this hard to read", "this is rambling", "make this more Socratic", "this reads like telling the student the answer", "the transition is sneaky/buried". NOT for AI-writing-tells detection (use avoid-ai-writing skill) or general pedagogy review of a whole document (use educational-reviewer agent) — this skill is for diagnosing and fixing ONE paragraph or transition at a time.
---

# Student Clarity Review

Diagnose and fix student-facing prose (lesson pages, notes, demo write-ups) that is
technically correct but hard to follow. Two distinct techniques, used separately or
together:

1. **Register-shift analysis** — explain *why* a paragraph gets hard to read.
2. **Socratic rewrite** — replace narration ("the data shows X, which means Y") with
   questions that let the reader find X and Y themselves.

## When to Use

- User says a paragraph/section "starts strong then gets hard to read" and asks why.
- A paragraph explains a table/result by telling the reader what to conclude from it.
- A section switches to a genuinely different concept, task, or scoring method but the
  switch is buried in a subordinate clause instead of called out.
- User asks to make something "more Socratic" or to stop "telling."

Do not use this for whole-document pedagogy audits (jargon, assumed background,
overall structure) — that's the `educational-reviewer` agent. This skill operates at
paragraph/transition granularity.

## Part 1: Register-Shift Analysis

A paragraph often starts clear (concrete example, plain claim) and then degrades
sentence by sentence because each sentence quietly changes *register* — the kind of
cognitive work required — without a bridge. None of the sentences are wrong in
isolation; the accumulation of un-bridged shifts is what exhausts the reader.

Common shift patterns to check for, in rough order of how much load they add:

- **Concrete → abstract hypothetical**: "If X were the target you optimized for
  directly, the cheapest way to improve it would be..." asks the reader to hold a
  counterfactual and a multi-step causal chain at once, right when they were coasting
  on a concrete example.
- **Named concept/law dropped with no lead-in**: "This is Goodhart's Law: '...'"
  introduces a proper noun and a quotation as if the reader already knows to expect it.
  Landing a citation or named principle immediately after an abstract sentence stacks
  two new things back to back.
- **Mid-clause parenthetical interruption**: "right up until something — training, or
  your own choice of examples — starts optimizing..." forces the reader to hold the
  main clause open across an aside before it resolves.
- **Circular or moralizing close**: "measuring what they think it is measuring" is a
  near-tautology; "a good researcher looks at both" is a generic virtue appeal instead
  of a concrete payoff. Endings like this feel unearned after a dense middle.

### Procedure

1. Read the paragraph sentence by sentence. For each sentence, name what kind of work
   it demands: concrete example, abstract claim, hypothetical/counterfactual, named
   citation, parenthetical aside, generic conclusion.
2. Flag every point where the register changes with no transition sentence bridging
   it.
3. Report back: which sentence is the pivot where it "gets hard," and which specific
   pattern (from the list above, or a new one) explains the jump. Don't just say
   "it's dense" — name the mechanism.
4. Only rewrite if asked. Diagnosis and rewrite are separate requests; some users just
   want to understand why before deciding what to do about it.

## Part 2: Socratic Rewrite

Convert paragraphs that *narrate* a result ("Table 2 shows the cherries are
suspiciously easy because...") into paragraphs that *ask* the reader to notice it
themselves.

### Procedure

1. Identify the concrete facts the reader can actually see (specific rows, numbers,
   words) without being told what they mean.
2. Identify the conclusion the original prose was stating on the reader's behalf.
3. Rewrite as a sequence of questions that walks the reader from the visible facts
   toward the conclusion, without stating the conclusion. End on an open question, not
   a restated answer.
4. Keep any load-bearing factual claims (numbers, terminology the reader needs) —
   Socratic framing removes *inferences*, not *facts*.
5. Do not pad with filler ("Let's explore...", "Consider the following..."). Each
   question should be answerable from what's already on the page.

### Worked Example

Before (narrating):
> Three different held-out blocks all read exactly "PETRUCHIO:" and score
> identically... "PETRUCHIO" is built almost entirely out of overlapping trigrams the
> order-3 model saw constantly, because Petruchio is a major, frequently-speaking
> character elsewhere in the training data... The lesson is not that short blocks are
> bad; it is that a block's difficulty depends on exactly which characters it
> contains.

After (Socratic):
> Three of the five cherries are the identical block, "PETRUCHIO:"... Both names are
> nearly the same length, so why does one score so much better than the other? Which
> of the two characters would you expect to speak more often elsewhere in the
> training data, and what would that mean for how familiar the model is with the
> letter-to-letter transitions inside that name?

## Explicit Callouts for Buried Transitions

When a section switches to a genuinely different task, scoring method, or concept
(not just a new example of the same thing), that switch needs its own sentence or
paragraph naming both sides of the switch — never a subordinate clause inside a
sentence about something else. If in doubt whether a transition counts as a "genuine
switch," check whether the columns/axes/what's-being-measured actually changed, not
just the specific numbers.

## Checklist Before Reporting Done

- [ ] Diagnosis names the specific sentence-to-sentence pivot, not just "it's dense"
- [ ] Rewrite (if requested) removes stated conclusions, not underlying facts
- [ ] No filler openers added ("Let's now...", "Here we see...")
- [ ] Genuine concept/task switches get their own explicit sentence, not a buried clause
- [ ] Re-read the surrounding paragraphs after a rewrite — a fixed paragraph can still
      read badly if the one before/after it assumed the old phrasing
