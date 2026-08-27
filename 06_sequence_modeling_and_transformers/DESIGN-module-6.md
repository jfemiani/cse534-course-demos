# Design Brief — Module 6: Sequence Modeling and Transformers

> Historical note: authored when this module was numbered 7 on Canvas. It
> was renamed to Module 6 (folder `06_sequence_modeling_and_transformers`)
> to close a numbering gap; internal `7.x`/`M7.x` references below are left
> as originally written and should be read as `6.x`/`M6.x`.

**Status: planning artifact only.** No student-facing HTML, slides, or demo code
were authored in this pass (see "Why authoring was deferred" below). This file
is internal, produced by the `lesson-design` skill process, and is meant to be
checked against the finished pages/demos later — it is not itself a Canvas
page or a regeneration prompt.

Canvas module: "7. Sequence Modeling and Transformers" (module id `895485`).
Item order treated as fixed for this pass: 7.1 Module Overview, 7.2 RNNs,
7.3 LSTMs, 7.4 Transformers/Attention/RLHF, 7.5 Discussion (RNN limitations),
7.6 Discussion (LSTM fundamentals), Pre-Test quiz (unnumbered, left as-is).
Existing page bodies on Canvas predate this redesign and are **not**
authoritative sources for content decisions below.

---

## 0. Why authoring was deferred this pass

The brief below is actionable, but I did not proceed to `canvas-page-editor`
or write demo code in this pass, for two concrete reasons rather than general
caution:

1. **No code-execution or network tool was available in this session.** This
   module's whole design depends on an unverified fact — that a Hugging Face
   English-French dataset can actually be downloaded and trained on (RNN,
   then LSTM, then Transformer) in a few minutes on a laptop CPU. I cannot
   confirm that without running code. Authoring three from-scratch PyTorch
   training scripts against an unverified dataset risks handing off code
   that looks finished but silently fails at the first `datasets.load_dataset`
   call.
2. Per the skill's own Step 8, authoring should start only once the brief is
   confirmed — and this brief has several assumptions (Section 6) that
   genuinely need a yes/no before code gets written, not just a read-through.

**What is actionable right now without further input:** the outcome
mapping, the prior-knowledge audit, the per-page canvas, and the "what
changes at each stage" demo design. A person (or `canvas-page-editor`, once
told which HF dataset actually works) could start writing code from Section 5
directly.

---

## 1. Outcome hierarchy

Source: `CSE 434 Syllabus.md` → "Student Learning Outcomes." Read directly
this session (not assumed from `course-plan.md`, which the `lesson-design`
skill flags as possibly stale).

### Course SLOs this module serves

- **LO1** — describe how generative AI relates to other ML areas and tasks.
- **LO2** — implement Python code to generate text/data; describe key
  generation concepts.
- **LO5** — apply probability theory to generative models; connect math to
  implementation.
- **LO7 [Graduate]** — adapt methods from recent research articles beyond
  what's covered in class.

(LO3/LO6 are not primary targets here — LO3's evaluation framing is only
*reinforced*, via the module's own cross-architecture comparison; LO6/RAG is
unrelated to this module.)

### Module 7 outcomes (drafted here — 7.1 does not currently state any;
see Assumption 9)

| # | Outcome (students will be able to...) | Bloom level | Traces to |
|---|---|---|---|
| M7.A | Explain why a fixed-context model (the n-gram model from Module 3) cannot represent arbitrary-length dependencies, and why a model needs a *state that persists across the whole sequence* to do so. | Understand | LO1, LO5 |
| M7.B | Implement and train a recurrent encoder-decoder (RNN) on a real sequence-to-sequence task, and diagnose the specific way it fails (vanishing gradient / long-range forgetting) using its own output as evidence. | Apply, Analyze | LO2, LO5 |
| M7.C | Implement and train a gated (LSTM) encoder-decoder on the identical task and data, and explain mechanistically why gating extends the model's effective memory versus 7.2's plain RNN. | Apply, Analyze | LO2, LO5 |
| M7.D | Implement and train a small Transformer encoder-decoder (self-attention + cross-attention) on the identical task, and explain attention as a learned, per-step weighted lookup over the whole source sequence rather than a compressed summary vector. | Apply, Understand | LO1, LO2, LO5 |
| M7.E | Describe the SFT → reward-model → PPO (RLHF) pipeline that turns a pretrained next-token predictor into an instruction-following assistant, and identify what each stage supplies that the previous stage lacks. | Understand | LO1, (LO7 stretch) |
| M7.F | Compare RNN, LSTM, and Transformer translation quality on the same held-out sentences (including a deliberately long one) and state which architectural property explains each gap. | Analyze | LO1, LO5 (reinforces LO3) |

### Lesson-level mapping

- **7.1 Module Overview** → states M7.A–M7.F in student-facing language;
  previews the one-corpus-three-architectures thread.
- **7.2 RNNs** → M7.A, M7.B.
- **7.3 LSTMs** → M7.C.
- **7.4 Transformers, Attention, and RLHF** → M7.D, M7.E, M7.F (M7.F's
  three-way comparison table is completed here, since it needs all three
  trained models).
- **7.5 / 7.6 Discussions** → reinforce M7.B / M7.C respectively (existing
  topics already fit; prompt text needs revision once 7.2/7.3 are authored —
  flagged as follow-up, out of scope this pass).

No orphan topics: every candidate topic below traces to one of M7.A–M7.F.

---

## 2. Prior-knowledge audit

### Already know (verified against actual prior-module content, not memory)

| Already know | Where it came from | How Module 7 reuses it |
|---|---|---|
| Cross-entropy / negative log-likelihood as a training objective | `03_mathematical_foundations/06_entropy`; reinforced in `05_evaluation_and_ethics/01_ngram_eval` | Same loss trains all three architectures — say so explicitly, don't re-derive it. |
| Fixed-context language modeling and its order/generalization tradeoff (n-grams) | `03_mathematical_foundations/07_ngram`; reinforced via the order-sweep grid search in `05_evaluation_and_ethics/01_ngram_eval` | This *is* the opening tension for 7.2: "the n-gram's fixed window was Module 3's whole problem — what if the window could grow with the sentence?" |
| Dot product / cosine similarity as a similarity measure | `03_mathematical_foundations/10_multivariate`, `12_mahalanobis`; used practically for embedding search in `04_tool_use_and_retrieval/03_chunking_retrieval` and `04_retrieval_approaches` | Attention scores in 7.4 are the same dot product, just learned and computed per token pair — name it as "the Module 3/4 dot product again," don't reintroduce it as new math. |
| "Embedding" as a concept — **but only in one specific sense** | `04_tool_use_and_retrieval` (an opaque, fixed vector returned by an API call, used for retrieval) | See vocabulary collision below — this is a false-friend, not a clean prior. |
| General idea that training = fitting parameters against a loss (regression framing, no backprop/gradient-descent terminology used) | `03_mathematical_foundations/09_gaussian_regression` (confirmed: page does not use the phrase "gradient descent" anywhere) | A soft prior only — treat as "they've fit one kind of model before," not as neural-network training literacy. |
| Basic Python fluency; comfort running a provided demo script | Bridge course + every prior module's demos | No change; PyTorch scripts should match the existing repo's demo scale/style. |
| Tokenization as a general idea (splitting text into model-sized units) | `02_prompt_engineering_api` demos use `tiktoken` for token counting | Reuse the word: "you've seen `tiktoken`'s subword tokenizer before — this module builds a much simpler word-level vocabulary from scratch, on purpose, to keep the three architectures comparable." |

### Do NOT yet know (must be taught here, or explicitly assumed from a
concurrent course — see Assumption 2)

- Feedforward neural network mechanics: weights, activation functions,
  backpropagation, gradient descent. **Confirmed not covered anywhere
  earlier in this course** (grepped `06. Normal Distributions and Gaussian
  Regression.html` for "gradient descent" — no hits).
- Recurrence: a hidden state carried forward and updated at every time step.
- Vanishing/exploding gradients.
- Gating (LSTM forget/input/output gates).
- Self-attention, cross-attention, positional encoding, multi-head attention.
- Encoder-decoder as a *structural* pattern (sequence-to-sequence vs.
  sequence-to-single-label, which is all Module 3/4 needed).
- Teacher forcing vs. autoregressive decoding at inference.
- RLHF: supervised fine-tuning, reward modeling, PPO.

### Vocabulary collisions to name explicitly on-page (same move as the
token/chunk fix already made on 4.2)

| Word | Meaning already used | New meaning here | Where to disambiguate |
|---|---|---|---|
| **embedding** | Module 4: an opaque fixed vector from an external API call, used only for retrieval | Module 7: a trainable lookup table that *is part of the model being trained* — its values change during backprop | One sentence, first appearance in 7.2 |
| **context** | Module 3 n-gram: a fixed small window of previous characters | 7.2 RNN: one fixed-size vector summarizing the *entire* sequence so far; 7.4 attention: a *different, freshly recomputed* weighted combination at every decode step | One sentence each in 7.2 and again in 7.4 — don't let "context" quietly mean three different things |
| **attention** | Everyday English meaning | A specific computed mechanism (weighted sum via dot-product similarity) | One bridge sentence before the mechanism is defined in 7.4 |

---

## 3. Framework application (how, not just checklist confirmation)

- **Backward design**: each page's "evidence of achievement" is the same
  three-way comparison table (M7.F) — students can point to their own
  training run's output on the same held-out sentences at every stage, not
  just a quiz question. Page content is built to produce that evidence, not
  the other way around.
- **Bloom's match**: 7.2/7.3 outcomes are Apply+Analyze, so each page's
  activity is a demo the student runs *and* a diagnostic reveal (long
  sentence breaks), not a code cell alone. 7.4's RLHF half is Understand-only
  on purpose (Assumption 8) — deliberately *not* paired with a training demo,
  since PPO training is out of scope for a laptop-CPU, single-page lesson.
- **Cognitive load / worked example**: 7.3's demo is written as a minimal
  diff against 7.2's (same data pipeline, same training loop, one line
  changes: `nn.RNN` → `nn.LSTM`) specifically so the *architecture* is the
  only variable a student has to reason about, not a reimplemented pipeline.
- **Segmenting/signaling**: 7.4 carries two aha moments (attention
  mechanism; RLHF) — right at the skill's stated per-page maximum. Structure
  it as two visually distinct segments with their own headers, not one
  continuous page (see Section 4.3 and Assumption 6).
- **Andragogy**: each architecture page opens by re-running the *same*
  failing sentence from the previous page, not a fresh abstract definition —
  a working professional's instinct ("last time this broke, did we fix it?")
  drives the page instead of a topic-sentence definition.

---

## 4. Per-page Lesson Design Canvas

### 4.1 — 7.2 RNNs (M7.A, M7.B)

| Question | Answer |
|---|---|
| New facts | A model can keep a *hidden state* updated at every input step instead of a fixed window; the same weights are reused (shared) at every time step; training uses teacher forcing, inference decodes autoregressively; the RNN's hidden state is a single fixed-size bottleneck vector. |
| New skill | Train a real encoder-decoder RNN on real sentence pairs and read its own output as evidence of a specific, nameable failure mode (not just "it's bad"). |
| Aha moment | "The n-gram's fixed window was never the real limit — the real fix is a state that keeps updating instead of a window that keeps sliding. But that state is compressed into one vector, and *that's* the next problem." |
| Takeaway | "A hidden state gives a model unlimited context length in principle, but a plain RNN forgets earlier words as gradients shrink over many steps." |

**Spine:**
1. *Tension*: reprise the Module 3 n-gram failure — a fixed 3-gram window
   cannot capture a dependency several words back (e.g., subject-verb
   agreement across an intervening clause). Pose: "What if context grew with
   the sentence instead of being fixed at training time?" **(predict-before-
   reveal: ask the reader to sketch what that might look like before showing
   the RNN diagram.)**
2. *Core idea*: hidden state updated every step, shared weights across time —
   unrolled-RNN diagram (GDL Ch. 5 candidate figure, see Section 7).
3. *Worked example*: train a small RNN encoder-decoder on the shared En-Fr
   corpus (Section 5); show correct short-sentence translations.
4. *Failure mode*: **(pause-and-think: "predict what happens as the test
   sentence gets longer" before revealing it)** — run the same model on a
   deliberately long held-out sentence; translation quality visibly
   collapses. One-paragraph plain-English vanishing-gradient explanation
   (phenomenon, not full derivation — that's graduate optional-reading
   territory).
5. *Takeaway*: as stated above; explicit forward pointer to 7.3.

### 4.2 — 7.3 LSTMs (M7.C)

| Question | Answer |
|---|---|
| New facts | Forget/input/output gates decide what to discard, add, and expose at each step; a separate cell state carries long-range information alongside the hidden state. |
| New skill | Make (and justify) a single, minimal architecture change to a working pipeline, and verify the change with the *same* diagnostic test used in the previous lesson. |
| Aha moment | "Gating doesn't remove the bottleneck vector — it just teaches the network what's worth protecting inside it." |
| Takeaway | "Gating lets a network choose what to remember, extending effective range far past a plain RNN — but the whole source sentence is still squeezed into one fixed-size vector." |

**Spine:**
1. *Tension*: reprise 7.2's exact failing long sentence, same corpus, same
   held-out set — "same task, same data: what has to change?"
2. *Core idea*: forget/input/output gates; LSTM cell diagram (confirmed GDL
   candidate: figure showing gates + cell state, see Section 7).
3. *Worked example*: same training loop as 7.2, swap `nn.RNN` → `nn.LSTM`;
   direct side-by-side output on the same sentences.
4. *Limitation*: **(predict-before-reveal: "will this fully fix the long
   sentence?")** — LSTM does noticeably better but still degrades on very
   long sentences, and still can't let the decoder look back at a *specific*
   earlier source word — it only carries one running cell state forward.
   This is the transition tension into 7.4.
5. *Takeaway*: as stated above.

### 4.3 — 7.4 Transformers, Attention, and RLHF (M7.D, M7.E, M7.F)

Two aha moments on one page — the skill's stated maximum. Author as **two
clearly separated, independently headed segments**, not one continuous
essay (Mayer segmenting). The Canvas merge rationale (RLHF folded into this
lesson because it's GDL Ch. 9's own scope) is treated as a fixed constraint
this pass, not re-litigated — but flagged in Assumption 6 as a real
authoring-difficulty risk.

**Segment A — attention/Transformer architecture (M7.D)**

| Question | Answer |
|---|---|
| New facts | Attention computes a per-step weighted lookup over *every* source position using the same dot-product/cosine-similarity idea from Module 3/4, now learned; self-attention lets every word attend to every other word in the same pass; no recurrence means the whole sequence trains in parallel. |
| New skill | Train a small Transformer encoder-decoder on the identical corpus and visualize its own attention weights as evidence, not just trust the label "attention." |
| Aha moment | "The bottleneck vector is gone — the decoder can look directly at any source word, every step, and it's the *same dot product* you already used for retrieval in Module 4." |
| Takeaway | "Attention lets every output step see every input step directly, and removing recurrence lets training parallelize across the whole sequence — this is the architecture behind every modern LLM." |

Spine: (1) tension = LSTM's fixed-size bottleneck from 7.3; (2) core idea =
attention as learned weighted lookup, self-attention as parallel; (3) worked
example = train Transformer on the shared corpus, visualize attention
weights on one sentence (e.g., confirm "le chat" aligns to "the cat"); (4)
limitation = it's still just predicting the next most likely token, with no
notion of what a human actually wants — bridges to Segment B; (5) takeaway
as above.

**Segment B — RLHF/PPO (M7.E)**

| Question | Answer |
|---|---|
| New facts | Three-stage pipeline: supervised fine-tuning (SFT) on human demonstrations, a reward model trained on human preference comparisons, PPO to optimize the policy against that reward model. |
| New skill | Read a labeled RLHF pipeline diagram and correctly state what each stage supplies that the previous one lacks (not run PPO themselves — see Assumption 8). |
| Aha moment | "Pretraining and RLHF are training the same network for two *different* things: predict plausible text, versus produce text people actually prefer." |
| Takeaway | "RLHF is a second training stage on top of pretraining, and because the reward model is itself just a trained approximation of human preference, it inherits the same failure mode Module 5 already named: Goodhart's Law." |

Spine: (1) tension = "your trained Transformer completes text — but completing
text isn't the same as following instructions or being honest; how do real
systems close that gap?" **(predict-before-reveal: "what would you need in
addition to a great next-word predictor?")**; (2) core idea = SFT → reward
model → PPO, one labeled diagram; (3) "worked example" = a single concrete
preference-comparison pair (two candidate replies, a human picks one) to
make the reward-model step tangible, not a training run; (4) limitation =
reward hacking, explicitly named as the same Goodhart's Law failure taught
in `05_evaluation_and_ethics/01_ngram_eval` — a deliberate cross-module
callback; (5) takeaway as above.

Graduate stretch reading (LO7): Ouyang et al., 2022 ("Training language
models to follow instructions with human feedback" — InstructGPT) as
optional reference for the RLHF segment; Vaswani et al., 2017 ("Attention Is
All You Need") as optional reference for Segment A. Both are real, correctly
citable papers — verify exact URLs at authoring time rather than guessing
one here.

---

## 5. The running example: English→French MT, one corpus, three architectures

**Controlled-variable design, stated explicitly so canvas-page-editor doesn't
redesign it accidentally**: build the tokenizer, vocabulary, train/val split,
and batching **once**, in a shared utility (not duplicated three times), so
that translation-quality differences across 7.2/7.3/7.4 are attributable to
the architecture change alone — this is itself a small ablation study, the
same methodology already taught in Module 5.

- **Tokenization**: word-level (whitespace + basic punctuation split,
  lowercased), not subword/BPE. This is an intentional simplification —
  say so on the page, since students already saw `tiktoken`'s BPE tokenizer
  in Module 2 and may otherwise assume this is the production approach.
  Fixed special tokens: `<sos>`, `<eos>`, `<pad>`, `<unk>`.
- **Corpus candidate (unverified — see Assumption 3)**: Hugging Face
  `datasets` library, `Helsinki-NLP/opus-100` (en-fr config), filtered to
  short sentences (roughly ≤ 12 tokens per side) and subsampled to a few
  thousand–20k pairs. Fallback candidate: a Tatoeba-style short
  sentence-pairs set (`Helsinki-NLP/tatoeba_mt` en-fr, or an embedded small
  curated set if HF access is unreliable in the demo environment). Whichever
  is chosen, verify actual download size and training wall-clock time on
  CPU before committing to it in a demo file.
- **Scale target**: small hidden dimensions (roughly 128–256), a handful of
  epochs, sized so each of the three scripts trains in a few minutes on a
  laptop CPU — matches this repo's "no GPU cluster assumed" convention
  (`03_mathematical_foundations`, `02_prompt_engineering_api` demo scale).
- **Fixed held-out evaluation set**: a small handful of sentences, including
  at least one deliberately long one, reused unchanged across all three
  lessons — this is what produces the M7.F comparison table.

**What specifically changes at each stage:**

| Stage | Encoder | Decoder | What's new vs. previous stage |
|---|---|---|---|
| 7.2 RNN | `nn.RNN` | `nn.RNN`, final encoder hidden state as one fixed-size "context vector" | Baseline: everything (data pipeline, training loop, greedy decoding) built for the first time. |
| 7.3 LSTM | `nn.LSTM` | `nn.LSTM` | **Only** the cell type changes (`nn.RNN` → `nn.LSTM`, cell state added). Same data pipeline, same training loop, same eval sentences — a genuine minimal diff. |
| 7.4 Transformer | `nn.TransformerEncoderLayer` (self-attention) | `nn.TransformerDecoderLayer` (self-attention + cross-attention), positional encoding added | Recurrence removed entirely; use PyTorch's built-in transformer layers rather than a hand-rolled attention implementation, to stay at this repo's usual demo scale (see Assumption 7) — the *math* is explained via diagram, the *code* stays minimal. Same data pipeline, same eval sentences, now producing the full three-way table. |

Candidate folder layout (not created this pass):

```
07_sequence_modeling_and_transformers/
  README.md
  requirements-sequence-modeling-and-transformers.txt
  mt_data.py                     # shared tokenizer/vocab/dataset/split, built once
  01_rnn_mt/
    01_rnn_mt.py
    01_rnn_mt.md
  02_lstm_mt/
    02_lstm_mt.py
    02_lstm_mt.md
  03_transformer_mt/
    03_transformer_mt.py
    03_transformer_mt.md
  pages/
  slides/
```

---

## 6. Assumptions made in the user's absence (flagged explicitly)

1. **No separate bridge-course syllabus exists to check.** Grepped
   `CSE434/planning/` for "bridge course" — no hits. Treated the
   `lesson-design` skill's built-in audience model (bachelor's degree,
   completed this program's math+Python bridge course, possibly concurrent
   in other ML/DL courses) as authoritative rather than a documented
   course-specific fact.
2. **Feedforward NN / backprop / gradient descent are assumed to come from
   a concurrent or prior ML/DL course, not taught here.** Confirmed this
   course itself never uses the phrase "gradient descent" before Module 7
   (checked `03_mathematical_foundations`'s Gaussian Regression page
   directly). 7.2 gets a one-paragraph refresher callout, not a full lesson,
   per the andragogy principle (remind, don't reteach from zero) — but if
   this assumption is wrong for a given student, 7.2 will land hard. Worth
   confirming.
3. **The Hugging Face dataset choice is unverified.** I have no
   code-execution or network tool in this session, so I could not confirm
   `Helsinki-NLP/opus-100` (or the Tatoeba fallback) actually downloads at a
   reasonable size and trains in minutes on CPU. This must be checked before
   any demo code is written.
4. **GDL Chapter 9 figure metadata is not fully trustworthy.** Reading
   `figure-9.13.description.txt` directly returned a description labeled
   "Figure 9.11" with a mismatched original filename — the local
   text-extraction pipeline has at least one confirmed figure/caption
   mismatch in this chapter. Every figure candidate named in Section 4/7
   must be visually re-verified against its actual PNG before being placed
   on a page, not trusted from the `.description.txt` alone.
5. **No HTML, slides, or demo code were authored this pass** — see Section 0.
6. **7.4 is treated as carrying two aha moments (architecture + RLHF)
   rather than being split into two pages**, because the Canvas merge that
   folded RLHF into 7.4 was already committed this session per
   `course_outline_plan.md`. I did not re-litigate that item-count decision,
   but I am flagging it: this is the one page in the module at real risk of
   becoming a wall of prose, and it should be authored as two visually
   distinct segments (own headers, own mini-spine), not one continuous essay.
7. **Chose vanilla `nn.RNN` (not GRU) for 7.2**, specifically so 7.3's
   "swap in gating" story is a clean, minimal, honest before/after diff
   against 7.2 — a design choice, not something the user specified.
8. **Chose PyTorch's built-in `nn.TransformerEncoderLayer` /
   `nn.TransformerDecoderLayer`** for 7.4's demo rather than a hand-rolled
   multi-head attention implementation, to keep the demo at this repo's usual
   minimal scale (attention math explained via diagram/slides, not
   re-derived in code).
9. **RLHF/PPO in 7.4 is Understand-level only — no training demo.** This is
   a deliberate compute/scope decision on my part (laptop CPU, single page),
   not something the user confirmed. Worth explicit sign-off since it means
   half of 7.4 is conceptual-only while the rest of the module is
   consistently hands-on.
10. **Drafted Module 7 outcome statements (M7.A–M7.F) myself**, since the
    current 7.1 page (stale, pre-restructuring) does not state any and the
    skill's Step 1 requires them to exist before lesson outcomes can trace
    to them.

---

## 7. GDL figure candidates (verify visually before use — see Assumption 4)

| Page | Candidate figures (chapter-05/09 local extraction) | Caveat |
|---|---|---|
| 7.2 RNN | Early Ch. 5 diagrams depicting an unrolled recurrent architecture / embedding-to-LSTM data flow (e.g. the `figure-5.2`–`figure-5.3` neighborhood) | Chapter opens with an LSTM-metaphor illustration (`figure-5.1a`, "prisoners reading books") — fun as a hook image, not technically informative; don't use it as the technical diagram. |
| 7.3 LSTM | LSTM cell diagram showing forget/input/output gates and cell state (confirmed by description text, in the `figure-5.6`–`figure-5.9` neighborhood) | This one's description text is internally consistent (gates, cell state, hidden state all named) — best-confirmed candidate in the set. |
| 7.4 Attention | Attention-weight visualization on a real text example (wine-review attention heatmap, `figure-9.3`/`9.9`/`9.11` neighborhood — exact number unreliable, see Assumption 4); an encoder-decoder/translation attention diagram was reported by the user around `figure-9.13` | Re-open and visually confirm each candidate PNG directly; do not trust the `.description.txt` number-to-content mapping in this chapter. |
| 7.4 RLHF | An RLHF/SFT/reward-model/PPO pipeline diagram somewhere in Ch. 9 | Not confirmed this pass — a spot-check (`figure-9.18`) returned a GPT-2/GPT-3 scaling comparison, not an RLHF diagram, so the actual RLHF figure's number is still unknown. Locate it visually at authoring time. |

---

## 8. Handoff

- **Authoring**: once the Section 6 assumptions are confirmed (especially
  #2, #3, #8, #9), hand this brief to `canvas-page-editor` for 7.1–7.4 HTML
  and to the `beamer` skill for slides. It should not need to make outcome
  or structural decisions — those are fixed above.
- **Demo code**: write `mt_data.py` and the three architecture scripts only
  after the dataset choice (Assumption 3) is confirmed to actually run.
- **QA**: run `educational-reviewer` against each drafted page (check
  against M7.A–M7.F and the prior-knowledge audit specifically, not just
  general clarity), then `student-clarity-review` on any page that reads as
  rambling, then `avoid-ai-writing` before calling any page final.
- **Activities**: 7.5/7.6 discussion prompts need revision to reference the
  actual MT demo once 7.2/7.3 exist — flagged as follow-up, not done here.
  Pre-Test quiz left untouched per the user's instruction.
