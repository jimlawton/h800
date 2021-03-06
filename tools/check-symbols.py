#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Check symbols in ARGUS assembly source
#
# A script that uses the arguscard classes to read ARGUS assembly format source
# and check for multiply- or ill-defined symbols.
#
# This is intended for debugging assembler development.

from __future__ import print_function
import sys
from optparse import OptionParser

from h800.symbol_table import buildSymbolTable, checkSymbolTable, findSymbolDef


def main():
    parser = OptionParser("usage: %prog filename [filename]...")
    parser.add_option('-v', '--verbose',
                      dest='verbose',
                      action='store_true',
                      default=False,
                      help="Enable verbose output.")
    parser.add_option('-c', '--complex',
                      dest='complex',
                      action='store_true',
                      default=False,
                      help="Print errors for any complex-only definitions.")
    (opts, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("usage: %prog filename")
        sys.exit(1)

    toterrs = 0
    symtab = {}
    for filename in args:
        symtab, errcount = buildSymbolTable(filename, symtab,
                                            verbose=opts.verbose)
        toterrs += errcount
        print("%s: %d errors encountered building symbol table." %
              (filename, errcount), file=sys.stderr)

    errSyms = checkSymbolTable(symtab, verbose=opts.verbose,
                               complexOnlyError=opts.complex)
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
                print("  %s - Possible matches: " % symbol + ' '.join(matches))
        print("%d errors checking symbol table." % len(errSyms),
              file=sys.stderr)

    if len(args) > 1:
        print("Total: %d errors encountered." % toterrs, file=sys.stderr)


if __name__ == '__main__':
    main()
