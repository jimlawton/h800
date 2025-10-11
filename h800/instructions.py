# Instructions
# ============
#
# Key:
#   pppppp      6-bit peripheral address
#   s           sequence/cosequence bit
#   a,b,c       memory designators
#   mmmmm       5-bit mask address
#   x           don't care
#
#
#               +------------------+
#               | 1             12 |
# Opcode        +------------------+
#
# BA  masked    | s mmmmm  1 01001 |    101 001 |   51
# BA  unmasked  | s 10 abc 0 01001 | 10 001 001 | 2 11
# DA  masked    | s mmmmm  1 00001 |    100 001 |   41
# DA  unmasked  | s 10 abc 0 00001 | 10 000 001 | 2 01
# WA  masked    | s mmmmm  1 01101 |    101 101 |   55
# WA  unmasked  | s 10 abc 0 01101 | 10 001 101 | 2 15
# BS  masked    | s mmmmm  1 11001 |    111 001 |   71
# BS  unmasked  | s 10 abc 0 11001 | 10 011 001 | 2 31
# DS  masked    | s mmmmm  1 10001 |    110 001 |   61
# DS  unmasked  | s 10 abc 0 10001 | 10 010 001 | 2 21
# WD  masked    | s mmmmm  1 11101 |    111 101 |   75
# WD  unmasked  | s 10 abc 0 11101 | 10 011 101 | 2 35
# NA  masked    | s mmmmm  1 01100 |    101 100 |   54
# NA  unmasked  | s 10 abc 0 01100 | 10 001 100 | 2 14
# NN  masked    | s mmmmm  1 01000 |    101 000 |   50
# NN  unmasked  | s 10 abc 0 01000 | 10 001 000 | 2 10
# LA  masked    | s mmmmm  1 11100 |    111 100 |   74
# LA  unmasked  | s 10 abc 0 11100 | 10 011 100 | 2 34
# LN  masked    | s mmmmm  1 11000 |    111 000 |   70
# LN  unmasked  | s 10 abc 0 11000 | 10 011 000 | 2 30
# TX  masked    | s mmmmm  1 10000 |    110 000 |   60
# TX  unmasked  | s 10 abc 0 10000 | 10 010 000 | 2 20
# TS  masked    | s mmmmm  1 00100 |    100 100 |   44
# TS  unmasked  | s 10 abc 0 00100 | 10 000 100 | 2 04
# HA  masked    | s mmmmm  1 10101 |    110 101 |   65
# HA  unmasked  | s 10 abc 0 10101 | 10 010 101 | 2 25
# SM  masked    | s mmmmm  1 00101 |    100 101 |   45
# SM  unmasked  | s 10 abc 0 00101 | 10 000 101 | 2 05
# CP  masked    | s mmmmm  1 10100 |    110 100 |   64
# CP  unmasked  | s 10 abc 0 10100 | 10 010 100 | 2 24
# BM            | s 00 abc 0 01011 | 00 001 011 | 0 13
# DM            | s 00 abc 0 00011 | 00 000 011 | 0 03
# BT            | s 10 abc 0 01011 | 10 001 011 | 2 13
# DT            | s 10 abc 0 00011 | 10 000 011 | 2 03
# MT            | s 00 abc 0 10000 | 00 010 000 | 0 20
# TN            | s 01 abc 0 10000 | 01 010 000 | 1 20
# CC            | s 01 abc 0 01000 | 01 001 000 | 1 10
# IT            | s 01 abc 0 11000 | 01 011 000 | 1 30
# EBA           | s 11 abc 0 01011 | 11 001 011 | 3 13
# EBS           | s 11 abc 0 11011 | 11 011 011 | 3 33
# RT            | s 11 abc 0 11000 | 11 011 000 | 3 30
# MPC           | s 10 abc 0 00000 | 10 000 000 | 2 00
# PR            | x 00 0xx 0 00000 | 00 000 000 | 0 00
# SWS           | s 10 abc 0 00110 | 10 000 110 | 2 06
# SPS           | s 10 abc 0 00010 | 10 000 010 | 2 02
# SWE           | s 10 abc 0 01110 | 10 001 110 | 2 16
# SPE           | s 10 abc 0 01010 | 10 001 010 | 2 12
# SSL           | s 10 abc 0 10110 | 10 010 110 | 2 26
# SS            | s 00 abc 0 00110 | 00 000 110 | 0 06
# EX            | s 00 abc 0 01110 | 00 001 110 | 0 16
# RF            | pppppp   1 11010 |    111 010 |   72
# RB            | pppppp   1 01010 |    101 010 |   52
# WF            | pppppp   1 01110 |    101 110 |   56
# RW            | pppppp   1 00010 |    100 010 |   42
# PRA           | s xx abc 1 00110 | xx 100 110 | x 46
# PRD           | s xx abc 1 00110 | xx 100 110 | x 46
# PRO           | s xx abc 1 00110 | xx 100 110 | x 46
# S   direct    | 0 xx xxx x xx111 | xx xxx 111 | x x7
# S   indexed   | 1 xx xxx x xx111 | xx xxx 111 | x x7
# FBA           | s 01 abc 0 00001 | 01 000 001 | 1 01
# FDA           | s 01 abc 0 10001 | 01 010 001 | 1 21
# FBS           | s 01 abc 0 01001 | 01 001 001 | 1 11
# FDS           | s 01 abc 0 11001 | 01 011 001 | 1 31
# FBD           | s 01 abc 0 00101 | 01 000 101 | 1 05
# FDD           | s 01 abc 0 10101 | 01 010 101 | 1 25
# FBAU          | s 11 abc 0 00001 | 11 000 001 | 3 01
# FDAU          | s 11 abc 0 10001 | 11 010 001 | 3 21
# FBSU          | s 11 abc 0 01001 | 11 001 001 | 3 11
# FDSU          | s 11 abc 0 11001 | 11 011 001 | 3 31
# FBM           | s 11 abc 0 00101 | 11 000 101 | 3 05
# FDM           | s 11 abc 0 10101 | 11 010 101 | 3 25
# ULD           | s 11 abc 0 01101 | 11 001 101 | 3 15
# FBAE          | s 00 abc 0 00001 | 00 000 001 | 0 01
# FBSE          | s 00 abc 0 01001 | 00 001 001 | 0 11
# BD            | s 00 abc 0 00101 | 00 000 101 | 0 05
# DD            | s 00 abc 0 10101 | 00 010 101 | 0 25
# FFN           | s 00 abc 0 01101 | 00 001 101 | 0 15
# FCON          | s 00 abc 0 11101 | 00 011 101 | 0 35
# FLN           | s 00 abc 0 11000 | 00 011 000 | 0 30
# FNN           | s 10 abc 0 01100 | 10 001 100 | 2 14


from collections import namedtuple

from h800 import instruction


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


class NotImplementedError(Exception):
    def __init__(self):
        super().__init__("This feature is not yet implemented!")


# General instruction facades (single class per mnemonic supporting both masked and unmasked forms).
# Each facade accepts either a mask (for maskable form) OR operand flags (a,b,c) for unmasked usage.


# Facade classes removed; use get_instruction('DA', sequence=..., mask=... or a/b/c...) instead.


# Facade removed: get_instruction('WA', ...)


# Facade removed: get_instruction('BS', ...)


# Facade removed: get_instruction('DS', ...)


# Facade removed: get_instruction('TX', ...)


# Facade removed: get_instruction('TS', ...)


# Facade removed: get_instruction('HA', ...)


# Facade removed: get_instruction('SM', ...)


# Facade removed: get_instruction('CP', ...)


# General, unmasked.


# Facade removed: get_instruction('BM', sequence=..., a=..., b=..., c=...)


# Facade removed: get_instruction('DM', ...)


# Facade removed: get_instruction('BT', ...)


# Facade removed: get_instruction('DT', ...)


# Facade removed: get_instruction('MT', ...)


# Facade removed: get_instruction('TN', ...)


# Facade removed: get_instruction('CC', ...)


# Facade removed: get_instruction('IT', ...)


# Facade removed: get_instruction('EBS', ...)


# Facade removed: get_instruction('RT', ...)


# Facade removed: get_instruction('MPC', ...)


# Facade removed: get_instruction('PR', sequence=0, a=0, b=0, c=0)


# # Inherent mask.


# Facade removed: get_instruction('SWS', ...)


# Facade removed: get_instruction('SPS', ...)


# Facade removed: get_instruction('SWE', ...)


# Facade removed: get_instruction('SPE', ...)


# Facade removed: get_instruction('SSL', ...)


# Facade removed: get_instruction('SS', ...)


# Facade removed: get_instruction('EX', ...)


# Peripheral and print.


# Facade removed: get_instruction('RF', paddr=...)


# Facade removed: get_instruction('RB', paddr=...)


# Facade removed: get_instruction('WF', paddr=...)


# Facade removed: get_instruction('RW', paddr=...)


# Facade removed: get_instruction('PRA', sequence=..., a=..., b=..., c=...)


# Facade removed: get_instruction('PRD', ...)


# Facade removed: get_instruction('PRO', ...)


# Simulator.


# Facade removed: get_instruction('S', sequence=...)


# Scientific.


# Facade removed: get_instruction('FDA', ...)


# Facade removed: get_instruction('FBS', ...)


# Facade removed: get_instruction('FDS', ...)


# Facade removed: get_instruction('FBD', ...)


# Facade removed: get_instruction('FDD', ...)


# Facade removed: get_instruction('FBAU', ...)


# Facade removed: get_instruction('FDAU', ...)


# Facade removed: get_instruction('FBSU', ...)


# Facade removed: get_instruction('FDSU', ...)


# Facade removed: get_instruction('FBM', ...)


# Facade removed: get_instruction('FDM', ...)


# Facade removed: get_instruction('ULD', ...)


# Facade removed: get_instruction('FBAE', ...)


# Facade removed: get_instruction('FBSE', ...)


# Facade removed: get_instruction('BD', ...)


# Facade removed: get_instruction('DD', ...)


# Facade removed: get_instruction('FFN', ...)


# Facade removed: get_instruction('FCON', ...)


# Facade removed: get_instruction('FLN', ...)


# Facade removed: get_instruction('FNN', ...)


# Control Instructions.


# ASSIGN: Assign Tag to Complex Address
class AssignTag(instruction.AssemblyControl):
    pass


# END: Specify Information for Executive
class End(instruction.AssemblyControl):
    pass


# EQUALS: Assign Value to Tag
class Equals(instruction.AssemblyControl):
    pass


# EVEN: Set Location Counter to Next Even Address
class Even(instruction.AssemblyControl):
    pass


# MASKGRP: Assign Shift and Field Group Numbers
class MaskGroup(instruction.AssemblyControl):
    pass


# MODLOC: Set Location Counter Modulo-N.
class SetLocationCounterModuloN(instruction.AssemblyControl):
    pass


# RESERVE: Reserve N Words of Memory
class Reserve(instruction.AssemblyControl):
    pass


# SETLOC: Set Location Counter
class SetLocationCounter(instruction.AssemblyControl):
    pass


# SIMULATE: Start of Simulator Routine
class Simulate(instruction.AssemblyControl):
    pass


# TAS: Temporarily Assign Tag to Complex Address
class TemporarilyAssignTag(instruction.AssemblyControl):
    pass


# Data Constants.


# ALF: Alphanumeric Constant
def build_constant(mnemonic: str, value: int):
    """Unified constant factory replacing individual constant facade classes."""
    return instruction.Constant(mnemonic=mnemonic, value=value)


# Removed facade class: use build_constant("ALF", value)


# DEC: Fixed Decimal Constant
# Removed facade class: use build_constant("DEC", value)


# EBC: Extended Binary Constant
# Removed facade class: use build_constant("EBC", value)


# FLBIN: Floating-Point Binary Constant
# Removed facade class: use build_constant("FLBIN", value)


# FLDEC: Floating-Point Decimal Constant
# Removed facade class: use build_constant("FLDEC", value)


# FXBIN: Decimal to Fixed Binary Translation
# Removed facade class: use build_constant("FXBIN", value)


# OCT: Octal Constant
# Removed facade class: use build_constant("OCT", value)


# Control Constants.


# SPEC: Special Address Constant
# Removed facade class: use build_constant("SPEC", value)


# CAC: Complete Address Constant
# Removed facade class: use build_constant("CAC", value)


# MASKBASE: Mask Base Address Constant
# Removed facade class: use build_constant("MASKBASE", value)


# PCON: Program Control Constant
# Removed facade class: use build_constant("CONTROL", value)


# M: Mixed Constant
# Removed facade class: use build_constant("M", value)


# TAC: Tape Address Constant
# Removed facade class: use build_constant("TAC", value)


# LINK: Linkage Constant
# Removed facade class: use build_constant("LINK", value)


# SEGNAME: Segment Name Constant
# Removed facade class: use build_constant("SEGNAME", value)


# SUBCALL: Subroutine Call Constant
# Removed facade class: use build_constant("SUBCALL", value)


def print_instructions():
    """
    Emit all valid 12-bit instruction opcode values (octal) mapped to mnemonics.
    For print instructions (PRA/PRD/PRO) only PRA space is enumerated (they overlap).
    Constants are excluded (they are raw 48-bit data, not 12-bit opcodes).
    Branching reduced by using per-type generator functions.
    """

    def gen_maskable(mnemonic, meta):
        for sequence in (0, 1):
            for mask in range(32):
                yield make_masked_opcode(mnemonic, sequence, mask)
        # Unmasked variant for same mnemonic (bit7=0)
        for sequence in (0, 1):
            for a in (0, 1):
                for b in (0, 1):
                    for c in (0, 1):
                        yield make_unmasked_opcode(mnemonic, sequence, a, b, c)

    def gen_unmasked(mnemonic, meta):
        for sequence in (0, 1):
            for a in (0, 1):
                for b in (0, 1):
                    for c in (0, 1):
                        yield make_unmasked_opcode(mnemonic, sequence, a, b, c)

    def gen_peripheral(mnemonic, meta):
        for paddr in range(64):
            yield make_peripheral_opcode(mnemonic, paddr)

    def gen_print(mnemonic, meta):
        # Only enumerate PRA space (shared with PRD/PRO)
        if mnemonic != "PRA":
            return
        for sequence in (0, 1):
            for a in (0, 1):
                for b in (0, 1):
                    for c in (0, 1):
                        yield make_print_opcode(mnemonic, sequence, a, b, c)

    def gen_simulator(mnemonic, meta):
        yield from (0o0007, 0o4007)

    generators = {
        "maskable": gen_maskable,
        "unmasked": gen_unmasked,
        "peripheral": gen_peripheral,
        "print": gen_print,
        "simulator": gen_simulator,
    }

    opcodes = {}
    for mnemonic, meta in OPCODES.items():
        gen = generators.get(meta.type)
        if gen is None:
            continue
        codes = sorted(set(gen(mnemonic, meta)))
        if codes:
            opcodes[mnemonic] = codes

    inverse = {}
    for mnemonic, codes in opcodes.items():
        for code in codes:
            inverse.setdefault(code, []).append(mnemonic)

    for code in sorted(inverse):
        print(f"0o{code:04o} {','.join(inverse[code])}")


__all__ = [
    "ARGUS_INSTRUCTIONS",
    "CONTROL_CONSTANTS",
    "CONTROL_INSTRUCTIONS",
    "DATA_CONSTANTS",
    "EXTENDED_INSTRUCTIONS",
    "INSTRUCTIONS",
    "MISC_INSTRUCTIONS",
    "OPCODES",
    "build_constant",
    "make_masked_opcode",
    "make_peripheral_opcode",
    "make_print_opcode",
    "make_unmasked_opcode",
    "print_instructions",
]

if __name__ == "__main__":
    print_instructions()
