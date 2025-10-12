#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# check-symbols.py
#
# Validate symbols in ARGUS assembly source files.
# Modernized to use snake_case symbol table APIs and to return an explicit exit code.

import argparse
import sys

from h800.symbol_table import build_symbol_table, check_symbol_table, find_symbol_def


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="check-symbols",
        description="Check symbols in ARGUS assembly source for validity and report undefined or complex-only definitions.",
    )
    parser.add_argument(
        "filenames",
        metavar="filename",
        nargs="+",
        help="ARGUS assembly source file(s) to analyze",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output.",
    )
    parser.add_argument(
        "-c",
        "--complex",
        action="store_true",
        help="Report symbols that have only complex assignments (flag missing simple definitions).",
    )
    args = parser.parse_args()

    total_errors = 0
    symtab: dict = {}
    for filename in args.filenames:
        symtab, errcount = build_symbol_table(filename, symtab, verbose=args.verbose)
        total_errors += errcount
        print(f"{filename}: {errcount} errors encountered building symbol table.", file=sys.stderr)

    err_syms = check_symbol_table(symtab, verbose=args.verbose, complex_only_error=args.complex)
    total_errors += len(err_syms)

    if err_syms:
        print("", file=sys.stderr)
        print("Undefined symbols:", file=sys.stderr)
        for symbol in err_syms:
            matches = find_symbol_def(symtab, symbol, fuzzy=True)
            if not matches:
                print(f"  {symbol} - No matches!", file=sys.stderr)
            else:
                print(f"  {symbol} {' '.join(matches)} - Possible matches:", file=sys.stderr)
        print(f"{len(err_syms)} errors checking symbol table.", file=sys.stderr)

    if len(args.filenames) > 1:
        print(f"Total: {total_errors} errors encountered.", file=sys.stderr)

    # Exit code: 0 if no errors, 1 otherwise.
    return 1 if total_errors > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
