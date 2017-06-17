#!/usr/bin/env python

import sys
import struct


class SymbolTableEntry:

    def __init__(self, name, expression=None, value=None, type=None, file=None, line=0):
        self.name = name                    # Symbol name.
        self.expression = expression        # Symbolic expression.
        self.value = value                  # Actual value.
        self.recordIndex = None             # Index of the parser record containing the definition of this symbol.
        self.references = []                # List of references.
        self.type = type                    # Type of record the symbol refers to.
        self.file = file
        self.line = line

    def isComplete(self):
        return (self.value != None)

    def addReference(self, ref):
        self.references.append(ref)

    def getReferences(self):
        return self.references

    def __str__(self):
        text = "%-8s "  % (self.name)
        if self.value == None:
            text += "%-20s" % "******"
        else:
            text += "%-10s" % self.value
        return text


class SymbolTable:

    def __init__(self, context):
        self.symbols = {}
        self.undefs = []
        self.context = context

    def add(self, name, srcfile, linenum, expression=None, value=None, type=None):
        if name:
            if name in self.symbols:
                print "ERROR: Symbol \"%s\" already defined!" % (name)
            else:
                self.symbols[name] = SymbolTableEntry(self.context, name, expression, value, type, srcfile, linenum)
                self.symbols[name].recordIndex = self.context.global_linenum - 1
                if value is None:
                    self.undefs.append(name)

    def update(self, name, value=None, type=None):
        if name:
            if name not in self.symbols.keys():
                self.context.error("symbol \"%s\" not defined!" % (name))
            else:
                entry = self.symbols[name]
                entry.value = value
                entry.type = type
                self.symbols[name] = entry

    def resolve(self, maxPasses=10):
        nPrevUndefs = nUndefs = len(self.undefs)
        for i in range(maxPasses):
            print "Symbol pass %d: %d undefined symbols" % (i, nUndefs)
            if nUndefs == 0:
                print "All symbols resolved!"
                break
            for symbol in self.undefs:
                print "Attempting to resolve symbol \"%s\" (%d)" % (symbol, self.symbols[symbol].recordIndex)
                if not self.symbols[symbol].isComplete():
                    self.context.assembler.parseRecord(self.symbols[symbol].recordIndex)
                    if self.symbols[symbol].isComplete():
                        self.context.records[self.symbols[symbol].recordIndex].complete = True
            self.pruneUndefines()
            nUndefs = len(self.undefs)
            if nUndefs == nPrevUndefs:
                print "ERROR: No progress resolving symbols, %d undefined symbols" % nUndefs
                break
            nPrevUndefs = nUndefs
        if self.context.debug and nUndefs == 0:
            for symbol in self.symbols:
                entry = self.symbols[symbol]
                if entry.type == None:
                    entry.type = self.context.records[entry.recordIndex].type
                    self.symbols[symbol] = entry

    def pruneUndefines(self):
        # Prune the undefs list.
        numUndefs = len(self.undefs)
        print "Pruning undefined symbols list (%d undefs)" % numUndefs
        tmpUndefs = []
        for symbol in self.undefs:
            entry = self.symbols[symbol]
            if not entry.isComplete():
                tmpUndefs.append(symbol)
            else:
                print "Removing %s from undefined symbols list" % (symbol)
        self.undefs = tmpUndefs
        print "Removed %d symbols from undef list" % (numUndefs - len(self.undefs))
        #self.printUndefs()

    def keys(self):
        return self.symbols.keys()

    def getNumSymbols(self):
        return len(self.symbols.keys())

    def getNumUndefs(self):
        return len(self.undefs)

    def lookup(self, name):
        entry = None
        if name in self.symbols:
            entry = self.symbols[name]
        return entry

    def printTable(self, outfile=None):
        if outfile == None:
            out = sys.stdout
        else:
            out = outfile
        symbols = self.symbols.keys()
        symbols.sort()
        print >>out, "\nDefined symbols:\n"
        for symbol in symbols:
            print >>out, self.symbols[symbol]

        if len(self.undefs) > 0:
            print >>out, "\nUndefined symbols:\n"
            for symbol in self.undefs:
                print >>out, self.symbols[symbol]

    def printUndefs(self, outfile=None):
        if outfile == None:
            out = sys.stdout
        else:
            out = outfile
        print >>out, "\nUndefined symbols: %d\n" % (len(self.undefs))
        for symbol in self.undefs:
            print >>out, self.symbols[symbol]

