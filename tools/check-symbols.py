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

import h800.arguscard


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
    parser.add_option('-m', '--multiple',
                      dest='multiple',
                      action='store_true',
                      default=False,
                      help="Check for multiply-defined symbols.")
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
        opts.bad = opts.multiple = True

    toterrs = 0
    for filename in args:
        d = h800.arguscard.Deck(file=filename, verbose=opts.verbose)
        errcount = 0
        symtab = {}
        for card in d.cards:
            if card.label:
                strLabel = card.label.strip().replace(' ', '')
                symtabEntry = {
                    "def-file": card.filename,
                    "def-line": card.linenum,
                    "def-lognum": card.lognum
                }
                if opts.bad and strLabel.upper() != strLabel:
                    print("*** ERROR: Symbol %s is ill-formed!" % strLabel)
                    print("Current definition: %s" % symtabEntry)
                    errcount += 1
                    continue
                if strLabel not in symtab.keys():
                    symtab[strLabel] = symtabEntry
                else:
                    if opts.multiple:
                        # TODO: check the command code field. Depending on the
                        # command code field operation, multiple declarations
                        # might be allowed, e.g. RESERVE, EQUALS, ALF, SPEC,
                        # CAC, etc all reserve storage, but ASSIGN doesn't.
                        print("*** ERROR: Symbol %s is multiply-defined!" %
                              strLabel)
                        print("Previous definition: %s" % symtab[strLabel])
                        print("Current definition: %s" % symtabEntry)
                        errcount += 1
        print("%s: %d errors encountered." % (filename, errcount))
        toterrs += errcount

    if len(args) > 1:
        print("Total: %d errors encountered." % toterrs)


if __name__ == '__main__':
    main()
