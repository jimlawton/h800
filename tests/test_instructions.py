"""Compact parametrized tests for Honeywell H-800/H-1800 instruction encoding (factory-based)."""

from __future__ import annotations

import itertools

import pytest

from h800.instruction import (
    decode_instruction,
    get_instruction,
)
from h800.instructions import build_constant
from h800.opcodes import (
    OPCODES,
    make_masked_opcode,
    make_peripheral_opcode,
    make_print_opcode,
    make_unmasked_opcode,
)

# -----------------------------------------------------------------------------
# Positive encoding tests using unified get_instruction factory + OPCODES metadata
# -----------------------------------------------------------------------------

MASKABLE_MNEMONICS = [
    "BA",
    "DA",
    "WA",
    "BS",
    "DS",
    "WD",
    "NA",
    "NN",
    "LA",
    "LN",
    "TX",
    "TS",
    "HA",
    "SM",
    "CP",
]
UNMASKED_MNEMONICS = [
    "BA",
    "DA",
    "WA",
    "BS",
    "DS",
    "WD",
    "NA",
    "NN",
    "LA",
    "LN",
    "TX",
    "TS",
    "HA",
    "SM",
    "CP",
]
PERIPHERAL_MNEMONICS = ["RF", "RB", "WF", "RW"]
PRINT_MNEMONICS = ["PRA", "PRD", "PRO"]
SIMULATOR_MNEMONICS = ["S"]

CONSTANT_MNEMONICS = ["ALF", "DEC", "EBC", "FLBIN", "FLDEC", "FXBIN", "OCT"]

# Build parameter sets

MASKED_PARAMS = [
    (mnemonic, {"sequence": s, "mask": m}, make_masked_opcode(mnemonic, s, m))
    for mnemonic in MASKABLE_MNEMONICS
    for s in (0, 1)
    for m in (0, 1, 31)
]

UNMASKED_PARAMS = [
    (mnemonic, {"sequence": s, "a": a, "b": b, "c": c}, make_unmasked_opcode(mnemonic, s, a, b, c))
    for mnemonic in UNMASKED_MNEMONICS
    for s in (0, 1)
    for a, b, c in itertools.product((0, 1), repeat=3)
]

PERIPHERAL_PARAMS = [
    (mnemonic, {"paddr": p}, make_peripheral_opcode(mnemonic, p))
    for mnemonic in PERIPHERAL_MNEMONICS
    for p in (0, 1, 63)
]

PRINT_PARAMS = [
    (mnemonic, {"sequence": s, "a": a, "b": b, "c": c}, make_print_opcode(mnemonic, s, a, b, c))
    for mnemonic in PRINT_MNEMONICS
    for s in (0, 1)
    for a, b, c in itertools.product((0, 1), repeat=3)
]

SIMULATOR_PARAMS = [
    ("S", {"sequence": 0}, 0o0007),
    ("S", {"sequence": 1}, 0o4007),
]

CONSTANT_VALUES = (0, 1, 4095, 4096, 2**48 - 1)
CONSTANT_PARAMS = [(m, v) for m in CONSTANT_MNEMONICS for v in CONSTANT_VALUES]

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


@pytest.mark.parametrize("mnemonic,kwargs,expected", MASKED_PARAMS)
def test_maskable(mnemonic, kwargs, expected):
    inst = get_instruction(mnemonic, **kwargs)
    assert inst.value == expected


@pytest.mark.parametrize("mnemonic,kwargs,expected", UNMASKED_PARAMS)
def test_unmaskable(mnemonic, kwargs, expected):
    inst = get_instruction(mnemonic, **kwargs)
    assert inst.value == expected


@pytest.mark.parametrize("mnemonic,kwargs,expected", PERIPHERAL_PARAMS)
def test_peripheral(mnemonic, kwargs, expected):
    inst = get_instruction(mnemonic, **kwargs)
    assert inst.value == expected


@pytest.mark.parametrize("mnemonic,kwargs,expected", PRINT_PARAMS)
def test_print(mnemonic, kwargs, expected):
    inst = get_instruction(mnemonic, **kwargs)
    assert inst.value == expected


@pytest.mark.parametrize("mnemonic,kwargs,expected", SIMULATOR_PARAMS)
def test_simulator(mnemonic, kwargs, expected):
    inst = get_instruction(mnemonic, **kwargs)
    assert inst.value == expected


@pytest.mark.parametrize("mnemonic,value", CONSTANT_PARAMS)
def test_constants(mnemonic, value):
    const = build_constant(mnemonic, value)
    assert const.value == value


# -----------------------------------------------------------------------------
# Negative / invalid argument tests (get_instruction-driven)
# -----------------------------------------------------------------------------

INVALID_MASKED = [
    ("BA", {"sequence": 0, "mask": 32}),
    ("BA", {"sequence": 2, "mask": 0}),
    ("BS", {"sequence": 0, "mask": 32}),
    ("WA", {"sequence": 1, "mask": -1}),
    ("DA", {"sequence": 0, "mask": 99}),
]


@pytest.mark.parametrize("mnemonic,kwargs", INVALID_MASKED)
def test_invalid_masked(mnemonic, kwargs):
    with pytest.raises(ValueError):
        get_instruction(mnemonic, **kwargs)


INVALID_UNMASKED = [
    ("BA", {"sequence": 2, "a": 0, "b": 0, "c": 0}),
    ("BA", {"sequence": 0, "a": 2, "b": 0, "c": 0}),
    ("BA", {"sequence": 0, "a": 1, "b": 2, "c": 3}),
    ("DS", {"sequence": 0, "a": 0, "b": 0, "c": 2}),
]


@pytest.mark.parametrize("mnemonic,kwargs", INVALID_UNMASKED)
def test_invalid_unmasked(mnemonic, kwargs):
    with pytest.raises(ValueError):
        get_instruction(mnemonic, **kwargs)


INVALID_PERIPHERAL = [
    ("RF", {"paddr": -1}),
    ("RF", {"paddr": 64}),
    ("RB", {"paddr": 999}),
]


@pytest.mark.parametrize("mnemonic,kwargs", INVALID_PERIPHERAL)
def test_invalid_peripheral(mnemonic, kwargs):
    with pytest.raises(ValueError):
        get_instruction(mnemonic, **kwargs)


INVALID_PRINT = [
    ("PRA", {"sequence": 2, "a": 0, "b": 0, "c": 0}),
    ("PRA", {"sequence": 0, "a": 2, "b": 0, "c": 0}),
]


@pytest.mark.parametrize("mnemonic,kwargs", INVALID_PRINT)
def test_invalid_print(mnemonic, kwargs):
    with pytest.raises(ValueError):
        get_instruction(mnemonic, **kwargs)


INVALID_CONSTANTS = [
    ("ALF", -1),
    ("ALF", 2**48),
    ("DEC", -5),
    ("FLBIN", 2**48),
]


@pytest.mark.parametrize("mnemonic,value", INVALID_CONSTANTS)
def test_invalid_constants(mnemonic, value):
    with pytest.raises(ValueError):
        build_constant(mnemonic, value)


def test_proceed_opcode():
    # Proceed mnemonic PR
    inst = get_instruction("PR", sequence=0, a=0, b=0, c=0)
    assert inst.value == 0


# -----------------------------------------------------------------------------
# Uniqueness test
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


# -----------------------------------------------------------------------------
# Reverse decode (disassembly) tests
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "mnemonic,kwargs",
    [
        ("BA", {"sequence": 1, "mask": 0}),  # Masked form
        ("BA", {"sequence": 0, "a": 1, "b": 0, "c": 1}),  # Unmasked form
        ("RF", {"paddr": 0}),  # Peripheral
        ("PRA", {"sequence": 1, "a": 1, "b": 1, "c": 0}),  # Print (colliding space)
        ("S", {"sequence": 0}),  # Simulator
    ],
)
def test_decode_roundtrip(mnemonic, kwargs):
    inst = get_instruction(mnemonic, **kwargs)
    info = decode_instruction(inst.value, OPCODES)
    assert mnemonic in info["mnemonics"], f"{mnemonic} missing in decode candidates {info}"
    # Basic field consistency for one representative (first candidate)
    if mnemonic == "RF":
        assert "paddr" in info["fields"]
        assert info["fields"]["paddr"] == kwargs["paddr"]
    elif mnemonic == "S":
        assert info["fields"]["sequence"] == kwargs["sequence"]
    elif mnemonic in ("PRA", "PRD", "PRO"):
        # Collision space; PRA chosen but others possible
        assert set(info["mnemonics"]).issuperset({"PRA", "PRD", "PRO"})
    elif "mask" in kwargs:
        assert info["fields"]["mask"] == kwargs["mask"]
    else:
        for f in ("a", "b", "c"):
            if f in kwargs:
                assert info["fields"][f] == kwargs[f]


def test_decode_print_collision():
    # All three print mnemonics share opcode space; decode should list all.
    inst = get_instruction("PRA", sequence=0, a=1, b=0, c=1)
    info = decode_instruction(inst.value, OPCODES)
    assert set(info["mnemonics"]) == {"PRA", "PRD", "PRO"}
    assert info["fields"]["a"] == 1
    assert info["fields"]["c"] == 1


def test_decode_invalid_word():
    with pytest.raises(ValueError):
        decode_instruction(0o10000, OPCODES)  # Outside 12-bit range


# End
