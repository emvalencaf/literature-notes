#!/usr/bin/env python3
"""Check .literature-notes/ for broken tag/source/influence/term references."""
import argparse
import glob
import os
import re
import sys

import yaml

WIKILINK_RE = re.compile(r"\[\[([^\]#]+)(?:#([^\]]+))?\]\]")
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s+", "-", text)


def strip_wikilink(value: str) -> str:
    """"[[id]]" -> "id"; a plain "id" passes through unchanged."""
    if not isinstance(value, str):
        return value
    m = re.fullmatch(r"\[\[([^\]#]+)\]\]", value.strip())
    return m.group(1) if m else value


def load_frontmatter_and_body(path: str) -> tuple[dict, str]:
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if not content.startswith("---"):
        return {}, content
    _, fm, body = content.split("---", 2)
    return yaml.safe_load(fm) or {}, body


def load_tags_vocab(root: str) -> set[str]:
    path = os.path.join(root, "tags.md")
    if not os.path.exists(path):
        return set()
    tags = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("- "):
                tags.add(line[2:].split(" ")[0].strip("`"))
    return tags


def load_glossary_terms(root: str) -> set[str]:
    path = os.path.join(root, "Glossary.md")
    if not os.path.exists(path):
        return set()
    terms = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"#{1,6}\s+(.+)", line.strip())
            if m:
                terms.add(m.group(1).strip())
    return terms


def check_glossary_wikilinks(path: str, body: str, terms: set[str], errors: list[str]) -> None:
    for target, heading in WIKILINK_RE.findall(body):
        if target != "Glossary" or not heading:
            continue
        if terms and heading not in terms:
            errors.append(f"{path}: [[Glossary#{heading}]] has no matching term in Glossary.md")

    term_slugs = {slugify(t) for t in terms}
    for target in MD_LINK_RE.findall(body):
        if "Glossary.md#" not in target:
            continue
        anchor = target.split("Glossary.md#", 1)[1]
        if term_slugs and anchor not in term_slugs:
            errors.append(
                f"{path}: markdown link to Glossary.md#{anchor} has no matching term in Glossary.md"
            )


def check_type(path: str, meta: dict, warnings: list[str]) -> None:
    if not meta.get("type"):
        warnings.append(f"{path}: missing 'type' field")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a literature-notes bundle.")
    parser.add_argument("root", nargs="?", default=".literature-notes")
    args = parser.parse_args()
    root = args.root

    errors = []
    warnings = []
    vocab = load_tags_vocab(root)
    terms = load_glossary_terms(root)

    for name in ("RESEARCH.md", "Glossary.md"):
        if not os.path.exists(os.path.join(root, name)):
            warnings.append(f"{root}/{name} does not exist yet")
        else:
            meta, _ = load_frontmatter_and_body(os.path.join(root, name))
            check_type(os.path.join(root, name), meta, warnings)

    source_ids = set()
    source_meta_by_id = {}
    for path in glob.glob(os.path.join(root, "sources", "*.md")):
        source_id = os.path.splitext(os.path.basename(path))[0]
        source_ids.add(source_id)
        meta, body = load_frontmatter_and_body(path)
        source_meta_by_id[source_id] = (path, meta, body)
        check_type(path, meta, warnings)
        for tag in meta.get("tags") or []:
            if vocab and tag not in vocab:
                errors.append(f"{path}: tag '{tag}' not in tags.md")
        check_glossary_wikilinks(path, body, terms, errors)

    note_meta_by_id = {}
    for path in glob.glob(os.path.join(root, "notes", "*.md")):
        note_id = os.path.splitext(os.path.basename(path))[0]
        meta, body = load_frontmatter_and_body(path)
        note_meta_by_id[note_id] = (path, meta, body)

    note_ids = set(note_meta_by_id)
    for note_id, (path, meta, body) in note_meta_by_id.items():
        check_type(path, meta, warnings)
        for tag in meta.get("tags") or []:
            if vocab and tag not in vocab:
                errors.append(f"{path}: tag '{tag}' not in tags.md")
        source_id = strip_wikilink(meta.get("source_id"))
        if source_id and source_id not in source_ids:
            errors.append(f"{path}: source_id '{source_id}' has no matching sources/{source_id}.md")
        for raw_target in meta.get("influences") or []:
            target = strip_wikilink(raw_target)
            if target not in note_ids:
                errors.append(f"{path}: influences '{target}' does not exist in notes/")
        check_glossary_wikilinks(path, body, terms, errors)

    decision_ids = set()
    for path in glob.glob(os.path.join(root, "decisions", "*.md")):
        decision_id = os.path.splitext(os.path.basename(path))[0]
        decision_ids.add(decision_id)
        meta, body = load_frontmatter_and_body(path)
        check_type(path, meta, warnings)
        for raw_target in meta.get("triggered_by") or []:
            target = strip_wikilink(raw_target)
            if target not in note_ids:
                errors.append(f"{path}: triggered_by '{target}' does not exist in notes/")

    for name in ("RESEARCH.md", "Glossary.md"):
        path = os.path.join(root, name)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            body = f.read()
        for target, _heading in WIKILINK_RE.findall(body):
            if target.startswith("decisions/") and target[len("decisions/"):] not in decision_ids:
                errors.append(f"{path}: [[{target}]] has no matching decisions/{target[len('decisions/'):]}.md")

        for target in MD_LINK_RE.findall(body):
            m = re.search(r"decisions/([^/)]+)\.md", target)
            if m and m.group(1) not in decision_ids:
                errors.append(f"{path}: markdown link to {target} has no matching decisions/{m.group(1)}.md")

    if warnings:
        print(f"{len(warnings)} warning(s):\n")
        for w in warnings:
            print(f"- {w}")
        print()

    if errors:
        print(f"{len(errors)} problem(s) found:\n")
        for e in errors:
            print(f"- {e}")
        sys.exit(1)

    print(
        f"OK: {len(source_ids)} source(s), {len(note_ids)} note(s), "
        f"{len(decision_ids)} decision(s), no broken references."
    )


if __name__ == "__main__":
    main()
