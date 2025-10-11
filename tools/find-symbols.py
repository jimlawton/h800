#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
find-symbols.py

Search for symbol definitions in ARGUS assembly source files.

Supports:
  - Exact matching (default)
  - Prefix matching (--begin)
  - Suffix matching (--end)
  - Fuzzy matching (--fuzzy) using rapidfuzz via symbol_table
  - Optional detailed output of definition locations (--details)

Conflicting option rules (enforced):
  * Only one of --exact, --begin, --end may be used at a time.
  * --fuzzy cannot be combined with any of --exact/--begin/--end.

Exit codes:
  0 - Success (match(es) found or fuzzy suggestions printed)
  1 - Usage / argument error
  2 - No matches found

Usage examples:
  find-symbols.py SYMBOL file1.argus file2.argus
  find-symbols.py --begin PREF file1.argus
  find-symbols.py --end SUFFIX file1.argus
  find-symbols.py --fuzzy SYM file1.argus
  find-symbols.py --fuzzy --details SYM file1.argus other.argus
"""

from __future__ import annotations

import argparse
import sys
from typing import Any, Dict, Iterable

from h800.symbol_table import buildSymbolTable, findSymbolDef


def build_combined_symbol_table(
    filenames: Iterable[str], verbose: bool
) -> Dict[str, Any]:
    """Build a combined symbol table from multiple source files."""
    symtab: Dict[str, Any] = {}
    total_errors = 0
    for filename in filenames:
        symtab, file_errors = buildSymbolTable(filename, symtab, verbose=verbose)
        total_errors += file_errors
        if verbose:
            print(
                f"{filename}: {file_errors} errors encountered building symbol table.",
                file=sys.stderr,
            )
    if verbose and total_errors:
        print(f"Total symbol table build errors: {total_errors}", file=sys.stderr)
    return symtab


def format_symbol_definition(symbol: str, sym_entry: Dict[str, Any]) -> str:
    """
    Produce a human-readable multi-line string describing a symbol's definitions.

    sym_entry structure (from symbol_table):
      sym_entry[segment][subsegment][symtype] = {
          'file': ...,
          'line': ...,
          'lognum': ...,
          'tagtype': ...,
          'card': <Card object>
      }
    """
    lines = [symbol]
    for segment in sorted(sym_entry.keys()):
        lines.append(f"  Segment: {segment}")
        for subsegment in sorted(sym_entry[segment].keys()):
            lines.append(f"    Subsegment: {subsegment}")
            for symtype in sorted(sym_entry[segment][subsegment].keys()):
                data = sym_entry[segment][subsegment][symtype]
                filebase = data["file"].split(".")[0]
                line = data["line"]
                tagtype = data["tagtype"]
                card = data["card"]
                lines.append(
                    f"      <{symtype:7s}> {tagtype or ' '} {filebase}:{line:<5d}  {card.line.strip()}"
                )
    return "\n".join(lines)


def print_symbol_details(symbol: str, symtab: Dict[str, Any]) -> None:
    """Print detailed definition info for one symbol if present."""
    if symbol not in symtab:
        print(f"{symbol} (no exact definition found)", file=sys.stderr)
        return
    print(format_symbol_definition(symbol, symtab[symbol]))


def resolve_and_display(
    symtab: Dict[str, Any],
    symbol: str,
    *,
    begin: bool,
    end: bool,
    fuzzy: bool,
    exact: bool,
    details: bool,
) -> int:
    """
    Resolve symbol(s) based on match mode and print results.

    Returns an exit code (0 success, 2 no matches).
    """
    result = findSymbolDef(
        symtab,
        symbol,
        begin=begin,
        end=end,
        fuzzy=fuzzy,
        symtype=None,
    )

    # Matching mode outputs.
    if begin or end or fuzzy:
        matched_symbols = result or []
        if not matched_symbols:
            print(f"No matches for pattern '{symbol}'", file=sys.stderr)
            return 2
        if details:
            for msym in matched_symbols:
                print_symbol_details(msym, symtab)
                print()
        else:
            for msym in matched_symbols:
                print(msym)
        return 0

    # Exact match path: result is nested dict or None.
    if result is None:
        print(f"Symbol '{symbol}' not found.", file=sys.stderr)
        return 2

    if details:
        print_symbol_details(symbol, symtab)
    else:
        # Raw representation (original behavior printed the entry dict)
        # Provide a concise summary instead.
        print(symbol)
    return 0


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="find-symbols",
        description="Find symbol definition(s) in ARGUS assembly source files.",
    )
    parser.add_argument(
        "symbol",
        help="Symbol name / pattern to search for.",
    )
    parser.add_argument(
        "filenames",
        metavar="filename",
        nargs="+",
        help="ARGUS assembly source file(s).",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-b",
        "--begin",
        action="store_true",
        help="Match symbols that begin with the supplied pattern.",
    )
    group.add_argument(
        "-e",
        "--end",
        action="store_true",
        help="Match symbols that end with the supplied pattern.",
    )
    group.add_argument(
        "-x",
        "--exact",
        action="store_true",
        help="Require exact symbol match (default if no other mode selected).",
    )
    parser.add_argument(
        "-f",
        "--fuzzy",
        action="store_true",
        help="Fuzzy match symbols (cannot combine with --begin/--end/--exact).",
    )
    parser.add_argument(
        "-D",
        "--details",
        action="store_true",
        help="Print detailed definition locations.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output while building symbol table.",
    )
    args = parser.parse_args(list(argv))

    # Conflict: fuzzy cannot be combined with any other match mode.
    if args.fuzzy and (args.begin or args.end or args.exact):
        parser.error("--fuzzy cannot be combined with --begin/--end/--exact.")

    # If no explicit mode flags, default to exact.
    if not (args.begin or args.end or args.fuzzy or args.exact):
        args.exact = True

    return args


def main(argv: Iterable[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)

    symtab = build_combined_symbol_table(args.filenames, verbose=args.verbose)

    exit_code = resolve_and_display(
        symtab,
        args.symbol,
        begin=args.begin,
        end=args.end,
        fuzzy=args.fuzzy,
        exact=args.exact,
        details=args.details,
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
