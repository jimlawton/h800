#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Check opcodes in ARGUS assembly source
#
# A script that uses the arguscard classes to read ARGUS assembly format source
# and list all lines containing the specified OPCODE.
#
# This is intended for debugging assembler development.

from __future__ import print_function
import sys
from optparse import OptionParser
from collections import OrderedDict

import h800.arguscard
import h800.instructions


def main():
    parser = OptionParser("usage: %prog opcode filename [filename]...")
    parser.add_option('-D', '--details',
                      dest='details',
                      action='store_true',
                      default=False,
                      help="Print details (file, line number, etc.).")
    parser.add_option('-v', '--verbose',
                      dest='verbose',
                      action='store_true',
                      default=False,
                      help="Enable verbose output.")
    (opts, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("usage: %prog filename [filename]...")
    opcode = args[0]
    masked = False
    command = opcode
    if ',' in opcode:
        masked = True
        command = opcode.split(',')[0]
    if command not in h800.instructions.INSTRUCTIONS:
        parser.error("ERROR: invalid opcode \"%s\"" % opcode)

    for filename in args[1:]:
        d = h800.arguscard.Deck(file=filename, verbose=opts.verbose)
        for card in d.cards:
            if card.operation:
                if card.record["column8"] == '*':
                    if opts.verbose:
                        print("Skipping card with * in column 8:")
                        print(card.filename, card.linenum, card.line.replace('\n', ''))
                    continue
                instruction = card.operation.strip().replace(' ', '')
                if ',' in instruction and ',' not in opcode:
                    instruction = instruction.split(',')[0]
                if instruction == opcode or (
                        opcode.endswith(',') and instruction.startswith(opcode)):
                    if opts.details:
                        print(card.filename, card.linenum, card.line.replace('\n', ''))
                    else:
                        print(card.line.replace('\n', ''))


if __name__ == '__main__':
    main()