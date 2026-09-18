# Example bundle: judicial activism at the STF

A worked, self-consistent `.literature-notes/` bundle you can read end to
end or point the skills' scripts at directly — not a live research project,
just a fixture showing what the system produces after a few read →
rescope cycles.

It follows the same scenario as the [main README](../../README.md)'s worked
example (a researcher studying judicial activism at Brazil's Supreme Court,
STF) but carries it one step further: a second source
([[streck-2014]]) whose notes conflict with the initial theoretical
framework, triggering a `/literature-notes-rescope` interview that records a
[decision](.literature-notes/decisions/2026-09-15--incorporate-streck-critique.md)
and updates `RESEARCH.md`/`Glossary.md`.

```
CLAUDE.md           # literature-notes:start/end block (from /setup-literature-notes)
AGENTS.md           # same block
.literature-notes/
├── config.md       # link_style: obsidian
├── tags.md
├── index.md        # 2 reviewed rows, 1 still pending
├── RESEARCH.md
├── Glossary.md      # Judicial Activism, Decisionismo
├── sources/
│   ├── dworkin-1986.md
│   └── streck-2014.md
├── notes/
│   ├── dworkin-1986--p52--regra-vs-principio.md      (interpretive)
│   ├── streck-2014--p89--ativismo-judicial.md        (authorial, draft)
│   └── streck-2014--p112--decisionismo.md            (summary)
└── decisions/
    └── 2026-09-15--incorporate-streck-critique.md
```

Try the scripts against it directly:

```bash
cd examples/dworkin-stf-judicial-activism
python3 ../../skills/literature-notes-validate/scripts/validate.py
# OK: 2 source(s), 3 note(s), 1 decision(s), no broken references.

python3 ../../skills/literature-notes-query/scripts/query.py --tag decisionismo
```

Or open `/literature-notes-query` / `/literature-notes-validate` from inside
this directory in a session to see the skills themselves work against it.
