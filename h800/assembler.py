import time

from pylog import info, debug, critical
from parser_record import ParserRecord

from h800.symbol_table import buildSymbolTable


class Assembler:
    """H-x800 Assembler class."""

    def __init__(self, verbose=False):
        self._verbose = verbose
        self._symtab = {}

    def createSymbolTable(self, srcfile):
        info("Processing %s" % srcfile)
        self._symtab, errcount = buildSymbolTable(srcfile, self._symtab,
                                                  verbose=self._verbose)

    def assemble(self, srcfile):
        info("Assembling %s" % srcfile)
        self._srcfile = srcfile
        self._linenum = 0
        with open(srcfile, 'r') as f:
            lines = f.readlines()
        debug("assemble: file %s, lines %d" % (srcfile, len(lines)))

        for line in lines:
            # Parse lines.
            pass

    def parse(self, label, opcode, operands):
        try:
            info(7, "parse: label='%s' opcode='%s' operands=%s" %
                 (label, opcode, operands))
            # TODO: parse operation here.
        except Exception:
            critical("Exception processing line:")
            raise

    def parseRecord(self, recordIndex):
        """
        Parse a ParserRecord, without affecting assembler state.
        Return the generated code words, if any.
        """
        pass

    def resolve(self, maxPasses=10):
        "Resolve a symbol."
        startTime = time.time()
        # self.context.symtab.resolve(maxPasses)
        endTime = time.time()
        delta = endTime - startTime
        debug("Symbol resolution: %3.2f seconds" % delta)

        startTime = time.time()
        numRecords = len(self.context.records)
        debug("Updating %d parser records..." % (numRecords))
        nUndefs = nPrevUndefs = 0
        for i in range(maxPasses):
            self._passnum = i + 1
            # self.reset()
            nPrevUndefs = nUndefs
            nUndefs = 0
            undefRecords = []
            for j in range(numRecords):
                record = self._records[j]
                if record.isParseable():
                    self._currentRecord = record
                    self._previousRecord = self.context.records[j-1]
                    # self.load(record)
                    debug("resolve: %s" % (record.srcline))
                    # self.parse(record.label, record.opcode, record.operands)
                    self._records[j] = self.context.currentRecord
                    if not record.isComplete():
                        nUndefs += 1
                        undefRecords.append(record)
            info("%d incomplete parser records" % (nUndefs))
            if nUndefs == 0:
                info("All parser records complete")
                break
            if nUndefs == nPrevUndefs:
                for urec in undefRecords:
                    urec.error("undefined symbol")
                    self._errors += 1
                self.context.error("no progress resolving parser records, "
                                   "%d undefined records" % nUndefs,
                                   source=False, count=False)
                break
        if self._verbose:
            endTime = time.time()
            delta = endTime - startTime
            print("Pass 2: %3.2f seconds" % delta)
