#!/usr/bin/env python3
"""Extract per-page text from a PDF, optionally restricted to a page range."""
import argparse
import sys

from pypdf import PdfReader


def parse_range(spec: str | None, num_pages: int) -> range:
    if not spec:
        return range(1, num_pages + 1)
    start_s, _, end_s = spec.partition("-")
    start = int(start_s)
    end = int(end_s) if end_s else start
    return range(start, end + 1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract text from a PDF page range.")
    parser.add_argument("pdf_path")
    parser.add_argument("--pages", help="1-based inclusive page range, e.g. 10-25")
    args = parser.parse_args()

    reader = PdfReader(args.pdf_path)
    num_pages = len(reader.pages)

    for page_num in parse_range(args.pages, num_pages):
        if page_num < 1 or page_num > num_pages:
            print(f"warning: page {page_num} out of range (1-{num_pages})", file=sys.stderr)
            continue
        text = reader.pages[page_num - 1].extract_text() or ""
        print(f"\n=== PAGE {page_num} ===\n")
        print(text)


if __name__ == "__main__":
    main()
