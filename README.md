# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

My community is Hacker News, specifically the top-level comments under
threads about AI coding tools (Claude Code, Codex, Cursor, Copilot, OpenCode
and so on). My classifier sorts each comment into one of three labels:
`experience` (the writer reports their own use of a tool), `claim` (a
statement about AI tools that isn't grounded in their own use), and
`question` (the writer wants an answer). The idea is to separate people
reporting what actually happened from people arguing about what AI is or
will be, since those two get mixed together in every one of these threads.

---

## Label Taxonomy

### `experience`

**Definition:** The comment is built around the writer's own use of a
specific tool: something they did with it and what happened, or verdicts
that clearly come from that use.

**Example 1:**
> Ok, just got documentation and fixed two bugs in my open source project.
> $1.42. This thing is a game changer.

**Example 2:**
> I've been using Claude Code daily for months on a project with Elixir,
> Rust, and Python in the same repo. It handles multi-language stuff
> surprisingly well most of the time. The worst failure mode for me is when
> it does a replace_all on a string that also appears inside a constant
> definition -- ended up with GROQ_URL = GROQ_URL instead of the actual URL.

### `claim`

**Definition:** A statement about AI tools (an argument, prediction,
complaint or fact) that isn't grounded in the writer's own described use.

**Example 1:**
> My bet: LLMs will never be creative and will never be reliable. It is a
> matter of paradigm.

**Example 2:**
> Ai tooling is fantastic but not being able to version and control the
> model into which you pump your dependant workflows is such a liability.

### `question`

**Definition:** The writer is asking the thread for information, and the
comment would be pointless if nobody answered.

**Example 1:**
> What's the privacy like for Claude Code? Is it memorizing all the codebase?

**Example 2:**
> Is there a way to run the model locally? I'd rather not have to pay a
> monthly fee, if possible.

### The hardest boundary

**Which two labels:** `experience` and `claim`.

**The decision rule I used every time:**
Ask whether the comment is *built around* the writer's own use of a named
tool. If it is, it's `experience`, even if it goes on to argue a bigger
point. If the use is just a one-line lead-in before an argument, it's
`claim`. When a comment is about half and half, the tie-breaker is whether
they name a specific tool: "I tell AI exactly what to test" followed by
opinions about AI in general is `claim`.

Two smaller rules: a rhetorical question ("How employable is that?") is
`claim`, not `question`. And a comment I couldn't label from its own text
(cut off mid-sentence, or only makes sense next to the comment it replies
to) was skipped, not forced into a label.

I didn't start with this rule. I started with "any described use counts as
`experience`," and changed it after comparing my cold labels with a second
labeller (see The Dataset below).

---

## The Dataset

**Where the posts came from:** Top-level comments from 8 Hacker News threads
about AI coding tools, collected with `collect_hn.py` through the public HN
search API (no account or key needed). Threads: 47282777, 47660925,
43163011, 46765460, 46542036, 50059523, 43708025, 47460525. I only took
top-level comments, because a reply needs the comment it's replying to and
the model never sees that. I capped it at 36 random comments per thread so
no single thread or tool dominates, removed exact duplicates, and kept no
usernames. That gave 287 comments. 68 were skipped (jokes, self-promotion,
link-only posts, critiques of the linked article, and replies that don't
make sense on their own), leaving 219.

**How I labelled them:** Claude pre-labelled all 287. Before looking at any
of its labels, I labelled 20 of them cold. I agreed with Claude on 14 of
the 18 I decided on my own (78%). Two of the four disagreements showed the
same pattern: comments with one line of tool use followed by an argument. I
consistently called those `claim` and Claude called them `experience`, so I
rewrote the rule to match how I was actually labelling (the rule above).
Claude then flagged 9 borderline comments under the new rule and I decided
each one. Claude applied my final rules to the remaining 191, and I did
**not** check those individually. The `note` column says which is which:
`cold` (19, after skipping one), `pre-labelled, decided by me` (9),
`pre-labelled` (191).

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `experience` | 101 | 46% |
| `claim` | 97 | 44% |
| `question` | 21 | 10% |
| **Total** | 219 | 100% |

**Three hard cases**

**1.**
> *The post:* A long story about a company all-hands where the leader said
> everyone must adopt AI. The writer sent a private note arguing that AI
> erodes their skills ("What do I put in my resume now? That I vibe coded
> Cassandra migration?"). It opens with "I just had what you might probably
> describe as the opposite experience."
>
> *Could have been:* `experience`, `claim` or `question`. It literally says
> "experience" and it's full of questions.
>
> *I chose, because:* `claim`. Nothing in the story involves using an AI
> tool (it's a meeting and a note), and the questions are rhetorical. This
> one taught me not to label by the word "experience".

**2.**
> *The post:* "Claude is great I really love it but keen to know will you
> ever have one plan and one history across all the different tools…"
> followed by a long list of complaints (no single sign-on, no shared
> history, missing connectors), with one sentence about code reviews being
> incomplete and having to prompt multiple times.
>
> *Could have been:* `experience` (that one sentence is first-hand use) or
> `claim`.
>
> *I chose, because:* `claim`. The one sentence of use is buried in eight
> complaints. This is where Claude and I disagreed, and it's what made me
> change the rule from "any use counts" to "built around use".

**3.**
> *The post:* "From my experience with playing with Claude Code vs Cline…
> I don't want anything that doesn't let me set my own models. Deepseek is
> about 1/20th of the price and only slightly behind Claude. Both have a
> tendency to over engineer."
>
> *Could have been:* `experience` or `claim`. It's mostly verdicts and
> never describes a specific task.
>
> *I chose, because:* `experience`. The verdicts clearly come from their own
> use of two named tools. I then went back and changed a similar comment
> (verdicts about Opus 4.5 and data science code) from `claim` to
> `experience` so the two would match.

---

## The Training Run

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, seed 42. Trained
on `mps` (Apple Silicon GPU), torch 2.14.1.

**Anything I changed from the defaults, and why:** `MAX_LENGTH` from 128 to
256. I measured my comments with the model's tokenizer: at 128 tokens only
71% of them are read in full, and at 256 it's 92%. A lot of my comments
start with a story and only argue a point later (or the other way round),
so cutting them at 128 would hide exactly the part my labels depend on.

**Split sizes:** 153 train / 33 val / 33 test.

| | train | val | test |
|---|---|---|---|
| `experience` | 71 | 15 | 15 |
| `claim` | 67 | 15 | 15 |
| `question` | 15 | 3 | 3 |

`question` has only 3 examples in the test split, so its F1 will move a lot
between seeds. Missing one question changes recall by 33 points.

---

## How I Used AI

**Moment 1**

- *What I asked for:* For Claude to label the whole dataset for me.
- *What came back:* It pre-labelled everything, but held back 20 comments
  for me to label cold and then compared our answers.
- *What I changed:* The comparison showed I was using a different rule than
  the one written down (I only counted tool use if the comment was built
  around it). I rewrote the experience/claim rule to match my judgment, and
  Claude relabelled under my version.

**Moment 2**

- *What I asked for:* Whether the model could read the whole comment
  instead of just the start.
- *What came back:* It measured my comments with the tokenizer: 71% fit in
  128 tokens, 92% in 256, 99% in 512, and DistilBERT can't go past 512.
- *What I changed:* I set `MAX_LENGTH = 256`, which covers almost all of my
  comments without making training much slower.

**Pre-labelling disclosure:** All labels started as Claude's pre-labels. I
labelled 20 cold before seeing its labels (19 kept, 1 skipped), and
decided 9 borderline comments myself. The other 191 are Claude's labels
under my final rules, and I did not check them one by one. Claude also
wrote `collect_hn.py` and picked the 8 threads after I chose the topic.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

Baseline is `facebook/bart-large-mnli`, zero-shot, using my definitions from
`label_definitions.txt`. Both columns are scored on the same 33 held-out
posts (`test_split.csv`).

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.455 | 0.758 | +0.303 |
| Macro F1 | 0.208 | 0.531 | +0.323 |
| F1 — `experience` | 0.000 | 0.778 | +0.778 |
| F1 — `claim` | 0.625 | 0.815 | +0.190 |
| F1 — `question` | 0.000 | 0.000 | +0.000 |

I also ran the baseline with bare label names instead of definitions
(`baseline_results_bare_names.json`): accuracy 0.545, macro F1 0.521, F1
0.667 / 0.435 / 0.462 for experience / claim / question.

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

I ran the baseline two ways: first with bare label names (0.545 accuracy),
then with my definitions. This prediction is for the definitions run,
written before running it.

I expect it to land around **0.60**: better than bare names, but still well
below my trained model. I think the definitions will help most with
`claim`, which bare names only caught a third of the time, because "a
statement that is not based on the writer's own use" tells the model much
more than the word "claim" does. I expect it to still struggle on experience
vs. claim, because my real rule (is the comment *built around* the use?) is
about how much of a comment is first-hand, and a one-sentence definition
can't carry that. My trained model should beat it most clearly there.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->

My prediction was wrong. I expected my definitions to help the baseline
reach about 0.60. Instead they made it worse: 0.455 with definitions against
0.545 with bare names. With definitions it predicted `claim` for all 33
posts, so 0.455 is just the share of `claim` in the test set. My `claim`
definition starts with "a statement about AI tools", which is true of every
comment in my dataset. The part that's supposed to rule things out ("not
based on the writer's own use") is a negation, and the zero-shot model
ignored it. So my definitions work for a person applying my rule, but not
as a prompt.

Fine-tuning clearly added something for experience vs. claim: +0.30
accuracy over the definitions baseline and +0.21 over bare names, and
experience went from 0.000 to 0.778. The trained model learned the
boundary from examples that a one-sentence definition couldn't express.

For `question`, fine-tuning added nothing. Both models score 0.000, and the
bare-names baseline actually did better (0.462, it caught all 3 questions,
though it also called 7 other posts questions). With only 15 training
questions, my model learned to never predict that label, while the plain
word "question" was enough for the zero-shot model to find them.



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

All three runs on `mps` (Apple Silicon GPU), torch 2.14.1, `MAX_LENGTH`
256, 33 test posts each (15 experience, 15 claim, 3 question).

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.65 | 0.758 | 0.727 | 0.758 | MET |
| 2. F1 `experience` / `claim` | ≥ 0.60 each | 0.778 / 0.815 | 0.812 / 0.710 | 0.800 / 0.789 | MET |
| 3. F1 `question` | ≥ 0.50 | 0.000 | 0.000 | 0.000 | MISSED |
| 4. Confidence gap (most vs. least sure third) | ≥ 15 pts | 0 (0.727 vs 0.727) | 54.5 (1.000 vs 0.455) | 54.5 (1.000 vs 0.455) | MISSED |
| 5. Agreement with staff labels | ≥ 70% | 30/30 (not seed-dependent) | — | — | MET (see caveat in Agreement Report) |

Accuracy moved only 3 points across the three seeds (0.727 to 0.758), so
the overall number is stable. `claim` F1 moved the most (0.710 to 0.815).

### Confusion matrix

Rows are what I labelled, columns are what the model guessed. The diagonal
(top-left to bottom-right) is correct; every other cell is a mistake. For
example, the `claim` row in seed 42 means: of 15 posts I labelled `claim`,
the model called 4 of them `experience` and 11 of them `claim`.

Seed 42 (the notebook's section 7 prints the first seed):

| true \ predicted | experience | claim | question |
|---|---|---|---|
| **experience** | 14 | 1 | 0 |
| **claim** | 4 | 11 | 0 |
| **question** | 3 | 0 | 0 |

Summed over all three seeds (99 test predictions), from
`results_three_seeds_before.json`:

| true \ predicted | experience | claim | question |
|---|---|---|---|
| **experience** | 37 | 8 | 0 |
| **claim** | 8 | 37 | 0 |
| **question** | 3 | 6 | 0 |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

- **Seed 42 on its own:** the biggest mistake is 4 real `claim` posts called
  `experience`, with only 1 going the other way. That looks like the model
  leans toward `experience`.
- **All three seeds added up:** the biggest off-diagonal number is 8, and
  it's a tie: 8 real `claim` posts called `experience` and 8 real
  `experience` posts called `claim`. Seed 2024 even went the
  opposite way (5 `experience` called `claim`, 0 `claim` called
  `experience`). So there's no lean. The model mixes up `experience` and
  `claim` equally in both directions, which fits how many close calls I had
  on that boundary while labelling.
- **The one error that holds on every seed:** the model never predicted
  `question`. All 9 test questions across the three seeds were called
  `experience` or `claim`.



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** 30 / 30 = 100%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

That's higher than staff said to expect (the 70s), so it needs a caveat.
`data/staff_posts.csv` is sorted by label: posts 1–10 are all `analysis`,
11–20 all `hot_take`, 21–30 all `reaction`. My labels came out in those same
three blocks. I gave a reason for every post from the staff rules, but the
order was a strong hint, so 100% overstates how well I'd do on shuffled
posts. The more useful evidence is the 7 posts staff marked as HARD, below.

**Disagreements**

None. Instead, here are the 7 posts staff flagged as borderline. These are
the ones where I could most easily have disagreed, so they're where my
reading of the rules can actually be checked.

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1. Post 14 (the closest call for me)**
> *The post:* "Times are down about 3% since the shoe rules changed, so
> obviously the shoes are the whole story and the sport has a problem."
>
> *Staff said / I said:* `hot_take` / `hot_take`
>
> *My call, and why:* This is the one I nearly called `analysis`, because
> "since the shoe rules changed" and "so" sound like an argument. Rule 1
> settles it: the 3% doesn't show that shoes are "the whole story". It's
> decoration on a conclusion the writer already had, and "so obviously" is
> doing the work. It's almost the same as the staff's own shoe example.
>
> *Which pile:* none (agreed), but the rule covered it only because rule 1
> has a worked example this close.

**2. Post 5**
> *The post:* "Carbon plates aren't the whole story. My times dropped 2% in
> the shoes and another 2% the following year in the same pair, when the only
> thing that changed was going from 35 to 50 miles a week."
>
> *Staff said / I said:* `analysis` / `analysis`
>
> *My call, and why:* The first sentence reads like a hot take, but the
> second does the arguing: two comparable numbers with only mileage changed.
> The fact carries the conclusion (rule 1). The opposite case from post 14.

**3. Post 10**
> *The post:* "Three of us ran the same session on the same day, different
> shoes, within 10 seconds of each other over 5 miles. I'm not saying shoes
> do nothing, but whatever they do was smaller than the noise between three
> people."
>
> *Staff said / I said:* `analysis` / `analysis`
>
> *My call, and why:* Tiny sample, but the conclusion is limited to exactly
> what the observation shows. A weak fact that carries the argument is still
> `analysis`; rule 1 is about whether the fact does work, not how strong it is.

**4. Post 19**
> *The post:* "Nobody actually enjoys the long run. They enjoy having done
> it, which is a completely different thing, and the sport would be more
> honest if it said so."
>
> *Staff said / I said:* `hot_take` / `hot_take`
>
> *My call, and why:* It sounds personal and reflective, almost `reaction`,
> but it's a claim about everyone, not a report of the writer's own run. Rule
> 2: about the world, not the writer.

**5. Post 20**
> *The post:* "Every injury thread on this forum is the same injury and the
> same three replies."
>
> *Staff said / I said:* `hot_take` / `hot_take`
>
> *My call, and why:* Could be checked in principle, but no count or example
> is given, so it's asserted, not shown. Checkable isn't enough; the fact has
> to actually be there.

**6. Post 28**
> *The post:* "Third DNF this year. I don't really want to talk about it,
> just wanted to put it somewhere."
>
> *Staff said / I said:* `reaction` / `reaction`
>
> *My call, and why:* "Third this year" is a countable fact, but nothing is
> argued from it. It's the writer reporting how they feel. Rule 3 only makes
> something `analysis` when a fact is load-bearing.

**7. Post 29**
> *The post:* "Just realised the shoes I set every PB in this year are the
> ones I bought by accident in the wrong size."
>
> *Staff said / I said:* `reaction` / `reaction`
>
> *My call, and why:* Could be a wry hot take about shoe hype, but it reports
> the writer's own realisation, right now, without arguing that the size
> caused the PBs. Rule 2.

**What the pattern in my disagreements tells me:**

I don't think 30/30 tells me as much as it looks like. The posts were sorted
by label, and the staff rules come with worked examples very close to the
hard cases (post 14 is nearly their own shoe example). My own
experience/claim rule had neither of those, and it was still changing while
I labelled. My cold 20 only agreed with a second labeller 78% of the time.

What I can take from it is smaller: when a rule is written clearly with
examples, I can follow it. That applies to the 28 labels I decided myself.
The other 191 were applied by Claude under my rules and I didn't check them
one by one, so this check doesn't tell me much about those.

For my diagnosis, that means I can't rule out labelling as a cause of the
experience/claim confusion. It's probably partly a hard boundary, since the
model gets it wrong equally in both directions, but if labels are part of
it, the 191 unchecked rows are where I'd look first.



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
