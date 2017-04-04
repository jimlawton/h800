#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Check opcodes in ARGUS assembly source
#
# A script that uses the arguscard classes to read ARGUS assembly format source
# and check for invalid opcodes.
#
# This is intended for debugging assembler development.

from __future__ import print_function
import sys
from optparse import OptionParser

import h800.arguscard


def main():
    parser = OptionParser("usage: %prog filename")
    parser.add_option('-a', '--all',
                      dest='all',
                      action='store_true',
                      default=False,
                      help="Check for all errors.")
    parser.add_option('-c', '--count',
                      dest='count',
                      action='store_true',
                      default=False,
                      help="Print opcode frequency count.")
    parser.add_option('-i', '--invalid',
                      dest='invalid',
                      action='store_true',
                      default=False,
                      help="Check for invalid opcodes.")
    parser.add_option('-p', '--print-opcodes',
                      dest='printOpcodes',
                      action='store_true',
                      default=False,
                      help="Print all opcodes found.")
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
        opts.invalid = True

    filename = args[0]

    d = h800.arguscard.Deck(file=filename, verbose=opts.verbose)

    errcount = 0

    optab = {}
    for card in d.cards:
        if card.operation:
            if opts.printOpcodes:
                print(card.filename, card.linenum, card.line.replace('\n', ''))
            opcode = card.operation.strip().replace(' ', '')
            if ',' in opcode:
                opcode = opcode.split(',')[0]
            optabEntry = {
                "opcode": opcode,
                "count": 1,
                "file": card.filename,
                "line": card.linenum
            }
            if opcode not in optab.keys():
                optab[opcode] = optabEntry
            else:
                optab[opcode]["count"] += 1

    if opts.count:
        import pprint
        pprint.pprint(optab)


if __name__ == '__main__':
    main()
