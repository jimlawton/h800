#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# List symbols in ARGUS assembly source
# =====================================
#
# A script that uses the arguscard classes to read ARGUS assembly format source
# and generate a symbol table listing.

from __future__ import print_function
import sys
from optparse import OptionParser

import arguscard


def main():
    parser = OptionParser("usage: %prog filename")
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("usage: %prog filename")
        sys.exit(1)

    filename = args[0]

    d = arguscard.Deck(file=filename)

    symtab = {}
    for card in d.cards:
        if card.label:
            strLabel = card.label.strip().replace(' ', '')
            if strLabel not in symtab.keys():
                symtab[strLabel] = {
                    "def-file": card.filename,
                    "def-line": card.linenum,
                    "def-lognum": card.lognum
                }

    import pprint
    pprint.pprint(symtab)



if __name__ == '__main__':
    main()