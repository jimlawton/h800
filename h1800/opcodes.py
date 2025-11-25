"""
H-1800 Opcode Metadata Module
===============================

This module provides opcode metadata in a neutral structure that can be
reused by both the decoder and executor.

The metadata is ported from h800.opcodes but restructured for simulation
purposes rather than assembly/encoding.

Opcode Metadata Structure:
    mnemonic: Instruction mnemonic (e.g., "BA", "TX", "RF")
    name: Full instruction name
    opcode: Base opcode value (bits 8-12)
    type: Instruction type ("maskable", "unmasked", "peripheral", "print", "simulator")
    variant: Variant bits (bits 2-3) for unmasked instructions
    bit7: Expected value of bit 7 (0 or 1)
    category: Instruction category for executor dispatch
    cycles: Typical execution cycles (for timing simulation)
    description: Brief description of operation

Key Components:
    OpcodeMetadata  - Dataclass for opcode metadata
    OPCODES         - Dictionary mapping mnemonics to metadata
    OPCODES_BY_CODE - Reverse mapping for decoder
"""

from dataclasses import dataclass


@dataclass
class OpcodeMetadata:
    """
    Metadata for a single opcode.

    Attributes:
        mnemonic: Instruction mnemonic (e.g., "BA", "TX")
        name: Full instruction name
        opcode: Base opcode value (bits 8-12, 0-31)
        type: Instruction type
        variant: Variant bits (bits 2-3) for unmasked, None otherwise
        bit7: Expected value of bit 7 (0=unmasked, 1=masked/peripheral/print)
        category: Instruction category for executor dispatch
        cycles: Typical execution cycles
        description: Brief operation description
    """

    mnemonic: str
    name: str
    opcode: int
    type: str = "unmasked"
    variant: int | None = None
    bit7: int | None = None
    category: str = "general"
    cycles: int = 1
    description: str = ""

    def matches(self, opcode: int, bit7: int, variant: int | None = None) -> bool:
        """
        Check if this metadata matches the given instruction fields.

        Args:
            opcode: Opcode value (bits 8-12)
            bit7: Value of bit 7
            variant: Variant bits (bits 2-3) for unmasked instructions

        Returns:
            True if this metadata matches the instruction fields
        """
        if self.opcode != opcode:
            return False

        if self.bit7 is not None and self.bit7 != bit7:
            return False

        if self.type == "unmasked" and variant is not None:
            if self.variant is not None and self.variant != variant:
                return False

        return True


# =============================================================================
# Opcode Metadata Definitions
# =============================================================================

OPCODES = {
    # -------------------------------------------------------------------------
    # Maskable Instructions (bit7=1 when masked, variant=0b10 when unmasked)
    # -------------------------------------------------------------------------
    "BA": OpcodeMetadata(
        mnemonic="BA",
        name="Binary Add",
        opcode=0o11,
        type="maskable",
        variant=0b10,
        bit7=1,
        category="arithmetic",
        cycles=1,
        description="Binary addition with optional masking",
    ),
    "DA": OpcodeMetadata(
        mnemonic="DA",
        name="Decimal Add",
        opcode=0o01,
        type="maskable",
        variant=0b10,
        bit7=1,
        category="arithmetic",
        cycles=1,
        description="Decimal addition with optional masking",
    ),
    "WA": OpcodeMetadata(
        mnemonic="WA",
        name="Word Add",
        opcode=0o15,
        type="maskable",
        variant=0b10,
        bit7=1,
        category="arithmetic",
        cycles=1,
        description="Word addition with optional masking",
    ),
    "BS": OpcodeMetadata(
        mnemonic="BS",
        name="Binary Subtract",
        opcode=0o31,
        type="maskable",
        variant=0b10,
        bit7=1,
        category="arithmetic",
        cycles=1,
        description="Binary subtraction with optional masking",
    ),
    "DS": OpcodeMetadata(
        mnemonic="DS",
        name="Decimal Subtract",
        opcode=0o21,
        type="maskable",
        variant=0b10,
        bit7=1,
        category="arithmetic",
        cycles=1,
        description="Decimal subtraction with optional masking",
    ),
    "WD": OpcodeMetadata(
        mnemonic="WD",
        name="Word Difference",
        opcode=0o35,
        type="maskable",
        variant=0b10,
        bit7=1,
        category="arithmetic",
        cycles=1,
        description="Word difference with optional masking",
    ),
    "NA": OpcodeMetadata(
        mnemonic="NA",
        name="Not Equal Alphabetic",
        opcode=0o14,
        type="maskable",
        variant=0b10,
        bit7=1,
        category="comparison",
        cycles=1,
        description="Alphabetic not-equal comparison",
    ),
    "NN": OpcodeMetadata(
        mnemonic="NN",
        name="Not Equal Numeric",
        opcode=0o10,
        type="maskable",
        variant=0b10,
        bit7=1,
        category="comparison",
        cycles=1,
        description="Numeric not-equal comparison",
    ),
    "LA": OpcodeMetadata(
        mnemonic="LA",
        name="Less Than or Equal Alphabetic",
        opcode=0o34,
        type="maskable",
        variant=0b10,
        bit7=1,
        category="comparison",
        cycles=1,
        description="Alphabetic less-than-or-equal comparison",
    ),
    "LN": OpcodeMetadata(
        mnemonic="LN",
        name="Less Than or Equal Numeric",
        opcode=0o30,
        type="maskable",
        variant=0b10,
        bit7=1,
        category="comparison",
        cycles=1,
        description="Numeric less-than-or-equal comparison",
    ),
    "TX": OpcodeMetadata(
        mnemonic="TX",
        name="Transfer",
        opcode=0o20,
        type="maskable",
        variant=0b10,
        bit7=1,
        category="transfer",
        cycles=1,
        description="Transfer data with optional masking",
    ),
    "TS": OpcodeMetadata(
        mnemonic="TS",
        name="Transfer and Change Sequence",
        opcode=0o04,
        type="maskable",
        variant=0b10,
        bit7=1,
        category="transfer",
        cycles=1,
        description="Transfer and change sequence bit",
    ),
    "HA": OpcodeMetadata(
        mnemonic="HA",
        name="Half Add",
        opcode=0o25,
        type="maskable",
        variant=0b10,
        bit7=1,
        category="arithmetic",
        cycles=1,
        description="Half add (add without carry)",
    ),
    "SM": OpcodeMetadata(
        mnemonic="SM",
        name="Superimpose",
        opcode=0o05,
        type="maskable",
        variant=0b10,
        bit7=1,
        category="logical",
        cycles=1,
        description="Superimpose (OR) operation",
    ),
    "CP": OpcodeMetadata(
        mnemonic="CP",
        name="Check Parity",
        opcode=0o24,
        type="maskable",
        variant=0b10,
        bit7=1,
        category="logical",
        cycles=1,
        description="Check parity of data",
    ),
    # -------------------------------------------------------------------------
    # Unmasked Instructions (bit7=0)
    # -------------------------------------------------------------------------
    "BM": OpcodeMetadata(
        mnemonic="BM",
        name="Binary Multiply",
        opcode=0o13,
        type="unmasked",
        variant=0b00,
        bit7=0,
        category="arithmetic",
        cycles=2,
        description="Binary multiplication",
    ),
    "DM": OpcodeMetadata(
        mnemonic="DM",
        name="Decimal Multiply",
        opcode=0o03,
        type="unmasked",
        variant=0b00,
        bit7=0,
        category="arithmetic",
        cycles=2,
        description="Decimal multiplication",
    ),
    "BT": OpcodeMetadata(
        mnemonic="BT",
        name="Binary Accumulate",
        opcode=0o13,
        type="unmasked",
        variant=0b10,
        bit7=0,
        category="arithmetic",
        cycles=2,
        description="Binary accumulate (multiply and accumulate)",
    ),
    "DT": OpcodeMetadata(
        mnemonic="DT",
        name="Decimal Accumulate",
        opcode=0o03,
        type="unmasked",
        variant=0b10,
        bit7=0,
        category="arithmetic",
        cycles=2,
        description="Decimal accumulate (multiply and accumulate)",
    ),
    "MT": OpcodeMetadata(
        mnemonic="MT",
        name="Multiple Transfer",
        opcode=0o20,
        type="unmasked",
        variant=0b00,
        bit7=0,
        category="transfer",
        cycles=2,
        description="Transfer multiple words",
    ),
    "TN": OpcodeMetadata(
        mnemonic="TN",
        name="Transfer N Words",
        opcode=0o20,
        type="unmasked",
        variant=0b01,
        bit7=0,
        category="transfer",
        cycles=2,
        description="Transfer N words",
    ),
    "CC": OpcodeMetadata(
        mnemonic="CC",
        name="Compute Orthocount",
        opcode=0o10,
        type="unmasked",
        variant=0b01,
        bit7=0,
        category="arithmetic",
        cycles=2,
        description="Compute orthocount (population count)",
    ),
    "IT": OpcodeMetadata(
        mnemonic="IT",
        name="Item Transfer",
        opcode=0o30,
        type="unmasked",
        variant=0b01,
        bit7=0,
        category="transfer",
        cycles=1,
        description="Transfer item (variable length)",
    ),
    "EBA": OpcodeMetadata(
        mnemonic="EBA",
        name="Extended Binary Add",
        opcode=0o13,
        type="unmasked",
        variant=0b11,
        bit7=0,
        category="arithmetic",
        cycles=2,
        description="Extended precision binary addition",
    ),
    "EBS": OpcodeMetadata(
        mnemonic="EBS",
        name="Extended Binary Subtract",
        opcode=0o33,
        type="unmasked",
        variant=0b11,
        bit7=0,
        category="arithmetic",
        cycles=2,
        description="Extended precision binary subtraction",
    ),
    "RT": OpcodeMetadata(
        mnemonic="RT",
        name="Record Transfer",
        opcode=0o30,
        type="unmasked",
        variant=0b11,
        bit7=0,
        category="transfer",
        cycles=2,
        description="Transfer record (block)",
    ),
    "MPC": OpcodeMetadata(
        mnemonic="MPC",
        name="Control Program",
        opcode=0o00,
        type="unmasked",
        variant=0b10,
        bit7=0,
        category="control",
        cycles=1,
        description="Program control operation",
    ),
    "PR": OpcodeMetadata(
        mnemonic="PR",
        name="Proceed",
        opcode=0o00,
        type="unmasked",
        variant=0b00,
        bit7=0,
        category="control",
        cycles=1,
        description="Proceed (no operation)",
    ),
    # -------------------------------------------------------------------------
    # Shift Instructions (inherent mask, bit7=0)
    # -------------------------------------------------------------------------
    "SWS": OpcodeMetadata(
        mnemonic="SWS",
        name="Shift Word and Substitute",
        opcode=0o06,
        type="unmasked",
        variant=0b10,
        bit7=0,
        category="shift",
        cycles=1,
        description="Shift word and substitute",
    ),
    "SPS": OpcodeMetadata(
        mnemonic="SPS",
        name="Shift Preserving Sign and Substitute",
        opcode=0o02,
        type="unmasked",
        variant=0b10,
        bit7=0,
        category="shift",
        cycles=1,
        description="Shift preserving sign and substitute",
    ),
    "SWE": OpcodeMetadata(
        mnemonic="SWE",
        name="Shift Word and Extract",
        opcode=0o16,
        type="unmasked",
        variant=0b10,
        bit7=0,
        category="shift",
        cycles=1,
        description="Shift word and extract",
    ),
    "SPE": OpcodeMetadata(
        mnemonic="SPE",
        name="Shift Preserving Sign and Extract",
        opcode=0o12,
        type="unmasked",
        variant=0b10,
        bit7=0,
        category="shift",
        cycles=1,
        description="Shift preserving sign and extract",
    ),
    "SSL": OpcodeMetadata(
        mnemonic="SSL",
        name="Shift and Select",
        opcode=0o26,
        type="unmasked",
        variant=0b10,
        bit7=0,
        category="shift",
        cycles=1,
        description="Shift and select",
    ),
    "SS": OpcodeMetadata(
        mnemonic="SS",
        name="Substitute",
        opcode=0o06,
        type="unmasked",
        variant=0b00,
        bit7=0,
        category="shift",
        cycles=1,
        description="Substitute (no shift)",
    ),
    "EX": OpcodeMetadata(
        mnemonic="EX",
        name="Extract",
        opcode=0o16,
        type="unmasked",
        variant=0b00,
        bit7=0,
        category="shift",
        cycles=1,
        description="Extract (no shift)",
    ),
    # -------------------------------------------------------------------------
    # Peripheral Instructions (bit7=1)
    # -------------------------------------------------------------------------
    "RF": OpcodeMetadata(
        mnemonic="RF",
        name="Read Forward",
        opcode=0o32,
        type="peripheral",
        variant=None,
        bit7=1,
        category="peripheral",
        cycles=10,
        description="Read forward from peripheral device",
    ),
    "RB": OpcodeMetadata(
        mnemonic="RB",
        name="Read Backward",
        opcode=0o12,
        type="peripheral",
        variant=None,
        bit7=1,
        category="peripheral",
        cycles=10,
        description="Read backward from peripheral device",
    ),
    "WF": OpcodeMetadata(
        mnemonic="WF",
        name="Write Forward",
        opcode=0o16,
        type="peripheral",
        variant=None,
        bit7=1,
        category="peripheral",
        cycles=10,
        description="Write forward to peripheral device",
    ),
    "RW": OpcodeMetadata(
        mnemonic="RW",
        name="Rewind",
        opcode=0o02,
        type="peripheral",
        variant=None,
        bit7=1,
        category="peripheral",
        cycles=100,
        description="Rewind peripheral device",
    ),
    # -------------------------------------------------------------------------
    # Print Instructions (bit7=1, share opcode 0o06)
    # -------------------------------------------------------------------------
    "PRA": OpcodeMetadata(
        mnemonic="PRA",
        name="Print Alphabetic",
        opcode=0o06,
        type="print",
        variant=None,
        bit7=1,
        category="print",
        cycles=10,
        description="Print alphabetic characters",
    ),
    "PRD": OpcodeMetadata(
        mnemonic="PRD",
        name="Print Decimal",
        opcode=0o06,
        type="print",
        variant=None,
        bit7=1,
        category="print",
        cycles=10,
        description="Print decimal numbers",
    ),
    "PRO": OpcodeMetadata(
        mnemonic="PRO",
        name="Print Octal",
        opcode=0o06,
        type="print",
        variant=None,
        bit7=1,
        category="print",
        cycles=10,
        description="Print octal numbers",
    ),
    # -------------------------------------------------------------------------
    # Simulator Instruction
    # -------------------------------------------------------------------------
    "S": OpcodeMetadata(
        mnemonic="S",
        name="Simulator",
        opcode=0o07,
        type="simulator",
        variant=None,
        bit7=None,
        category="simulator",
        cycles=1,
        description="Simulator control operation",
    ),
    # -------------------------------------------------------------------------
    # Scientific Instructions (floating-point)
    # -------------------------------------------------------------------------
    "FBA": OpcodeMetadata(
        mnemonic="FBA",
        name="Floating Binary Add",
        opcode=0o01,
        type="unmasked",
        variant=0b01,
        bit7=0,
        category="scientific",
        cycles=3,
        description="Floating-point binary addition",
    ),
    "FDA": OpcodeMetadata(
        mnemonic="FDA",
        name="Floating Decimal Add",
        opcode=0o21,
        type="unmasked",
        variant=0b01,
        bit7=0,
        category="scientific",
        cycles=3,
        description="Floating-point decimal addition",
    ),
    "FBS": OpcodeMetadata(
        mnemonic="FBS",
        name="Floating Binary Subtract",
        opcode=0o11,
        type="unmasked",
        variant=0b01,
        bit7=0,
        category="scientific",
        cycles=3,
        description="Floating-point binary subtraction",
    ),
    "FDS": OpcodeMetadata(
        mnemonic="FDS",
        name="Floating Decimal Subtract",
        opcode=0o31,
        type="unmasked",
        variant=0b01,
        bit7=0,
        category="scientific",
        cycles=3,
        description="Floating-point decimal subtraction",
    ),
    "FBD": OpcodeMetadata(
        mnemonic="FBD",
        name="Floating Binary Divide",
        opcode=0o05,
        type="unmasked",
        variant=0b01,
        bit7=0,
        category="scientific",
        cycles=8,
        description="Floating-point binary division",
    ),
    "FDD": OpcodeMetadata(
        mnemonic="FDD",
        name="Floating Decimal Divide",
        opcode=0o25,
        type="unmasked",
        variant=0b01,
        bit7=0,
        category="scientific",
        cycles=8,
        description="Floating-point decimal division",
    ),
    "FBAU": OpcodeMetadata(
        mnemonic="FBAU",
        name="Floating Binary Add Unnormalized",
        opcode=0o01,
        type="unmasked",
        variant=0b11,
        bit7=0,
        category="scientific",
        cycles=3,
        description="Floating-point binary addition (unnormalized)",
    ),
    "FDAU": OpcodeMetadata(
        mnemonic="FDAU",
        name="Floating Decimal Add Unnormalized",
        opcode=0o21,
        type="unmasked",
        variant=0b11,
        bit7=0,
        category="scientific",
        cycles=3,
        description="Floating-point decimal addition (unnormalized)",
    ),
    "FBSU": OpcodeMetadata(
        mnemonic="FBSU",
        name="Floating Binary Subtract Unnormalized",
        opcode=0o11,
        type="unmasked",
        variant=0b11,
        bit7=0,
        category="scientific",
        cycles=3,
        description="Floating-point binary subtraction (unnormalized)",
    ),
    "FDSU": OpcodeMetadata(
        mnemonic="FDSU",
        name="Floating Decimal Subtract Unnormalized",
        opcode=0o31,
        type="unmasked",
        variant=0b11,
        bit7=0,
        category="scientific",
        cycles=3,
        description="Floating-point decimal subtraction (unnormalized)",
    ),
    "FBM": OpcodeMetadata(
        mnemonic="FBM",
        name="Floating Binary Multiply",
        opcode=0o05,
        type="unmasked",
        variant=0b11,
        bit7=0,
        category="scientific",
        cycles=5,
        description="Floating-point binary multiplication",
    ),
    "FDM": OpcodeMetadata(
        mnemonic="FDM",
        name="Floating Decimal Multiply",
        opcode=0o25,
        type="unmasked",
        variant=0b11,
        bit7=0,
        category="scientific",
        cycles=5,
        description="Floating-point decimal multiplication",
    ),
    "ULD": OpcodeMetadata(
        mnemonic="ULD",
        name="Multiple Unload",
        opcode=0o15,
        type="unmasked",
        variant=0b11,
        bit7=0,
        category="transfer",
        cycles=2,
        description="Unload multiple registers",
    ),
    "FBAE": OpcodeMetadata(
        mnemonic="FBAE",
        name="Floating Binary Add Extended Precision",
        opcode=0o01,
        type="unmasked",
        variant=0b00,
        bit7=0,
        category="scientific",
        cycles=4,
        description="Floating-point binary addition (extended precision)",
    ),
    "FBSE": OpcodeMetadata(
        mnemonic="FBSE",
        name="Floating Binary Subtract Extended Precision",
        opcode=0o11,
        type="unmasked",
        variant=0b00,
        bit7=0,
        category="scientific",
        cycles=4,
        description="Floating-point binary subtraction (extended precision)",
    ),
    "BD": OpcodeMetadata(
        mnemonic="BD",
        name="Fixed Binary Divide",
        opcode=0o05,
        type="unmasked",
        variant=0b00,
        bit7=0,
        category="arithmetic",
        cycles=4,
        description="Fixed-point binary division",
    ),
    "DD": OpcodeMetadata(
        mnemonic="DD",
        name="Fixed Decimal Divide",
        opcode=0o25,
        type="unmasked",
        variant=0b00,
        bit7=0,
        category="arithmetic",
        cycles=4,
        description="Fixed-point decimal division",
    ),
    "FFN": OpcodeMetadata(
        mnemonic="FFN",
        name="Fixed to Floating Normalize",
        opcode=0o15,
        type="unmasked",
        variant=0b00,
        bit7=0,
        category="scientific",
        cycles=2,
        description="Convert fixed to floating-point (normalized)",
    ),
    "FCON": OpcodeMetadata(
        mnemonic="FCON",
        name="Conversion",
        opcode=0o35,
        type="unmasked",
        variant=0b00,
        bit7=0,
        category="scientific",
        cycles=2,
        description="Floating-point conversion",
    ),
    "FLN": OpcodeMetadata(
        mnemonic="FLN",
        name="Floating Less Than Normalized",
        opcode=0o30,
        type="unmasked",
        variant=0b00,
        bit7=0,
        category="scientific",
        cycles=2,
        description="Floating-point less-than comparison (normalized)",
    ),
    "FNN": OpcodeMetadata(
        mnemonic="FNN",
        name="Floating Not Equal Normalized",
        opcode=0o14,
        type="unmasked",
        variant=0b10,
        bit7=0,
        category="scientific",
        cycles=2,
        description="Floating-point not-equal comparison (normalized)",
    ),
}


# =============================================================================
# Reverse Lookup Structures
# =============================================================================


def build_reverse_lookup():
    """
    Build reverse lookup structures for decoder.

    Returns:
        Dictionary mapping (opcode, bit7, variant) tuples to lists of metadata
    """
    reverse = {}

    for meta in OPCODES.values():
        # Build key based on instruction type
        if meta.type == "peripheral":
            # Peripheral: opcode + bit7=1, variant doesn't matter
            key = (meta.opcode, 1, None)
        elif meta.type == "print":
            # Print: opcode + bit7=1, variant doesn't matter
            key = (meta.opcode, 1, None)
        elif meta.type == "maskable":
            # Maskable when masked: opcode + bit7=1, variant doesn't matter
            key_masked = (meta.opcode, 1, None)
            if key_masked not in reverse:
                reverse[key_masked] = []
            reverse[key_masked].append(meta)
            # Maskable when unmasked: opcode + bit7=0 + variant
            key_unmasked = (meta.opcode, 0, meta.variant)
            if key_unmasked not in reverse:
                reverse[key_unmasked] = []
            reverse[key_unmasked].append(meta)
            continue
        elif meta.type == "unmasked":
            # Unmasked: opcode + bit7=0 + variant
            key = (meta.opcode, 0, meta.variant)
        elif meta.type == "simulator":
            # Simulator: opcode only (bits 10-12)
            key = (meta.opcode, None, None)
        else:
            # Fallback
            key = (meta.opcode, meta.bit7, meta.variant)

        if key not in reverse:
            reverse[key] = []
        reverse[key].append(meta)

    return reverse


OPCODES_BY_CODE = build_reverse_lookup()


# =============================================================================
# Lookup Functions
# =============================================================================


def lookup_opcode(opcode: int, bit7: int, variant: int | None = None) -> list[OpcodeMetadata]:
    """
    Lookup opcode metadata by instruction fields.

    Args:
        opcode: Opcode value (bits 8-12)
        bit7: Value of bit 7
        variant: Variant bits (bits 2-3) for unmasked instructions

    Returns:
        List of matching OpcodeMetadata instances (may be multiple for ambiguous cases)
    """
    # Try exact match first
    key = (opcode, bit7, variant)
    if key in OPCODES_BY_CODE:
        return OPCODES_BY_CODE[key]

    # Try without variant for peripheral/print/masked
    if bit7 == 1:
        key = (opcode, 1, None)
        if key in OPCODES_BY_CODE:
            return OPCODES_BY_CODE[key]

    # No match
    return []


def get_opcode(mnemonic: str) -> OpcodeMetadata | None:
    """
    Get opcode metadata by mnemonic.

    Args:
        mnemonic: Instruction mnemonic (e.g., "BA", "TX")

    Returns:
        OpcodeMetadata instance or None if not found
    """
    return OPCODES.get(mnemonic)


def list_opcodes_by_category(category: str) -> list[OpcodeMetadata]:
    """
    List all opcodes in a given category.

    Args:
        category: Category name (e.g., "arithmetic", "transfer", "scientific")

    Returns:
        List of OpcodeMetadata instances in the category
    """
    return [meta for meta in OPCODES.values() if meta.category == category]


def get_categories() -> list[str]:
    """
    Get list of all instruction categories.

    Returns:
        Sorted list of unique category names
    """
    return sorted(set(meta.category for meta in OPCODES.values()))
