# Research Scope Format

`RESEARCH.md` states the scope of the dissertation research: what it's about,
what it deliberately excludes, and what it's trying to answer. It exists so
that reading notes are taken **in light of** this research, not as a neutral
summary of whatever a source says.

Create it from [`assets/research.md`](../assets/research.md) — that file has
the exact skeleton (frontmatter + section placeholders) to fill in.

## Frontmatter

- `type` is always `"Research Scope"` — fixed, no variants.
- `status` starts at `draft` when the file is first created and stays there
  until the researcher themself changes it to `stable` (e.g. once the scope
  is locked for the defense) or `deprecated`. No skill ever flips this on its
  own — it's a read on how settled the researcher's own thinking is, and only
  they can judge that.
- `generated.by`/`generated.at` — set (or refreshed) whenever the file's
  content actually changes, whoever drove the edit.
- `reviewed.by`/`reviewed.at` — set whenever a human updates the scope to add
  or change something. `reviewed.assisted_by` is optional: fill it with the
  invoking skill/model when an agent helped draft the update
  (`literature-notes-scope/<model-id>`), omit it entirely when the human
  edited the file directly with no agent involved.
- No `verified` here — `RESEARCH.md` is always edited interactively (the
  human is present for every change this skill makes), so a separate
  after-the-fact confirmation adds nothing `reviewed` doesn't already
  capture.

## Rules

- **Keep every section short.** This is a scope statement, not a chapter —
  one or two sentences per bullet, a short paragraph max for prose sections.
- **Be specific about exclusions.** "Delimitation" is most useful when it says
  what's *out*, since that's what decides whether a passage in a source is
  worth a note.
- **This is the default lens.** When `/literature-notes` is invoked without
  `--focus`, "Research Question" + "Delimitation" together are the focus used
  to decide what's worth annotating.
- **Update it when the scope actually shifts** — not on every reading
  session. A research question narrowing, a new exclusion becoming clear, or
  a sub-objective being dropped are the kind of changes that belong here;
  day-to-day reading doesn't.
