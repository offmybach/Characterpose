# Pam Pereira — review of record

Attorney, former district attorney, and mediator. Parent of a second grader.

**Two versions are kept here on purpose.** The first is exactly what she wrote. The second
is the lightly edited text now running on the site, made with her permission, relayed
through Jonathan on 28 July 2026.

If anyone ever asks what she actually said, the answer is section 1 — not whatever is on
the site at the time. Keep both.

---

## 1. As submitted — do not edit this section, ever

```
I really enjoyed Clarence Gets a Bargain. As the parent of a second grader, I appreciated that the money concepts are worked into the story in a way that feels natural. It does not feel like a lesson or a homework assignment. My child could follow the story and enjoy it, while still picking up ideas about money, value, and making choices.

I also liked how the glossary terms show up again in the story. That helped make the words easier to understand because they were not just definitions on a page. They were connected to what was actually happening.

The illustrations are great too. They have a fun, polished look that my kiddo responded to, with enough realism to make the characters feel familiar.

I would definitely recommend this book for teachers, parents, and grandparents. It is not just a one-time read. It is the kind of book you can keep nearby and come back to when you want to help a child understand money in a simple and meaningful way.
```

---

## 2. Approved edit — the canonical text on the site

```
I really enjoyed Clarence Gets a Bargain. As the parent of a second grader, I appreciated that the money concepts are worked into the story in a way that feels natural. It does not feel like a lesson or a homework assignment. My child could follow the story and enjoy it, and still picked up ideas about money, value, and making choices.

I also liked how the glossary terms show up again in the story. That helped make the words easier to understand, because they were not definitions sitting alone on a page. They were connected to what was actually happening.

The illustrations are great too. They have a fun, polished look that my kiddo responded to, with enough realism to make the characters feel familiar.

I would definitely recommend this book for teachers, parents, and grandparents. It is not a one-time read. It is the kind of book you keep nearby and come back to when you want to help a child understand money without turning it into a lecture.
```

---

## 3. What changed, and why — five edits, nothing else

| # | Was | Now | Why |
|---|---|---|---|
| 1 | "while still picking up ideas" | "and still picked up ideas" | Past tense. She is reporting what her kid did, not what a kid might do. Concrete beats hypothetical. |
| 2 | "not just definitions on a page" | "not definitions sitting alone on a page" | Kills a "not just" construction. Says the same thing more plainly. |
| 3 | "It is not just a one-time read." | "It is not a one-time read." | Drops the hedge. The flat statement is stronger. |
| 4 | "the kind of book you can keep nearby" | "the kind of book you keep nearby" | Same reason. "Can" softens a claim she clearly means. |
| 5 | "in a simple and meaningful way" | "without turning it into a lecture" | The weakest phrase in the review, and it calls back to her own line in the first paragraph about it not feeling like a lesson. |

## What was deliberately left alone

- **No contractions were added.** She writes "It is not" and "does not." That is how a lawyer
  writes, it is the most identifying thing about the piece, and smoothing it would make her
  sound like the marketing copy around her.
- Sentence order, paragraph breaks, and every substantive observation are untouched.
- "The illustrations are great too" stayed. It is plain and it is hers.

## The pull-quote used in short slots

```
I appreciated that the money concepts are worked into the story in a way that feels natural. It does not feel like a lesson or a homework assignment.
```

Unchanged by the edit, and an exact contiguous excerpt of both versions. Any replacement
pull-quote must also be an exact contiguous stretch of section 2 — no stitching two
sentences together from different paragraphs.

## Guard

`scripts/check_pereira_quote.py` compares every rendering on the site against section 2 and
fails if the full text drifts or a short version stops being an exact excerpt. Run it after
touching any review markup. If she revises again, update section 2 and the log below —
never section 1.

## Change log

- **28 Jul 2026** — Added to site (index.html schema + testimonials, review-cards.html,
  press-kit.html). Original text.
- **28 Jul 2026** — Five-edit revision applied with her permission, relayed by Jonathan.
