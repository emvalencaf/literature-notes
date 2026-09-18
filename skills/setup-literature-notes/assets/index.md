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
