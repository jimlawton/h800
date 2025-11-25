"""
Test module for H-1800 opcode metadata.

Tests the opcode metadata structure and lookup functions.
"""

import pytest

from h1800.opcodes import (
    OPCODES,
    OPCODES_BY_CODE,
    OpcodeMetadata,
    get_categories,
    get_opcode,
    list_opcodes_by_category,
    lookup_opcode,
)


def test_opcode_metadata_structure():
    """Test that opcode metadata has the expected structure."""
    # Check that we have opcodes defined
    assert len(OPCODES) > 0

    # Check a few known opcodes
    assert "BA" in OPCODES
    assert "TX" in OPCODES
    assert "RF" in OPCODES
    assert "PRA" in OPCODES

    # Check metadata structure
    ba = OPCODES["BA"]
    assert isinstance(ba, OpcodeMetadata)
    assert ba.mnemonic == "BA"
    assert ba.name == "Binary Add"
    assert ba.opcode == 0o11
    assert ba.type == "maskable"
    assert ba.category == "arithmetic"
    assert ba.cycles >= 1


def test_maskable_instructions():
    """Test maskable instruction metadata."""
    maskable = [
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

    for mnemonic in maskable:
        meta = OPCODES[mnemonic]
        assert meta.type == "maskable"
        assert meta.bit7 == 1
        assert meta.variant == 0b10


def test_unmasked_instructions():
    """Test unmasked instruction metadata."""
    unmasked = ["BM", "DM", "MT", "TN", "CC", "IT", "PR", "MPC"]

    for mnemonic in unmasked:
        meta = OPCODES[mnemonic]
        assert meta.type == "unmasked"
        assert meta.bit7 == 0
        assert meta.variant is not None


def test_peripheral_instructions():
    """Test peripheral instruction metadata."""
    peripheral = ["RF", "RB", "WF", "RW"]

    for mnemonic in peripheral:
        meta = OPCODES[mnemonic]
        assert meta.type == "peripheral"
        assert meta.bit7 == 1
        assert meta.category == "peripheral"


def test_print_instructions():
    """Test print instruction metadata."""
    print_instructions = ["PRA", "PRD", "PRO"]

    for mnemonic in print_instructions:
        meta = OPCODES[mnemonic]
        assert meta.type == "print"
        assert meta.bit7 == 1
        assert meta.category == "print"
        assert meta.opcode == 0o06  # All share same opcode


def test_scientific_instructions():
    """Test scientific (floating-point) instruction metadata."""
    scientific = ["FBA", "FBS", "FBM", "FBD", "FDA", "FDS", "FDM", "FDD"]

    for mnemonic in scientific:
        meta = OPCODES[mnemonic]
        assert meta.category == "scientific"
        assert meta.type == "unmasked"


def test_get_opcode():
    """Test get_opcode lookup function."""
    # Test valid opcodes
    ba = get_opcode("BA")
    assert ba is not None
    assert ba.mnemonic == "BA"

    # Test invalid opcode
    invalid = get_opcode("INVALID")
    assert invalid is None


def test_lookup_opcode():
    """Test reverse opcode lookup."""
    # Test maskable instruction (masked form)
    # BA: opcode=0o11, bit7=1 (masked)
    results = lookup_opcode(0o11, 1, None)
    assert len(results) > 0
    mnemonics = [r.mnemonic for r in results]
    assert "BA" in mnemonics

    # Test maskable instruction (unmasked form)
    # BA: opcode=0o11, bit7=0, variant=0b10
    results = lookup_opcode(0o11, 0, 0b10)
    assert len(results) > 0
    mnemonics = [r.mnemonic for r in results]
    assert "BA" in mnemonics

    # Test unmasked instruction
    # BM: opcode=0o13, bit7=0, variant=0b00
    results = lookup_opcode(0o13, 0, 0b00)
    assert len(results) > 0
    mnemonics = [r.mnemonic for r in results]
    assert "BM" in mnemonics

    # Test peripheral instruction
    # RF: opcode=0o32, bit7=1
    results = lookup_opcode(0o32, 1, None)
    assert len(results) > 0
    mnemonics = [r.mnemonic for r in results]
    assert "RF" in mnemonics

    # Test print instruction (all three share same opcode)
    # PRA/PRD/PRO: opcode=0o06, bit7=1
    results = lookup_opcode(0o06, 1, None)
    assert len(results) >= 3
    mnemonics = [r.mnemonic for r in results]
    assert "PRA" in mnemonics or "PRD" in mnemonics or "PRO" in mnemonics


def test_get_categories():
    """Test category enumeration."""
    categories = get_categories()
    assert isinstance(categories, list)
    assert len(categories) > 0

    # Check for expected categories
    expected = ["arithmetic", "transfer", "comparison", "peripheral", "scientific"]
    for cat in expected:
        assert cat in categories


def test_list_opcodes_by_category():
    """Test listing opcodes by category."""
    # Test arithmetic category
    arithmetic = list_opcodes_by_category("arithmetic")
    assert len(arithmetic) > 0
    mnemonics = [m.mnemonic for m in arithmetic]
    assert "BA" in mnemonics
    assert "BS" in mnemonics

    # Test transfer category
    transfer = list_opcodes_by_category("transfer")
    assert len(transfer) > 0
    mnemonics = [m.mnemonic for m in transfer]
    assert "TX" in mnemonics
    assert "MT" in mnemonics

    # Test peripheral category
    peripheral = list_opcodes_by_category("peripheral")
    assert len(peripheral) > 0
    mnemonics = [m.mnemonic for m in peripheral]
    assert "RF" in mnemonics

    # Test empty category
    empty = list_opcodes_by_category("nonexistent")
    assert len(empty) == 0


def test_opcode_metadata_matches():
    """Test OpcodeMetadata.matches() method."""
    ba = get_opcode("BA")

    # Test masked form match
    assert ba.matches(0o11, 1, None)

    # Test unmasked form match
    assert ba.matches(0o11, 0, 0b10)

    # Test non-match (wrong opcode)
    assert not ba.matches(0o20, 1, None)

    # Test non-match (wrong bit7)
    bm = get_opcode("BM")
    assert not bm.matches(0o13, 1, None)  # BM needs bit7=0


def test_reverse_lookup_structure():
    """Test that reverse lookup structure is properly built."""
    assert len(OPCODES_BY_CODE) > 0

    # Check that some expected keys exist
    # Maskable instructions should have entries for both masked and unmasked
    assert (0o11, 1, None) in OPCODES_BY_CODE  # BA masked
    assert (0o11, 0, 0b10) in OPCODES_BY_CODE  # BA unmasked

    # Peripheral instructions
    assert (0o32, 1, None) in OPCODES_BY_CODE  # RF

    # Print instructions (collision - multiple mnemonics)
    print_key = (0o06, 1, None)
    assert print_key in OPCODES_BY_CODE
    print_opcodes = OPCODES_BY_CODE[print_key]
    print_mnemonics = [op.mnemonic for op in print_opcodes]
    # Should include PRA, PRD, PRO
    assert len(print_mnemonics) >= 3


def test_cycle_counts():
    """Test that cycle counts are reasonable."""
    # Simple instructions should have low cycle counts
    assert get_opcode("BA").cycles <= 2
    assert get_opcode("TX").cycles <= 2

    # Multiply/divide should have higher cycle counts
    assert get_opcode("BM").cycles >= 2
    assert get_opcode("FBD").cycles >= 5

    # I/O operations should have high cycle counts
    assert get_opcode("RF").cycles >= 10
    assert get_opcode("RW").cycles >= 100


def test_all_opcodes_valid():
    """Test that all opcodes have valid metadata."""
    for mnemonic, meta in OPCODES.items():
        # Check required fields
        assert meta.mnemonic == mnemonic
        assert meta.name is not None and len(meta.name) > 0
        assert 0 <= meta.opcode <= 0o37
        assert meta.type in ["maskable", "unmasked", "peripheral", "print", "simulator"]
        assert meta.category is not None and len(meta.category) > 0
        assert meta.cycles >= 1

        # Check type-specific constraints
        if meta.type == "maskable":
            assert meta.bit7 == 1
            assert meta.variant == 0b10
        elif meta.type == "unmasked":
            assert meta.bit7 == 0
            assert meta.variant is not None
        elif meta.type == "peripheral":
            assert meta.bit7 == 1
            assert meta.variant is None
        elif meta.type == "print":
            assert meta.bit7 == 1
            assert meta.variant is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
