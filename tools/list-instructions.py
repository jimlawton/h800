#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Check opcodes in ARGUS assembly source
#
# A script that uses the arguscard classes to read ARGUS assembly format source
# and list all lines containing the specified OPCODE.
#
# This is intended for debugging assembler development.


from optparse import OptionParser

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
                        print("%-48s %6d %s" % (card.filename, card.linenum,
                                                card.line))
                    continue
                instruction = card.operation.strip().replace(' ', '')
                if ',' in instruction and ',' not in opcode:
                    instruction = instruction.split(',')[0]
                if instruction == opcode or (
                        opcode.endswith(',') and
                        instruction.startswith(opcode)):
                    if opts.details:
                        print("%-48s %6d %s" % (card.filename, card.linenum,
                                                card.line))
                    else:
                        print(card.line)


if __name__ == '__main__':
    main()
