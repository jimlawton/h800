#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# List symbols in ARGUS assembly source
#
# A script that uses the arguscard classes to read ARGUS assembly format source
# and search for symbol occurrences (definitions, use, or both). Both exact and
# partial matching are supported.
#
# This is intended for debugging assembler development.

from __future__ import print_function
import sys
from optparse import OptionParser

import h800.arguscard
from h800.symbol_table import buildSymbolTable, findSymbolDef


def main():
    parser = OptionParser("usage: %prog [options] symbol filename "
                          "[filename]...")
    parser.add_option('-b', '--begin',
                      dest='begin',
                      action='store_true',
                      default=False,
                      help="Match symbols that begin with the specified "
                      "string.")
    parser.add_option('-D', '--details',
                      dest='details',
                      action='store_true',
                      default=False,
                      help="Print details for matching lines.")
    parser.add_option('-e', '--end',
                      dest='end',
                      action='store_true',
                      default=False,
                      help="Match symbols that end with the specified string.")
    parser.add_option('-v', '--verbose',
                      dest='verbose',
                      action='store_true',
                      default=False,
                      help="Enable verbose output.")
    parser.add_option('-x', '--exact',
                      dest='exact',
                      action='store_true',
                      default=False,
                      help="Exact matching. Default is partial.")
    (opts, args) = parser.parse_args()
    if opts.begin and opts.exact or opts.end and opts.exact or opts.begin and \
            opts.end:
        parser.error("Conflicting options!")
    if len(args) < 2:
        parser.error("usage: %prog [options] symbol filename [filename]...")
    symbol = args[0]

    for filename in args[1:]:
        d = h800.arguscard.Deck(file=filename, verbose=opts.verbose)
        for card in d.cards:
            if card.label is None:
                continue
            strLabel = card.label.strip().replace(' ', '')
            match = False
            if strLabel == symbol:
                match = True
            else:
                if opts.exact:
                    continue
                if opts.begin and strLabel.startswith(symbol) or \
                        opts.end and strLabel.endswith(symbol):
                    match = True
                elif not opts.begin and not opts.end and symbol in strLabel:
                    match = True
                else:
                    continue
                if match:
                    if opts.details:
                        print(card.filename, card.linenum, card.line)
                    else:
                        print(card.line)


if __name__ == '__main__':
    main()
