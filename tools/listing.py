#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Print a simple listing of ARGUS assembly source
#
# A script that uses the arguscard classes to read ARGUS assembly format source
# and print a simple listing output.
#
# This is intended for debugging assembler development.

from __future__ import print_function
import sys
from optparse import OptionParser

import h800.arguscard


def main():
    parser = OptionParser("usage: %prog filename")
    parser.add_option('-v', '--verbose',
                      dest='verbose',
                      action='store_true',
                      default=False,
                      help="Enable verbose output.")
    (opts, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("usage: %prog filename")
        sys.exit(1)

    filename = args[0]
    listfile = '.'.join(filename.split('.')[:-1]) + ".lst"

    d = h800.arguscard.Deck(file=filename, verbose=opts.verbose)

    errcount = 0

    fnamelen = 0
    for card in d.cards:
        if len(card.filename) > fnamelen:
            fnamelen = len(card.filename)

    symtab = {}
    with open(listfile, 'w') as f:
        for card in d.cards:
            line = card.line.replace('\n', '')
            print("%-64s %-06d %s" % (card.filename, card.linenum, line), file=f)

    if opts.verbose:
        print("Wrote listing file to %s" % listfile)


if __name__ == '__main__':
    main()
