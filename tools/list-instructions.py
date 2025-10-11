#!/usr/bin/env python
"""
list-instructions.py

List lines containing a specified ARGUS instruction (opcode) from one or more
ARGUS/H-800/H-1800 assembly source files.

Features:
  - Exact opcode matching.
  - Masked opcode/prefix matching (use a trailing comma, e.g. "BA," to match all
    masked forms beginning with "BA,").
  - Optional detailed output with filename and line numbers.
  - Skips cards whose column 8 contains '*' (treated as comments/annotations).
  - Verbose mode for diagnostic output.
  - Clear exit codes for scripting.

Usage:
    list-instructions.py OPCODE file1.argus [file2.argus ...]
    list-instructions.py -D BA file1.argus
    list-instructions.py -v BA, file1.argus

Match semantics:
  - Plain opcode (e.g. "BA") matches exactly that mnemonic (after stripping
    internal spaces).
  - Opcode with a trailing comma (e.g. "BA,") is treated as a prefix and will
    match any instruction whose (stripped) text starts with that prefix.
  - If a card's operation contains a comma and the user-supplied opcode does NOT
    contain a comma, only the part before the first comma is compared (legacy behavior).

Exit codes:
  0 - Success (at least one match or no matches but valid execution)
  1 - Invalid user input (opcode not recognized, file missing, parse error)

Python requirement: 3.13+
"""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Iterable

import h800.arguscard
import h800.instructions


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="list-instructions",
        description="List lines containing a specified ARGUS instruction (opcode).",
    )
    parser.add_argument(
        "opcode",
        help=(
            "Opcode to search for. Trailing comma enables prefix/masked matching "
            "(e.g. 'BA,' matches all masked BA variants)."
        ),
    )
    parser.add_argument(
        "filenames",
        metavar="filename",
        nargs="+",
        help="ARGUS assembly source file(s) to search.",
    )
    parser.add_argument(
        "-D",
        "--details",
        action="store_true",
        help="Include filename and line number with each match.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output (diagnostics, skipped cards).",
    )
    return parser.parse_args(list(argv))


def normalize_opcode(op: str) -> str:
    """Remove interior spaces and strip surrounding whitespace."""
    return op.strip().replace(" ", "")


def is_valid_base_opcode(opcode: str) -> bool:
    """
    Validate the base part of an opcode (before any comma) against known instructions.
    A trailing comma indicates prefix/masked matching and the base (minus comma) is validated.
    """
    base = opcode[:-1] if opcode.endswith(",") else opcode
    base = normalize_opcode(base)
    return base in h800.instructions.INSTRUCTIONS


def card_operation_for_matching(raw: str, user_has_comma: bool) -> str:
    """
    Given a card's raw operation field, produce the comparable instruction token:
      - Strip spaces.
      - If card includes a comma but user-supplied opcode does not, compare only the part before comma.
    """
    op = normalize_opcode(raw)
    if "," in op and not user_has_comma:
        return op.split(",", 1)[0]
    return op


def opcode_matches(requested: str, candidate: str) -> bool:
    """
    Determine if the candidate operation matches the requested opcode.
    If requested ends with a comma, treat as prefix match.
    Otherwise, require exact match.
    """
    if requested.endswith(","):
        # Prefix match (requested already normalized).
        return candidate.startswith(requested)
    return candidate == requested


def process_file(
    filename: str,
    requested_opcode: str,
    details: bool,
    verbose: bool,
    matches: list[str],
) -> None:
    """Process a single ARGUS source file, appending formatted matches to matches list."""
    deck = h800.arguscard.Deck(file=filename, verbose=verbose)
    for card in deck.cards:
        if not card.operation:
            continue

        # Skip cards with '*' in column 8 (comment / annotation).
        if card.record.get("column8") == "*":
            if verbose:
                print(
                    f"[verbose] Skipping card with '*' in column 8: {card.filename}:{card.linenum}",
                    file=sys.stderr,
                )
            continue

        # Normalize both user opcode and card operation.
        user_has_comma = requested_opcode.endswith(",")
        card_op = card_operation_for_matching(card.operation, user_has_comma)
        # Reconstruct masked match scenario: If user requested prefix with comma, candidate must
        # be compared in its original normalized form (including commas) for prefix semantics.
        if user_has_comma:
            candidate = normalize_opcode(card.operation)
        else:
            candidate = card_op

        if opcode_matches(requested_opcode, candidate):
            if details:
                matches.append(
                    f"{card.filename:<48s} {card.linenum:6d} {card.line.rstrip()}"
                )
            else:
                matches.append(card.line.rstrip())


def main(argv: Iterable[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)

    requested = normalize_opcode(args.opcode)

    # Validate opcode base part.
    if not is_valid_base_opcode(requested):
        print(f"ERROR: invalid opcode '{args.opcode}'", file=sys.stderr)
        return 1

    # Validate files exist.
    for fname in args.filenames:
        if not os.path.exists(fname):
            print(f"ERROR: file not found '{fname}'", file=sys.stderr)
            return 1

    matches: list[str] = []
    for fname in args.filenames:
        try:
            process_file(
                fname,
                requested,
                details=args.details,
                verbose=args.verbose,
                matches=matches,
            )
        except Exception as exc:
            print(f"ERROR: Exception processing '{fname}': {exc}", file=sys.stderr)
            return 1

    # Output matches.
    for m in matches:
        print(m)

    if args.verbose:
        print(
            f"[verbose] {len(matches)} match(es) for opcode '{args.opcode}' across {len(args.filenames)} file(s).",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
