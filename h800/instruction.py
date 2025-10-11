"""
Instruction core module for the Honeywell H-800/H-1800 toolset.

This module provides:
- A dataclass-based `Instruction` with post-initialization validation and bitfield encoding.
- Typed protocol / TypedDict definitions for opcode metadata used to build instructions.
- 48-bit `Constant` dataclass for assembler constants.
- Factory helper functions for creating instructions of different categories.
- Unified factories (`build_masked`, `build_unmasked`, `build_peripheral`, `build_print`, `build_simulator`, `get_instruction`) and reverse decoder `decode_instruction` for disassembly.

Encoding summary (12-bit instruction word, bits numbered MSB=1 .. LSB=12):
    Maskable:   [1]=sequence, [2..6]=mask, [7]=1, [8..12]=opcode
    Unmasked:   [1]=sequence, [2..3]=variant, [4]=A, [5]=B, [6]=C, [7]=0, [8..12]=opcode
    Peripheral: [1..6]=paddr,  [7]=1, [8..12]=opcode
    Print:      Same field usage as unmasked + bit7=1
    Simulator:  Bits 10..12 define operation (special case handled by mapping)

Bit numbering scheme relies on `BitField` configured MSB-left with MSB-1 indexing.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Protocol, TypedDict

from .bitfield import BitField

# ---------------------------------------------------------------------------
# Validation constants
# ---------------------------------------------------------------------------

MASK_MAX = 31  # 5-bit mask (0..31)
PADDR_MAX = 63  # 6-bit peripheral address (0..63)
BITS23_MAX = 3  # Bits 2-3 variant (00..11)
OPCODE_MAX = 31  # Bits 8-12 opcode field (00000..11111)
WORD_48_MAX = 2**48 - 1  # Maximum 48-bit constant value

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
    """TypedDict alternative for dynamic metadata sources."""

    m: str
    b23: int | None
    b7: int | None
    op: int
    type: str


# ---------------------------------------------------------------------------
# Instruction dataclass
# ---------------------------------------------------------------------------


@dataclass
class Instruction:
    """
    Dataclass representing a 12-bit machine instruction.

    Parameters:
        opcode_meta : Metadata object (must satisfy OpcodeMeta Protocol).
        sequence    : 0 / 1 (mutually exclusive with paddr).
        mask        : 0..31 for maskable instructions (exclusive with operands and paddr).
        operands    : Iterable or mapping (a, b, c flags). If provided overrides a/b/c args.
        a, b, c     : Operand presence flags (deprecated direct form; retained for convenience).
        paddr       : 0..63 peripheral address (exclusive with sequence/mask/operands).
        pseudo      : If True, binary emission may be suppressed (placeholder for future).
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

    # Computed / internal fields.
    data: BitField = field(init=False, repr=False)
    _operands: dict[str, int | None] = field(init=False, repr=False)
    _mnemonic: str = field(init=False, repr=False)
    _bits23: int | None = field(init=False, repr=False)
    _bit7: int | None = field(init=False, repr=False)
    _op: int = field(init=False, repr=False)
    _type: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        # Extract metadata.
        self._mnemonic = self.opcode_meta.m
        self._bits23 = getattr(self.opcode_meta, "b23", None)
        self._bit7 = getattr(self.opcode_meta, "b7", None)
        self._op = getattr(self.opcode_meta, "op", 0)
        self._type = getattr(self.opcode_meta, "type", "unmasked")

        # Normalize operands into grouped dict.
        if self.operands is not None:
            if isinstance(self.operands, Mapping):
                a_val = self.operands.get("a")
                b_val = self.operands.get("b")
                c_val = self.operands.get("c")
            else:
                seq = list(self.operands)
                while len(seq) < 3:
                    seq.append(None)
                a_val, b_val, c_val = seq[:3]
        else:
            a_val, b_val, c_val = self.a, self.b, self.c
        self._operands = {"a": a_val, "b": b_val, "c": c_val}

        # Initialize bitfield (12 bits).
        self.data = BitField(
            0,
            width=12,
            numbering=BitField.BIT_SCHEME_MSB_1,
            order=BitField.BIT_ORDER_MSB_LEFT,
        )

        # Validate input combinations before encoding.
        self._validate()

        # Encode sequence (bit 1).
        if self.sequence is not None:
            self.data[1] = 1 if bool(self.sequence) else 0

        # Bit 7 (masked/unmasked indicator) for applicable types.
        if self._type in ("maskable", "peripheral", "print"):
            if (self._type == "maskable" and self.mask is not None) or self._type != "maskable":
                if self._bit7 is not None:
                    self.data[7] = self._bit7

        # Mask vs bits 2-3.
        if self.mask is not None:
            self.data[2:6] = self.mask
        elif self._bits23 is not None:
            self.data[2:3] = self._bits23

        # Operand flags (bits 4-6).
        for bit_index, name in enumerate(("a", "b", "c"), start=4):
            val = self._operands[name]
            if val is not None:
                self.data[bit_index] = 1 if bool(val) else 0

        # Peripheral address overrides bits 1-6.
        if self.paddr is not None:
            self.data[1:6] = self.paddr

        # Base opcode bits (8..12).
        self.data[8:12] = self._op

    # -----------------------------------------------------------------------
    # Validation
    # -----------------------------------------------------------------------

    def _validate(self) -> None:
        # Mutual exclusions.
        if self.sequence is not None and self.paddr is not None:
            raise ValueError("Cannot specify both sequence and peripheral address.")
        if self.mask is not None and self.paddr is not None:
            raise ValueError("Cannot specify both mask and peripheral address.")
        if self.mask is not None and any(v is not None for v in self._operands.values()):
            # Strict mutual exclusivity: maskable form cannot carry operand flags.
            raise ValueError("Operand flags (a,b,c) must be omitted when a mask is specified.")

        # Range checks.
        if self.sequence is not None and self.sequence not in (0, 1, True, False):
            raise ValueError("Sequence must be 0/1 or boolean.")

        if self.mask is not None:
            if self._type != "maskable":
                raise ValueError("Mask provided to a non-maskable instruction.")
            if not (0 <= self.mask <= MASK_MAX):
                raise ValueError(f"Mask out of range 0..{MASK_MAX}.")

        for name, val in self._operands.items():
            if val is not None and val not in (0, 1, True, False):
                raise ValueError(f"Operand flag '{name}' must be 0/1 or boolean.")

        if self.paddr is not None:
            if (
                self.sequence is not None
                or self.mask is not None
                or any(v is not None for v in self._operands.values())
            ):
                raise ValueError(
                    "Peripheral address is mutually exclusive with sequence, mask, and operand flags."
                )
            if not (0 <= self.paddr <= PADDR_MAX):
                raise ValueError(f"Peripheral address out of range 0..{PADDR_MAX}.")

        if self._bit7 is not None and self._bit7 not in (0, 1):
            raise ValueError("Bit7 indicator must be 0 or 1.")

        if self._bits23 is not None and not (0 <= self._bits23 <= BITS23_MAX):
            raise ValueError(f"Bits 2-3 variant out of range 0..{BITS23_MAX}.")

        if not (0 <= self._op <= OPCODE_MAX):
            raise ValueError(f"Opcode field out of range 0..{OPCODE_MAX}.")

    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    @property
    def mnemonic(self) -> str:
        return self._mnemonic

    @property
    def value(self) -> int:
        """Return encoded 12-bit instruction word as integer."""
        return int(self.data)

    @property
    def operands_group(self) -> dict[str, int | None]:
        """Return operand flags grouped."""
        return dict(self._operands)

    def __int__(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return (
            f"Instruction(mnemonic={self._mnemonic!r}, value=0o{self.value:04o}, "
            f"type={self._type}, sequence={self.sequence}, mask={self.mask}, "
            f"operands={self._operands}, paddr={self.paddr})"
        )


# ---------------------------------------------------------------------------
# Constant dataclass (48-bit)
# ---------------------------------------------------------------------------


@dataclass
class Constant:
    """48-bit constant wrapper (range enforced)."""

    mnemonic: str
    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise TypeError("Constant value must be int.")
        if not (0 <= self.value <= WORD_48_MAX):
            raise ValueError(f"Constant '{self.mnemonic}' out of range 0..{WORD_48_MAX}.")

    def __int__(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return f"Constant(mnemonic={self.mnemonic!r}, value={self.value})"


# ---------------------------------------------------------------------------
# Factory helpers
# ---------------------------------------------------------------------------


def build_masked(opcode_meta: OpcodeMeta, sequence: int, mask: int) -> Instruction:
    return Instruction(opcode_meta=opcode_meta, sequence=sequence, mask=mask)


def build_unmasked(
    opcode_meta: OpcodeMeta,
    sequence: int,
    a: int = 0,
    b: int = 0,
    c: int = 0,
) -> Instruction:
    return Instruction(opcode_meta=opcode_meta, sequence=sequence, operands=(a, b, c))


def build_peripheral(opcode_meta: OpcodeMeta, paddr: int) -> Instruction:
    return Instruction(opcode_meta=opcode_meta, paddr=paddr)


def build_print(
    opcode_meta: OpcodeMeta,
    sequence: int,
    a: int = 0,
    b: int = 0,
    c: int = 0,
) -> Instruction:
    return Instruction(opcode_meta=opcode_meta, sequence=sequence, operands=(a, b, c))


def build_simulator(opcode_meta: OpcodeMeta, sequence: int) -> Instruction:
    return Instruction(opcode_meta=opcode_meta, sequence=sequence)


def get_instruction(mnemonic: str, **kwargs) -> Instruction:
    """
    Unified convenience factory: resolve mnemonic from global OPCODES table and
    instantiate an Instruction with provided keyword arguments.

    Parameters:
        mnemonic: Instruction mnemonic (e.g., 'BA', 'RF', 'PRA', 'S', etc.).
        **kwargs: Arguments accepted by Instruction (sequence, mask, operands/a,b,c, paddr, pseudo).

    Returns:
        Instruction instance.

    Raises:
        KeyError: Unknown mnemonic.
        ValueError: Validation errors from Instruction.
    """
    # Local import to avoid circular dependency at module import time.
    from .instructions import OPCODES  # type: ignore

    meta = OPCODES[mnemonic]
    return Instruction(opcode_meta=meta, **kwargs)


# ---------------------------------------------------------------------------
# Reverse decoder (disassembly helper)
# ---------------------------------------------------------------------------


def decode_instruction(word: int, opcodes: Mapping[str, OpcodeMeta]) -> dict[str, object]:
    """
    Reverse decode a 12-bit instruction word into possible mnemonic(s) and field values.

    Returns a dictionary with:
        'word': original integer
        'mnemonics': list of candidate mnemonics (handles PRA/PRD/PRO collision)
        'fields': dict of extracted fields (only those relevant for candidates)
        'types': list of candidate types
    """
    if not (0 <= word <= 0o7777):  # 12 bits
        raise ValueError("Word must be a 12-bit integer (0..0o7777).")

    bf = BitField(
        word,
        width=12,
        numbering=BitField.BIT_SCHEME_MSB_1,
        order=BitField.BIT_ORDER_MSB_LEFT,
    )

    sequence = bf[1]
    bits23 = bf[2:3]
    bits2_6 = bf[2:6]  # mask or part of variant/paddr
    a_flag = bf[4]
    b_flag = bf[5]
    c_flag = bf[6]
    bit7 = bf[7]
    opcode_field = bf[8:12]

    candidates: list[str] = []
    types: list[str] = []
    fields: dict[str, int] = {}

    # Simulator special case (opcode 0o07)
    # Two valid words: 0o0007 (sequence 0) and 0o4007 (sequence 1)
    # Bit7 for simulator meta is None.
    for mnemonic, meta in opcodes.items():
        if meta.op != opcode_field:
            continue

        mtype = getattr(meta, "type", "unmasked")
        b7 = getattr(meta, "b7", None)
        b23 = getattr(meta, "b23", None)

        # Maskable: bit7 MUST be 1 and mask present (we cannot distinguish sequence-only unmasked form here
        # because maskable mnemonics also have an unmasked variant with bit7=0; treat both).
        if mtype == "maskable":
            if bit7 == 1 and b7 == 1:
                # Mask form
                mask = bits2_6
                candidates.append(mnemonic)
                types.append("maskable(mask)")
                fields = {"sequence": sequence, "mask": mask}
            elif bit7 == 0 and b23 == bits23:
                # Unmasked form
                candidates.append(mnemonic)
                types.append("maskable(unmasked)")
                fields = {
                    "sequence": sequence,
                    "a": a_flag,
                    "b": b_flag,
                    "c": c_flag,
                }

        elif mtype == "unmasked":
            if bit7 == 0 and b23 == bits23:
                candidates.append(mnemonic)
                types.append("unmasked")
                fields = {
                    "sequence": sequence,
                    "a": a_flag,
                    "b": b_flag,
                    "c": c_flag,
                }

        elif mtype == "peripheral":
            if bit7 == 1 and b7 == 1:
                paddr = bits2_6
                candidates.append(mnemonic)
                types.append("peripheral")
                fields = {"paddr": paddr}

        elif mtype == "print":
            if bit7 == 1 and b7 == 1:
                # PRA/PRD/PRO collide; include them all if opcode matches
                # Sequence bit and operand flags are meaningful.
                candidates.append(mnemonic)
                fields = {
                    "sequence": sequence,
                    "a": a_flag,
                    "b": b_flag,
                    "c": c_flag,
                }
                types.append("print")

        elif mtype == "simulator":
            # Simulator meta has bit7 None, opcode_field match already; bit pattern must be xxxxx00111
            # We only need sequence bit.
            if opcode_field == meta.op:
                candidates.append(mnemonic)
                types.append("simulator")
                fields = {"sequence": sequence}

    # Deduplicate candidates (print collision may add PRA/PRD/PRO)
    candidates = sorted(set(candidates))
    types = [t for i, t in enumerate(types) if i == 0 or t != types[i - 1]]

    return {
        "word": word,
        "mnemonics": candidates,
        "fields": fields,
        "types": types,
    }


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
    "decode_instruction",
    "get_instruction",
]
