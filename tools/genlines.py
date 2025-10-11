#!/usr/bin/env python
"""
genlines.py

Generate formatted line (card) numbers for ARGUS/MITIGUS style source files.

ARGUS assembly source lines traditionally begin with a (decimal) card number
field of up to 6 digits (columns 2–7 in some transcriptions). This utility
emits a sequence of such line numbers with configurable:
  - start / end (inclusive)
  - step
  - starting column
  - ending column
  - minimum width (zero‑padded)
The output for each generated number positions the numeric field so that its
rightmost digit sits at `endcol`, preceded by spaces so that the field begins
at `startcol`. The number is zero‑padded to the computed width (default >=4).

Examples:
    # Basic: numbers 20..120 inclusive
    genlines.py 20 120

    # With a step of 5
    genlines.py 20 120 --step 5

    # Use columns 1..6 (startcol=1, endcol=6)
    genlines.py 1 200 --start-col 1 --end-col 6

    # Wider numbering (forces width >=5)
    genlines.py 1 300 --min-width 5

    # Disable zero padding (right aligned, space filled)
    genlines.py 1 15 --no-zero-pad

Exit codes:
    0 - Success
    1 - Argument / validation error

Python 3 only (>=3.13 as per project requirements).
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterable

MAX_WIDTH = 6
DEFAULT_MIN_WIDTH = 4


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="genlines",
        description="Generate ARGUS/MITIGUS format line numbers.",
    )
    parser.add_argument(
        "start",
        type=int,
        help="Starting line number (inclusive).",
    )
    parser.add_argument(
        "end",
        type=int,
        help="Ending line number (inclusive). Must be >= start.",
    )
    parser.add_argument(
        "--step",
        type=int,
        default=1,
        help="Increment between successive numbers (default: 1).",
    )
    parser.add_argument(
        "--start-col",
        type=int,
        default=2,
        help="1-based column at which the number field begins (default: 2).",
    )
    parser.add_argument(
        "--end-col",
        type=int,
        default=7,
        help="1-based column at which the number field ends (default: 7).",
    )
    parser.add_argument(
        "--min-width",
        type=int,
        default=DEFAULT_MIN_WIDTH,
        help=f"Minimum zero-padded field width (default: {DEFAULT_MIN_WIDTH}).",
    )
    parser.add_argument(
        "--no-zero-pad",
        action="store_true",
        help="Use spaces instead of zeros for left padding.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress trailing summary comment line.",
    )
    return parser.parse_args(list(argv))


def validate(args: argparse.Namespace) -> None:
    if args.step <= 0:
        raise ValueError("Step must be > 0.")
    if args.end < args.start:
        raise ValueError("End must be >= start.")
    if args.start_col <= 0 or args.end_col <= 0:
        raise ValueError("Columns must be > 0.")
    if args.end_col < args.start_col:
        raise ValueError("end-col must be >= start-col.")
    max_digits = max(len(str(args.start)), len(str(args.end)))
    if max_digits > MAX_WIDTH:
        raise ValueError(f"Line number digit width exceeds {MAX_WIDTH}.")
    if args.min_width > MAX_WIDTH:
        raise ValueError(f"min-width cannot exceed {MAX_WIDTH}.")
    if args.min_width < 1:
        raise ValueError("min-width must be >= 1.")
    field_span = args.end_col - args.start_col + 1
    if field_span < max(args.min_width, max_digits):
        raise ValueError(
            f"Specified column span ({field_span}) too small for required width "
            f"{max(args.min_width, max_digits)}."
        )


def compute_width(start: int, end: int, min_width: int) -> int:
    width = max(len(str(start)), len(str(end)), min_width)
    return min(width, MAX_WIDTH)


def emit_lines(args: argparse.Namespace) -> int:
    width = compute_width(args.start, args.end, args.min_width)
    fill_char = " " if args.no_zero_pad else "0"
    left_margin_spaces = args.start_col - 1
    total_count = 0

    # Inclusive iteration: range(start, end+step, step) produces an overshoot.
    # Instead, iterate while current <= end.
    current = args.start
    while current <= args.end:
        num_str = f"{current:{fill_char}{width}d}"
        # Space to pad after the number until end_col (inclusive).
        # number ends at column start_col + width - 1
        trailing_spaces = args.end_col - (args.start_col + width - 1)
        if trailing_spaces < 0:
            # Should have been validated out; safeguard.
            print(
                f"Internal error: negative trailing space for number {current}",
                file=sys.stderr,
            )
            return 1
        line = (" " * left_margin_spaces) + num_str + (" " * trailing_spaces)
        print(line)
        total_count += 1
        current += args.step

    if not args.quiet:
        print(
            f"# Generated {total_count} line numbers "
            f"(start={args.start}, end={args.end}, step={args.step}, width={width})"
        )
    return 0


def main(argv: Iterable[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    try:
        args = parse_args(argv)
        validate(args)
        return emit_lines(args)
    except ValueError as ve:
        print(f"Error: {ve}", file=sys.stderr)
        return 1
    except Exception as exc:  # Unexpected
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
