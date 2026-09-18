---
name: literature-notes-validate
description: >-
  Check the `.literature-notes/` reading-notes bundle for broken references —
  tags outside the controlled vocabulary, notes pointing at a nonexistent
  source, `influences` links to a note that doesn't exist, a Glossary
  cross-reference (`[[Glossary#...]]` or a markdown link to `Glossary.md#...`)
  to an undefined term, a `decisions/` record whose `triggered_by` or inbound
  link is broken, or a concept file missing its `type` field. Use before
  committing `.literature-notes/` changes, or whenever asked to validate/lint
  the reading-notes bundle.
user-invocable: true
argument-hint: "[bundle-dir]"
allowed-tools: Bash
---

# literature-notes-validate

Runs a deterministic checker against `.literature-notes/` (or the path given
as `$ARGUMENTS`, default `.literature-notes`).

```bash
uv run "${CLAUDE_SKILL_DIR}/scripts/validate.py" $ARGUMENTS
```

Fall back if `uv` is unavailable:

```bash
python3 -m pip install --quiet pyyaml && \
python3 "${CLAUDE_SKILL_DIR}/scripts/validate.py" $ARGUMENTS
```

It reports every:

- tag (in a source or a note) not present in `tags.md`
- note whose `source_id` has no matching `sources/<source_id>.md` (accepts
  both a plain ID and a `[[wikilink]]`)
- note's `influences` entry pointing at a note ID that doesn't exist (same,
  plain ID or `[[wikilink]]`)
- any Glossary cross-reference, in a note or source body, pointing at a term
  that doesn't exist in `Glossary.md` — both `[[Glossary#Term]]` (obsidian)
  and a markdown link to `Glossary.md#term-slug` (markdown; the slug is
  matched against each heading lowercased with spaces turned to hyphens)
- a `decisions/*.md` record's `triggered_by` pointing at a note that doesn't
  exist
- a decision cross-reference in `RESEARCH.md`/`Glossary.md` pointing at a
  decision record that doesn't exist — both `[[decisions/...]]` and a
  markdown link to `decisions/<id>.md`

This check works regardless of the bundle's `link_style` — it recognizes
both syntaxes, so it validates correctly whichever one `config.md` selects.

Exit code is non-zero when any of the above are found. Fix every reported
problem before considering `.literature-notes/` changes ready to commit —
either correct the file, or add the missing tag/term to
`tags.md`/`Glossary.md` after confirming it with the user (see the tag rules
in the `literature-notes` skill and the term rules in
`literature-notes-scope`).

Missing `RESEARCH.md` or `Glossary.md` altogether is reported as a warning,
not an error — it doesn't affect the exit code, since early-stage or legacy
bundles may not have them yet. Same treatment for a note or source missing
`type`: warning only, so a bundle predating this metadata convention still
validates cleanly — fix it opportunistically rather than being forced to
backfill every existing file at once.
