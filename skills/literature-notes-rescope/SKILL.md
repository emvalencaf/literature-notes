---
name: literature-notes-rescope
description: >-
  Interview the user, one work/author at a time, about reading notes that
  haven't been confronted with the dissertation's scope yet, and update
  `RESEARCH.md`/`Glossary.md`/`index.md` as understanding is reached. Reads
  `.literature-notes/index.md` to pick a pending work when no argument is
  given; a source id or a note path can be passed to target one directly.
user-invocable: true
disable-model-invocation: true
argument-hint: "[source-id-or-note-path]"
allowed-tools: Read Write Edit Glob Grep Bash
---

# literature-notes-rescope

Where `literature-notes-scope` writes `RESEARCH.md`/`Glossary.md` when the
user states a scope change directly, this skill goes the other way: it walks
the user through notes nobody has confronted with the scope yet and grills
them, work by work, on whether those notes should reshape it. Always
user-invoked — never fires on its own. Every review is a real interview —
this skill never decides "no impact" on the user's behalf.

**Requires the `grilling` skill.** If it's not installed, tell the user to
run `npx skills@latest add mattpocock/skills --skill grilling` and stop —
don't attempt the interview without it.

Read `.literature-notes/config.md`'s `link_style` before writing anything
(default `obsidian` if `config.md` predates this setting) — see
`literature-notes`'s Step 0 for the exact syntax of each; every `[[...]]`
example below assumes `obsidian` and has a `markdown`-style equivalent.

## Step 0 — pick the note set

Read `.literature-notes/index.md` first regardless of arguments — it's the
tracking source for what's pending.

- **No `$ARGUMENTS`**: filter `index.md` rows where `review_status: pending`,
  and group them by `source`.
  - No pending rows at all: say so and stop — nothing to review.
  - Exactly one source with pending rows: proceed straight to Step 1 with
    that source's pending notes.
  - More than one source: list them (author/work + pending count) and ask
    the user which one to review now. Proceed with only that source's
    pending notes — don't try to cover every pending source in one run.
- **`$ARGUMENTS` is a source id** (or a path under `.literature-notes/sources/`):
  pull that source's rows from `index.md`. Default to its `pending` rows; if
  it has none pending, tell the user everything for that source is already
  `reviewed` and ask whether to re-open any specific note anyway (don't
  silently re-run a full interview on already-reviewed notes).
- **`$ARGUMENTS` is a note path**: that single note only, regardless of its
  `review_status` — naming a note directly is the user asking to re-open it
  now. Skip straight to Step 1 for that one note; don't batch it with others.

## Step 1 — cluster and interview

Read the selected notes against the current `.literature-notes/RESEARCH.md`
("Delimitation" + "Research Question") and `Glossary.md`. If there's more than
one note, group them by the scope question they raise — several notes often
push toward the same underlying shift, and that shift is the actual decision,
not each note individually. A cluster can be a single note; don't force
merges that aren't real.

For each cluster, note for yourself: what claim/term/direction in it is
worth putting to the user (a claim outside the stated delimitation, a term
used in tension with a `Glossary.md` entry, a direction the delimitation never
anticipated), even without a literal conflict. This is prep for the
interview, not a filter — every cluster gets put to the user, including ones
that look like they'll land as "no impact."

Invoke the `grilling` skill, one design-tree branch per cluster, each branch
stating: which notes raised it, what in `RESEARCH.md`/`Glossary.md` it's in
tension with (or "no tension found, but here's the claim — confirm it needs
no change"), and a recommended resolution.

Frame every question provocatively, not as a yes/no rubber stamp: press on
consequence — what keeping the current scope forces the dissertation to
ignore, what changing it forecloses instead, which claim in the note the
delimitation can't currently account for — so the user has to argue their own
position rather than accept a suggestion by default. Make each recommended
resolution didactic: explain briefly *why* it's recommended (the mechanism —
how the note's claim interacts with the stated `Research Question` or a
`Glossary.md` term — not just the verdict), so the user is choosing from
understanding, not from trust in the recommendation.

## Step 2 — apply, decide, and record — after every round

Don't wait for the whole interview to finish before writing anything. As
**each cluster's branch resolves** in the grilling session, immediately:

1. **Edit `RESEARCH.md`/`Glossary.md` directly** per the agreed resolution (or
   make no edit, if the resolution is "no impact") — the grilling session
   already forced the "is this a real scope change" question into the open,
   so don't hand off to `literature-notes-scope`'s own challenge flow and ask
   it again. Follow `RESEARCH-FORMAT.md` / `GLOSSARY-FORMAT.md` (in
   `literature-notes-scope/references/`) for structure; create either file
   lazily from `literature-notes-scope/assets/{research,glossary}.md` if it
   doesn't exist yet. Stamp `reviewed.by`/`reviewed.at`
   (with `reviewed.assisted_by: "literature-notes-rescope/<model-id>"`) and
   refresh `generated.at` on whichever file you actually edited — same
   frontmatter contract `literature-notes-scope` uses.
2. **Judge whether the resolution is hard to reverse and resignifies the
   research** (narrows/drops an objective, changes the central question,
   redefines a `Glossary.md` term the argument depends on — not a wording
   tweak or an additive exclusion). If so, ask the user explicitly: "This
   looks like a structural decision — record it as a decision in
   `decisions/`?" Only propose it; never record one unasked, and never skip
   asking just because a change looks minor to you.
   - If yes: write `.literature-notes/decisions/<ISO-date>--<slug>.md` per
     the format below, listing every note in the cluster under
     `triggered_by`. Add a trailing link to it at the point of the
     `RESEARCH.md`/`Glossary.md` edit, per the active style, e.g.
     `(see [[decisions/2026-09-13--expand-scope-llm-kg]])` (obsidian) or
     `(see [2026-09-13--expand-scope-llm-kg](./decisions/2026-09-13--expand-scope-llm-kg.md))`
     (markdown).
3. Set `scope_reviewed_at` to today's ISO date on every note in the cluster,
   whether or not it drove a change — a note that legitimately needs no
   scope change must not resurface as pending.
4. **Update `.literature-notes/index.md` for this cluster's rows right now**
   (see Step 3) — never batch the index update to the end of the session. If
   the interview is interrupted after this point, `index.md` must already
   reflect every cluster resolved so far.

Repeat for the next cluster until all clusters for the chosen source/note are
resolved.

## Step 3 — update `index.md`

`.literature-notes/index.md` is a derived cache, not a source of truth (each
note's frontmatter is) — update it incrementally, one row per note, each time
Step 2 resolves a cluster:

```md
| note | source | review_status | reviewed_at | outcome | decision |
| --- | --- | --- | --- | --- | --- |
| `[[bragagnollo-2024--p197--...]]` | `[[bragagnollo-2024]]` | reviewed | 2026-09-13 | no impact | |
| `[[ghanem-2025--p3--...]]` | `[[ghanem-2025]]` | reviewed | 2026-09-13 | scope updated | `[[decisions/2026-09-13--expand-scope-llm-kg]]` |
```

(markdown style: each cell a relative link instead, e.g.
`[ghanem-2025--p3--...](notes/ghanem-2025--p3--....md)`,
`[2026-09-13--expand-scope-llm-kg](decisions/2026-09-13--expand-scope-llm-kg.md)`,
both relative to `.literature-notes/`.)

If a row for a note doesn't exist yet (e.g. `index.md` predates that note),
add it rather than skipping the update.

## Step 4 — close out

Once every cluster for the chosen source/note is resolved and `index.md` is
current, report a short summary: what changed in `RESEARCH.md`/`Glossary.md`,
which decisions were recorded, and — if invoked with no `$ARGUMENTS` — how
many other sources still have pending notes, so the user knows whether to
run this again.

## Decision record format

`.literature-notes/decisions/<ISO-date>--<slug>.md` (filename mirrors a
note's `<source>--p<page>--<slug>` convention). Bespoke and lightweight —
it borrows only the `type` key from OKF's metadata conventions (see
`README.md`), not a full `Decision` concept, since `.literature-notes/` stays
outside any `.knowledge/` bundle (see `CLAUDE.md`). Note that its own
`decision_status` field is deliberately **not** named `status` — OKF's
`status` is a fixed `draft|stable|deprecated` lifecycle enum, and this field's
values (`accepted`, etc.) mean something else entirely; reusing the same key
name for a different enum would mislead a generic OKF consumer.

```md
---
type: "Decision"
date: "2026-09-13"
decision_status: "accepted"
triggered_by: ["[[ghanem-2025--p3--...]]", "[[han-2025--p12--...]]"]
---

## Context

{What the prior scope said, and what in these notes put pressure on it. Link
every note/source you mention, not just the ones already in `triggered_by`.}

## Decision

{What changed in RESEARCH.md/Glossary.md, stated as a decision, not a diff.}

## Consequences

{What this opens up or forecloses going forward — including for the notes
already reviewed before this decision, if any of them now read differently
(link them too).}
```

(`triggered_by` in markdown style: `["ghanem-2025--p3--...", "han-2025--p12--..."]`
— bare ids, same as a note's `influences` field.)

`Context`/`Decision`/`Consequences` prose is written **in the user's own
language** (whatever language they're writing to you in), same as a note's
body — a decision record is for the researcher, not a fixed-language
deliverable. Keep any directly quoted term or passage in its original
language.

A later decision that resignifies the research again is a new record, never
an edit to an old one's `decision_status` — the trail is the point.
