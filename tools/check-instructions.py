#!/usr/bin/env python
"""
check-instructions.py

Validate and analyze instruction (opcode) usage in ARGUS / H-800 / H-1800 assembly
source files.

Features (modern argparse rewrite of legacy optparse script):
  - Detect invalid instructions (mnemonics not in h800.instructions.INSTRUCTIONS).
  - Print every opcode occurrence (--print-opcodes).
  - Frequency analysis of opcode usage (--count) with optional sorting by frequency (--sort).
  - List unused instructions (--unused).
  - Combined convenience flag (--all) that enables invalid checks (legacy behavior preserved).
  - Verbose diagnostics (--verbose).
  - Exit codes suitable for CI scripting.

Usage:
  check-instructions.py file1.argus
  check-instructions.py --invalid file1.argus file2.argus
  check-instructions.py --count --sort file1.argus
  check-instructions.py --print-opcodes file1.argus
  check-instructions.py --unused --count file1.argus
  check-instructions.py --all file1.argus

Exit codes:
  0 - Success (no invalid instructions OR invalid check not requested)
  1 - Invalid instruction(s) encountered (when --invalid or --all specified)
  2 - Usage / argument error
  3 - Other processing error

Python requirement: 3.13+
"""

from __future__ import annotations

import argparse
import sys
from collections import OrderedDict
from collections.abc import Iterable

import h800.arguscard
import h800.instructions


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="check-instructions",
        description="Validate and analyze ARGUS instruction usage in source files.",
    )
    parser.add_argument(
        "filenames",
        metavar="filename",
        nargs="+",
        help="ARGUS assembly source file(s) to process.",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Shorthand: perform invalid instruction checks (same as --invalid).",
    )
    parser.add_argument(
        "-i",
        "--invalid",
        action="store_true",
        help="Check for invalid instructions and report errors.",
    )
    parser.add_argument(
        "-p",
        "--print-opcodes",
        action="store_true",
        help="Print each opcode occurrence (filename, line number, line text).",
    )
    parser.add_argument(
        "-c",
        "--count",
        action="store_true",
        help="Print frequency count of each instruction encountered.",
    )
    parser.add_argument(
        "-s",
        "--sort",
        action="store_true",
        help="Sort frequency output by descending count (use with --count).",
    )
    parser.add_argument(
        "-u",
        "--unused",
        action="store_true",
        help="When combined with --count, only show unused instructions (zero occurrences).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose diagnostic output.",
    )
    return parser.parse_args(list(argv))


def initialize_frequency_table() -> dict[str, int]:
    return dict.fromkeys(h800.instructions.INSTRUCTIONS, 0)


def process_files(
    filenames: list[str],
    opts: argparse.Namespace,
    instrtab: dict[str, int],
) -> int:
    """
    Iterate through all cards in each file, updating frequency table,
    counting invalid instructions (if requested), and optionally printing occurrences.

    Returns number of invalid instruction errors encountered.
    """
    invalid_errors = 0

    for filename in filenames:
        try:
            deck = h800.arguscard.Deck(file=filename, verbose=opts.verbose)
        except Exception as exc:
            print(f"ERROR: Failed to parse '{filename}': {exc}", file=sys.stderr)
            return 3  # treat parse failure as processing error

        for card in deck.cards:
            # Count every source line processed only when we have an instruction, else skip
            if not card.instruction:
                continue

            if opts.print_opcodes:
                print(
                    f"{card.filename} {card.linenum:6d} {card.line.rstrip()}",
                )

            # Skip starred cards in column8 (comments/annotations)
            if card.record.get("column8") == "*":
                if opts.verbose:
                    print(
                        f"[verbose] Skipping card with '*' in column 8: "
                        f"{card.filename}:{card.linenum}",
                        file=sys.stderr,
                    )
                continue

            instr = card.instruction
            if instr not in instrtab:
                # Unknown instruction: treat as warning unless --invalid / --all supplied.
                if opts.invalid or opts.all:
                    print(
                        f"*** ERROR: Invalid instruction '{instr}'\n"
                        f"    File {card.filename}, line {card.linenum}: {card.line.rstrip()}",
                        file=sys.stderr,
                    )
                    invalid_errors += 1
                else:
                    print(
                        f"[warning] Invalid instruction '{instr}' (file {card.filename}, line {card.linenum})",
                        file=sys.stderr,
                    )
                # Do not record frequency for invalid instructions.
                continue

            # Valid instruction; increment count.
            instrtab[instr] += 1

    return invalid_errors


def output_frequencies(
    instrtab: dict[str, int],
    opts: argparse.Namespace,
) -> None:
    """
    Print frequency table.
    If --sort is specified, order by descending frequency; otherwise alphabetically.
    If --unused is specified, only show instructions with zero occurrences.
    """
    total = sum(instrtab.values())

    print("\nInstruction Frequencies:")
    print(f"{'Total':8s} {total:6d}  {100.0:6.2f}%")

    if opts.sort:
        ordered = OrderedDict(sorted(instrtab.items(), key=lambda kv: kv[1], reverse=True))
        iterable = ordered.items()
    else:
        iterable = sorted(instrtab.items())

    for inst, count in iterable:
        if opts.unused and count != 0:
            continue
        percent = (100.0 * count / total) if total else 0.0
        print(f"{inst:8s} {count:6d}  {percent:6.2f}%")


def output_unused(instrtab: dict[str, int]) -> None:
    unused = sorted([inst for inst, count in instrtab.items() if count == 0])
    print("\nUnused Instructions:")
    for inst in unused:
        print(inst)


def main(argv: Iterable[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    opts = parse_args(argv)

    # Legacy behavior: --all implies invalid checking.
    if opts.all:
        opts.invalid = True

    instrtab = initialize_frequency_table()

    invalid_errors = process_files(opts.filenames, opts, instrtab)
    if invalid_errors == 3:  # parse failure sentinel
        return 3

    # Frequency output.
    if opts.count:
        output_frequencies(instrtab, opts)

    # Unused list separate from frequency listing (legacy script printed both).
    if opts.unused and not opts.count:
        output_unused(instrtab)

    # Summary of invalid errors.
    if opts.invalid or opts.all:
        if invalid_errors == 1:
            print("1 invalid instruction encountered.", file=sys.stderr)
        elif invalid_errors > 1:
            print(f"{invalid_errors} invalid instructions encountered.", file=sys.stderr)

    # Exit code logic:
    # - If invalid checks requested (or --all) and errors found -> exit 1
    # - Otherwise always succeed (warnings never force non-zero)
    if (opts.invalid or opts.all) and invalid_errors > 0:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
