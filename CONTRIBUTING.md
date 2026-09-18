# Contributing

Thanks for considering a contribution to `literature-notes`.

## Repository layout

Each skill lives under `skills/<skill-name>/` and follows the standard
[Agent Skill](https://www.skills.sh/docs) layout:

```
skills/<skill-name>/
├── SKILL.md        # required: YAML frontmatter (name, description, ...) + instructions
├── scripts/        # optional: deterministic helper scripts the skill shells out to
├── assets/         # optional: file templates the skill fills in or copies as-is
└── references/     # optional: docs the skill points to but doesn't load by default
```

Any file a skill scaffolds or fills in as a template — a note/source
template, a starter config file, a block of text injected into another
file — lives under that skill's own `assets/`, not inlined as a string
constant in a script. Scripts read them from disk (e.g. relative to the
script's own file path) instead of embedding their content.

Longer documentation `SKILL.md` links out to instead of inlining — a format
spec, an extended rules doc — lives under that skill's own `references/`.
`SKILL.md` itself stays the short, always-loaded entry point; a `references/`
doc is read only when its link is actually followed.

`SKILL.md` frontmatter must at minimum declare `name` and `description`. Keep
`description` specific about *when* to use the skill — that's what a model
uses to decide whether to invoke it.

## Making a change

1. Fork and clone the repository.
2. Edit the relevant `skills/<skill-name>/SKILL.md` and/or its `scripts/`.
3. If you change a script's behavior, update the `SKILL.md` sections that
   describe it, and manually exercise the skill's workflow end to end.
4. If you add a new skill, add a row for it to the table in `README.md` and
   an entry to `CHANGELOG.md` under `[Unreleased]`.
5. Open a pull request describing the change and why it's needed.

## Conventions

- All documentation and code in this repository — `SKILL.md` files,
  `README.md`, this file, scripts, comments — is written in English.
- Content a skill *generates* inside a user's `.literature-notes/` bundle
  (note/decision bodies, `RESEARCH.md`, `Glossary.md`) is a different matter:
  it's written in **the user's own language**, whatever they're writing to
  the agent in, not hardcoded to English. A directly quoted passage from a
  source stays in that source's original language regardless.
- Scripts are plain Python, run via `uv run` with a `pip install` fallback —
  keep new scripts consistent with that pattern and avoid adding a dependency
  that isn't already vendored via `uv`'s inline script metadata or a `pip
  install` line in the calling `SKILL.md`.

## Reporting issues

Open a GitHub issue describing the problem, the skill involved, and — for a
bug in generated notes or query/validate output — a minimal `.literature-notes/`
fixture that reproduces it.
