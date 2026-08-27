---
name: lesson-design
description: 'Use when: designing a brand-new CSE 534 lesson or module from scratch, deciding what a new Canvas page should cover, mapping lesson outcomes to module outcomes to course SLOs, deciding how many pages a module needs or what goes on each one, or figuring out what students already know versus what a lesson must newly teach. This is a PLANNING/DELIBERATION skill — its output is a lesson design brief used to drive authoring, not text that gets written onto the student-facing page. Triggers: "design a lesson", "plan module N", "what should this page cover", "create a new lesson for module 7", "map course outcomes", "backward design this lesson", "what will students already know". NOT for revising prose clarity (use student-clarity-review), whole-document pedagogy critique of already-written content (use educational-reviewer agent), or HTML/Canvas mechanics (use canvas-page-editor agent) — this skill runs BEFORE those, to decide what the lesson should be before anyone writes it.'
---

# Lesson Design

A backward-design process for planning new CSE 534 lessons before any student-facing
prose is written. The output is a **lesson design brief**: a short internal artifact
(not a slide, not a page) that pins down outcomes, prior knowledge, and the one or two
ideas each page will carry. `canvas-page-editor` authors the actual HTML/Beamer content
from that brief; this skill decides what the brief should say.

## Audience model (assume this unless told otherwise)

CSE 534 is a **self-paced, online graduate certificate** course. Design for:

- A working adult with a **bachelor's degree, often earned ~20 years ago**, often in a
  field other than CS. Rusty on formal math/CS notation even where the underlying
  reasoning ability is strong.
- Already completed this program's **math + Python bridge course** — comfortable with
  basic probability/linear algebra notation and can read/write Python, but should not be
  assumed to remember specific bridge-course derivations without a reminder.
- May be concurrently or previously taking this program's other ML/Deep Learning
  courses — some vocabulary (loss functions, gradient descent, embeddings) may already
  be familiar from those courses. Don't re-teach it from zero, but don't assume it was
  taught the same way either; a one-line reminder beats a silent assumption.
- Self-paced and asynchronous: no live whiteboard, no classmate to ask a quick question.
  Everything a student would ask "wait, what?" about must be answered on the page itself.

## Step 1 — Map the outcome hierarchy

Every lesson must trace upward through three levels. Do this explicitly before writing
anything:

1. **Course SLOs** — the canonical list lives in the separate `CSE434` repo/workspace
   folder, at `CSE 434 Syllabus.md` under "Student Learning Outcomes" (LO1-LO6, plus
   graduate LO7-LO8). Read the current text rather than assuming — this list has been
   revised more than once and course-plan.md drafts in that repo are known to be stale.
2. **Module outcomes** — usually stated (or should be stated) on that module's "N.1
   Module Overview" page. If the module overview doesn't state outcomes yet, write them
   as part of this step, in the same LO-numbered style, each traceable to one or more
   course SLOs.
3. **Lesson outcomes** — one page (or tight cluster of pages) should map to one or two
   module outcomes. Write each lesson outcome as "students will be able to \_\_\_",
   using a Bloom's-taxonomy verb (Step 3) that matches how deep this lesson actually
   goes — don't default to "understand" for everything.

If a candidate lesson topic doesn't trace to any module outcome, that's a signal it
either belongs in a different module or the module outcomes are incomplete — fix the
outcome statement, don't just add an orphan lesson.

## Step 2 — Prior-knowledge audit

Before deciding what's new, write down what's **not** new. For the specific lesson:

- What did the immediately preceding lesson(s) in this module already establish?
- What does the math+Python bridge course already cover that this lesson can build on
  without re-deriving? (Check `CSE434/planning/` and the bridge course's own materials
  if unsure — don't guess.)
- What vocabulary/notation is this lesson introducing for the **first time** in this
  course vs. reusing from an earlier module? (Reuse earlier module pages via
  `grep_search` to check the actual prior text, not memory of what it "probably" said.)
- What might students carry in from a concurrent/previous ML or Deep Learning course
  that's adjacent but uses different terminology or framing? Name the mapping
  explicitly on the page if it's likely to cause confusion (e.g., "loss" vs.
  "objective," "embedding" meaning something narrower/broader elsewhere).

Write this as a short two-column list: **Already know** / **Do not yet know**. Anything
that isn't clearly in the left column must be taught, not assumed.

### Reference other lessons by title, not by bare module number

When a page needs to point at material from another lesson (something a student
already knows, or something a later lesson will build on), name that lesson by its
**title**, not by a bare number like "Module 3" or "Module 5":

- Module numbers change whenever the course gets reordered or renumbered (it has
  happened more than once in this course's history), silently breaking every bare
  numeric reference. A title survives a renumbering; a number doesn't.
- A number like "3" carries no meaning on its own — it forces the reader to recall
  what that non-semantic label stood for. A title ("the N-Gram Language Generation
  lesson," "the Evaluating LLMs lesson") reminds the reader what the referenced
  content actually was, which is the whole point of the reference.
- This applies even to same-module cross-references between sibling pages (e.g. from
  6.6 back to 6.4), not just cross-module ones — page numbers within a module can also
  shift when pages are inserted or reordered.
- A page number/title pair (e.g. "the 4.2 Function Calling with the Responses API
  lesson") is fine if the number adds useful "you already saw this" orientation, as
  long as the title is present and carries the actual meaning. Never write the bare
  number alone.

## Step 3 — Apply a pedagogical framework, don't wing it

Use these together, not as a checklist to satisfy independently — they reinforce each
other:

- **Backward design** (Wiggins & McTighe): decide the outcome first, then what evidence
  would show a student achieved it (a demo they can run, a question they can answer
  correctly, a distinction they can now draw), and only then design the page content
  that gets them there. Never start from "what's interesting about this topic" — start
  from "what should a student be able to do afterward."
- **Bloom's revised taxonomy** (Anderson & Krathwohl, 2001): pick the cognitive level
  each lesson outcome actually targets — remember, understand, apply, analyze,
  evaluate, create — and match the page's activity to that level. A lesson whose
  outcome is "explain why LSTMs solve vanishing gradients" is at the *understand/
  analyze* level and needs a worked derivation or failure-case comparison, not just a
  code demo (which targets *apply*). Don't write an "understand"-level outcome and then
  only give students an "apply"-level code cell — the demo must match the verb.
- **Cognitive load / worked-example effect** (Sweller): for anything procedurally new
  (a new architecture, a new training loop), show one fully worked example before
  asking students to reason about a variant or a failure case. Avoid split attention
  (don't force students to cross-reference a diagram and prose that don't sit near
  each other) and avoid redundancy (don't re-explain in prose what a labeled diagram
  already shows).
- **Segmenting and signaling** (Mayer's multimedia learning principles): break content
  into short, learner-paced segments rather than one long continuous exposition; use
  explicit headers/callouts to signal structure ("Here's the failure case," "Here's why
  that fails") instead of relying on paragraph transitions alone.
- **Andragogy** (Knowles): this audience learns better anchored to a concrete problem
  than to abstract subject-matter sequencing. Where possible, open a lesson with a
  scenario a working professional would recognize, not a topic-sentence definition.
  Respect their prior experience — invite them to notice where an old intuition (from
  their bridge course, from experience, from another ML course) breaks, rather than
  presenting new material as though they know nothing.

## Step 4 — Fill the Lesson Design Canvas (per page, not per module)

For **each candidate page**, answer these four questions before writing prose. If you
can't answer one, the page probably doesn't need to exist yet, or needs to be split /
merged with another page:

| Question | What to write |
|---|---|
| **New facts** | The specific claims this page states for the first time in the course. |
| **New skill/capability** | What can a student *do* after this page that they couldn't before (run a demo, derive a step, diagnose a failure mode)? |
| **The aha moment** | The one reframe or "wait, that's why X happens" moment this page is built around. If there isn't one, question whether this page earns a place on its own. |
| **One-sentence takeaway** | If a student remembers exactly one sentence from this page a month later, what should it be? |

A module should not be built by listing subtopics and giving each a page. It should be
built by deciding the aha moments first, then checking that they cover every mapped
lesson outcome from Step 1.

## Step 5 — Structure using the conceptual spine

Once outcomes, prior knowledge, and aha moments are pinned down, structure each page
using the spine already established in the `CSE434` repo's `docs/pedagogy.md`:

1. tension or puzzle
2. core idea
3. worked example
4. limitation or failure mode
5. takeaway

Keep each page to a **small number of focused ideas** — one aha moment per page is
ideal; two is a maximum before splitting into separate pages. Resist the urge to cover
everything a topic "could" include; cut anything that doesn't serve a mapped lesson
outcome from Step 1.

## Step 6 — Plan engagement mechanics, don't just plan content

Barraging students with declarative prose is the default failure mode to avoid. While
still at the planning stage, mark where the page should:

- Pose a question and let the student predict an answer before revealing it, rather
  than stating the answer first.
- Use a "pause and think" checkpoint before a worked example, especially right after
  introducing the tension/puzzle in Step 5.
- Show a failure case *before* the fix, so the fix answers a question the student
  already has, instead of presenting a solution to a problem they haven't felt yet.

Actual prose-level execution of these techniques (Socratic rewrites, fixing rambling
paragraphs) is not this skill's job — hand that to the `student-clarity-review` skill
once a draft exists.

## Step 7 — Write the design brief (internal artifact, not a page)

Capture Steps 1-6 as a short internal document before authoring begins — a scratch
markdown file (e.g. `NN_module/DESIGN-lesson-name.md`, not committed as student content)
or session memory. It should be short enough to re-check against the finished page
later. Minimum contents:

- Outcome chain: course SLO(s) → module outcome → this lesson's outcome(s), with Bloom
  level named for each.
- Prior-knowledge two-column list from Step 2.
- One Lesson Design Canvas row (Step 4) per planned page.
- Which spine stage (Step 5) each page section maps to.

## Step 8 — Hand off to authoring and QA

This skill's output feeds directly into existing tools — don't re-solve what they
already do:

1. **Authoring**: hand the finished design brief to the `canvas-page-editor` agent (or
   the `beamer` skill for slides) to produce the actual HTML/LaTeX. It should not need
   to make outcome or structural decisions — those are already fixed by this brief.
2. **Pedagogy QA**: after a draft exists, run the `educational-reviewer` agent against
   it — check the draft still matches the design brief's outcomes and prior-knowledge
   assumptions, not just general clarity.
3. **Prose QA**: run `student-clarity-review` on any paragraph that reads as rambling or
   narrates a result instead of engaging the reader.
4. **Voice QA**: run `avoid-ai-writing` before treating the page as final.

If a QA pass surfaces a page that can't satisfy its design brief as written, revise the
brief (fewer ideas, different Bloom level, added prior-knowledge scaffolding) rather
than patching prose around a structural problem.
