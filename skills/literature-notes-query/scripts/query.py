#!/usr/bin/env python3
"""Query the .literature-notes/ bundle by structured filters and/or free text."""
import argparse
import glob
import os
import re

import yaml

ROOT = ".literature-notes"


def strip_wikilink(value):
    """"[[id]]" -> "id"; a plain "id" passes through unchanged."""
    if not isinstance(value, str):
        return value
    m = re.fullmatch(r"\[\[([^\]#]+)\]\]", value.strip())
    return m.group(1) if m else value


def load_doc(path: str):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if not content.startswith("---"):
        return {}, content
    _, fm, body = content.split("---", 2)
    meta = yaml.safe_load(fm) or {}
    return meta, body.strip()


def iter_docs(kind: str):
    for path in sorted(glob.glob(os.path.join(ROOT, kind, "*.md"))):
        meta, body = load_doc(path)
        yield path, meta, body


def matches(meta: dict, body: str, args) -> bool:
    if args.tag and args.tag not in (meta.get("tags") or []):
        return False
    if args.source_id and strip_wikilink(meta.get("source_id")) != args.source_id:
        return False
    if args.note_kind and meta.get("note_kind") != args.note_kind:
        return False
    if args.page:
        pages = str(meta.get("page", meta.get("pages", "")))
        if args.page not in pages.split("-"):
            return False
    if args.influences and args.influences not in (
        strip_wikilink(t) for t in (meta.get("influences") or [])
    ):
        return False
    if args.text:
        haystack = f"{body} {meta}".lower()
        if args.text.lower() not in haystack:
            return False
    if args.verified is not None:
        is_verified = bool(meta.get("verified"))
        if is_verified != (args.verified == "true"):
            return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Query literature-notes.")
    parser.add_argument("--scope", choices=["notes", "sources", "both"], default="both")
    parser.add_argument("--tag")
    parser.add_argument("--source-id")
    parser.add_argument("--note-kind", choices=["authorial", "interpretive", "summary"])
    parser.add_argument("--page")
    parser.add_argument("--influences", help="note-id this note influences")
    parser.add_argument("--influenced-by", help="note-id that influences this note")
    parser.add_argument("--text", help="free-text search across body and metadata")
    parser.add_argument(
        "--verified",
        choices=["true", "false"],
        help="filter by whether a verified{} block is present in frontmatter",
    )
    parser.add_argument("--output", help="write results to this markdown file instead of stdout")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help=(
            "max number of results to return. Default: 5 when printing to "
            "stdout, unlimited when --output is set. Pass 0 for unlimited."
        ),
    )
    args = parser.parse_args()

    kinds = ["notes", "sources"] if args.scope == "both" else [args.scope]

    results = []
    for kind in kinds:
        for path, meta, body in iter_docs(kind):
            if args.influenced_by and args.influenced_by not in (
                strip_wikilink(t) for t in (meta.get("influences") or [])
            ):
                continue
            if not matches(meta, body, args):
                continue
            results.append((kind, path, meta, body))

    total = len(results)
    limit = args.limit
    if limit is None:
        limit = 0 if args.output else 5
    truncated = limit and total > limit
    if truncated:
        results = results[:limit]

    lines = []
    for kind, path, meta, body in results:
        lines.append(f"## {path}")
        if kind == "notes":
            lines.append(
                f"- source: {meta.get('source_id')}, page(s): "
                f"{meta.get('page', meta.get('pages'))}, kind: {meta.get('note_kind')}"
            )
        else:
            lines.append(f"- {meta.get('author', '')} ({meta.get('year', '')}) — {meta.get('title', '')}")
        lines.append(f"- tags: {', '.join(meta.get('tags') or [])}")
        lines.append("")
        lines.append(body)
        lines.append("")

    output_text = "\n".join(lines) if results else "No matches."
    if truncated:
        output_text += (
            f"\n\n_Showing {limit} of {total} match(es). Re-run with "
            f"`--limit {total}` (or a higher number) to see the rest if "
            "this isn't conclusive._"
        )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_text + "\n")
        print(f"Wrote {len(results)} of {total} result(s) to {args.output}")
    else:
        print(output_text)


if __name__ == "__main__":
    main()
