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
    parser = OptionParser("usage: %prog filename [filename]...")
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

    errcount = 0
    instrtab = {}
    for instruction in h800.instructions.INSTRUCTIONS.keys():
        instrtab[instruction] = 0

    for filename in args:
        d = h800.arguscard.Deck(file=filename, verbose=opts.verbose)
        for card in d.cards:
            if card.operation:
                if opts.printOpcodes:
                    print(card.filename, card.linenum, card.line.replace('\n', ''))
                if card.record["column8"] == '*':
                    if opts.verbose:
                        print("Skipping card with * in column 8:")
                        print(card.filename, card.linenum, card.line.replace('\n', ''))
                    continue
                instruction = card.operation.strip().replace(' ', '')
                if ',' in instruction:
                    instruction = instruction.split(',')[0]
                if instruction not in instrtab.keys():
                    print("*** ERROR: Invalid instruction \"%s\":" % instruction)
                    print("File %s, line %d: %s" % (card.filename, card.linenum, card.line))
                    errcount += 1
                    continue
                instrtab[instruction] += 1
                if opts.invalid:
                    if instruction not in h800.instructions.INSTRUCTIONS.keys():
                        print("*** ERROR: Invalid instruction \"%s\":" % instruction)
                        print("File %s, line %d: %s" % (card.filename, card.linenum, card.line))
                        errcount += 1

    if opts.count:
        import pprint
        pprint.pprint(instrtab)

    if errcount == 1:
        print("1 error encountered.")
    else:
        print("%d errors encountered." % errcount)


if __name__ == '__main__':
    main()
