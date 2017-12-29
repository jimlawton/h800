#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# List symbols in ARGUS assembly source
#
# A script that uses the arguscard classes to read ARGUS assembly format source
# and generate a symbol table listing.
#
# This is intended for debugging assembler development.


import sys
from optparse import OptionParser

import h800.arguscard


def main():
    parser = OptionParser("usage: %prog filename [filename]...")
    parser.add_option('-v', '--verbose',
                      dest='verbose',
                      action='store_true',
                      default=False,
                      help="Enable verbose output.")
    (opts, args) = parser.parse_args()
    if len(args) < 1:
        parser.error("usage: %prog filename")
        sys.exit(1)

    errors = 0

    for filename in args:
        d = h800.arguscard.Deck(file=filename, verbose=opts.verbose)

        file_errors = 0

        symtab = {}
        for card in d.cards:
            if card.label:
                strLabel = card.label.strip().replace(' ', '')
                if strLabel not in list(symtab.keys()):
                    symtab[strLabel] = {
                        "def-file": card.filename,
                        "def-line": card.linenum,
                        "def-lognum": card.lognum,
                        "def-source": card.line
                    }
                else:
                    if card.operation != "ASSIGN" and card.operation != "TAS":
                        # ASSIGN and TAS can doubly-define symbols in some
                        # arcane way that I do not yet understand.
                        print("\n*** ERROR: Symbol %s is multiply-defined!" %
                              strLabel, file=sys.stderr)
                        print(card.filename, card.linenum, card.lognum,
                              file=sys.stderr)
                        print(card.line, file=sys.stderr)
                        print("Previous definition:", file=sys.stderr)
                        print(symtab[strLabel]["def-file"],
                              symtab[strLabel]["def-line"],
                              symtab[strLabel]["def-lognum"], file=sys.stderr)
                        print(symtab[strLabel]["def-source"], file=sys.stderr)
                        print("", file=sys.stderr)
                        file_errors += 1
        errors += file_errors

        for sym in sorted(symtab.keys()):
            print("%-9s %s" % (sym, symtab[sym]))

    if errors > 0:
        print("%d errors found" % errors, file=sys.stderr)


if __name__ == '__main__':
    main()
