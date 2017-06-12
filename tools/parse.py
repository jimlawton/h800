#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Parse ARGUS source.
#
# A script that uses the arguscard classes to read ARGUS assembly format source
# and parse instructions.
#
# This is intended for debugging assembler development.

from __future__ import print_function
import sys
from optparse import OptionParser
from collections import OrderedDict

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
    instrtab = {}
    for instruction in h800.instructions.INSTRUCTIONS:
        instrtab[instruction] = 0

    for filename in args:
        d = h800.arguscard.Deck(file=filename, verbose=opts.verbose)
        for card in d.cards:
            linecount += 1
            if card.operation:
                instrcount += 1
                if opts.debug:
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
                if instruction not in h800.instructions.INSTRUCTIONS:
                    print("*** ERROR: Invalid instruction \"%s\":" % instruction)
                    print("File %s, line %d: %s" % (card.filename, card.linenum, card.line))
                    errcount += 1

    print("\nSource lines: %d" % linecount)
    print("\nInstruction Frequencies:")
    print("%-8s %6d  %6.2f%%" % ("Total", instrcount, 100.0))
    freqtab = OrderedDict(sorted(instrtab.items(), key=lambda t: t[1], reverse=True))
    for inst in freqtab.keys():
        if freqtab[inst] != 0:
            print("%-8s %6d  %6.2f%%" % (inst, freqtab[inst], 100 * float(freqtab[inst])/float(instrcount)))

    print("\nUnused Instructions:")
    for inst in sorted(instrtab.keys()):
        if instrtab[inst] == 0:
            print(inst)

    if errcount == 1:
        print("1 error encountered.")
    else:
        print("%d errors encountered." % errcount)


if __name__ == '__main__':
    main()
