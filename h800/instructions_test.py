"""Compact parametrized tests for Honeywell H-800/H-1800 instruction encoding."""

from __future__ import annotations

import itertools

import pytest

from h800.instructions import (
    OPCODES,
    AlphanumericConstant,
    BinaryAdd,
    BinarySubtract,
    DecimalAdd,
    DecimalConstant,
    DecimalSubtract,
    ExtendedBinaryConstant,
    FixedBinaryConstant,
    FloatingBinaryConstant,
    FloatingDecimalConstant,
    OctalConstant,
    PrintAlphabetic,
    Proceed,
    ReadBackward,
    ReadForward,
    Simulator,
    WordAdd,
    WriteForward,
    make_masked_opcode,
    make_peripheral_opcode,
    make_print_opcode,
    make_unmasked_opcode,
)

# Mapping for maskable / unmaskable mnemonics to classes (subset representative)
MASKABLE = {
    "BA": BinaryAdd,
    "DA": DecimalAdd,
    "WA": WordAdd,
    "BS": BinarySubtract,
}

UNMASKABLE = {
    "BA": BinaryAdd,
    "DA": DecimalAdd,
    "WA": WordAdd,
    "BS": BinarySubtract,
}

PERIPHERAL = {
    "RF": ReadForward,
    "RB": ReadBackward,
    "WF": WriteForward,
}

PRINT = {"PRA": PrintAlphabetic}

CONSTANT_CLASSES = [
    AlphanumericConstant,
    DecimalConstant,
    ExtendedBinaryConstant,
    FloatingBinaryConstant,
    FloatingDecimalConstant,
    FixedBinaryConstant,
    OctalConstant,
]

# -----------------------------------------------------------------------------
# Positive encoding tests
# -----------------------------------------------------------------------------

MASKED_PARAMS = [
    (cls, mnemonic, {"sequence": s, "mask": m}, make_masked_opcode(mnemonic, s, m))
    for mnemonic, cls in MASKABLE.items()
    for s in (0, 1)
    for m in (0, 1, 31)
]

UNMASKED_PARAMS = [
    (
        cls,
        mnemonic,
        {"sequence": s, "a": a, "b": b, "c": c},
        make_unmasked_opcode(mnemonic, s, a, b, c),
    )
    for mnemonic, cls in UNMASKABLE.items()
    for s in (0, 1)
    for a, b, c in itertools.product((0, 1), repeat=3)
]

PERIPHERAL_PARAMS = [
    (cls, mnemonic, {"paddr": p}, make_peripheral_opcode(mnemonic, p))
    for mnemonic, cls in PERIPHERAL.items()
    for p in (0, 1, 63)
]

PRINT_PARAMS = [
    (
        cls,
        mnemonic,
        {"sequence": s, "a": a, "b": b, "c": c},
        make_print_opcode(mnemonic, s, a, b, c),
    )
    for mnemonic, cls in PRINT.items()
    for s in (0, 1)
    for a, b, c in itertools.product((0, 1), repeat=3)
]

SIMULATOR_PARAMS = [
    (Simulator, "SIM", {"sequence": 0}, 0o0007),
    (Simulator, "SIM", {"sequence": 1}, 0o4007),
]

CONSTANT_VALUES = (0, 1, 4095, 4096, 2**48 - 1)
CONSTANT_PARAMS = [
    (cls, cls.__name__, {"data": v}, v) for cls in CONSTANT_CLASSES for v in CONSTANT_VALUES
]


@pytest.mark.parametrize("cls,mnemonic,kwargs,expected", MASKED_PARAMS)
def test_maskable(cls, mnemonic, kwargs, expected):
    inst = cls(**kwargs)
    assert inst.value == expected


@pytest.mark.parametrize("cls,mnemonic,kwargs,expected", UNMASKED_PARAMS)
def test_unmaskable(cls, mnemonic, kwargs, expected):
    inst = cls(**kwargs)
    assert inst.value == expected


@pytest.mark.parametrize("cls,mnemonic,kwargs,expected", PERIPHERAL_PARAMS)
def test_peripheral(cls, mnemonic, kwargs, expected):
    inst = cls(**kwargs)
    assert inst.value == expected


@pytest.mark.parametrize("cls,mnemonic,kwargs,expected", PRINT_PARAMS)
def test_print(cls, mnemonic, kwargs, expected):
    inst = cls(**kwargs)
    assert inst.value == expected


@pytest.mark.parametrize("cls,mnemonic,kwargs,expected", SIMULATOR_PARAMS)
def test_simulator(cls, mnemonic, kwargs, expected):
    inst = cls(**kwargs)
    assert inst.value == expected


@pytest.mark.parametrize("cls,mnemonic,kwargs,expected", CONSTANT_PARAMS)
def test_constants(cls, mnemonic, kwargs, expected):
    inst = cls(**kwargs)
    assert inst.value == expected


# -----------------------------------------------------------------------------
# Negative / invalid argument tests
# -----------------------------------------------------------------------------

INVALID_MASKABLE = [
    (BinaryAdd, {"sequence": 0, "mask": 32}),
    (BinaryAdd, {"sequence": 2, "mask": 0}),
    (BinarySubtract, {"sequence": 0, "mask": 32}),
    (WordAdd, {"sequence": 1, "mask": -1}),
    (DecimalAdd, {"sequence": 0, "mask": 99}),
]


@pytest.mark.parametrize("cls,kwargs", INVALID_MASKABLE)
def test_invalid_maskable(cls, kwargs):
    with pytest.raises(ValueError):
        cls(**kwargs)


INVALID_UNMASKABLE = [
    (BinaryAdd, {"sequence": 2, "a": 0, "b": 0, "c": 0}),
    (BinaryAdd, {"sequence": 0, "a": 2, "b": 0, "c": 0}),
    (BinaryAdd, {"sequence": 0, "a": 1, "b": 2, "c": 3}),
    (DecimalSubtract, {"sequence": 0, "a": 0, "b": 0, "c": 2}),
]


@pytest.mark.parametrize("cls,kwargs", INVALID_UNMASKABLE)
def test_invalid_unmaskable(cls, kwargs):
    with pytest.raises(ValueError):
        cls(**kwargs)


INVALID_PERIPHERAL = [
    (ReadForward, {"paddr": -1}),
    (ReadForward, {"paddr": 64}),
    (ReadBackward, {"paddr": 999}),
]


@pytest.mark.parametrize("cls,kwargs", INVALID_PERIPHERAL)
def test_invalid_peripheral(cls, kwargs):
    with pytest.raises(ValueError):
        cls(**kwargs)


INVALID_PRINT = [
    (PrintAlphabetic, {"sequence": 2, "a": 0, "b": 0, "c": 0}),
    (PrintAlphabetic, {"sequence": 0, "a": 2, "b": 0, "c": 0}),
]


@pytest.mark.parametrize("cls,kwargs", INVALID_PRINT)
def test_invalid_print(cls, kwargs):
    with pytest.raises(ValueError):
        cls(**kwargs)


INVALID_CONSTANTS = [
    (AlphanumericConstant, -1),
    (AlphanumericConstant, 2**48),
    (DecimalConstant, -5),
    (FloatingBinaryConstant, 2**48),
]


@pytest.mark.parametrize("cls,value", INVALID_CONSTANTS)
def test_invalid_constants(cls, value):
    with pytest.raises(ValueError):
        cls(data=value)


def test_proceed_opcode():
    assert Proceed().value == 0


# -----------------------------------------------------------------------------
# Uniqueness test (compressed form)
# -----------------------------------------------------------------------------


def test_opcode_uniqueness():
    seen = set()
    for mnemonic, meta in OPCODES.items():
        t = meta.type
        if t == "maskable":
            for s in (0, 1):
                for m in range(32):
                    code = make_masked_opcode(mnemonic, s, m)
                    assert code not in seen, f"Duplicate masked opcode {oct(code)}"
                    seen.add(code)
        elif t == "unmasked":
            for s in (0, 1):
                for a, b, c in itertools.product((0, 1), repeat=3):
                    code = make_unmasked_opcode(mnemonic, s, a, b, c)
                    assert code not in seen, f"Duplicate unmasked opcode {oct(code)}"
                    seen.add(code)
        elif t == "peripheral":
            for p in range(64):
                code = make_peripheral_opcode(mnemonic, p)
                assert code not in seen, f"Duplicate peripheral opcode {oct(code)}"
                seen.add(code)
        elif t == "print":
            # Only cover PRA domain (others overlap)
            if mnemonic == "PRA":
                for s in (0, 1):
                    for a, b, c in itertools.product((0, 1), repeat=3):
                        code = make_print_opcode(mnemonic, s, a, b, c)
                        assert code not in seen, f"Duplicate print opcode {oct(code)}"
                        seen.add(code)
        elif t == "simulator":
            for code in (0o0007, 0o4007):
                assert code not in seen, f"Duplicate simulator opcode {oct(code)}"
                seen.add(code)
    assert seen, "No opcodes generated"


# End
