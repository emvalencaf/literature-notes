---
name: literature-notes-query
description: >-
  Search the `.literature-notes/` reading-notes bundle by tag, source, note kind,
  page, influence links, verification status, or free text, with results
  combinable. Use when the user wants to find, list, or compile existing
  reading notes/annotations for a dissertation — e.g. "what notes do I have
  about X", "show me all summary notes from Dworkin 1986" — or to work
  through the backlog of notes a human hasn't verified yet.
user-invocable: true
argument-hint: '[--scope notes|sources|both] [--tag x] [--source-id x] [--note-kind authorial|interpretive|summary] [--page n] [--influences id] [--influenced-by id] [--text "..."] [--verified true|false] [--limit n] [--output file.md]'
allowed-tools: Bash Read Edit
---

# literature-notes-query

Runs the structured filter over `.literature-notes/` and prints matches.
Filters are combinable (AND) and all optional; with none, prints every
document in scope.

```bash
uv run "${CLAUDE_SKILL_DIR}/scripts/query.py" $ARGUMENTS
```

Fall back if `uv` is unavailable:

```bash
python3 -m pip install --quiet pyyaml && \
python3 "${CLAUDE_SKILL_DIR}/scripts/query.py" $ARGUMENTS
```

- Default `--scope both` searches `sources/` and `notes/`; note-only filters
  (`--note-kind`, `--page`, `--influences`, `--influenced-by`) simply never
  match a source record.
- `--text` is a case-insensitive substring search across the body (quotes +
  prose) and all metadata values — use it as a fallback when no structured
  filter fits, or to combine with structured filters for a tighter search.
  It's also how you search by `Glossary.md` term: `--text "[[Glossary#Judicial
  Activism]]"` finds every note that wikilinks that term.
- `--verified true|false` filters by whether a note carries a `verified{}`
  block. This is the entry point for the verification backlog: run
  `--verified false --note-kind authorial` (or drop `--note-kind` for every
  kind) to see what a human hasn't confirmed yet. Present each one, and for
  every note the user confirms as fine, edit its frontmatter to add
  `verified: {by: "human:<id>", at: "<today, ISO8601>"}` — don't ask the user
  to hand-edit the YAML themselves.
- `--source-id`, `--influences`, and `--influenced-by` take a plain ID (e.g.
  `dworkin-1986`) even though the matching frontmatter fields are stored as
  `[[wikilink]]`s — the query script strips the brackets for you.
- Without `--output`, results print to the chat. With `--output <file.md>`,
  they're written to that file instead (e.g. to compile every citation for a
  chapter before drafting) and only a summary line is printed.
- `--limit` caps how many matches are returned, to keep a broad query cheap.
  Default is **5** when printing to the chat (unlimited when `--output` is
  set, since a file write doesn't cost context). If the 5 shown aren't
  conclusive for what the user needs, re-run with a higher `--limit` (the
  script's own "Showing X of Y" note tells you the total available) rather
  than assuming those 5 are everything.

Present results to the user grouped by source when there are several, and
always show the file path so they can open a note directly.
