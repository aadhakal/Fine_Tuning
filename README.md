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

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



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

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

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

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



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
