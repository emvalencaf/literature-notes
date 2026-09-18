---
name: literature-notes-scope
description: >-
  Build and sharpen the scope and glossary of a dissertation's
  `.literature-notes/` bundle: `RESEARCH.md` (the research question,
  objectives, and delimitation) and `Glossary.md` (the controlled vocabulary
  of concepts this research turns on). Use when defining or revising what the
  research is about, resolving what a term means in this research, or when
  `/literature-notes` needs a scope to read against and neither file exists
  yet.
user-invocable: true
argument-hint: ""
allowed-tools: Read Write Edit Glob Grep
---

# literature-notes-scope

The active counterpart to `/literature-notes`: that skill *reads* the scope
and glossary; this skill is where they get written and challenged. Same
relationship as `domain-modeling` has to a codebase's `CONTEXT.md` — this
skill exists for when you're changing the research model, not just consuming
it while annotating.

Both files live in `.literature-notes/`, are single files (one dissertation,
one scope — no multi-context map), and are created **lazily**: the first time
there's an actual research question or term to write down, not as an empty
scaffold. `setup-literature-notes` does not create them.

Read `.literature-notes/config.md`'s `link_style` before writing either file
(default `obsidian` if `config.md` predates this setting) — it decides
whether a cross-reference is a `[[wikilink]]` or a relative Markdown link;
see `literature-notes`'s Step 0 for the exact syntax of each.

Both files' prose is written **in the user's own language** (whatever
language they're writing to you in), same as a note's body — this is the
researcher's own scope/glossary, not a fixed-language deliverable. A quoted
term from a source that uses a different language stays untranslated where
it's directly quoted. **Exception**: a `Glossary.md` term (the `####`
heading itself) stays in whatever language it was originally coined in,
never translated to match the surrounding prose — see references/GLOSSARY-FORMAT.md.

## `RESEARCH.md`

Format in [RESEARCH-FORMAT.md](./references/RESEARCH-FORMAT.md). Holds the research
question, objectives, delimitation, justification, and a starting theoretical
map.

- If it doesn't exist and the user is stating a research question/scope for
  the first time, create it from [`assets/research.md`](./assets/research.md).
- If it exists, treat conflicts seriously: if the user's current statement
  narrows, contradicts, or drops part of the existing scope, point that out
  before editing — "Your RESEARCH.md says the delimitation is X, but you just
  described Y. Is this a scope change or a refinement?"
- Update it the moment the scope actually shifts. Don't batch edits.
- Every edit stamps `reviewed.by`/`reviewed.at` (and `reviewed.assisted_by`
  with this skill's actor id, since you're the one drafting the change) per
  [RESEARCH-FORMAT.md](./references/RESEARCH-FORMAT.md)'s Frontmatter section. On first
  creation, also set `generated.by`/`generated.at` and `status: draft`.

## `Glossary.md`

Format in [GLOSSARY-FORMAT.md](./references/GLOSSARY-FORMAT.md). One `####` heading per
term, linkable per the active link style (`[[Glossary#Term Name]]` in
obsidian mode, `[Term Name](./Glossary.md#term-name)` in markdown mode).

- Create it lazily, from [`assets/glossary.md`](./assets/glossary.md), the
  moment the first term needs pinning down. The heading is the term's
  original-language name (don't translate it); the definition body is in
  the user's own language.
- **Challenge against it.** When the user (or a source being read) uses a
  term that conflicts with an existing `Glossary.md` entry, call it out
  immediately: "Your glossary defines 'judicial activism' as X, but this
  source uses it as Y. Do you want to record this divergence (as an
  `interpretive` note) or adjust the definition?"
- **Sharpen fuzzy language.** When the user uses an overloaded or vague term
  central to the research, propose pinning it down as a `Glossary.md` entry
  rather than letting it float undefined across notes.
- **Discuss concrete cases.** When a term's boundary is unclear, invent a
  concrete scenario ("a decision that does X but not Y — does that count as
  judicial activism under your definition?") to force precision.
- A term entry is independent from a `tags.md` entry — don't force a 1:1 (see
  the rules in references/GLOSSARY-FORMAT.md). Don't propose a `Glossary.md` entry just
  because a tag exists.
- The glossary is definitions only — never drift into recording what a
  specific author argued (that's a note's job) or a decision about the
  dissertation's own structure.
- Every edit stamps `reviewed`/`generated` the same way as `RESEARCH.md` —
  see references/GLOSSARY-FORMAT.md's Frontmatter section.
- When a term's definition or an `_Avoid_` note mentions a specific
  author/work already in `sources/`, link to that source record too — don't
  leave it as a bare name.

## Link everything you can — this is a wiki, not a pile of files

Same discipline as `literature-notes`: when `RESEARCH.md`'s theoretical
framework names an author/work already in `sources/`, or a passage in either
file touches a `Glossary.md` term, link it — don't restate it in bare prose.
Only the first-ever mention of something not yet in the bundle stays
unlinked.

## Relationship to `/literature-notes`

`/literature-notes` reads `RESEARCH.md` as its default focus lens when
`--focus` is omitted, and reads `Glossary.md` before writing notes so it can
link defined terms it recognizes in a passage. This skill is what keeps
those two files worth reading — if you're mid-annotation and notice the scope
or a term needs to change, switch into this skill's mode right there instead
of deferring it.
