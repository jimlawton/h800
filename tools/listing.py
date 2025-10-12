#!/usr/bin/env python
"""
listing.py

Generate plain-text listing (.lst) files for one or more ARGUS / H-800 / H-1800
assembly source files. Each output line contains:

    <source-filename> <zero-padded-line-number> <raw-source-line>

Behavior mirrors earlier legacy script but is updated for modern Python (3.13+)
and exposes a richer CLI (argparse). The input files are parsed with the
`h800.arguscard.Deck` class so line metadata comes from card objects rather than
raw file iteration.

Features:
  - Multiple input source files.
  - Optional output directory.
  - Optional custom output file suffix (default ".lst").
  - Choose to write a single combined listing to stdout instead of per-file
    outputs.
  - Skip cards whose column 8 contains '*' (treat as comments/annotations) unless
    --include-star is specified.
  - Verbose mode for progress details.
  - Quiet mode suppresses non-error informational messages.
  - Detect and warn if an output file would overwrite an existing file (unless
    --force specified).
  - Optional truncation of overly long source lines to a maximum width (without
    modifying the underlying card data).

Exit codes:
  0 - Success
  1 - Argument or processing error

Examples:
  listing.py source1.argus
  listing.py -v source1.argus source2.argus
  listing.py --output-dir build/listings source1.argus
  listing.py --stdout source1.argus source2.argus
  listing.py --suffix .listing --force source1.argus
  listing.py --include-star source1.argus
  listing.py --max-width 100 source1.argus

Python requirement: 3.13+ (no symbol table usage; no snake_case adaptation needed).
"""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Iterable

import h800.arguscard  # Uses Deck only; no symbol table functions needed (snake_case migration not required here).

DEFAULT_SUFFIX = ".lst"


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="listing",
        description="Generate listing files for ARGUS assembly source.",
    )
    parser.add_argument(
        "filenames",
        metavar="filename",
        nargs="+",
        help="ARGUS assembly source file(s) to process.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        metavar="DIR",
        help="Directory to write listing files (created if missing). Default: same directory as each source file.",
    )
    parser.add_argument(
        "-s",
        "--suffix",
        default=DEFAULT_SUFFIX,
        help=f"Suffix for listing files (default: '{DEFAULT_SUFFIX}').",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Write a combined listing for all files to stdout (no per-file outputs).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose progress output.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress non-error informational messages (overrides verbose).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing listing files without prompting.",
    )
    parser.add_argument(
        "--include-star",
        action="store_true",
        help="Include cards whose column 8 contains '*' (normally skipped).",
    )
    parser.add_argument(
        "--max-width",
        type=int,
        metavar="N",
        help="Truncate source line content to at most N characters (excluding filename & line number).",
    )
    return parser.parse_args(list(argv))


def ensure_output_dir(path: str | None, verbose: bool, quiet: bool) -> None:
    if not path:
        return
    if not os.path.exists(path):
        if verbose and not quiet:
            print(f"[listing] Creating output directory: {path}", file=sys.stderr)
        try:
            os.makedirs(path, exist_ok=True)
        except OSError as exc:
            print(
                f"ERROR: Unable to create output directory '{path}': {exc}",
                file=sys.stderr,
            )
            raise SystemExit(1) from exc
    elif not os.path.isdir(path):
        print(
            f"ERROR: Output path '{path}' exists and is not a directory.",
            file=sys.stderr,
        )
        raise SystemExit(1)


def listing_filename(src: str, suffix: str, outdir: str | None) -> str:
    base = os.path.basename(src)
    stem, _sep, _ext = base.partition(".")
    # If no dot present, stem == base; that's fine.
    name = stem + suffix
    if outdir:
        return os.path.join(outdir, name)
    return os.path.join(os.path.dirname(src), name)


def write_listing_file(
    source_filename: str,
    cards: list,
    outfile: str,
    include_star: bool,
    max_width: int | None,
    verbose: bool,
    quiet: bool,
    force: bool,
) -> None:
    if os.path.exists(outfile) and not force:
        print(
            f"ERROR: Output file '{outfile}' exists (use --force to overwrite).",
            file=sys.stderr,
        )
        raise SystemExit(1)

    # Determine maximum filename display width (cap at 64 for legacy formatting).
    max_name_len = max((len(card.filename) for card in cards), default=len(source_filename))
    max_name_len = min(max_name_len, 64)

    n_written = 0
    try:
        with open(outfile, "w", encoding="utf-8") as f:
            for card in cards:
                if not include_star and card.record.get("column8") == "*":
                    continue
                raw_line = card.line.rstrip("\n")
                if max_width is not None and max_width >= 0:
                    if len(raw_line) > max_width:
                        raw_line = raw_line[: max_width - 1] + "…"
                # Format line number zero-padded to 6 digits (legacy style).
                ln = f"{card.linenum:06d}"
                # %-<width>s formatting for file name, then space, line number, space, text.
                f.write(f"{card.filename:<{max_name_len}} {ln} {raw_line}\n")
                n_written += 1
    except OSError as exc:
        print(f"ERROR: Unable to write listing file '{outfile}': {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    if verbose and not quiet:
        print(
            f"[listing] Wrote {n_written} line(s) to {outfile} (source: {source_filename})",
            file=sys.stderr,
        )


def combined_listing_to_stdout(
    all_cards: list,
    include_star: bool,
    max_width: int | None,
    verbose: bool,
    quiet: bool,
) -> None:
    # Similar formatting, dynamic width per filename capped at 64.
    max_name_len = min(max((len(card.filename) for card in all_cards), default=0), 64)
    n_written = 0
    for card in all_cards:
        if not include_star and card.record.get("column8") == "*":
            continue
        raw_line = card.line.rstrip("\n")
        if max_width is not None and max_width >= 0:
            if len(raw_line) > max_width:
                raw_line = raw_line[: max_width - 1] + "…"
        ln = f"{card.linenum:06d}"
        print(f"{card.filename:<{max_name_len}} {ln} {raw_line}")
        n_written += 1
    if verbose and not quiet:
        print(f"[listing] Wrote {n_written} line(s) to stdout.", file=sys.stderr)


def load_deck(filename: str, verbose: bool, quiet: bool):
    if not os.path.exists(filename):
        print(f"ERROR: Source file '{filename}' does not exist.", file=sys.stderr)
        raise SystemExit(1)
    try:
        deck = h800.arguscard.Deck(file=filename, verbose=verbose and not quiet)
    except Exception as exc:
        print(f"ERROR: Failed to parse '{filename}': {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    return deck


def main(argv: Iterable[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)

    # Validate suffix.
    if not args.suffix.startswith("."):
        print("ERROR: Listing file suffix must begin with a '.'", file=sys.stderr)
        return 1

    ensure_output_dir(args.output_dir, args.verbose, args.quiet)

    all_cards: list = []
    for src in args.filenames:
        deck = load_deck(src, args.verbose, args.quiet)
        if args.stdout:
            all_cards.extend(deck.cards)
        else:
            outpath = listing_filename(src, args.suffix, args.output_dir)
            write_listing_file(
                source_filename=src,
                cards=deck.cards,
                outfile=outpath,
                include_star=args.include_star,
                max_width=args.max_width,
                verbose=args.verbose,
                quiet=args.quiet,
                force=args.force,
            )

    if args.stdout:
        combined_listing_to_stdout(
            all_cards,
            include_star=args.include_star,
            max_width=args.max_width,
            verbose=args.verbose,
            quiet=args.quiet,
        )

    if args.verbose and not args.quiet and not args.stdout:
        print("[listing] Completed.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
