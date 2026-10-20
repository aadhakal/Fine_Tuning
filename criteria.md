# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy

Overall accuracy on the held-out test split is at least **0.65**, on every
one of the three seeds.

**Why this target:**

Always guessing `experience`, my biggest label, already gets about 46%, so
anything near 0.50 would mean the model learned basically nothing. On the
other end, when I labelled 18 comments on my own and compared them with a
second labeller using the same rules, we only agreed 78% of the time. The
model is learning from labels that are that consistent, so I can't really
expect it to beat ~0.78. 0.65 is about halfway between the two, which is
where I'd start calling it useful.

---

## 2. F1 for `experience` and `claim`

F1 is at least **0.60** for `experience` and at least **0.60** for `claim`,
on every seed.

**Why this target:**

This is my hardest boundary. Two of my four disagreements during the cold
labelling were experience vs. claim, and all 9 comments I had to flag for a
second look were this same pair: comments that mention using a tool once and
then argue a bigger point. So I expect most of the model's
mistakes to be here too. I'm not setting it lower than 0.60 because these
are my two big labels (around 100 comments each, so roughly 15 each in the
test split), which means their scores shouldn't jump around too much
between seeds.

---

## 3. F1 for `question`

F1 for `question` is at least **0.50** on every seed.

**Why this target:**

I only have 21 questions, so about 3 of them end up in the test split. With
3 examples, one wrong prediction changes the F1 a lot, so this target has to
be looser than the other two. I didn't go lower than 0.50 though, because
questions are the easiest label to spot: most of them are short and ask
something directly ("how does it compare to Aider?").

---

## 4. Confidence

On the test split, the model's most confident third of predictions is at
least **15 percentage points** more accurate than its least confident third,
on every seed.

**Why this target:**

If the confidence score doesn't separate right answers from wrong ones,
it's useless for deciding which predictions to trust. I expect the
confident predictions to be the short questions and the obvious personal
stories, and the unsure ones to be the mixed comments I struggled with
myself, so there should be a real gap. 15 points is a gap I'd actually
notice, not just noise on a test set of ~33 comments.

---

## 5. Consistency with the staff labels

When I label the 30 staff posts in unit 6 using the staff taxonomy, I agree
with the staff labels on at least **70%** of them (21 of 30).

**Why this target:**

Under my own rules I agreed with the other labeller 78% of the time, and
those were rules I wrote. The staff taxonomy is someone else's, so I expect
to do a bit worse applying it. 70% would show I can apply written rules
consistently. If I land well below that, it's a sign my own 219 labels are
less consistent than I think.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
