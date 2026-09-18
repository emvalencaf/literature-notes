<!-- literature-notes:start -->
## Literature Notes

This project keeps academic reading notes in `.literature-notes/`,
separate from any `.knowledge/` OKF bundle — it targets dissertation research,
not project/software knowledge. Source PDFs are not versioned; source records
reference a local path plus, when available, the download URI and date.

- **This bundle is a navigable wiki, not a pile of files** -> link
  liberally, especially when citing. Whenever text mentions a source already
  in `sources/`, a term defined in `Glossary.md`, another existing note, or a
  decision record, turn that mention into a link (not bare prose) using the
  active `link_style` — see below. Only the *first-ever* mention of
  something not yet in the bundle stays unlinked (nothing to link to yet).
- **Link style** -> `.literature-notes/config.md`'s `link_style` decides the
  cross-reference syntax: `obsidian` (`[[wikilink]]`s, e.g.
  `source_id: "[[dworkin-1986]]"`, inline `[[Glossary#Judicial Activism]]`)
  or `markdown` (plain relative links, e.g. `source_id: "dworkin-1986"`,
  inline `[Judicial Activism](../Glossary.md#judicial-activism)`). Set once
  by `/setup-literature-notes`; every content-writing skill reads it first.
- **Scope and glossary** -> `.literature-notes/RESEARCH.md` (research
  question, objectives, delimitation) and `.literature-notes/Glossary.md`
  (controlled vocabulary of concepts this research turns on) are written and
  revised via `/literature-notes-scope`. Both are single files, created
  lazily the moment there's an actual scope/term to write down.
- **Reading a new source** -> `/literature-notes <pdf-path> [--focus
  "<research lens>"]` (add `--pages a-b` to scope, `--source-id` to reuse an
  existing source record, `--type authorial|interpretive|summary` to restrict
  the kind of note produced). `--focus` decides which passages are worth a
  note; if omitted, it falls back to `RESEARCH.md`'s scope.
- **Tracking pending review** -> `.literature-notes/index.md` lists every
  ingested note with a `review_status` (`pending` until reviewed), grouped by
  source. Scaffolded empty by `/setup-literature-notes`, appended to by
  `/literature-notes`, and updated by `/literature-notes-rescope`.
- **Looking up existing notes** -> `/literature-notes-query` with combinable
  filters (`--tag`, `--source-id`, `--note-kind`, `--page`, `--influences`,
  `--influenced-by`, `--verified`, `--text`); add `--output <file.md>` to
  compile results for a draft section.
- **Before committing** `.literature-notes/` changes -> run
  `/literature-notes-validate` and resolve every broken reference, undefined
  term, or out-of-vocabulary tag.
- **Tags** are a controlled vocabulary in `.literature-notes/tags.md` — propose
  new entries there instead of inventing free-form tags.
- **Metadata** loosely follows the Open Knowledge Format (OKF): every concept
  file carries a `type` (`Reading Note`, `Reference`, `Research Scope`,
  `Glossary`, `Decision`); notes/`RESEARCH.md`/`Glossary.md` also carry
  `generated{by,at}`; authorial notes and `RESEARCH.md` carry `status`
  (`draft`/`stable`/`deprecated`, human-only to change); a note gains
  `verified{by,at}` once a human confirms it as-is (see
  `/literature-notes-query --verified false`), and `reviewed{by,at,
  assisted_by?}` when a human (optionally agent-assisted) updates it.
- **Scope re-alignment** -> `/literature-notes-rescope` reads
  `.literature-notes/index.md` for notes with `review_status: pending`; if
  more than one source has pending notes it asks which author/work to review
  first (or takes a source id / note path as `$ARGUMENTS` directly). It then
  interviews you about those notes and updates `RESEARCH.md`/`Glossary.md`/
  `index.md` after every round, never batching the update to the end.
  Hard-to-reverse, research-resignifying resolutions get recorded as
  `.literature-notes/decisions/<date>--<slug>.md`. Requires the `grilling`
  skill (`npx skills@latest add mattpocock/skills --skill grilling`) —
  install it if `/literature-notes-rescope` reports it's missing.
<!-- literature-notes:end -->
