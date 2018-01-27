#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# List symbols in ARGUS assembly source
#
# A script that uses the arguscard classes to read ARGUS assembly format source
# and generate a symbol table listing.
#
# This is intended for debugging assembler development.

from __future__ import print_function
import sys
from optparse import OptionParser

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

    symtab = {}
    for filename in args:
        symtab, file_errors = buildSymbolTable(filename, symtab,
                                               verbose=opts.verbose)
        errors += file_errors

    for sym in sorted(symtab.keys()):
        print(sym)
        for seg in sorted(symtab[sym].keys()):
            print("  Segment: %s" % seg)
            for subseg in sorted(symtab[sym][seg].keys()):
                print("    Subsegment: %s" % subseg)
                for symtype in sorted(symtab[sym][seg][subseg].keys()):
                    symdata = symtab[sym][seg][subseg][symtype]
                    print("        %-9s: %-38s      %s" %
                          ("<%s>" % symtype,
                           "%s:%s" % (symdata["file"].split('.')[0],
                                      symdata["line"]),
                           symdata["card"]))

    if errors > 0:
        print("%d errors found" % errors, file=sys.stderr)


if __name__ == '__main__':
    main()
