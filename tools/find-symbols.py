#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# List symbols in ARGUS assembly source
#
# A script that uses the arguscard classes to read ARGUS assembly format source
# and search for symbol occurrences (definitions, use, or both). Both exact and
# partial matching are supported.
#
# This is intended for debugging assembler development.

from __future__ import print_function
import sys
from optparse import OptionParser

import h800.arguscard
from h800.symbol_table import buildSymbolTable, findSymbolDef


def main():
    parser = OptionParser("usage: %prog [options] symbol filename "
                          "[filename]...")
    parser.add_option('-b', '--begin',
                      dest='begin',
                      action='store_true',
                      default=False,
                      help="Match symbols that begin with the specified "
                      "string.")
    parser.add_option('-D', '--details',
                      dest='details',
                      action='store_true',
                      default=False,
                      help="Print details for matching lines.")
    parser.add_option('-e', '--end',
                      dest='end',
                      action='store_true',
                      default=False,
                      help="Match symbols that end with the specified string.")
    parser.add_option('-f', '--fuzzy',
                      dest='fuzzy',
                      action='store_true',
                      default=False,
                      help="Fuzzy match symbols with the specified string.")
    parser.add_option('-v', '--verbose',
                      dest='verbose',
                      action='store_true',
                      default=False,
                      help="Enable verbose output.")
    parser.add_option('-x', '--exact',
                      dest='exact',
                      action='store_true',
                      default=False,
                      help="Exact matching. Default is partial.")
    (opts, args) = parser.parse_args()
    if (opts.begin and opts.exact) or (opts.end and opts.exact) or \
            (opts.begin and opts.end) or \
            (opts.fuzzy and (opts.begin or opts.end or opts.exact)):
        parser.error("Conflicting options!")
    if len(args) < 2:
        parser.error("usage: %prog [options] symbol filename [filename]...")
    symbol = args[0]

    toterrs = 0
    symtab = {}
    for filename in args[1:]:
        symtab, errcount = buildSymbolTable(filename, symtab,
                                            verbose=opts.verbose)
        toterrs += errcount
        print("%s: %d errors encountered building symbol table." %
              (filename, errcount), file=sys.stderr)

    entry = findSymbolDef(symtab, symbol, begin=opts.begin, end=opts.end,
                          fuzzy=opts.fuzzy)
    if entry:
        print(entry)


if __name__ == '__main__':
    main()
