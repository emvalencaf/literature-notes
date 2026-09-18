---
name: literature-notes
description: >-
  Produce reading-notes-style annotations from an academic PDF for academic
  research. Extracts text from a page range, then generates one Markdown file
  per annotation (authorial / interpretive / summary) with ABNT citation
  metadata, page references, and quotes — filed under `.literature-notes/`.
  Use when the user wants to read/annotate a PDF, extract concepts or
  quotations for a thesis, or annotate a source.
user-invocable: true
argument-hint: '<pdf-path> [--focus "<research lens>"] [--pages a-b] [--source-id x] [--type authorial|interpretive|summary]'
allowed-tools: Read Write Edit Bash Glob Grep
---

# literature-notes

Turns a PDF (or a page range of it) into reading-notes filed under
`.literature-notes/`, a bundle **separate from** any `.knowledge/` OKF bundle —
this is for academic research, not project/software knowledge.

If `.literature-notes/` does not exist yet, tell the user to run
`/setup-literature-notes` first (do not scaffold it yourself here — that skill
also owns the `tags.md` template and the CLAUDE.md/AGENTS.md documentation).

## Step 0 — read the link style

Read `.literature-notes/config.md`'s `link_style` before writing anything
(default to `obsidian` if the file predates this setting). It decides how
every cross-reference below is written:

- **`obsidian`**: `[[id]]` for a plain reference (`source_id`, `influences`,
  an `index.md` row), `[[Glossary#Term]]` / `[[decisions/id]]` for a
  heading/decision link.
- **`markdown`**: the bare id with no brackets for a plain reference
  (`source_id: "dworkin-1986"`), a relative Markdown link for anything
  inline in prose or pointing at a heading, e.g.
  `[dworkin-1986](../sources/dworkin-1986.md)`,
  `[Judicial Activism](../Glossary.md#judicial-activism)` — the anchor is
  the heading lowercased, spaces turned to hyphens, punctuation stripped.

## Arguments

Parse `$ARGUMENTS` as: `<pdf-path> [--focus "<text>"] [--pages a-b] [--source-id x] [--type authorial|interpretive|summary]`.

- `--focus` decides which passages are worth a note — not every concept in a
  source belongs; skip passages that don't serve it. If given, use it as-is.
  If omitted, fall back to `.literature-notes/RESEARCH.md`: use its "Research
  Question" and "Delimitation" sections as the focus, so every note is taken in
  light of the research scope rather than as a neutral summary. If
  `RESEARCH.md` doesn't exist either, ask the user for a focus interactively
  before doing anything else — never annotate with no lens at all.
- `--pages a-b` (1-based, inclusive) restricts extraction; omit to process the
  whole PDF.
- `--source-id` reuses an existing `.literature-notes/sources/<id>.md`. If
  omitted or the file doesn't exist yet, ask the user for the source metadata
  (author, title, year, and — if applicable — the URI it was downloaded from
  and the download date) and create the source record first.
- `--type` restricts note generation to one `note_kind`. Omit it to let
  yourself decide the kind per concept found — a single passage can justify
  both a `summary` note and, separately, an `interpretive` one.

## Step 1 — extract the text

```bash
uv run "${CLAUDE_SKILL_DIR}/scripts/extract_pdf.py" <pdf-path> [--pages a-b]
```

Fall back if `uv` is unavailable:

```bash
python3 -m pip install --quiet pypdf && \
python3 "${CLAUDE_SKILL_DIR}/scripts/extract_pdf.py" <pdf-path> [--pages a-b]
```

Output is plain text with `=== PAGE N ===` markers so you can attribute quotes
to the correct page.

## Step 2 — resolve the source record

`source-id` convention: `<author-surname-lowercase>-<year>`, e.g. `dworkin-1986`.

If `.literature-notes/sources/<source-id>.md` doesn't exist, create it from
`assets/source.md`. Frontmatter fields (English):

- `type` — always `"Reference"`, fixed, no variants
- `author`, `title`, `year`
- `pdf_path` — local path to the PDF (never versioned in the repo)
- `uri` — optional, where it was downloaded from
- `downloaded_at` — optional, ISO date, only if `uri` is set
- `abnt_reference` — the full ABNT (NBR 6023) reference string
- `tags` — general themes of the work, drawn from `.literature-notes/tags.md`
  (see tag rules below)

## Step 3 — read for the stated focus, write notes

Read the extracted text with `--focus` as your search lens. For each passage
worth capturing, create one file per annotation at
`.literature-notes/notes/<source-id>--p<page>--<slug>.md` (`slug` = a short
kebab-case label for the concept), from `assets/note.md`. Frontmatter:

- `type` — always `"Reading Note"`, fixed, no variants
- `source_id` — the source's ID per the active link style, e.g.
  `"[[dworkin-1986]]"` (obsidian) or `"dworkin-1986"` (markdown)
- `page` (single) or `pages` (range, `a-b`) — where the passage is
- `note_kind` — one of `authorial`, `interpretive`, `summary` (respect `--type`
  if given):
  - `authorial` — your own research notes; may or may not cite other authors
    or other notes
  - `interpretive` — your interpretation of what the author said
  - `summary` — a straight account of the author's own reasoning, without
    your judgment (this is what a traditional reading-notes record means)
- `tags` — the specific concept(s) this note is about, from the controlled
  vocabulary
- `influences` — optional list of other note IDs, per the active link style,
  e.g. `["[[dworkin-1986--p45--regra-vs-principio]]"]` (obsidian) or
  `["dworkin-1986--p45--regra-vs-principio"]` (markdown), that this note
  builds on or changes the reading of. Write it only on the influencing
  note, pointing at the influenced one(s); don't try to keep a reverse field
  in sync by hand.
- `abnt_citation` — the short in-text ABNT citation, e.g. `(DWORKIN, 1986, p.
  45)`, derived from the source's `author`/`year` + this note's `page`
- `generated.by`/`generated.at` — always set at creation: `by` is this
  skill's actor id, `literature-notes/<model-id>` (fill `<model-id>` with the
  model actually running this session, e.g. `claude-sonnet-5`); `at` is now,
  in ISO8601.
- `status: draft` — **only** when `note_kind: authorial`. Omit entirely for
  `interpretive`/`summary` notes — they report someone else's reasoning, not
  the researcher's own evolving idea, so a maturity axis doesn't apply. Never
  transition it yourself once set; that's the researcher's call to make by
  hand.
- Leave `verified` and `reviewed` **unset** at creation — they're stamped
  later: `verified` by a human confirming the note is fine as-is (see
  `literature-notes-query`'s `--verified` filter), `reviewed` by a human
  (optionally `assisted_by` an agent) who comes back to add or change
  something in the note.

Before writing the body, read `.literature-notes/Glossary.md` if it exists
(same discipline as reading `tags.md`). When the passage touches a term
defined there, link it inline in the body per the active style — don't
restate the definition, just link it. If the source uses a defined term in a
way that conflicts with `Glossary.md`, don't silently pick one reading: flag
the conflict to the user (this is `literature-notes-scope` territory, switch
into it) before writing the note.

Body: **in the user's own language** (whatever language they're writing to
you in) — the note is for them and for you-in-a-future-session, not for
publication in a fixed language. Quote the original passage verbatim
whenever possible, **in the source's original language** (never translate a
quote), followed by your note/interpretation/summary in the user's language.
Always anchor the quote to its page.

## Link everything you can — this is a wiki, not a pile of files

`.literature-notes/` is meant to be browsed and followed, not just grepped.
Whenever the body's prose mentions:

- **another author/work already in `sources/`** (you're citing them, not
  just the one you're currently reading) → link to that source record, not
  just a bare name-year in prose
- **a term defined in `Glossary.md`** → link it (see above)
- **another existing note** whose claim this one restates, builds on, or
  contradicts, beyond what `influences` already captures → link it inline
  too, so the connection is visible from the body text itself, not only from
  frontmatter
- **a decision record** relevant to why this note reads the way it does →
  link it

Skip linking only the *first-ever* mention of something that doesn't exist
in the bundle yet (a source/term/note not created yet — nothing to point
at). Every mention after that should be a link. This is what makes the
bundle a navigable wiki instead of disconnected files that happen to share a
folder.

## Style: write for humans and agents

A note is read cold, much later, by you-in-a-future-session or by the user
mid-draft — neither has the source open. Optimize for that:

- Structure the body with headings/lists rather than one dense paragraph, so
  a reader (or a future query) can skim straight to the point.
- Whenever it clarifies the concept, add a brief illustrative example (a
  short hypothetical case, a minimal analogy) — but keep it short; the point
  is to make the abstract concrete, not to pad the note.
- When the passage describes a structure, process, taxonomy, or relationship
  between concepts (a flow, a hierarchy, competing positions), add a small
  diagram as a fenced ```mermaid``` block. Skip it for anything that's just
  linear prose with nothing structural to show — a diagram forced onto plain
  narrative adds noise, not clarity.

## Tag rules

Tags are a controlled vocabulary in `.literature-notes/tags.md`. Read it
before assigning tags. Reuse an existing entry whenever it fits. If none fits,
**propose** a new tag to the user (name + short description) instead of
writing it into `tags.md` yourself — only add it after they confirm.

## Step 4 — track the note in `index.md`

For every note file written in Step 3, append one row to
`.literature-notes/index.md` (create it from `setup-literature-notes`' empty
template if it's somehow missing), using the active link style for both
columns:

```md
| `[[<source-id>--p<page>--<slug>]]` | `[[<source-id>]]` | pending | | | |
```

(markdown style: `[<source-id>--p<page>--<slug>](notes/<source-id>--p<page>--<slug>.md)`
and `[<source-id>](sources/<source-id>.md)`, both relative to `.literature-notes/`.)

`review_status: pending` means "not yet confronted with the research scope" —
`/literature-notes-rescope` is what interviews the user about it and flips it
to `reviewed`. Never set it to anything but `pending` here, and never touch a
row for a note this run didn't just create.
