#!/usr/bin/env python
"""
parse.py

Parse ARGUS assembly source files (H-800/H-1800) and perform basic validation:
  - Build a combined symbol table across all input files.
  - Iterate over all cards, counting total source lines and instruction lines.
  - Validate instruction mnemonics against h800.instructions.INSTRUCTIONS.
  - Optionally emit per-line debug output.
  - Report summary statistics and error counts.

Python 3.13+ only; legacy Python 2 compatibility has been removed.

Exit codes:
  0 - Success (no invalid instructions)
  1 - Errors encountered (invalid instructions or symbol table build errors)
  2 - Usage / argument error

Examples:
  parse.py file1.argus
  parse.py -v -d file1.argus file2.argus
  parse.py --strict file1.argus
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterable

import h800.arguscard
from h800.opcodes import INSTRUCTIONS
from h800.symbol_table import build_symbol_table


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="parse",
        description="Parse ARGUS assembly source files and validate instructions.",
    )
    parser.add_argument(
        "filenames",
        metavar="filename",
        nargs="+",
        help="ARGUS assembly source file(s) to parse",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output (extra status).",
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Print each parsed instruction line."
    )
    parser.add_argument(
        "-s",
        "--strict",
        action="store_true",
        help="Return a non-zero exit code if any invalid instructions are found.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress normal summary output (only errors and final counts).",
    )
    return parser.parse_args(list(argv))


class ParseStats:
    def __init__(self) -> None:
        self.source_lines: int = 0
        self.instruction_lines: int = 0
        self.invalid_instructions: int = 0
        self.symbol_errors: int = 0

    @property
    def total_errors(self) -> int:
        return self.invalid_instructions + self.symbol_errors


def build_symbols(filenames: list[str], verbose: bool) -> int:
    """
    Build symbol table across all files.
    Returns total number of errors encountered while building.
    """
    symtab = {}
    total_errors = 0
    for filename in filenames:
        symtab, errcount = build_symbol_table(filename, symtab, verbose=verbose)
        total_errors += errcount
        if verbose:
            print(
                f"{filename}: {errcount} errors encountered building symbol table.",
                file=sys.stderr,
            )
    return total_errors


def process_files(filenames: list[str], stats: ParseStats, args: argparse.Namespace) -> None:
    """
    Iterate through cards in each file, updating stats and performing validation.
    """
    for filename in filenames:
        deck = h800.arguscard.Deck(file=filename, verbose=args.verbose)
        for card in deck.cards:
            stats.source_lines += 1

            if not card.instruction:
                continue

            stats.instruction_lines += 1

            # Debug output before any filtering.
            if args.debug:
                print(
                    f"{card.filename}:{card.linenum:06d} {card.line.rstrip()}",
                )

            # Skip cards explicitly marked with '*' in column 8 (comment / annotation).
            if card.record.get("column8") == "*":
                if args.verbose and args.debug:
                    print(
                        f"Skipping card with '*' in column 8: {card.filename}:{card.linenum}",
                        file=sys.stderr,
                    )
                continue

            # Instruction validation.
            instruction = card.instruction
            if instruction not in INSTRUCTIONS:
                stats.invalid_instructions += 1
                print(
                    f"*** ERROR: Invalid instruction '{instruction}'\n"
                    f"    File {card.filename}, line {card.linenum}: {card.line.rstrip()}",
                    file=sys.stderr,
                )
                continue

            # Perform the card-level parse (may populate internal fields).
            try:
                card.parse()
            except Exception as exc:  # Broad catch; parsing is experimental.
                stats.invalid_instructions += 1
                print(
                    f"*** ERROR: Exception parsing instruction '{instruction}': {exc}\n"
                    f"    File {card.filename}, line {card.linenum}: {card.line.rstrip()}",
                    file=sys.stderr,
                )


def print_summary(stats: ParseStats, args: argparse.Namespace) -> None:
    if args.quiet:
        return

    print()
    print(f"Source lines:      {stats.source_lines}")
    print(f"Instruction lines: {stats.instruction_lines}")
    print(f"Invalid instructions: {stats.invalid_instructions}")
    print(f"Symbol table errors:  {stats.symbol_errors}")
    print(f"Total errors:         {stats.total_errors}")

    if stats.invalid_instructions == 1:
        print("1 invalid instruction encountered.")
    elif stats.invalid_instructions > 1:
        print(f"{stats.invalid_instructions} invalid instructions encountered.")

    if stats.symbol_errors == 1:
        print("1 symbol table error encountered.")
    elif stats.symbol_errors > 1:
        print(f"{stats.symbol_errors} symbol table errors encountered.")


def main(argv: Iterable[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)

    stats = ParseStats()

    # Build symbol table first (may surface symbol definition issues).
    stats.symbol_errors = build_symbols(args.filenames, verbose=args.verbose)

    # Parse and validate instructions.
    process_files(args.filenames, stats, args)

    # Output summary.
    print_summary(stats, args)

    # Determine exit code.
    if args.strict and stats.total_errors > 0:
        return 1
    if stats.invalid_instructions > 0 or stats.symbol_errors > 0:
        # Non-strict mode: still indicate issues with non-zero exit.
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
