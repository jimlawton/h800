#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Check symbols in ARGUS assembly source
#
# A script that uses the arguscard classes to read ARGUS assembly format source
# and check for multiply- or ill-defined symbols.
#
# This is intended for debugging assembler development.


import sys
from optparse import OptionParser

import h800.arguscard


def main():
    parser = OptionParser("usage: %prog filename [filename]...")
    parser.add_option('-a', '--all',
                      dest='all',
                      action='store_true',
                      default=False,
                      help="Check for all errors.")
    parser.add_option('-b', '--bad',
                      dest='bad',
                      action='store_true',
                      default=False,
                      help="Check for bad symbol names.")
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
        opts.bad = True

    toterrs = 0
    subsegs = []
    subseg = None
    for filename in args:
        d = h800.arguscard.Deck(file=filename, verbose=opts.verbose)
        errcount = 0
        symtab = {}
        for card in d.cards:
            if card.column8 == "*":
                continue
            command = card.operation
            if command and command.startswith("SETLOC"):
                if ',' in command:
                    subseg = command.split(',')[1].strip()
                else:
                    subseg = "0"
                subsegs.append(subseg)
                # print("Subsegment: %s" % subseg)
                symtab[subseg] = {}
            if card.label:
                strLabel = card.label.strip().replace(' ', '')
                symtabEntry = {
                    "file": card.filename,
                    "line": card.linenum,
                    "lognum": card.lognum,
                    "card": card
                }
                if subseg is None:
                    print("*** ERROR: Symbol %s defined outside a segment!" %
                          strLabel)
                    print("Current definition: %s" % symtabEntry)
                    errcount += 1
                    continue
                if opts.bad and strLabel.upper() != strLabel:
                    print("*** ERROR: Symbol %s is ill-formed!" % strLabel)
                    print("Current definition: %s" % symtabEntry)
                    errcount += 1
                    continue
                # Check the command code field. Depending on the command code
                # field operation, multiple declarations might be allowed,
                # e.g. RESERVE, EQUALS, ALF, SPEC, CAC, etc., all reserve
                # storage, but ASSIGN doesn't.
                if command is None:
                    print("*** ERROR: Symbol %s has no operation!" % strLabel)
                    print("Current definition: %s" % symtabEntry)
                    errcount += 1
                    continue
                if command == "ASSIGN":
                    symtype = "complex"
                else:
                    symtype = "simple"
                if strLabel not in list(symtab[subseg].keys()):
                    symtab[subseg][strLabel] = {}
                    symtab[subseg][strLabel][symtype] = symtabEntry
                else:
                    prevdef = symtab[subseg][strLabel]
                    if symtype not in prevdef.keys():
                        symtab[subseg][strLabel][symtype] = symtabEntry
                    else:
                        if command == "EQUALS":
                            prevcard = prevdef[symtype]["card"]
                            if prevcard.operation == "EQUALS":
                                if card.addressa == prevcard.addressa and \
                                        card.addressb == prevcard.addressb \
                                        and card.addressc == prevcard.addressc:
                                    # Equivalent assignment, ignore.
                                    continue
                        print("*** ERROR: Symbol %s is multiply-defined!" %
                              strLabel)
                        print("Previous definitions: %s" %
                              symtab[subseg][strLabel])
                        print("Current definition: %s" % symtabEntry)
                        print("command: %s" % command)
                        errcount += 1
        print("%s: %d errors encountered." % (filename, errcount))
        toterrs += errcount

    if len(args) > 1:
        print("Total: %d errors encountered." % toterrs)


if __name__ == '__main__':
    main()
