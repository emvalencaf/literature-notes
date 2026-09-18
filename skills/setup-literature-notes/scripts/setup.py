#!/usr/bin/env python3
"""Idempotently scaffold .literature-notes/ and document the workflow."""
import argparse
import os

ROOT = ".literature-notes"
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")


def read_asset(name: str) -> str:
    with open(os.path.join(ASSETS, name), encoding="utf-8") as f:
        return f.read()


BLOCK_START = "<!-- literature-notes:start -->"
BLOCK_END = "<!-- literature-notes:end -->"


def build_block() -> str:
    body = read_asset("claude-md-block.md").rstrip("\n")
    return f"{BLOCK_START}\n{body}\n{BLOCK_END}"


def ensure_scaffold(link_style: str) -> list[str]:
    created = []
    for sub in ("sources", "notes"):
        path = os.path.join(ROOT, sub)
        if not os.path.isdir(path):
            os.makedirs(path)
            created.append(path)
    tags_path = os.path.join(ROOT, "tags.md")
    if not os.path.exists(tags_path):
        with open(tags_path, "w", encoding="utf-8") as f:
            f.write(read_asset("tags.md"))
        created.append(tags_path)
    index_path = os.path.join(ROOT, "index.md")
    if not os.path.exists(index_path):
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(read_asset("index.md"))
        created.append(index_path)
    config_path = os.path.join(ROOT, "config.md")
    if not os.path.exists(config_path):
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(read_asset("config.md").format(link_style=link_style))
        created.append(config_path)
    return created


def upsert_block(doc_path: str) -> str:
    block = build_block()

    if not os.path.exists(doc_path):
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(block + "\n")
        return "created"

    with open(doc_path, encoding="utf-8") as f:
        content = f.read()

    if BLOCK_START in content and BLOCK_END in content:
        start = content.index(BLOCK_START)
        end = content.index(BLOCK_END) + len(BLOCK_END)
        if content[start:end] == block:
            return "unchanged"
        content = content[:start] + block + content[end:]
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(content)
        return "updated"

    with open(doc_path, "a", encoding="utf-8") as f:
        if content and not content.endswith("\n"):
            f.write("\n")
        f.write("\n" + block + "\n")
    return "appended"


def main() -> None:
    parser = argparse.ArgumentParser(description="Set up a literature-notes bundle.")
    parser.add_argument(
        "--link-style",
        choices=["obsidian", "markdown"],
        default="obsidian",
        help="cross-reference style for a first-time config.md; ignored if config.md already exists",
    )
    args = parser.parse_args()

    created = ensure_scaffold(args.link_style)
    for path in created:
        print(f"created {path}")
    if not created:
        print(".literature-notes/ scaffold already present")

    for doc in ("CLAUDE.md", "AGENTS.md"):
        status = upsert_block(doc)
        print(f"{doc}: {status}")


if __name__ == "__main__":
    main()
