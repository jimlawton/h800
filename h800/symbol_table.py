from __future__ import print_function
import sys

import h800


class SymbolTableEntry:

    def __init__(self, name, value=None, symtype=None, file=None, line=0,
                 segment=None, subsegment=None):
        self._name = name                    # Symbol name
        self._absoluteValue = self._complexValue = None
        self._symtype = symtype                    # Type of record
        if symtype == "absolute":
            self._absoluteValue = value      # Absolute value
        else:
            self._complexValue = value       # Complex value
        self._file = file
        self._line = line
        self._segment = segment
        self._subsegment = subsegment
        self._references = []

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def references(self):
        return self._references

    @property
    def segment(self):
        return self._segment

    @property
    def subsegment(self):
        return self._subsegment

    @property
    def file(self):
        return self._file

    @property
    def line(self):
        return self._line

    def isValid(self):
        return (self._absoluteValue is not None or
                self._complexValue is not None)

    def isAbsolute(self):
        return (self._absoluteValue is not None)

    def isComplex(self):
        return (self._complexValue is not None)

    def isMultiple(self):
        return self.isAbsolute() and self.isComplex()

    def addReference(self, ref):
        self._references.append(ref)


class SymbolTable:

    def __init__(self):
        self._symbols = {}
        self._undefs = []

    @property
    def symbols(self):
        return self._symbols

    @property
    def undefines(self):
        return self._undefs

    def add(self, name, srcfile, linenum, value=None,
            symtype=None, segment=None, subsegment=None):
        if name:
            if name in self._symbols:
                print("ERROR: Symbol \"%s\" already defined!" % (name))
            else:
                self._symbols[name] = SymbolTableEntry(name, value, symtype,
                                                       srcfile, linenum,
                                                       segment, subsegment)
                if value is None:
                    self._undefs.append(name)

    def update(self, name, value=None, symtype=None):
        if name:
            if name not in list(self._symbols.keys()):
                self.context.error("symbol \"%s\" not defined!" % (name))
            else:
                entry = self._symbols[name]
                entry.value = value
                entry.type = symtype
                self._symbols[name] = entry

    def resolve(self, maxPasses=10):
        nPrevUndefs = nUndefs = len(self._undefs)
        for i in range(maxPasses):
            print("Symbol pass %d: %d undefined symbols" % (i, nUndefs))
            if nUndefs == 0:
                print("All symbols resolved!")
                break
            for symbol in self._undefs:
                print("Attempting to resolve symbol \"%s\"" % (symbol))
                # TODO
            self.pruneUndefines()
            nUndefs = len(self._undefs)
            if nUndefs == nPrevUndefs:
                print("ERROR: No progress resolving symbols, %d undefined "
                      "symbols" % nUndefs)
                break
            nPrevUndefs = nUndefs

    def pruneUndefines(self):
        # Prune the undefs list.
        numUndefs = len(self._undefs)
        print("Pruning undefined symbols list (%d undefs)" % numUndefs)
        for i, symbol in enumerate(self._undefs):
            entry = self._symbols[symbol]
            if entry.isValid():
                print("Removing %s from undefined symbols list" % (symbol))
                del self._undefs[i]
        print("Removed %d symbols from undef list" %
              (numUndefs - len(self._undefs)))

    def getNumSymbols(self):
        return len(list(self._symbols.keys()))

    def getNumUndefs(self):
        return len(self._undefs)

    def lookup(self, name):
        entry = None
        if name in self._symbols:
            entry = self._symbols[name]
        return entry

    def printTable(self, outfile=None):
        if outfile is None:
            out = sys.stdout
        else:
            out = outfile
        symbols = list(self._symbols.keys())
        symbols.sort()
        print("\nDefined symbols:\n", file=out)
        for symbol in symbols:
            print(self._symbols[symbol], file=out)

        if len(self._undefs) > 0:
            print("\nUndefined symbols:\n", file=out)
            for symbol in self._undefs:
                print(self._symbols[symbol], file=out)

    def printUndefs(self, outfile=None):
        if outfile is None:
            out = sys.stdout
        else:
            out = outfile
        print("\nUndefined symbols: %d\n" % (len(self._undefs)), file=out)
        for symbol in self._undefs:
            print(self._symbols[symbol], file=out)


def buildSymbolTable(filename, verbose=False, bad=False):
    seg = filename.split('.')[0]  # Default: name of the first file.
    subsegs = []        # List of subsegments.
    subseg = "1"        # Current subsegment, default is 1 (no starting SETLOC)
    d = h800.arguscard.Deck(file=filename, verbose=verbose)
    errcount = 0
    symtab = {}
    symtab[seg] = {}
    print("Segment: %s" % seg)
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
            print("Subsegment: %s" % subseg)
            symtab[seg][subseg] = {}
        if card.label:
            strLabel = card.label.strip().replace(' ', '')
            symtabEntry = {
                "file": card.filename,
                "line": card.linenum,
                "lognum": card.lognum,
                "card": card
            }
            if bad and strLabel.upper() != strLabel:
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
            if strLabel not in list(symtab[seg][subseg].keys()):
                symtab[seg][subseg][strLabel] = {}
                symtab[seg][subseg][strLabel][symtype] = symtabEntry
            else:
                prevdef = symtab[seg][subseg][strLabel]
                if symtype not in prevdef.keys():
                    symtab[seg][subseg][strLabel][symtype] = symtabEntry
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
                          symtab[seg][subseg][strLabel])
                    print("Current definition: %s" % symtabEntry)
                    print("command: %s" % command)
                    errcount += 1
    return symtab, errcount
