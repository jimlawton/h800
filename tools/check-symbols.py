#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Check symbols in ARGUS assembly source
#
# A script that uses the arguscard classes to read ARGUS assembly format source
# and check for multiply- or ill-defined symbols.
#
# This is intended for debugging assembler development.


import sys
from optparse import OptionParser

import h800.arguscard
from h800.symbol_table import buildSymbolTable


def main():
    parser = OptionParser("usage: %prog filename [filename]...")
    parser.add_option('-a', '--all',
                      dest='all',
                      action='store_true',
                      default=False,
                      help="Check for all errors.")
    parser.add_option('-b', '--bad',
                      dest='bad',
                      action='store_true',
                      default=False,
                      help="Check for bad symbol names.")
    parser.add_option('-v', '--verbose',
                      dest='verbose',
                      action='store_true',
                      default=False,
                      help="Enable verbose output.")
    (opts, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("usage: %prog filename")
        sys.exit(1)
    if opts.all:
        opts.bad = True

    toterrs = 0
    for filename in args:
        symtab, errcount = buildSymbolTable(filename, verbose=opts.verbose,
                                            bad=opts.bad)
        print("%s: %d errors encountered." % (filename, errcount))
        toterrs += errcount

    if len(args) > 1:
        print("Total: %d errors encountered." % toterrs)


if __name__ == '__main__':
    main()
