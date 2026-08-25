---
name: student-clarity-review
description: 'Use when: a lesson paragraph/page "starts strong but gets hard to read", reads as rambling, narrates a table/result instead of engaging the reader, needs a jargon/concept transition made explicit instead of buried, or strings too many ideas into one sentence instead of letting points land separately. Diagnoses WHY prose is hard to follow via register-shift and argument-chaining analysis, and rewrites narrating prose into Socratic questions, explicit callouts, or short landed statements. Triggers: "why is this hard to read", "this is rambling", "make this more Socratic", "this reads like telling the student the answer", "the transition is sneaky/buried", "you keep chaining ideas together", "too many em dashes". Also self-check this after generating any explanatory paragraph, since chaining and em-dash overuse are a known failure mode of this assistant, not just something to fix on request. Complements avoid-ai-writing (formatting/vocabulary tells) with structural chaining and paragraph-level flow. NOT for whole-document pedagogy review (use educational-reviewer agent) — this skill is for diagnosing and fixing ONE paragraph or transition at a time.
---

# Student Clarity Review

Diagnose and fix student-facing prose (lesson pages, notes, demo write-ups) that is
technically correct but hard to follow. Three distinct techniques, used separately or
together:

1. **Register-shift analysis** — explain *why* a paragraph gets hard to read.
2. **Socratic rewrite** — replace narration ("the data shows X, which means Y") with
   questions that let the reader find X and Y themselves.
3. **Argument-chaining check** — a self-check on this assistant's own output: catch
   the habit of stringing claim + justification + hedge + consequence into one
   sentence instead of letting each point land on its own.

## When to Use

- User says a paragraph/section "starts strong then gets hard to read" and asks why.
- A paragraph explains a table/result by telling the reader what to conclude from it.
- A section switches to a genuinely different concept, task, or scoring method but the
  switch is buried in a subordinate clause instead of called out.
- User asks to make something "more Socratic" or to stop "telling."
- **Any time this assistant writes an explanatory paragraph longer than two or three
  sentences** — run Part 3 before presenting it, unprompted. This is a documented
  failure mode of this assistant specifically (see Part 3), not just a user complaint
  to react to.

Do not use this for whole-document pedagogy audits (jargon, assumed background,
overall structure) — that's the `educational-reviewer` agent. For formatting/vocabulary
AI-tells (em dash rate, hollow intensifiers, Tier 1 vocabulary), defer to
`avoid-ai-writing` — but note Part 3 below: back-to-back em dashes found during a
clarity review are usually a *symptom* of chaining, not an isolated formatting slip,
so fix the chaining first and the dash count drops on its own.

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
- **Elided-verb garden path**: "Table 2 reveals something Table 1's number cannot"
  drops the verb after "cannot" (cannot *what*? — "reveal," but the reader has to
  backfill it), and often stacks a dense noun phrase ("Table 1's single averaged
  number") right before the gap, so the hardest parsing moment lands on top of the
  densest phrase instead of being spaced away from it. Fix by giving each clause its
  own explicit subject and verb: "The examples in Table 2 show us something that the
  single averaged numbers shown in Table 1 cannot" resolves both the ellipsis and the
  stacking, and additionally puts the true subject of the sentence (the examples doing
  the showing) first instead of burying it inside a possessive.

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

## Part 3: Argument-Chaining Check (Self-Check)

This is the deepest and most persistent failure mode this assistant has toward its own
explanatory writing: **stringing multiple separately-landable ideas into one sentence**
instead of writing a series of short sentences that each land one point before the
next one starts. This is not primarily an em-dash problem. Em dashes are just the
most visible symptom, because chaining needs a connective, and an em dash is the
cheapest one to reach for. Removing the dashes without un-chaining the sentence just
swaps in a comma or "since" and leaves the actual defect in place.

**What a chained sentence looks like**: claim + justification + hedge/correction +
hypothetical + consequence, all in one sentence, connected by dashes, colons, "since,"
"but," or "though." Example (an actual first draft on this page):

> This model's training does not optimize for that number directly [em dash]
> counting how often a character follows a given context is nothing like searching for
> the lowest possible cross-entropy. But Table 1's order sweep did select on that
> number: order 3 won because it scored lowest. If that same kind of selection also
> had a say in how long a generated passage runs, it would favor a model that stops
> early or reaches for short, common words over long, informative ones, since fewer
> characters mean fewer chances to be surprised [em dash] a cheaper route to a low
> score that has nothing to do with writing better text.

Three sentences, and every one of them tries to carry an entire argument (a claim, its
justification, and its consequence) instead of making one point and stopping. The
second em dash is not the disease; it is where the chaining became visible enough to
notice.

**The fix**: split each chained sentence at every point where a new claim starts,
even if the result feels choppy at first. Let each sentence do one job.

> This model's training does not optimize for that number directly. Counting how
> often a character follows a given context is nothing like searching for the lowest
> possible cross-entropy. Table 1's order sweep did, though: order 3 won because it
> scored lowest. Suppose that same kind of selection also decided how long a
> generated passage runs. Short, common words would beat long, informative ones every
> time, because fewer characters mean fewer chances to be surprised. That is a
> cheaper route to a low score. It has nothing to do with writing better text.

Same content, same number of ideas, but each one now lands before the next begins.

### Procedure (run on this assistant's own draft prose before presenting it)

1. Count the ideas in each sentence: how many independent claims, justifications, or
   consequences does it try to hold? More than one is a chaining candidate.
2. Check connectives (em dash, colon, "since," "but," "though," "if... then") for
   whether they join two *landable* points or one point and its own restatement. The
   former is chaining; the latter is fine.
3. Split at every chaining connective into its own sentence, even if it looks short
   or blunt on its own. Short and landed beats long and layered.
4. Recount em-dash usage after splitting. If it dropped without a deliberate pass to
   remove dashes, that confirms the dashes were a chaining symptom, not the root
   issue.
5. Be honest in the report: if the user flags chaining, confirm it plainly rather than
   softening it into a formatting note. This is a known, recurring pattern, not a
   one-off slip.

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
- [ ] No sentence chains claim + justification + hedge + consequence together (Part 3)
- [ ] Em-dash count checked only after chaining is fixed, not as a substitute for it
- [ ] Re-read the surrounding paragraphs after a rewrite — a fixed paragraph can still
      read badly if the one before/after it assumed the old phrasing
