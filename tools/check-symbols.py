#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Check symbols in ARGUS assembly source
#
# A script that uses the arguscard classes to read ARGUS assembly format source
# and check for multiply- or ill-defined symbols.
#
# This is intended for debugging assembler development.


import argparse
import sys

from h800.symbol_table import buildSymbolTable, checkSymbolTable, findSymbolDef


def main():
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
        help="Report symbols that have only complex assignments.",
    )
    args = parser.parse_args()

    toterrs = 0
    symtab = {}
    for filename in args.filenames:
        symtab, errcount = buildSymbolTable(filename, symtab, verbose=args.verbose)
        toterrs += errcount
        print(
            f"{filename}: {errcount} errors encountered building symbol table.",
            file=sys.stderr,
        )

    err_syms = checkSymbolTable(symtab, verbose=args.verbose, complexOnlyError=args.complex)
    toterrs += len(err_syms)
    if len(err_syms) > 0:
        print("", file=sys.stderr)
        print("Undefined symbols:", file=sys.stderr)
        for symbol in err_syms:
            matches = findSymbolDef(symtab, symbol, fuzzy=True)
            if matches is None or matches == []:
                print(f"  {symbol} - No matches!", file=sys.stderr)
            else:
                print(f"  {symbol + ' '.join(matches)} - Possible matches: ")
        print(f"{len(err_syms)} errors checking symbol table.", file=sys.stderr)

    if len(args.filenames) > 1:
        print(f"Total: {toterrs} errors encountered.", file=sys.stderr)


if __name__ == "__main__":
    main()
