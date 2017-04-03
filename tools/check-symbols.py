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
    parser = OptionParser("usage: %prog filename")
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("usage: %prog filename")
        sys.exit(1)

    filename = args[0]

    d = h800.arguscard.Deck(file=filename)

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
            if strLabel.upper() != strLabel:
                print("*** ERROR: Symbol %s is ill-formed!" % strLabel)
                print("Current definition: %s" % symtabEntry)
                errcount += 1
                continue
            if strLabel not in symtab.keys():
                symtab[strLabel] = symtabEntry
            else:
                # TODO: check the command code field. Depending on the command
                # code field operation, multiple declarations might be allowed,
                # e.g. RESERVE, EQUALS, ALF, SPEC, CAC, etc all reserve storage,
                # but ASSIGN doesn't.
                print("*** ERROR: Symbol %s is multiply-defined!" % strLabel)
                print("Previous definition: %s" % symtab[strLabel])
                print("Current definition: %s" % symtabEntry)
                errcount += 1

    print("\n%d errors encountered!" % errcount)


if __name__ == '__main__':
    main()
