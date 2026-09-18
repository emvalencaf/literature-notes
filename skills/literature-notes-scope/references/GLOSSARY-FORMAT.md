# Research Glossary Format

`Glossary.md` is the controlled vocabulary of concepts used *within this
research* — the same term can mean different things across sources, and this
file pins down which meaning this dissertation adopts. It's the same idea as
a codebase's domain glossary (see the `domain-modeling` skill's
`CONTEXT-FORMAT.md`), applied to academic/theoretical concepts instead of
code.

Create it from [`assets/glossary.md`](../assets/glossary.md) — that file has
the exact skeleton (frontmatter + a `####`-heading term entry) to fill in,
one heading per term. For example, two related-but-distinct terms would look
like:

```md
#### Judicial Activism

{One or two sentence definition — the meaning *this research* adopts when
authors diverge.}

_Avoid_: Activism (alone, unqualified), Judicialization of politics (a
related but distinct concept — see note below)

#### Judicialization of Politics

{Definition.}

_Avoid_: Judicial activism (not synonyms in this work)
```

Each term is a `####` heading (not bold text) so it can be linked directly
from a note or from `RESEARCH.md`, per the active link style: `[[Glossary#Judicial
Activism]]` (obsidian — resolves `[[file#Heading]]` as a real link, which
bold text can't be addressed by) or `[Judicial Activism](./Glossary.md#judicial-activism)`
(markdown — a plain relative link with a lowercased, hyphenated anchor).

**The term (heading) stays in whatever language it was originally coined
in** — a term from a Portuguese-language source stays "Ativismo Judicial,"
one from an English-language source stays "Judicial Activism"; don't
translate it to match the surrounding prose. The **definition body**, by
contrast, is written in the user's own language (see `literature-notes-scope`'s
`SKILL.md`) — only the heading itself is pinned to its term of origin, since
that's the identifier other notes wikilink against and translating it would
fragment the same concept under two different headings.

## Frontmatter

- `type` is always `"Glossary"` — fixed, no variants.
- `generated.by`/`generated.at` — set (or refreshed) whenever the file's
  content actually changes, whoever drove the edit.
- `reviewed.by`/`reviewed.at` — set whenever a human updates the glossary to
  add or change a definition. `reviewed.assisted_by` is optional: fill it
  with the invoking skill/model when an agent helped draft the update
  (`literature-notes-scope/<model-id>`), omit it entirely when the human
  edited the file directly with no agent involved.
- No `status` and no `verified` here — a glossary entry doesn't have a
  "how settled is this idea" axis the way `RESEARCH.md` does, and it's
  always edited interactively (the human is present for every change), so a
  separate after-the-fact confirmation adds nothing `reviewed` doesn't
  already capture.

## Rules (same spirit as `domain-modeling`'s glossary)

- **Be opinionated.** When authors use different words for the same concept,
  or the same word for different concepts, this file picks the meaning this
  research uses and lists what to avoid.
- **Keep definitions tight.** One or two sentences. State what the concept
  *is*, as used here — not a literature review of every author's take (that
  belongs in a note referencing the source).
- **Only include terms this research actually turns on.** A term any reader
  of the field already agrees on doesn't need an entry; only ones where
  precision matters for *this* dissertation's argument do.
- **A term entry is not the same as a `tags.md` entry.** `tags.md` classifies
  notes/sources for retrieval (a label); `Glossary.md` defines what a concept
  *means* in this research. Most tags won't have a matching term, and that's
  fine — don't force a 1:1.
- **Link liberally.** When a note's body or `RESEARCH.md` uses a defined
  term, link it (see the two syntaxes above). This is what makes the
  glossary a real hub — in Obsidian's graph view in `obsidian` mode, or just
  a followable page in `markdown` mode — instead of a dead reference page.

## When to update

Update `Glossary.md` the moment a term's meaning is resolved or challenged —
same discipline as `domain-modeling`: don't batch it up. If a note reveals
that an author uses a term in a way that conflicts with the current
definition, surface that conflict to the user before writing the note, the
same way `domain-modeling` challenges a codebase term against the glossary.
Stamp `reviewed` on every such update (see Frontmatter above).
