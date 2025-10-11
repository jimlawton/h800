from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import (
    Protocol,
    TypedDict,
)

# ---------------------------------------------------------------------------
# Opcode metadata typing
# ---------------------------------------------------------------------------

class OpcodeMeta(Protocol):
    """Protocol describing required attributes of an opcode metadata object."""

    m: str
    b23: int | None
    b7: int | None
    op: int
    type: str

class OpcodeDict(TypedDict, total=False):
    """TypedDict alternative for dynamic opcode metadata."""

    m: str
    b23: int | None
    b7: int | None
    op: int
    type: str

# ---------------------------------------------------------------------------
# Core instruction & constant data structures
# ---------------------------------------------------------------------------

@dataclass
class Instruction:
    """
    12-bit instruction representation.

    Fields:
        opcode_meta : Metadata object implementing OpcodeMeta.
        sequence    : 0/1 flag (mutually exclusive with paddr).
        mask        : 0..31 for maskable instructions (exclusive with operands/paddr).
        operands    : Mapping or iterable providing up to three flags (a,b,c).
        a,b,c       : Convenience individual operand flags (overridden by operands if provided).
        paddr       : 0..63 peripheral address (exclusive with sequence/mask/operands).
        pseudo      : If True, emission may be suppressed (placeholder hook).
    Computed:
        data        : Internal BitField (implementation detail; runtime only).
    """

    opcode_meta: OpcodeMeta
    sequence: int | None = None
    mask: int | None = None
    operands: Mapping[str, int | None] | Iterable[int | None] | None = None
    a: int | None = None
    b: int | None = None
    c: int | None = None
    paddr: int | None = None
    pseudo: bool = False

    # Internal/private attributes (set in __post_init__ at runtime; stubs only)
    _operands: dict[str, int | None]
    _mnemonic: str
    _bits23: int | None
    _bit7: int | None
    _op: int
    _type: str
    # data: BitField  # Omitted from stub to avoid dependency; treated as runtime-only.
    def __post_init__(self) -> None: ...
    def mnemonic(self) -> str: ...
    @property
    def value(self) -> int: ...
    @property
    def operands_group(self) -> dict[str, int | None]: ...
    def __int__(self) -> int: ...
    def __repr__(self) -> str: ...

@dataclass
class Constant:
    """48-bit constant wrapper."""

    mnemonic: str
    value: int

    def __post_init__(self) -> None: ...
    def __int__(self) -> int: ...
    def __repr__(self) -> str: ...

# ---------------------------------------------------------------------------
# Factory helpers
# ---------------------------------------------------------------------------

def build_masked(opcode_meta: OpcodeMeta, sequence: int, mask: int) -> Instruction: ...
def build_unmasked(
    opcode_meta: OpcodeMeta,
    sequence: int,
    a: int = 0,
    b: int = 0,
    c: int = 0,
) -> Instruction: ...
def build_peripheral(opcode_meta: OpcodeMeta, paddr: int) -> Instruction: ...
def build_print(
    opcode_meta: OpcodeMeta,
    sequence: int,
    a: int = 0,
    b: int = 0,
    c: int = 0,
) -> Instruction: ...
def build_simulator(opcode_meta: OpcodeMeta, sequence: int) -> Instruction: ...

__all__ = [
    "Constant",
    "Instruction",
    "OpcodeDict",
    "OpcodeMeta",
    "build_masked",
    "build_peripheral",
    "build_print",
    "build_simulator",
    "build_unmasked",
]
