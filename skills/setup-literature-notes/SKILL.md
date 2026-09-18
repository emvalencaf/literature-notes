---
name: setup-literature-notes
description: >-
  One-time (idempotent) setup for the literature-notes reading-notes system:
  scaffolds `.literature-notes/{sources,notes}`, `tags.md`, `index.md`, and
  `config.md` (link style), and documents the workflow in CLAUDE.md and
  AGENTS.md. Use when starting to use literature-notes in a project for the
  first time, or to re-sync the docs after the skill's workflow changes.
user-invocable: true
argument-hint: "[--link-style obsidian|markdown]"
allowed-tools: Bash
---

# setup-literature-notes

Scaffolds the `.literature-notes/` bundle and documents the workflow in
`CLAUDE.md`/`AGENTS.md`. Safe to re-run: it only creates what's missing and
never overwrites `tags.md`, `index.md`, `config.md`, existing sources, or
existing notes.

## Step 0 — ask the link style (only if `.literature-notes/config.md` doesn't exist yet)

Check first — if `config.md` already exists, skip straight to running the
script with no `--link-style` flag (it's ignored once the file is there).
Otherwise, unless `$ARGUMENTS` already gives `--link-style`, ask the user:

> This bundle can cross-reference itself two ways:
> 1. **Obsidian** — `[[wikilink]]` syntax. Best if you open `.literature-notes/`
>    as an Obsidian vault (or another wikilink-aware tool) — links are
>    clickable and feed the graph view.
> 2. **Plain Markdown** — ordinary relative links (`[label](path.md)`).
>    Best if you'll read this on GitHub/GitLab, a static-site generator, or
>    any viewer that doesn't understand `[[wikilinks]]`.
>
> Which one?

Pass the answer through as `--link-style obsidian` or `--link-style markdown`.

```bash
uv run "${CLAUDE_SKILL_DIR}/scripts/setup.py" $ARGUMENTS
```

Fall back if `uv` is unavailable:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/setup.py" $ARGUMENTS
```

It:

1. Creates `.literature-notes/sources/` and `.literature-notes/notes/` if
   missing.
2. Creates `.literature-notes/tags.md` (from `assets/tags.md`, an empty
   controlled-vocabulary template) if missing.
3. Creates `.literature-notes/index.md` (from `assets/index.md`, an empty
   tracking table, header only) if missing — it tracks which ingested
   works/notes still need to be confronted with, or used to update, the
   research scope. `/literature-notes` appends a `pending` row per new note;
   `/literature-notes-rescope` flips rows to `reviewed` as it interviews the
   user about them.
4. Creates `.literature-notes/config.md` (from `assets/config.md`) if
   missing, recording the chosen `link_style`. Every content-writing skill
   reads this before writing a cross-reference — see each skill's own docs
   for the two syntaxes.
5. Inserts or updates a marked block (`<!-- literature-notes:start/end -->`,
   from `assets/claude-md-block.md`) in both `CLAUDE.md` and `AGENTS.md`,
   describing when to use `/literature-notes`, `/literature-notes-scope`,
   `/literature-notes-query`, `/literature-notes-rescope`, and
   `/literature-notes-validate`. If a file doesn't exist yet, it's created
   with just that block. If the block already exists and is up to date,
   that file is left untouched.

This skill does **not** create `RESEARCH.md` or `Glossary.md` — those are
scaffolded lazily by `/literature-notes-scope` the moment there's an actual
scope or term to write down, not as empty placeholders here.

## Dependency: the `grilling` skill

`/literature-notes-rescope` invokes the `grilling` skill to run its interview
— it isn't bundled here. If it isn't already installed, tell the user to run:

```bash
npx skills@latest add mattpocock/skills --skill grilling
```

`/literature-notes-rescope` doesn't work without it.

Report to the user what was created vs. already present, per the script's
output, plus the chosen `link_style` and whether `grilling` needs installing.
