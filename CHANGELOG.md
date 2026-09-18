# Changelog

All notable changes to this repository are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- `README.pt-BR.md`, a full Portuguese (Brazil) translation of the README,
  with a language switcher at the top of both files. Commands, flags, file
  names, and YAML keys stay literal; the worked example's generated note
  shows its body in Portuguese to match the language rule it documents.
- README: a "Search internals & token cost" section explaining the two-tier
  skill loading model, why `/literature-notes-query`/`-validate` cost scales
  with matches/problems rather than bundle size, and the role of `--limit`,
  `--output`, and `index.md` in keeping that cost low.
- README: a "How to use" section with a Mermaid flowchart of the setup →
  scope → read → query → rescope → validate cycle, a step-by-step walkthrough,
  and a worked example (commands, a sample generated note, and the resulting
  `.literature-notes/` directory tree).
- Initial public release of the `literature-notes` skill pack:
  - `literature-notes-ask-how` — a router skill explaining which of the other skills fits a
    given situation, inspired by mattpocock/skills' `ask-matt`.
  - `setup-literature-notes` — one-time, idempotent bundle scaffolding.
  - `literature-notes` — PDF ingestion and authorial/interpretive/summary note generation.
  - `literature-notes-scope` — research scope (`RESEARCH.md`) and glossary (`Glossary.md`) authoring.
  - `literature-notes-rescope` — interview-driven reconciliation of pending notes against the current scope.
  - `literature-notes-query` — structured search over the note bundle.
  - `literature-notes-validate` — deterministic reference/link checker for the note bundle.
- Repository restructured under `skills/` for `npx skills add` discovery.
- Metadata aligned with the Open Knowledge Format (OKF) spec: `type` on
  every concept file; `generated{by,at}` provenance; opt-in
  `verified{by,at}` (human confirms a note as-is) and
  `reviewed{by,at,assisted_by?}` (human updates content, optionally
  agent-assisted); `status` (`draft|stable|deprecated`) on authorial notes
  and `RESEARCH.md`. See the README's Metadata section.
- `literature-notes-query --verified true|false` filter, to work through the
  backlog of notes a human hasn't confirmed yet.
- `literature-notes-validate` now warns (non-fatal) on a concept file
  missing `type`.
- `.literature-notes/config.md`, created by `/setup-literature-notes` (which
  now asks the user's preferred link style up front): `link_style: obsidian`
  (`[[wikilink]]`s, default) or `link_style: markdown` (plain relative
  links), read by every content-writing skill before it writes a
  cross-reference. `literature-notes-validate` recognizes both syntaxes when
  checking Glossary/decision links.
- Explicit "link everything, especially when citing" guidance in
  `literature-notes`, `literature-notes-scope`, and `literature-notes-rescope`
  — the bundle is meant to read as a navigable wiki.
- `literature-notes-rescope` now states its dependency on the `grilling`
  skill and how to install it
  (`npx skills@latest add mattpocock/skills --skill grilling`), both in its
  own `SKILL.md` and in the README/CLAUDE.md/AGENTS.md documentation.

### Changed

- All skill templates moved to `assets/` (per-skill), replacing both the
  `literature-notes/templates/` directory and the string-constant templates
  previously embedded in `setup-literature-notes`'s script (`tags.md`,
  `index.md`, `config.md`, and the CLAUDE.md/AGENTS.md block are now real
  files under `skills/setup-literature-notes/assets/`, read from disk).
  Same for `literature-notes-scope`: the `RESEARCH.md`/`Glossary.md`
  skeletons that used to be inlined as fenced code blocks in
  `RESEARCH-FORMAT.md`/`GLOSSARY-FORMAT.md` are now
  `skills/literature-notes-scope/assets/{research,glossary}.md`.
- `literature-notes-scope`'s `RESEARCH-FORMAT.md`/`GLOSSARY-FORMAT.md` moved
  into `skills/literature-notes-scope/references/` — they're linked-to
  documentation, not part of `SKILL.md`'s always-loaded instructions.
- `CONTEXT.md` renamed to `Glossary.md` (and `CONTEXT-FORMAT.md` to
  `GLOSSARY-FORMAT.md`) for a more semantic name; wikilinks change from
  `[[CONTEXT#Term]]` to `[[Glossary#Term]]`.
- `decisions/*.md`'s `status` field renamed to `decision_status`, to avoid
  colliding with OKF's `status` lifecycle enum now used elsewhere in the
  bundle.
- Generated content (note/decision bodies, `RESEARCH.md`, `Glossary.md`) is
  now written in **the user's own language** instead of being hardcoded to
  English — `literature-notes`, `literature-notes-scope`, and
  `literature-notes-rescope` all updated. Directly quoted passages always
  stay in the source's original language, regardless of the body's
  language.
- `Glossary.md` term headings are the one exception: a term stays in
  whatever language it was originally coined in (e.g. "Ativismo Judicial"
  from a Portuguese source), never translated to match the surrounding
  prose — only the definition body follows the user's language.
