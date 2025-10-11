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


try:
    from h800.memory import MemoryMap, MemoryType
except ImportError:
    MemoryMap = MemoryType = None

try:
    from h800.opcodes import OPCODES
except ImportError:
    OPCODES = {}

try:
    from h800.record_type import RecordType
except ImportError:
    RecordType = None

from h800.symbol_table import SymbolTable


class Context:
    def __init__(self, listfile, binfile, options, log_level=0, logfile=None):
        self.options = options
        self.verbose = options.verbose
        self.debug = options.debug
        self.logfile = logfile
        self.assembler = None
        self.listfile = listfile
        self.binfile = binfile
        self.srcfile = None
        # self.opcodes = OPCODES.get(getattr(self, 'arch', None), {})  # Legacy placeholder
        self.symtab = SymbolTable() if SymbolTable else {}
        self.coloc = 0
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
        self.log_level = log_level

        self.loc = 0  # Assembler PC..
        self.bank = 0  # Current bank.

        self.bankloc = {}  # Saved current location for each bank.

        # for bank in range(len(self.memmap.banks[MemoryType.ERASABLE])):
        #     self.ebankloc[bank] = 0

        self.errors = 0
        self.warnings = 0

    def __str__(self):
        parts = [
            f"options: {self.options}",
            f"logfile: {self.logfile}",
            f"listfile: {self.listfile}",
            f"binfile: {self.binfile}",
            f"srcfile: {self.srcfile}",
            f"linenum={self.linenum}",
            f"global_linenum={self.global_linenum}",
            f"code: {self.code}",
            f"srcline: {self.srcline}",
            f"currentRecord: {self.currentRecord}",
        ]
        if RecordType and self.currentRecord and hasattr(self.currentRecord, "type"):
            parts.append(
                f"currentRecord.type: {RecordType.toString(self.currentRecord.type)} ({self.currentRecord.type})"
            )
        parts.append(f"previousRecord: {self.previousRecord}")
        if RecordType and self.previousRecord and hasattr(self.previousRecord, "type"):
            parts.append(
                f"previousRecord.type: {RecordType.toString(self.previousRecord.type)} ({self.previousRecord.type})"
            )
        parts.extend(
            [
                f"addSymbol={self.addSymbol}",
                f"reparse={self.reparse}",
                f"passnum={self.passnum}",
                f"log_level={self.log_level}",
                f"loc={self.loc:06o}",
                f"bank={self.bank:02o}",
                f"bankloc: {self.bankloc}",
                f"errors={self.errors}",
                f"warnings={self.warnings}",
            ]
        )
        return "\n".join(parts)

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

    def set_loc(self, address):
        """Set the primary location (program counter). Legacy wrapper: setLoc()."""
        if hasattr(self, "memmap") and self.memmap and not self.memmap.isValid(address):
            self.error(f"trying to set loc to an invalid address ({address:06o})")
            return
        if not self.reparse:
            self.log(5, f"changing loc from {self.loc:06o} to {address:06o}")
            self.loc = address

    def set_coloc(self, address):
        """Set the co-location (secondary program counter). Legacy wrapper: setCoLoc()."""
        if hasattr(self, "memmap") and self.memmap and not self.memmap.isValid(address):
            self.error(f"trying to set coloc to an invalid address ({address:06o})")
            return
        if not self.reparse:
            self.log(5, f"changing coloc from {self.coloc:06o} to {address:06o}")
            self.coloc = address

    # Legacy camelCase wrappers (deprecated)
    def setLoc(self, address):  # noqa: N802
        self.set_loc(address)

    def setCoLoc(self, address):  # noqa: N802
        self.set_coloc(address)
