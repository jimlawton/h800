#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Parse ARGUS source.
#
# A script that uses the arguscard classes to read ARGUS assembly format source
# and parse instructions.
#
# This is intended for debugging assembler development.


import sys
from optparse import OptionParser

import h800.arguscard
import h800.instructions


def main():
    parser = OptionParser("usage: %prog filename [filename]...")
    parser.add_option('-d', '--debug',
                      dest='debug',
                      action='store_true',
                      default=False,
                      help="Enable debug output.")
    parser.add_option('-v', '--verbose',
                      dest='verbose',
                      action='store_true',
                      default=False,
                      help="Enable verbose output.")
    (opts, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("usage: %prog filename")
        sys.exit(1)

    errcount = 0
    linecount = 0
    instrcount = 0

    symtab = {}
    loc = 0
    coloc = 0

    for filename in args:
        d = h800.arguscard.Deck(file=filename, verbose=opts.verbose)
        for card in d.cards:
            linecount += 1
            if card.instruction:
                instrcount += 1
                if opts.debug:
                    print(card.filename, card.linenum,
                          card.line.replace('\n', ''))
                if card.record["column8"] == '*':
                    if opts.verbose:
                        print("Skipping card with * in column 8:")
                        print(card.filename, card.linenum,
                              card.line.replace('\n', ''))
                    continue
                if card.instruction not in h800.instructions.INSTRUCTIONS:
                    print("*** ERROR: Invalid instruction \"%s\":" %
                          card.instruction)
                    print("File %s, line %d: %s" % (card.filename,
                                                    card.linenum, card.line))
                    errcount += 1
                    continue
                card.parse()

    print("\nSource lines: %d" % linecount)

    if errcount == 1:
        print("1 error encountered.")
    else:
        print("%d errors encountered." % errcount)


if __name__ == '__main__':
    main()
