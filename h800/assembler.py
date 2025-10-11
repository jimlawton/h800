"""
Assembler module for the h800 project.

Provides the Assembler class responsible for building a symbol table,
orchestrating basic multi-pass resolution of parser records, and offering
extension points for future code generation.

The original version of this file contained placeholder methods referencing
an external context object that was not implemented. This refactored version
introduces a minimal internal ParserRecord dataclass so that the resolve()
workflow can execute without external dependencies.

NOTE:
- Real parsing / code generation logic has not yet been implemented.
- The symbol table builder (buildSymbolTable) is reused.
- Logging uses pylog's info / debug / critical functions.
- All naming follows Python / ruff conventions (snake_case).
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from pylog import critical, debug, info

from h800.symbol_table import buildSymbolTable


@dataclass
class ParserRecord:
    """Represents a single parsed source line (ARGUS card)."""

    srcline: str
    label: str | None = None
    opcode: str | None = None
    operands: list[str] = field(default_factory=list)
    complete: bool = False
    errors: list[str] = field(default_factory=list)

    def is_parseable(self) -> bool:
        return self.opcode is not None

    def is_complete(self) -> bool:
        return self.complete

    def mark_complete(self) -> None:
        self.complete = True

    def error(self, message: str) -> None:
        self.errors.append(message)
        self.complete = False

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return (
            f"ParserRecord(label={self.label!r}, opcode={self.opcode!r}, "
            f"operands={self.operands!r}, complete={self.complete}, "
            f"errors={self.errors})"
        )


class Assembler:
    """H-x800 Assembler class (refactored).

    High-level workflow:
        1. build symbol table via create_symbol_table()
        2. read source in assemble() -> populate self._records
        3. multi-pass resolution via resolve()

    Methods parse() and parse_record() are placeholders for future
    semantic parsing and code word emission.
    """

    def __init__(self, verbose: bool = False) -> None:
        self._verbose = verbose
        self._symtab = {}
        self._records: list[ParserRecord] = []
        self._errors = 0
        self._passnum = 0

    @property
    def symbol_table(self):
        return self._symtab

    @property
    def records(self) -> list[ParserRecord]:
        return self._records

    def create_symbol_table(self, src_file: str) -> None:
        """Populate (or extend) the internal symbol table from src_file."""
        info(f"Processing {src_file}")
        self._symtab, _errcount = buildSymbolTable(src_file, self._symtab, verbose=self._verbose)

    def assemble(self, src_file: str) -> None:
        """Load source lines and create ParserRecord placeholders."""
        info(f"Assembling {src_file}")
        self._records.clear()
        try:
            with open(src_file) as f:
                lines = f.readlines()
        except OSError as exc:
            critical(f"Failed to read {src_file}: {exc}")
            raise
        debug(f"assemble: file {src_file}, lines {len(lines)}")
        for line in lines:
            stripped = line.rstrip("\n")
            # Extremely naive tokenization; real grammar TBD.
            # Format assumption: LABEL: OPCODE OPERAND...
            parts = stripped.split()
            label = None
            opcode = None
            operands: list[str] = []
            if parts:
                if parts[0].endswith(":"):
                    label = parts[0][:-1]
                    if len(parts) > 1:
                        opcode = parts[1]
                        operands = parts[2:]
                else:
                    opcode = parts[0]
                    operands = parts[1:]
            record = ParserRecord(
                srcline=stripped,
                label=label,
                opcode=opcode,
                operands=operands,
            )
            self._records.append(record)

    def parse(self, label: str | None, opcode: str | None, operands: list[str]) -> None:
        """Parse a single line's components (placeholder)."""
        try:
            info(f"parse: label={label!r} opcode={opcode!r} operands={operands!r}")
            # TODO: implement actual parsing and mark completion conditions.
        except Exception:
            critical("Exception during parse")
            raise

    def parse_record(self, record: ParserRecord) -> None:
        """Parse a ParserRecord without affecting assembler global state."""
        if record.opcode:
            self.parse(record.label, record.opcode, record.operands)
            # Mark complete immediately for now.
            record.mark_complete()

    def resolve(self, max_passes: int = 10) -> None:
        """Multi-pass resolution loop to finalize records."""
        start_time = time.time()
        num_records = len(self._records)
        debug(f"Starting resolution: {num_records} parser records")
        n_undefs = n_prev_undefs = 0
        for i in range(max_passes):
            self._passnum = i + 1
            n_prev_undefs = n_undefs
            n_undefs = 0
            undef_records: list[ParserRecord] = []
            for record in self._records:
                if record.is_parseable():
                    debug(f"resolve pass {self._passnum}: {record.srcline}")
                    self.parse_record(record)
                    if not record.is_complete():
                        n_undefs += 1
                        undef_records.append(record)
            info(f"{n_undefs} incomplete parser records")
            if n_undefs == 0:
                info("All parser records complete")
                break
            if n_undefs == n_prev_undefs:
                for urec in undef_records:
                    urec.error("undefined symbol")
                    self._errors += 1
                info(f"No progress resolving parser records, {n_undefs} undefined records")
                break
        if self._verbose:
            delta = time.time() - start_time
            info(f"Resolution elapsed: {delta:0.2f}s")

    @property
    def errors(self) -> int:
        return self._errors


__all__ = ["Assembler", "ParserRecord"]
