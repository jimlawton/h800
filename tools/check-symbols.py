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
            "%s: %d errors encountered building symbol table." % (filename, errcount),
            file=sys.stderr,
        )

    errSyms = checkSymbolTable(
        symtab, verbose=args.verbose, complexOnlyError=args.complex
    )
    toterrs += len(errSyms)
    if len(errSyms) > 0:
        print("", file=sys.stderr)
        print("Undefined symbols:", file=sys.stderr)
        for symbol in errSyms:
            matches = findSymbolDef(symtab, symbol, fuzzy=True)
            # print(matches)
            if matches is None or matches == []:
                print("  %s - No matches!" % symbol, file=sys.stderr)
            else:
                print("  %s - Possible matches: " % symbol + " ".join(matches))
        print("%d errors checking symbol table." % len(errSyms), file=sys.stderr)

    if len(args.filenames) > 1:
        print("Total: %d errors encountered." % toterrs, file=sys.stderr)


if __name__ == "__main__":
    main()
