# Review Index

Tracks ingested works/notes that still need to be confronted with the
research, or used to update it. The source of truth for scope review is
each note's frontmatter (`scope_reviewed_at`, absent = pending); this table
is a derived cache, maintained by other skills:

- `/literature-notes` appends one row per new note, with
  `review_status: pending`.
- `/literature-notes-rescope` flips `review_status` to `reviewed` after
  each completed interview round, filling in `reviewed_at`, `outcome`, and
  `decision`.

| note | source | review_status | reviewed_at | outcome | decision |
| --- | --- | --- | --- | --- | --- |
| `[[dworkin-1986--p52--regra-vs-principio]]` | `[[dworkin-1986]]` | reviewed | 2026-09-12 | no impact | |
| `[[streck-2014--p89--ativismo-judicial]]` | `[[streck-2014]]` | reviewed | 2026-09-15 | scope updated | `[[decisions/2026-09-15--incorporate-streck-critique]]` |
| `[[streck-2014--p112--decisionismo]]` | `[[streck-2014]]` | pending | | | |
