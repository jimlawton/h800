#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# List symbols in ARGUS assembly source
#
# A script that uses the arguscard classes to read ARGUS assembly format source
# and generate a symbol table listing.
#
# This is intended for debugging assembler development.


import sys
from optparse import OptionParser
import pprint

from h800.symbol_table import buildSymbolTable


def main():
    parser = OptionParser("usage: %prog filename [filename]...")
    parser.add_option('-v', '--verbose',
                      dest='verbose',
                      action='store_true',
                      default=False,
                      help="Enable verbose output.")
    (opts, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("usage: %prog filename")
        sys.exit(1)

    errors = 0

    for filename in args:
        symtab, file_errors = buildSymbolTable(filename, verbose=opts.verbose,
                                               bad=True)
        errors += file_errors

        for seg in sorted(symtab.keys()):
            print("Segment: %s" % seg)
            for subseg in sorted(symtab[seg].keys()):
                print("Subsegment: %s" % subseg)
                for sym in sorted(symtab[seg][subseg].keys()):
                    pprint.pprint("%-9s %s" % (sym, symtab[seg][subseg][sym]))

    if errors > 0:
        print("%d errors found" % errors, file=sys.stderr)


if __name__ == '__main__':
    main()
