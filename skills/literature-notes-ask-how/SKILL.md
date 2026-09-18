---
name: literature-notes-ask-how
description: Ask which literature-notes skill fits what you're trying to do. A router over the skills in this pack.
user-invocable: true
argument-hint: ""
disable-model-invocation: true
---

# Ask How

You don't remember every skill, so ask.

There's one **flow** most sessions run: set up once, then cycle scope → read
→ query → reconcile. Everything else is a one-off maintenance step that
plugs into that cycle wherever it's needed.

## Precondition

**`/setup-literature-notes`** — run once per project, before anything else.
Scaffolds `.literature-notes/{sources,notes}`, `tags.md`, `index.md`, asks
your **link style** (Obsidian `[[wikilink]]`s vs. plain relative Markdown
links — `config.md` remembers the answer), and documents the whole workflow
in `CLAUDE.md`/`AGENTS.md`. Idempotent — safe to re-run any time to re-sync
the docs after a skill update.

## The main flow: scope → read → query → reconcile

1. **`/literature-notes-scope`** — state (or sharpen) the research question,
   objectives, and delimitation (`RESEARCH.md`), plus the controlled
   glossary of terms this research turns on (`Glossary.md`). Start here
   whenever there's no scope yet, or the scope itself needs to change — it's
   the lens every note below gets read through.
2. **`/literature-notes <pdf-path>`** — read a source (or a page range of
   it) and write one note per concept worth capturing: **authorial** (your
   own idea), **interpretive** (your reading of what the author meant), or
   **summary** (a neutral account of the author's own reasoning). No scope
   yet? It asks for a one-off focus instead of annotating with no lens at
   all.
3. **`/literature-notes-query`** — pull together what's already noted, by
   tag, source, note kind, page, influence links, verification status, or
   free text, before drafting a section or deciding what's still missing.
   Reach for this constantly, not just once at the end.
4. **`/literature-notes-rescope`** — periodically (not after every single
   note — batch it), confront the notes nobody's reconciled with the
   current scope yet, one work at a time, and let `RESEARCH.md`/`Glossary.md`
   evolve where the evidence actually pushes them to. With no argument it
   picks from the pending backlog; pass a source id or a note path
   (`/literature-notes-rescope dworkin-1986`) to target one directly instead
   of letting it choose. **Requires the `grilling` skill** (see Dependency
   below) — `/setup-literature-notes` flags this if it's missing.
5. **`/literature-notes-validate`** — before committing `.literature-notes/`
   changes, catch broken references: an out-of-vocabulary tag, a dangling
   `influences`/`triggered_by` link, an undefined `Glossary.md` term, a
   concept file missing its `type`.

Steps 2–5 repeat as you keep reading; step 1 only recurs when the scope
itself needs to move, which should be rarer.

## On-ramps

- **Already have reading notes from before this system existed?** Run
  `/setup-literature-notes` to scaffold the bundle and pick a link style,
  then either hand-write `sources/*.md`/`notes/*.md` matching the templates
  in `literature-notes`'s `assets/`, or just start fresh with
  `/literature-notes` for whatever you haven't captured yet — don't force a
  bulk migration up front.
- **Just want to search, nothing to add right now?** `/literature-notes-query`
  works the moment `/setup-literature-notes` has run once; you don't need a
  scope or any notes yet to try it (it'll just report no matches).

## Standalone

Not tied to a specific point in the cycle — reach for these whenever:

- **`/literature-notes-validate`** — a health check, not only a
  pre-commit gate.
- **`/literature-notes-query --verified false`** — the entry point to the
  verification backlog: notes an agent drafted that nobody's confirmed as
  fine-as-written yet.

## Dependency

`/literature-notes-rescope` invokes the `grilling` skill to run its
interview — it isn't bundled in this pack. If it isn't installed:

```bash
npx skills@latest add mattpocock/skills --skill grilling
```

Without it, the interview step of reconciling notes against scope won't run.

## Metadata and language, in one line each

- Every concept file loosely follows the Open Knowledge Format (`type`,
  `generated`, opt-in `verified`/`reviewed`, `status` on authorial notes and
  `RESEARCH.md`) — see the README's Metadata section for the full picture.
- Generated prose (note/decision bodies, `RESEARCH.md`, `Glossary.md`
  definitions) is written in **your own language**; a quoted passage stays
  in the source's original language; a `Glossary.md` term heading stays in
  whatever language it was originally coined in.
