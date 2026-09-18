---
link_style: obsidian
---

# Literature Notes Configuration

- `link_style: obsidian` — internal cross-references (`source_id`,
  `influences`, inline citations, Glossary terms, decision links) use
  `[[wikilink]]` syntax. Best when you read/edit this bundle in Obsidian (or
  another wikilink-aware tool).
- `link_style: markdown` — the same cross-references use plain relative
  Markdown links (`[label](path.md)`, `[label](path.md#anchor)`) instead, so
  the bundle renders correctly in GitHub, GitLab, mkdocs, or any plain
  Markdown viewer that doesn't understand `[[wikilinks]]`.

Change this value by hand at any time; every content-writing skill reads it
before writing a new cross-reference. Existing links already written in the
old style are **not** rewritten automatically when you switch — run
`/literature-notes-validate` afterward to see what a manual cleanup would
need to touch.
