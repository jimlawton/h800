# Copyright 2010 Jim Lawton <jim dot lawton at gmail dot com>
#
# This file is part of h800.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

#from memory import MemoryMap, MemoryType
#from opcode import OpcodeType
#from opcodes import OPCODES
#from symbol_table import SymbolTable
#from record_type import RecordType


class Context:
    def __init__(self, listfile, binfile, options, logLevel=0, logfile=None):
        self.options = options
        self.verbose = options.verbose
        self.debug = options.debug
        self.logfile = logfile
        self.assembler = None
        self.listfile = listfile
        self.binfile = binfile
        self.srcfile = None
        # self.opcodes = OPCODES[self.arch]
        self.symtab = SymbolTable(self)
        self.linenum = 0
        self.global_linenum = 0
        self.code = []
        self.records = []
        self.srcline = None
        self.currentRecord = None
        self.previousRecord = None
        self.addSymbol = True
        self.reparse = False
        self.passnum = 0
        self.errorMsg = None
        self.warningMsg = None
        # Log level:
        #  0 - None.
        #  1 - Errors.
        #  2 - Warnings.
        #  3 - Info messages.
        #  4 - Bank changes, binary generation.
        #  5 - LOC changes, detailed interpretive logging.
        #  6 - Symbol information, address conversion.
        #  7 - Parser operation.
        #  8 - Symbol resolution.
        self.logLevel = logLevel

        self.loc = 0        # Assembler PC..
        self.bank = 0       # Current bank.

        self.bankloc = {}   # Saved current location for each bank.

        # for bank in range(len(self.memmap.banks[MemoryType.ERASABLE])):
        #     self.ebankloc[bank] = 0

        self.errors = 0
        self.warnings = 0

    def __str__(self):
        text = ""
        text += "options: %s\n" % self.options
        text += "logfile: %s" % self.logfile
        # text += "arch=%d\n" % self.arch
        text += "listfile: %s\n" % self.listfile
        text += "binfile: %s\n" % self.binfile
        text += "srcfile: %s\n" % self.srcfile
        text += "linenum=%d\n" % self.linenum
        text += "global_linenum=%d\n" % self.global_linenum
        text += "code: %s\n" % self.code
        text += "srcline: %s\n" % self.srcline
        text += "currentRecord: %s\n" % self.currentRecord
        text += "currentRecord.type:  %s (%d)\n" % (RecordType.toString(self.currentRecord.type), self.currentRecord.type)
        text += "previousRecord: %s\n" % self.previousRecord
        text += "previousRecord.type: %s (%d)\n" % (RecordType.toString(self.previousRecord.type), self.previousRecord.type)
        text += "addSymbol=%s\n" % self.addSymbol
        text += "reparse=%s\n" % self.reparse
        text += "passnum=%d\n" % self.passnum
        text += "logLevel=%d\n" % self.logLevel
        text += "loc=%06o\n" % self.loc
        text += "bank=%02o\n" % self.bank
        text += "bankloc: %s\n" % self.bankloc
        text += "errors=%d\n" % self.errors
        text += "warnings=%d\n" % self.warnings
        return text

    def reset(self):
        self.linenum = 0
        self.global_linenum = 0
        self.code = []
        self.srcline = None
        self.currentRecord = None
        self.previousRecord = None
        self.addSymbol = True
        self.reparse = False
        self.loc = 0
        self.bank = 0

    def load(self, record, partial=True):
        self.linenum = record.linenum
        self.global_linenum = record.global_linenum
        self.code = record.code
        self.srcline = record.srcline
        self.loc = record.loc
        self.bank = record.bank
        self.coloc = record.coloc
        self.errorMsg = record.errorMsg
        self.warningMsg = record.warningMsg

    def save(self, record, partial=True):
        record.linenum = self.linenum
        record.global_linenum = self.global_linenum
        record.code = self.code
        record.srcline = self.srcline
        record.loc = self.loc
        record.coloc = self.coloc
        record.bank = self.bank
        record.errorMsg = self.errorMsg
        record.warningMsg = self.warningMsg

    def setLoc(self, address):
        if not self.memmap.isValid(address):
            self.error("trying to set loc to an invalid address (%06o)" % address)
        if not self.reparse:
            self.log(5, "changing loc from %06o to %06o" % (self.loc, address))
            self.loc = address

    def setCoLoc(self, address):
        if not self.memmap.isValid(address):
            self.error("trying to set loc to an invalid address (%06o)" % address)
        if not self.reparse:
            self.log(5, "changing loc from %06o to %06o" % (self.coloc, address))
            self.coloc = address
