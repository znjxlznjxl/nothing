#!/usr/bin/env python3
"""Create and convert Hangul HWP/HWPX documents with python-hwpx 6.11.0."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from hwpx import HwpxDocument

HWP_OLE_SIGNATURE = bytes.fromhex("D0 CF 11 E0 A1 B1 1A E1")
SUPPORTED = {".hwp", ".hwpx"}


def check_file_format(path: Path) -> None:
    """Verify the actual container format, not merely its filename suffix."""
    with path.open("rb") as stream:
        signature = stream.read(8)
    if path.suffix.lower() == ".hwp":
        if signature != HWP_OLE_SIGNATURE:
            raise ValueError(f"Not a genuine OLE-based HWP file: {path}")
    elif path.suffix.lower() == ".hwpx":
        if signature[:4] != b"PK\x03\x04":
            raise ValueError(f"Not a genuine ZIP-based HWPX file: {path}")
    else:
        raise ValueError("Output must end in .hwp or .hwpx")


def write_checked(doc: HwpxDocument, destination: Path, expected_text: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    doc.save_to_path(destination, mode="auto", fallback="error")
    check_file_format(destination)
    roundtrip = HwpxDocument.open(destination)
    if roundtrip.text.plain() != expected_text:
        raise ValueError(f"Text changed on round-trip: {destination}")
    print(f"Saved and verified: {destination} ({destination.stat().st_size:,} bytes)")


def convert(source: Path, destination: Path) -> None:
    if source.suffix.lower() not in SUPPORTED:
        raise ValueError("Input must be .hwp or .hwpx")
    if destination.suffix.lower() not in SUPPORTED:
        raise ValueError("Output must be .hwp or .hwpx")
    if source.resolve() == destination.resolve():
        raise ValueError("Input and output must differ")
    doc = HwpxDocument.open(source)
    write_checked(doc, destination, doc.text.plain())


def create(text_file: Path, destination: Path) -> None:
    if destination.suffix.lower() not in SUPPORTED:
        raise ValueError("Output must be .hwp or .hwpx")
    text = text_file.read_text(encoding="utf-8-sig")
    doc = HwpxDocument.new()
    # Each line becomes a separate paragraph.
    for line in text.split("\n"):
        doc.add_paragraph(line.rstrip("\r"))
    write_checked(doc, destination, doc.text.plain())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    p_convert = subs.add_parser("convert", help="Convert HWP <-> HWPX")
    p_convert.add_argument("input", type=Path)
    p_convert.add_argument("output", type=Path)
    p_create = subs.add_parser("create", help="Create HWP or HWPX from UTF-8 text")
    p_create.add_argument("input", type=Path)
    p_create.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "convert":
            convert(args.input, args.output)
        else:
            create(args.input, args.output)
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
