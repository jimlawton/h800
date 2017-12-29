#!/usr/bin/env python

import sys


class SymbolTableEntry:

    def __init__(self, name, expression=None, value=None, type=None,
                 file=None, line=0):
        self._name = name                    # Symbol name
        self._expression = expression        # Symbolic expression
        self._absoluteValue = self._complexValue = None
        if type == "absolute":
            self._absoluteValue = value      # Absolute value
        else:
            self._complexValue = value       # Complex value
        self._recordIndex = None             # Parser record containing defn
        self._references = []                # List of references
        self._type = type                    # Type of record
        self._file = file
        self._line = line

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
        self.references.append(ref)

    def getReferences(self):
        return self.references

    def __str__(self):
        text = "%-8s " % (self.name)
        if self.value is None:
            text += "%-20s" % "******"
        else:
            text += "%-10s" % self.value
        return text


class SymbolTable:

    def __init__(self, context):
        self.symbols = {}
        self.undefs = []
        self.context = context

    def add(self, name, srcfile, linenum, expression=None, value=None,
            symtype=None):
        if name:
            if name in self.symbols:
                print("ERROR: Symbol \"%s\" already defined!" % (name))
            else:
                self.symbols[name] = SymbolTableEntry(self.context, name,
                                                      expression, value,
                                                      symtype, srcfile,
                                                      linenum)
                self.symbols[name].recordIndex = \
                    self.context.global_linenum - 1
                if value is None:
                    self.undefs.append(name)

    def update(self, name, value=None, symtype=None):
        if name:
            if name not in list(self.symbols.keys()):
                self.context.error("symbol \"%s\" not defined!" % (name))
            else:
                entry = self.symbols[name]
                entry.value = value
                entry.type = symtype
                self.symbols[name] = entry

    def resolve(self, maxPasses=10):
        nPrevUndefs = nUndefs = len(self.undefs)
        for i in range(maxPasses):
            print("Symbol pass %d: %d undefined symbols" % (i, nUndefs))
            if nUndefs == 0:
                print("All symbols resolved!")
                break
            for symbol in self.undefs:
                print("Attempting to resolve symbol \"%s\" (%d)" %
                      (symbol, self.symbols[symbol].recordIndex))
                if not self.symbols[symbol].isComplete():
                    idx = self.symbols[symbol].recordIndex
                    self.context.assembler.parseRecord(idx)
                    if self.symbols[symbol].isComplete():
                        self.context.records[idx].complete = True
            self.pruneUndefines()
            nUndefs = len(self.undefs)
            if nUndefs == nPrevUndefs:
                print("ERROR: No progress resolving symbols, %d undefined "
                      "symbols" % nUndefs)
                break
            nPrevUndefs = nUndefs
        if self.context.debug and nUndefs == 0:
            for symbol in self.symbols:
                entry = self.symbols[symbol]
                if entry.type is None:
                    entry.type = self.context.records[entry.recordIndex].type
                    self.symbols[symbol] = entry

    def pruneUndefines(self):
        # Prune the undefs list.
        numUndefs = len(self.undefs)
        print("Pruning undefined symbols list (%d undefs)" % numUndefs)
        tmpUndefs = []
        for symbol in self.undefs:
            entry = self.symbols[symbol]
            if not entry.isComplete():
                tmpUndefs.append(symbol)
            else:
                print("Removing %s from undefined symbols list" % (symbol))
        self.undefs = tmpUndefs
        print("Removed %d symbols from undef list" %
              (numUndefs - len(self.undefs)))
        # self.printUndefs()

    def keys(self):
        return list(self.symbols.keys())

    def getNumSymbols(self):
        return len(list(self.symbols.keys()))

    def getNumUndefs(self):
        return len(self.undefs)

    def lookup(self, name):
        entry = None
        if name in self.symbols:
            entry = self.symbols[name]
        return entry

    def printTable(self, outfile=None):
        if outfile is None:
            out = sys.stdout
        else:
            out = outfile
        symbols = list(self.symbols.keys())
        symbols.sort()
        print("\nDefined symbols:\n", file=out)
        for symbol in symbols:
            print(self.symbols[symbol], file=out)

        if len(self.undefs) > 0:
            print("\nUndefined symbols:\n", file=out)
            for symbol in self.undefs:
                print(self.symbols[symbol], file=out)

    def printUndefs(self, outfile=None):
        if outfile is None:
            out = sys.stdout
        else:
            out = outfile
        print("\nUndefined symbols: %d\n" % (len(self.undefs)), file=out)
        for symbol in self.undefs:
            print(self.symbols[symbol], file=out)
