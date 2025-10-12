from collections import namedtuple


# A version of namedtuple that takes a list of default values and applies them.
def namedtuple_defaults(typename, field_names, default_values=()):
    T = namedtuple(typename, field_names)
    T.__new__.__defaults__ = (None,) * len(T._fields)
    prototype = T(*default_values)
    T.__new__.__defaults__ = tuple(prototype)
    return T


# Base opcodes (bits 8-12 of the command code). These are modified by the
# value of bit 7 (0 for unmasked, or 1 for masked), and bits 2-3 for unmasked
# instructions.

# Represents the fields making up a complete opcode:
#
#   m: mnemonic
#   c: class
#   b23: bits 2-3 (00 - 11)
#   b7: bit 7 (0, 1)
#   op: bits 8-12 (00000 - 11111)
#   type: the instruction type, one of
#     None: general unmasked or scientific instructions.
#     "maskable": maskable instructions.
#     "peripheral": peripheral instructions.
#     "print": print instructions.
#     "simulator": simulator instruction.
#
Opcode = namedtuple_defaults(
    "Opcode", ["m", "c", "b23", "b7", "op", "type"], (None, None, None, None, None, "unmasked")
)

OPCODES = {
    # Table format:
    #
    #   Mnemonic:  Opcode(Mnemonic, Class,
    #                     Unmasked bits 2-3, Masked bit 7, bits 8-12,
    #                     "maskable" / "peripheral" / "print" / "simulator")
    # General, masked or unmasked.
    "BA": Opcode("BA", "BinaryAdd", 0b10, 0b1, 0o11, "maskable"),
    "DA": Opcode("DA", "DecimalAdd", 0b10, 0b1, 0o01, "maskable"),
    "WA": Opcode("WA", "WordAdd", 0b10, 0b1, 0o15, "maskable"),
    "BS": Opcode("BS", "BinarySubtract", 0b10, 0b1, 0o31, "maskable"),
    "DS": Opcode("DS", "DecimalSubtract", 0b10, 0b1, 0o21, "maskable"),
    "WD": Opcode("WD", "WordDifference", 0b10, 0b1, 0o35, "maskable"),
    "NA": Opcode("NA", "NotEqualAlphabetic", 0b10, 0b1, 0o14, "maskable"),
    "NN": Opcode("NN", "NotEqualNumeric", 0b10, 0b1, 0o10, "maskable"),
    "LA": Opcode("LA", "LessThanOrEqualAlphabetic", 0b10, 0b1, 0o34, "maskable"),
    "LN": Opcode("LN", "LessThanOrEqualNumeric", 0b10, 0b1, 0o30, "maskable"),
    "TX": Opcode("TX", "Transfer", 0b10, 0b1, 0o20, "maskable"),
    "TS": Opcode("TS", "TransferAndChangeSequence", 0b10, 0b1, 0o04, "maskable"),
    "HA": Opcode("HA", "HalfAdd", 0b10, 0b1, 0o25, "maskable"),
    "SM": Opcode("SM", "Superimpose", 0b10, 0b1, 0o05, "maskable"),
    "CP": Opcode("CP", "CheckParity", 0b10, 0b1, 0o24, "maskable"),
    # General, unmasked.
    "BM": Opcode("BM", "BinaryMultiply", 0b00, 0b0, 0o13),
    "DM": Opcode("DM", "DecimalMultiply", 0b00, 0b0, 0o03),
    "BT": Opcode("BT", "BinaryAccumulate", 0b10, 0b0, 0o13),
    "DT": Opcode("DT", "DecimalAccumulate", 0b10, 0b0, 0o03),
    "MT": Opcode("MT", "MultipleTransfer", 0b00, 0b0, 0o20),
    "TN": Opcode("TN", "TransferNWords", 0b01, 0b0, 0o20),
    "CC": Opcode("CC", "ComputeOrthocount", 0b01, 0b0, 0o10),
    "IT": Opcode("IT", "ItemTransfer", 0b01, 0b0, 0o30),
    "EBA": Opcode("EBA", "ExtendedBinaryAdd", 0b11, 0b0, 0o13),
    "EBS": Opcode("EBS", "ExtendedBinarySubtract", 0b11, 0b0, 0o33),
    "RT": Opcode("RT", "RecordTransfer", 0b11, 0b0, 0o30),
    "MPC": Opcode("MPC", "ControlProgram", 0b10, 0b0, 0o00),
    "PR": Opcode("PR", "Proceed", 0b00, 0b0, 0o00),
    # Inherent mask.
    "SWS": Opcode("SWS", "ShiftWordAndSubstitute", 0b10, 0b0, 0o06),
    "SPS": Opcode("SPS", "ShiftPreservingSignAndSubstitute", 0b10, 0b0, 0o02),
    "SWE": Opcode("SWE", "ShiftWordAndExtract", 0b10, 0b0, 0o16),
    "SPE": Opcode("SPE", "ShiftPreservingSignAndExtract", 0b10, 0b0, 0o12),
    "SSL": Opcode("SSL", "ShiftAndSelect", 0b10, 0b0, 0o26),
    "SS": Opcode("SS", "Substitute", 0b00, 0b0, 0o06),
    "EX": Opcode("EX", "Extract", 0b00, 0b0, 0o16),
    # Peripheral and print.
    "RF": Opcode("RF", "ReadForward", None, 0b1, 0o32, "peripheral"),
    "RB": Opcode("RB", "ReadBackward", None, 0b1, 0o12, "peripheral"),
    "WF": Opcode("WF", "WriteForward", None, 0b1, 0o16, "peripheral"),
    "RW": Opcode("RW", "Rewind", None, 0b1, 0o02, "peripheral"),
    "PRA": Opcode("PRA", "PrintAlphabetic", None, 0b1, 0o06, "print"),
    "PRD": Opcode("PRD", "PrintDecimal", None, 0b1, 0o06, "print"),
    "PRO": Opcode("PRO", "PrintOctal", None, 0b1, 0o06, "print"),
    # Simulator.
    "S": Opcode("S", "Simulator", None, None, 0o07, "simulator"),
    # Scientific.
    "FBA": Opcode("FBA", "FloatingBinaryAdd", 0b01, 0b0, 0o01),
    "FDA": Opcode("FDA", "FloatingDecimalAdd", 0b01, 0b0, 0o21),
    "FBS": Opcode("FBS", "FloatingBinarySubtract", 0b01, 0b0, 0o11),
    "FDS": Opcode("FDS", "FloatingDecimalSubtract", 0b01, 0b0, 0o31),
    "FBD": Opcode("FBD", "FloatingBinaryDivide", 0b01, 0b0, 0o05),
    "FDD": Opcode("FDD", "FloatingDecimalDivide", 0b01, 0b0, 0o25),
    "FBAU": Opcode("FBAU", "FloatingBinaryAddUnnormalized", 0b11, 0b0, 0o01),
    "FDAU": Opcode("FDAU", "FloatingDecimalAddUnnormalized", 0b11, 0b0, 0o21),
    "FBSU": Opcode("FBSU", "FloatingBinarySubtractUnnormalized", 0b11, 0b0, 0o11),
    "FDSU": Opcode("FDSU", "FloatingDecimalSubtractUnnormalized", 0b11, 0b0, 0o31),
    "FBM": Opcode("FBM", "FloatingBinaryMultiply", 0b11, 0b0, 0o05),
    "FDM": Opcode("FDM", "FloatingDecimalMultiply", 0b11, 0b0, 0o25),
    "ULD": Opcode("ULD", "MultipleUnload", 0b11, 0b0, 0o15),
    "FBAE": Opcode("FBAE", "FloatingBinaryAddExtendedPrecision", 0b00, 0b0, 0o01),
    "FBSE": Opcode("FBSE", "FloatingBinarySubtractExtendedPrecision", 0b00, 0b0, 0o11),
    "BD": Opcode("BD", "FixedBinaryDivide", 0b00, 0b0, 0o05),
    "DD": Opcode("DD", "FixedDecimalDivide", 0b00, 0b0, 0o25),
    "FFN": Opcode("FFN", "FixedToFloatingNormalize", 0b00, 0b0, 0o15),
    "FCON": Opcode("FCON", "Conversion", 0b00, 0b0, 0o35),
    "FLN": Opcode("FLN", "FloatingLessThanNormalized", 0b00, 0b0, 0o30),
    "FNN": Opcode("FNN", "FloatingNotEqualNormalized", 0b10, 0b0, 0o14),
}

# The remaining instructions are pseudo-instructions of various types.

CONTROL_INSTRUCTIONS = {
    "ASSIGN": None,  # Assign Tag to Complex Address
    "END": None,  # Specify Information for Executive
    "EQUALS": None,  # Assign Value to Tag
    "EVEN": None,  # Set Location Counter to Next Even Address
    "MASKGRP": None,  # Assign Shift and Field Group Numbers
    "MODLOC": None,  # Set Location Counter Modulo-N.
    "RESERVE": None,  # Reserve N Words of Memory
    "SETLOC": None,  # Set Location Counter
    "SIMULATE": None,  # Start of Simulator Routine
    "TAS": None,  # Temporarily Assign Tag to Complex Address
}

DATA_CONSTANTS = {
    "ALF": None,  # Alphanumeric Constant
    "DEC": None,  # Fixed Decimal Constant
    "EBC": None,  # Extended Binary Constant
    "FLBIN": None,  # Floating-Point Binary Constant
    "FLDEC": None,  # Floating-Point Decimal Constant
    "FXBIN": None,  # Decimal to Fixed Binary Translation
    "OCT": None,  # Octal Constant
}

CONTROL_CONSTANTS = {
    "SPEC": None,  # Special Address Constant
    "CAC": None,  # Complete Address Constant
    "MASKBASE": None,  # Mask Base Address Constant
    "CONTROL": None,  # Program Control Constant
    "M": None,  # Mixed Constant
    "TAC": None,  # Tape Address Constant
    "LINK": None,  # Linkage Constant
    "SEGNAME": None,  # Segment Name Constant
    "SUBCALL": None,  # Subroutine Call Constant
}

EXTENDED_INSTRUCTIONS = {
    "CSCON": None,  # Turn On Programs, Use Cosequence Counters
    "DOFF": None,  # Turn Off Programs
    "DON": None,  # Turn On Programs
    "SCON": None,  # Turn On Programs, Use Sequence Counters
    "SPCR": None,  # Save PCR
    "STOP": None,  # Stop Current Program
}

MISC_INSTRUCTIONS = {
    "COREDUMP": None,  # ?
    "DUMP": None,  # ?
}

# These are not used by YUL, so not supported.
ARGUS_INSTRUCTIONS = {
    "ARGUS": None,  # First card of every ARGUS input deck
    "U": None,  # Program Director
    "MACRODEF": None,  # Define macro
    "FINIS": None,  # End of Macro definition
    "ELIMSEG": None,  # Eliminate segment from the new symbolic tape
    "SEGMENT": None,  # Start of a segment
    "PROGRAM": None,  # First segment of a program
    "TESTDATA": None,  # Start of test data set
    "ELIMDATA": None,  # Eliminate the specified set of test data from the SPT
    "ELIMDERL": None,  # Eliminate a derail
    "DELETE": None,  # Delete lines from a segment on symbolic program tape
    "ENDARGUS": None,  # End of the ARGUS input deck
}

INSTRUCTIONS = list(
    list(OPCODES.keys())
    + list(CONTROL_INSTRUCTIONS.keys())
    + list(DATA_CONSTANTS.keys())
    + list(CONTROL_CONSTANTS.keys())
    + list(EXTENDED_INSTRUCTIONS.keys())
    + list(MISC_INSTRUCTIONS.keys())
    + list(ARGUS_INSTRUCTIONS.keys())
)


def make_masked_opcode(mnemonic, sequence, mask):
    o = OPCODES[mnemonic]
    return (0o4000 * sequence) + (0o100 * mask) + (0o40 * o.b7) + o.op


def make_unmasked_opcode(mnemonic, sequence, a, b, c):
    o = OPCODES[mnemonic]
    return (0o4000 * sequence) + (0o1000 * o.b23) + (0o400 * a) + (0o200 * b) + (0o100 * c) + o.op


def make_peripheral_opcode(mnemonic, paddr):
    o = OPCODES[mnemonic]
    return (0o100 * paddr) + (0o40 * o.b7) + o.op


def make_print_opcode(mnemonic, sequence, a, b, c):
    o = OPCODES[mnemonic]
    return (0o4000 * sequence) + (0o400 * a) + (0o200 * b) + (0o100 * c) + (0o40 * o.b7) + o.op


__all__ = [
    "ARGUS_INSTRUCTIONS",
    "CONTROL_CONSTANTS",
    "CONTROL_INSTRUCTIONS",
    "DATA_CONSTANTS",
    "EXTENDED_INSTRUCTIONS",
    "INSTRUCTIONS",
    "MISC_INSTRUCTIONS",
    "OPCODES",
    "make_masked_opcode",
    "make_peripheral_opcode",
    "make_print_opcode",
    "make_unmasked_opcode",
]
