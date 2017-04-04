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
import h800.instructions


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

    instrtab = {}
    for card in d.cards:
        if card.operation:
            if opts.printOpcodes:
                print(card.filename, card.linenum, card.line.replace('\n', ''))
            instruction = card.operation.strip().replace(' ', '')
            if ',' in instruction:
                instruction = instruction.split(',')[0]
            instrtabEntry = {
                "instruction": instruction,
                "count": 1,
                "file": card.filename,
                "line": card.linenum
            }
            if instruction not in instrtab.keys():
                instrtab[instruction] = instrtabEntry
            else:
                instrtab[instruction]["count"] += 1
            if opts.invalid:
                if instruction not in h800.instructions.OPCODES.keys():
                    print("*** ERROR: Invalid instruction %s" % instruction)
                    print(instrtabEntry)
                    errcount += 1

    if opts.count:
        import pprint
        pprint.pprint(instrtab)

    print("%d errors encountered." % errcount)


if __name__ == '__main__':
    main()
