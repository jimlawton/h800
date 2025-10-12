"""
Protocol and metadata conformance tests for Honeywell H-800/H-1800 opcode definitions.

These tests ensure:
1. Every entry in OPCODES structurally conforms to the OpcodeMeta protocol
   (required attributes and their types/ranges).
2. Opcode field values are within documented numeric limits.
3. Masked/unmasked/peripheral/print/simulator classification is valid.
4. Factory helpers produce Instruction instances with expected encoding for a sample set.
"""

from __future__ import annotations

import itertools

import pytest

from h800.instruction import (
    Instruction,
    build_masked,
    build_peripheral,
    build_print,
    build_simulator,
    build_unmasked,
)
from h800.instructions import (
    OPCODES,
    make_masked_opcode,
    make_peripheral_opcode,
    make_print_opcode,
    make_unmasked_opcode,
)

# Allowed instruction type tags
ALLOWED_TYPES = {"unmasked", "maskable", "peripheral", "print", "simulator"}

# Numeric bounds (mirroring instruction.py constants)
MASK_MAX = 31
PADDR_MAX = 63
BITS23_MAX = 3
OPCODE_MAX = 31


def test_opcode_meta_presence_and_types():
    """
    Ensure every metadata object in OPCODES exposes required attributes with correct types
    and ranges. This is a structural (duck-typing) check for the OpcodeMeta protocol.
    """
    assert OPCODES, "OPCODES dictionary is empty"

    for mnemonic, meta in OPCODES.items():
        # Attribute existence
        for attr in ("m", "b23", "b7", "op", "type"):
            assert hasattr(meta, attr), f"Metadata for {mnemonic} missing attribute '{attr}'"

        # Types
        assert isinstance(meta.m, str) and meta.m == mnemonic, f"Mnemonic mismatch for {mnemonic}"
        assert (meta.b23 is None) or (isinstance(meta.b23, int) and 0 <= meta.b23 <= BITS23_MAX), (
            f"b23 invalid for {mnemonic}: {meta.b23}"
        )
        assert (meta.b7 is None) or (isinstance(meta.b7, int) and meta.b7 in (0, 1)), (
            f"b7 invalid for {mnemonic}: {meta.b7}"
        )
        assert isinstance(meta.op, int) and 0 <= meta.op <= OPCODE_MAX, (
            f"op out of range for {mnemonic}: {meta.op}"
        )
        assert isinstance(meta.type, str) and meta.type in ALLOWED_TYPES, (
            f"type invalid for {mnemonic}: {meta.type}"
        )

        # Basic classification sanity
        if meta.type == "maskable":
            assert meta.b7 == 1, f"Maskable instruction {mnemonic} must have b7 == 1"
        elif meta.type == "unmasked":
            assert meta.b7 == 0, f"Unmasked instruction {mnemonic} must have b7 == 0"
        elif meta.type in ("peripheral", "print"):
            assert meta.b7 == 1, f"{meta.type} instruction {mnemonic} must have b7 == 1"
        elif meta.type == "simulator":
            # Simulator may have b7 None
            assert meta.op == 0o07, f"Simulator base opcode unexpected for {mnemonic}"


def test_opcode_meta_protocol_conformance():
    """
    Check that each metadata object satisfies the OpcodeMeta Protocol structurally.
    (Runtime Protocol checks are shallow; we simulate by verifying attribute mapping.)
    """
    required = {"m": str, "b23": (int, type(None)), "b7": (int, type(None)), "op": int, "type": str}
    for mnemonic, meta in OPCODES.items():
        for attr, typespec in required.items():
            val = getattr(meta, attr, None)
            if isinstance(typespec, tuple):
                assert isinstance(val, typespec), f"{mnemonic}.{attr} has wrong type {type(val)}"
            else:
                assert isinstance(val, typespec), (
                    f"{mnemonic}.{attr} expected {typespec} got {type(val)}"
                )


def test_factory_build_masked_vs_direct_encoding_sample():
    """
    Sample a subset of mask values for a maskable instruction and compare factory result
    with raw encoding helper.
    """
    maskable = [m for m, meta in OPCODES.items() if meta.type == "maskable"]
    assert maskable, "No maskable mnemonics found"

    sample_mnemonic = maskable[0]
    for sequence in (0, 1):
        for mask in (0, 1, MASK_MAX):
            inst = build_masked(OPCODES[sample_mnemonic], sequence, mask)
            expected = make_masked_opcode(sample_mnemonic, sequence, mask)
            assert inst.value == expected, (
                f"Factory masked mismatch for {sample_mnemonic} seq={sequence} mask={mask}"
            )


def test_factory_build_unmasked_vs_direct_encoding_sample():
    """
    Compare unmasked factory output against direct encoding for a representative mnemonic.
    """
    unmasked = [m for m, meta in OPCODES.items() if meta.type == "unmasked"]
    assert unmasked, "No unmasked mnemonics found"

    sample_mnemonic = unmasked[0]
    for sequence in (0, 1):
        for a, b, c in itertools.product((0, 1), repeat=3):
            inst = build_unmasked(OPCODES[sample_mnemonic], sequence, a, b, c)
            expected = make_unmasked_opcode(sample_mnemonic, sequence, a, b, c)
            assert inst.value == expected, (
                f"Factory unmasked mismatch for {sample_mnemonic} seq={sequence} a={a} b={b} c={c}"
            )


def test_factory_build_peripheral_vs_direct_encoding_sample():
    peripherals = [m for m, meta in OPCODES.items() if meta.type == "peripheral"]
    assert peripherals, "No peripheral mnemonics found"

    sample_mnemonic = peripherals[0]
    for paddr in (0, 1, PADDR_MAX):
        inst = build_peripheral(OPCODES[sample_mnemonic], paddr)
        expected = make_peripheral_opcode(sample_mnemonic, paddr)
        assert inst.value == expected, (
            f"Peripheral factory mismatch {sample_mnemonic} paddr={paddr}"
        )


def test_factory_build_print_vs_direct_encoding_sample():
    prints = [m for m, meta in OPCODES.items() if meta.type == "print"]
    assert prints, "No print mnemonics found"

    # PRA / PRD / PRO share opcode space; test PRA only
    sample_mnemonic = "PRA" if "PRA" in prints else prints[0]
    for sequence in (0, 1):
        for a, b, c in itertools.product((0, 1), repeat=3):
            inst = build_print(OPCODES[sample_mnemonic], sequence, a, b, c)
            expected = make_print_opcode(sample_mnemonic, sequence, a, b, c)
            assert inst.value == expected, (
                f"Print factory mismatch {sample_mnemonic} seq={sequence} a={a} b={b} c={c}"
            )


def test_factory_build_simulator_values():
    sims = [m for m, meta in OPCODES.items() if meta.type == "simulator"]
    assert sims, "No simulator mnemonics found"
    mnem = sims[0]

    for sequence, expected in [(0, 0o0007), (1, 0o4007)]:
        inst = build_simulator(OPCODES[mnem], sequence)
        assert inst.value == expected, f"Simulator factory mismatch {mnem} seq={sequence}"


def test_instruction_instance_type():
    """
    Factories must return Instruction instances.
    """
    # Pick one of each category if available
    categories = {
        "maskable": None,
        "unmasked": None,
        "peripheral": None,
        "print": None,
        "simulator": None,
    }
    for m, meta in OPCODES.items():
        if categories.get(meta.type) is None:
            categories[meta.type] = m
    # Build sample instructions
    if categories["maskable"]:
        inst = build_masked(OPCODES[categories["maskable"]], 0, 0)
        assert isinstance(inst, Instruction)
    if categories["unmasked"]:
        inst = build_unmasked(OPCODES[categories["unmasked"]], 0, 0, 0, 0)
        assert isinstance(inst, Instruction)
    if categories["peripheral"]:
        inst = build_peripheral(OPCODES[categories["peripheral"]], 0)
        assert isinstance(inst, Instruction)
    if categories["print"]:
        inst = build_print(OPCODES[categories["print"]], 0, 0, 0, 0)
        assert isinstance(inst, Instruction)
    if categories["simulator"]:
        inst = build_simulator(OPCODES[categories["simulator"]], 0)
        assert isinstance(inst, Instruction)


def test_mask_and_operands_mutual_exclusion_maskable():
    """Ensure using both mask and operands simultaneously results in expected validation behavior."""
    maskable = [m for m, meta in OPCODES.items() if meta.type == "maskable"]
    if not maskable:
        pytest.skip("No maskable instructions")
    mnem = maskable[0]
    # Valid with mask only
    inst = Instruction(opcode_meta=OPCODES[mnem], sequence=0, mask=0)
    assert inst.value == make_masked_opcode(mnem, 0, 0)
    # Valid with operands only (treated as unmasked)
    inst2 = Instruction(opcode_meta=OPCODES[mnem], sequence=0, operands=(1, 0, 1))
    assert inst2.value == make_unmasked_opcode(mnem, 0, 1, 0, 1)
    # Supplying both should still generate masked form (operands ignored) or raise; verify current behavior
    inst3 = Instruction(opcode_meta=OPCODES[mnem], sequence=1, mask=3, operands=(1, 1, 1))
    assert inst3.value == make_masked_opcode(mnem, 1, 3)


def test_peripheral_address_range():
    peripherals = [m for m, meta in OPCODES.items() if meta.type == "peripheral"]
    if not peripherals:
        pytest.skip("No peripheral instructions")
    mnem = peripherals[0]
    # Valid extremes
    assert build_peripheral(OPCODES[mnem], 0).value == make_peripheral_opcode(mnem, 0)
    assert build_peripheral(OPCODES[mnem], PADDR_MAX).value == make_peripheral_opcode(
        mnem, PADDR_MAX
    )
    # Invalid
    with pytest.raises(ValueError):
        build_peripheral(OPCODES[mnem], -1)
    with pytest.raises(ValueError):
        build_peripheral(OPCODES[mnem], PADDR_MAX + 1)


def test_mask_range_validation():
    maskable = [m for m, meta in OPCODES.items() if meta.type == "maskable"]
    if not maskable:
        pytest.skip("No maskable instructions")
    mnem = maskable[0]
    # Valid bounds
    assert build_masked(OPCODES[mnem], 0, 0).value == make_masked_opcode(mnem, 0, 0)
    assert build_masked(OPCODES[mnem], 1, MASK_MAX).value == make_masked_opcode(mnem, 1, MASK_MAX)
    # Invalid
    with pytest.raises(ValueError):
        build_masked(OPCODES[mnem], 0, -1)
    with pytest.raises(ValueError):
        build_masked(OPCODES[mnem], 0, MASK_MAX + 1)


def test_operand_flag_validation():
    unmasked = [m for m, meta in OPCODES.items() if meta.type == "unmasked"]
    if not unmasked:
        pytest.skip("No unmasked instructions")
    mnem = unmasked[0]
    # Valid
    assert build_unmasked(OPCODES[mnem], 0, 0, 0, 0).value == make_unmasked_opcode(mnem, 0, 0, 0, 0)
    # Invalid a flag
    with pytest.raises(ValueError):
        build_unmasked(OPCODES[mnem], 0, 2, 0, 0)


def test_simulator_sequence_variants():
    sims = [m for m, meta in OPCODES.items() if meta.type == "simulator"]
    if not sims:
        pytest.skip("No simulator instructions")
    mnem = sims[0]
    assert build_simulator(OPCODES[mnem], 0).value == 0o0007
    assert build_simulator(OPCODES[mnem], 1).value == 0o4007
    with pytest.raises(ValueError):
        # Invalid sequence
        Instruction(opcode_meta=OPCODES[mnem], sequence=2)


def test_opcode_uniqueness_collision_check_subset():
    """
    Basic uniqueness sanity: collect a subset of generated codes (not exhaustive, full coverage
    handled in test_instructions.py) to ensure no immediate collisions in sampled space.
    """
    seen = set()
    sample_maskable = [m for m, meta in OPCODES.items() if meta.type == "maskable"][:2]
    sample_unmasked = [m for m, meta in OPCODES.items() if meta.type == "unmasked"][:2]
    sample_peripheral = [m for m, meta in OPCODES.items() if meta.type == "peripheral"][:1]
    sample_print = ["PRA"] if "PRA" in OPCODES else []
    sample_sim = [m for m, meta in OPCODES.items() if meta.type == "simulator"][:1]

    for m in sample_maskable:
        for s in (0, 1):
            for mask in (0, MASK_MAX):
                code = make_masked_opcode(m, s, mask)
                assert code not in seen, f"Collision masked {m} {oct(code)}"
                seen.add(code)

    for m in sample_unmasked:
        for s in (0, 1):
            for a, b, c in itertools.product((0, 1), repeat=3):
                code = make_unmasked_opcode(m, s, a, b, c)
                assert code not in seen, f"Collision unmasked {m} {oct(code)}"
                seen.add(code)

    for m in sample_peripheral:
        for p in (0, PADDR_MAX):
            code = make_peripheral_opcode(m, p)
            assert code not in seen, f"Collision peripheral {m} {oct(code)}"
            seen.add(code)

    for m in sample_print:
        for s in (0, 1):
            for a, b, c in itertools.product((0, 1), repeat=3):
                code = make_print_opcode(m, s, a, b, c)
                assert code not in seen, f"Collision print {m} {oct(code)}"
                seen.add(code)

    for m in sample_sim:
        for sequence in (0, 1):
            inst = build_simulator(OPCODES[m], sequence)
            code = inst.value
            assert code not in seen, f"Collision simulator {m} {oct(code)}"
            seen.add(code)

    assert seen, "No opcodes sampled"


def test_opcode_meta_runtime_protocol_check():
    """
    Perform a shallow runtime protocol check: ensure each metadata object would be acceptable
    as an OpcodeMeta by verifying required attributes via getattr (already done above).
    This test exists mostly for clarity; it reuses the structural approach.
    """
    for _, meta in OPCODES.items():
        # Simulate protocol acceptance
        for attr in ("m", "b23", "b7", "op", "type"):
            getattr(meta, attr)  # Should not raise
        assert isinstance(meta.m, str)
        assert isinstance(meta.op, int)
        assert isinstance(meta.type, str)


def test_instruction_repr_contains_mnemonic_and_octal():
    unmasked = [m for m, meta in OPCODES.items() if meta.type == "unmasked"]
    if not unmasked:
        pytest.skip("No unmasked instructions for repr test")
    mnem = unmasked[0]
    inst = build_unmasked(OPCODES[mnem], 0, 0, 0, 0)
    rep = repr(inst)
    assert mnem in rep
    assert "0o" in rep


def test_factories_reject_invalid_meta_object():
    """
    Pass a dummy object missing required attributes to ensure failure.
    """

    class Dummy:
        pass

    dummy = Dummy()
    with pytest.raises(AttributeError):
        # Construction raises when accessing missing attributes in Instruction.__post_init__
        Instruction(opcode_meta=dummy, sequence=0)


def test_maskable_vs_unmasked_encoding_difference():
    """
    Ensure a maskable mnemonic produces different code when using mask vs operands.
    """
    maskable = [m for m, meta in OPCODES.items() if meta.type == "maskable"]
    if not maskable:
        pytest.skip("No maskable instructions")
    mnem = maskable[0]
    masked_code = build_masked(OPCODES[mnem], sequence=0, mask=3).value
    unmasked_code = build_unmasked(OPCODES[mnem], sequence=0, a=1, b=0, c=1).value
    assert masked_code != unmasked_code, "Masked and unmasked encodings unexpectedly identical"


def test_print_opcode_overlap():
    """
    PRA / PRD / PRO share encoding space. Confirm collisions when generating same flag set.
    """
    required = {"PRA", "PRD", "PRO"}.intersection(OPCODES.keys())
    if len(required) < 2:
        pytest.skip("Insufficient print mnemonics for overlap test")
    codes = {}
    for m in required:
        code = make_print_opcode(m, 0, 0, 0, 0)
        codes.setdefault(code, []).append(m)
    # At least one code should map to multiple mnemonics
    assert any(len(v) > 1 for v in codes.values()), (
        "Expected overlapping print opcode space not found"
    )
