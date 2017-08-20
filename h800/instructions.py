#!/usr/bin/env python

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

import instruction


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
Opcode = namedtuple_defaults('Opcode',
                             ['m', 'c', 'b23', 'b7', 'op', 'type'],
                             (None, None, None, None, None, "unmasked"))

OPCODES = {

    # Table format:
    #
    #   Mnemonic  (Class, Unmasked Bits2-3, Masked Bit7, Bits8-12)
    #
    # "*" in the mnemonic is used as an internal representation of masked
    # instructions.

    # General, masked or unmasked.
    "BA":   Opcode("BA", "BinaryAdd", 0b10, 0b1, 0o11, "maskable"),
    "DA":   Opcode("DA", "DecimalAdd", 0b10, 0b1, 0o01, "maskable"),
    "WA":   Opcode("WA", "WordAdd", 0b10, 0b1, 0o15, "maskable"),
    "BS":   Opcode("BS", "BinarySubtract", 0b10, 0b1, 0o31, "maskable"),
    "DS":   Opcode("DS", "DecimalSubtract", 0b10, 0b1, 0o21, "maskable"),
    "WD":   Opcode("WD", "WordDifference", 0b10, 0b1, 0o35, "maskable"),
    "NA":   Opcode("NA", "NotEqualAlphabetic", 0b10, 0b1, 0o14, "maskable"),
    "NN":   Opcode("NN", "NotEqualNumeric", 0b10, 0b1, 0o10, "maskable"),
    "LA":   Opcode("LA", "LessThanOrEqualAlphabetic", 0b10, 0b1, 0o34, "maskable"),
    "LN":   Opcode("LN", "LessThanOrEqualNumeric", 0b10, 0b1, 0o30, "maskable"),
    "TX":   Opcode("TX", "Transfer", 0b10, 0b1, 0o20, "maskable"),
    "TS":   Opcode("TS", "TransferAndChangeSequence", 0b10, 0b1, 0o04, "maskable"),
    "HA":   Opcode("HA", "HalfAdd", 0b10, 0b1, 0o25, "maskable"),
    "SM":   Opcode("SM", "Superimpose", 0b10, 0b1, 0o05, "maskable"),
    "CP":   Opcode("CP", "CheckParity", 0b10, 0b1, 0o24, "maskable"),

    # General, unmasked.
    "BM":   Opcode("BM", "BinaryMultiply", 0b00, 0b0, 0o13),
    "DM":   Opcode("DM", "DecimalMultiply", 0b00, 0b0, 0o03),
    "BT":   Opcode("BT", "BinaryAccumulate", 0b10, 0b0, 0o13),
    "DT":   Opcode("DT", "DecimalAccumulate", 0b10, 0b0, 0o03),
    "MT":   Opcode("MT", "MultipleTransfer", 0b00, 0b0, 0o20),
    "TN":   Opcode("TN", "TransferNWords", 0b01, 0b0, 0o20),
    "CC":   Opcode("CC", "ComputeOrthocount", 0b01, 0b0, 0o10),
    "IT":   Opcode("IT", "ItemTransfer", 0b01, 0b0, 0o30),
    "EBA":  Opcode("EBA", "ExtendedBinaryAdd", 0b11, 0b0, 0o13),
    "EBS":  Opcode("EBS", "ExtendedBinarySubtract", 0b11, 0b0, 0o33),
    "RT":   Opcode("RT", "RecordTransfer", 0b11, 0b0, 0o30),
    "MPC":  Opcode("MPC", "ControlProgram", 0b10, 0b0, 0o00),
    "PR":   Opcode("PR", "Proceed", 0b00, 0b0, 0o00),

    # Inherent mask.
    "SWS":  Opcode("SWS", "ShiftWordAndSubstitute", 0b10, 0b0, 0o06),
    "SPS":  Opcode("SPS", "ShiftPreservingSignAndSubstitute", 0b10, 0b0, 0o02),
    "SWE":  Opcode("SWE", "ShiftWordAndExtract", 0b10, 0b0, 0o16),
    "SPE":  Opcode("SPE", "ShiftPreservingSignAndExtract", 0b10, 0b0, 0o12),
    "SSL":  Opcode("SSL", "ShiftAndSelect", 0b10, 0b0, 0o26),
    "SS":   Opcode("SS", "Substitute", 0b00, 0b0, 0o06),
    "EX":   Opcode("EX", "Extract", 0b00, 0b0, 0o16),

    # Peripheral and print.
    "RF":   Opcode("RF", "ReadForward", None, 0b1, 0o32, "peripheral"),
    "RB":   Opcode("RB", "ReadBackward", None, 0b1, 0o12, "peripheral"),
    "WF":   Opcode("WF", "WriteForward", None, 0b1, 0o16, "peripheral"),
    "RW":   Opcode("RW", "Rewind", None, 0b1, 0o02, "peripheral"),
    "PRA":  Opcode("PRA", "PrintAlphabetic", None, 0b1, 0o06, "print"),
    "PRD":  Opcode("PRD", "PrintDecimal", None, 0b1, 0o06, "print"),
    "PRO":  Opcode("PRO", "PrintOctal", None, 0b1, 0o06, "print"),

    # Simulator.
    "S":    Opcode("S", "Simulator", None, None, 0o07, "simulator"),

    # Scientific.
    "FBA":  Opcode("FBA", "FloatingBinaryAdd", 0b01, 0b0, 0o01),
    "FDA":  Opcode("FDA", "FloatingDecimalAdd", 0b01, 0b0, 0o21),
    "FBS":  Opcode("FBS", "FloatingBinarySubtract", 0b01, 0b0, 0o11),
    "FDS":  Opcode("FDS", "FloatingDecimalSubtract", 0b01, 0b0, 0o31),
    "FBD":  Opcode("FBD", "FloatingBinaryDivide", 0b01, 0b0, 0o05),
    "FDD":  Opcode("FDD", "FloatingDecimalDivide", 0b01, 0b0, 0o25),
    "FBAU": Opcode("FBAU", "FloatingBinaryAddUnnormalized", 0b11, 0b0, 0o01),
    "FDAU": Opcode("FDAU", "FloatingDecimalAddUnnormalized", 0b11, 0b0, 0o21),
    "FBSU": Opcode("FBSU", "FloatingBinarySubtractUnnormalized", 0b11, 0b0, 0o11),
    "FDSU": Opcode("FDSU", "FloatingDecimalSubtractUnnormalized", 0b11, 0b0, 0o31),
    "FBM":  Opcode("FBM", "FloatingBinaryMultiply", 0b11, 0b0, 0o05),
    "FDM":  Opcode("FDM", "FloatingDecimalMultiply", 0b11, 0b0, 0o25),
    "ULD":  Opcode("ULD", "MultipleUnload", 0b11, 0b0, 0o15),
    "FBAE": Opcode("FBAE", "FloatingBinaryAddExtendedPrecision", 0b00, 0b0, 0o01),
    "FBSE": Opcode("FBSE", "FloatingBinarySubtractExtendedPrecision", 0b00, 0b0, 0o11),
    "BD":   Opcode("BD", "FixedBinaryDivide", 0b00, 0b0, 0o05),
    "DD":   Opcode("DD", "FixedDecimalDivide", 0b00, 0b0, 0o25),
    "FFN":  Opcode("FFN", "FixedToFloatingNormalize", 0b00, 0b0, 0o15),
    "FCON": Opcode("FCON", "Conversion", 0b00, 0b0, 0o35),
    "FLN":  Opcode("FLN", "FloatingLessThanNormalized", 0b00, 0b0, 0o30),
    "FNN":  Opcode("FNN", "FloatingNotEqualNormalized", 0b10, 0b0, 0o14),
}

# The remaining instructions are pseudo-instructions of various types.

CONTROL_INSTRUCTIONS = {
    "ASSIGN":   None,   # Assign Tag to Complex Address
    "END":      None,   # Specify Information for Executive
    "EQUALS":   None,   # Assign Value to Tag
    "EVEN":     None,   # Set Location Counter to Next Even Address
    "MASKGRP":  None,   # Assign Shift and Field Group Numbers
    "MODLOC":   None,   # Set Location Counter Modulo-N.
    "RESERVE":  None,   # Reserve N Words of Memory
    "SETLOC":   None,   # Set Location Counter
    "SIMULATE": None,   # Start of Simulator Routine
    "TAS":      None    # Temporarily Assign Tag to Complex Address
}

DATA_CONSTANTS = {
    "ALF":   None,      # Alphanumeric Constant
    "DEC":   None,      # Fixed Decimal Constant
    "EBC":   None,      # Extended Binary Constant
    "FLBIN": None,      # Floating-Point Binary Constant
    "FLDEC": None,      # Floating-Point Decimal Constant
    "FXBIN": None,      # Decimal to Fixed Binary Translation
    "OCT":   None       # Octal Constant
}

CONTROL_CONSTANTS = {
    "SPEC":     None,   # Special Address Constant
    "CAC":      None,   # Complete Address Constant
    "MASKBASE": None,   # Mask Base Address Constant
    "CONTROL":  None,   # Program Control Constant
    "M":        None,   # Mixed Constant
    "TAC":      None,   # Tape Address Constant
    "LINK":     None,   # Linkage Constant
    "SEGNAME":  None,   # Segment Name Constant
    "SUBCALL":  None    # Subroutine Call Constant
}

EXTENDED_INSTRUCTIONS = {
    "CSCON": None,      # Turn On Programs, Use Cosequence Counters
    "DOFF":  None,      # Turn Off Programs
    "DON":   None,      # Turn On Programs
    "SCON":  None,      # Turn On Programs, Use Sequence Counters
    "SPCR":  None,      # Save PCR
    "STOP":  None       # Stop Current Program
}

MISC_INSTRUCTIONS = {
    "COREDUMP": None,   # ?
    "DUMP":     None    # ?
}

# These are not used by YUL, so not supported.
ARGUS_INSTRUCTIONS = {
    "ARGUS":    None,   # First card of every ARGUS input deck
    "U":        None,   # Program Director
    "MACRODEF": None,   # Define macro
    "FINIS":    None,   # End of Macro definition
    "ELIMSEG":  None,   # Eliminate segment from the new symbolic tape
    "SEGMENT":  None,   # Start of a segment
    "PROGRAM":  None,   # First segment of a program
    "TESTDATA": None,   # Start of test data set
    "ELIMDATA": None,   # Eliminate the specified set of test data from the SPT
    "ELIMDERL": None,   # Eliminate a derail
    "DELETE":   None,   # Delete lines from a segment on the symbolic program tape
    "ENDARGUS": None    # End of the ARGUS input deck
}

INSTRUCTIONS = list(OPCODES.keys() + CONTROL_INSTRUCTIONS.keys() +
                    DATA_CONSTANTS.keys() + CONTROL_CONSTANTS.keys() +
                    EXTENDED_INSTRUCTIONS.keys() + MISC_INSTRUCTIONS.keys())


def make_masked_opcode(mnemonic, sequence, mask):
    o = OPCODES[mnemonic]
    return ((0o4000 * sequence) + (0o100 * mask) + (0o40 * o.b7) + o.op)


def make_unmasked_opcode(mnemonic, sequence, a, b, c):
    o = OPCODES[mnemonic]
    return ((0o4000 * sequence) + (0o1000 * o.b23) + (0o400 * a) +
            (0o200 * b) + (0o100 * c) + o.op)


def make_peripheral_opcode(mnemonic, paddr):
    o = OPCODES[mnemonic]
    return ((0o100 * paddr) + (0o40 * o.b7) + o.op)


def make_print_opcode(mnemonic, sequence, a, b, c):
    o = OPCODES[mnemonic]
    return ((0o4000 * sequence) + (0o400 * a) + (0o200 * b) + (0o100 * c) +
            (0o40 * o.b7) + o.op)


class NotImplementedException(Exception):

    def __init__(self):
        super(NotImplementedException, self).__init__(
            "This feature is not yet implemented!")


# General, masked or unmasked.

class BinaryAdd(instruction.Instruction):

    def __init__(self, sequence, mask=None, a=None, b=None, c=None):
        instruction.Instruction.__init__(self, opcode=OPCODES["BA"],
                                         sequence=sequence,
                                         mask=mask,
                                         a=a, b=b, c=c)


class DecimalAdd(instruction.Instruction):

    def __init__(self, sequence, mask=None, a=None, b=None, c=None):
        instruction.Instruction.__init__(self, opcode=OPCODES["DA"],
                                         sequence=sequence,
                                         mask=mask,
                                         a=a, b=b, c=c)


class WordAdd(instruction.Instruction):

    def __init__(self, sequence, mask=None, a=None, b=None, c=None):
        instruction.Instruction.__init__(self, opcode=OPCODES["WA"],
                                         sequence=sequence,
                                         mask=mask,
                                         a=a, b=b, c=c)


class BinarySubtract(instruction.Instruction):

    def __init__(self, sequence, mask=None, a=None, b=None, c=None):
        instruction.Instruction.__init__(self, opcode=OPCODES["BS"],
                                         sequence=sequence,
                                         mask=mask,
                                         a=a, b=b, c=c)


class DecimalSubtract(instruction.Instruction):

    def __init__(self, sequence, mask=None, a=None, b=None, c=None):
        instruction.Instruction.__init__(self, opcode=OPCODES["DS"],
                                         sequence=sequence,
                                         mask=mask,
                                         a=a, b=b, c=c)


class WordDifference(instruction.Instruction):

    def __init__(self, sequence, mask=None, a=None, b=None, c=None):
        instruction.Instruction.__init__(self, opcode=OPCODES["WD"],
                                         sequence=sequence,
                                         mask=mask,
                                         a=a, b=b, c=c)


class NotEqualAlphabetic(instruction.Instruction):

    def __init__(self, sequence, mask=None, a=None, b=None, c=None):
        instruction.Instruction.__init__(self, opcode=OPCODES["NA"],
                                        sequence=sequence,
                                        mask=mask,
                                        a=a, b=b, c=c)


class NotEqualNumeric(instruction.Instruction):

    def __init__(self, sequence, mask=None, a=None, b=None, c=None):
        instruction.Instruction.__init__(self, opcode=OPCODES["NN"],
                                         sequence=sequence,
                                         mask=mask,
                                         a=a, b=b, c=c)


class LessThanOrEqualAlphabetic(instruction.Instruction):

    def __init__(self, sequence, mask=None, a=None, b=None, c=None):
        instruction.Instruction.__init__(self, opcode=OPCODES["LA"],
                                           sequence=sequence,
                                           mask=mask,
                                           a=a, b=b, c=c)


class LessThanOrEqualNumeric(instruction.Instruction):

    def __init__(self, sequence, mask=None, a=None, b=None, c=None):
        instruction.Instruction.__init__(self, opcode=OPCODES["LN"],
                                           sequence=sequence,
                                           mask=mask,
                                           a=a, b=b, c=c)


class Transfer(instruction.Instruction):

    def __init__(self, sequence, mask=None, a=None, b=None, c=None):
        instruction.Instruction.__init__(self, opcode=OPCODES["TX"],
                                           sequence=sequence,
                                           mask=mask,
                                           a=a, b=b, c=c)


class TransferChangeSequence(instruction.Instruction):

    def __init__(self, sequence, mask=None, a=None, b=None, c=None):
        instruction.Instruction.__init__(self, opcode=OPCODES["TS"],
                                           sequence=sequence,
                                           mask=mask,
                                           a=a, b=b, c=c)


class HalfAdd(instruction.Instruction):

    def __init__(self, sequence, mask=None, a=None, b=None, c=None):
        instruction.Instruction.__init__(self, opcode=OPCODES["HA"],
                                           sequence=sequence,
                                           mask=mask,
                                           a=a, b=b, c=c)


class Superimpose(instruction.Instruction):

    def __init__(self, sequence, mask=None, a=None, b=None, c=None):
        instruction.Instruction.__init__(self, opcode=OPCODES["SM"],
                                           sequence=sequence,
                                           mask=mask,
                                           a=a, b=b, c=c)


class CheckParity(instruction.Instruction):

    def __init__(self, sequence, mask=None, a=None, b=None, c=None):
        instruction.Instruction.__init__(self, opcode=OPCODES["CP"],
                                           sequence=sequence,
                                           mask=mask,
                                           a=a, b=b, c=c)


# General, unmasked.

class BinaryMultiply(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["BM"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class DecimalMultiply(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["DM"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class BinaryAccumulate(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["BT"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class DecimalAccumulate(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["DT"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class MultipleTransfer(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["MT"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class TransferNWords(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["TN"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class ComputeOrthocount(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["CC"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class ItemTransfer(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["IT"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class ExtendedBinaryAdd(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["EBA"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class ExtendedBinarySubtract(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["EBS"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class RecordTransfer(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["RT"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class ControlProgram(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["MPC"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class Proceed(instruction.GeneralUnmasked):

    def __init__(self):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["PR"],
                                             sequence=0,
                                             a=0, b=0, c=0)


# # Inherent mask.

class ShiftWordAndSubstitute(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["SWS"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class ShiftPreservingSignAndSubstitute(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["SPS"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class ShiftWordAndExtract(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["SWE"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class ShiftPreservingSignAndExtract(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["SPE"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class ShiftAndSelect(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["SSL"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class Substitute(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["SS"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class Extract(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["EX"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


# Peripheral and print.

class ReadForward(instruction.Peripheral):

    def __init__(self, paddr):
        instruction.Peripheral.__init__(self, opcode=OPCODES["RF"],
                                        paddr=paddr)


class ReadBackward(instruction.Peripheral):

    def __init__(self, paddr):
        instruction.Peripheral.__init__(self, opcode=OPCODES["RB"],
                                        paddr=paddr)


class WriteForward(instruction.Peripheral):

    def __init__(self, paddr):
        instruction.Peripheral.__init__(self, opcode=OPCODES["WF"],
                                        paddr=paddr)


class Rewind(instruction.Peripheral):

    def __init__(self, paddr):
        instruction.Peripheral.__init__(self, opcode=OPCODES["RW"],
                                        paddr=paddr)


class PrintAlphabetic(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["PRA"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class PrintDecimal(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["PRD"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


class PrintOctal(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, opcode=OPCODES["PRO"],
                                             sequence=sequence,
                                             a=a, b=b, c=c)


# Simulator.

class Simulator(instruction.Simulator):

    def __init__(self, sequence):
        instruction.Simulator.__init__(self, opcode=OPCODES["S"],
                                       sequence=sequence)


# Scientific.

class FloatingBinaryAdd(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["FBA"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class FloatingDecimalAdd(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["FDA"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class FloatingBinarySubtract(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["FBS"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class FloatingDecimalSubtract(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["FDS"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class FloatingBinaryDivide(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["FBD"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class FloatingDecimalDivide(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["FDD"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class FloatingBinaryAddUnnormalized(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["FBAU"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class FloatingDecimalAddUnnormalized(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["FDAU"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class FloatingBinarySubtractUnnormalized(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["FBSU"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class FloatingDecimalSubtractUnnormalized(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["FDSU"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class FloatingBinaryMultiply(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["FBM"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class FloatingDecimalMultiply(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["FDM"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class MultipleUnload(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["ULD"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class FloatingBinaryAddExtendedPrecision(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["FBAE"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class FloatingBinarySubtractExtendedPrecision(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["FBSE"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class FixedBinaryDivide(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["BD"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class FixedDecimalDivide(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["DD"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class FixedToFloatingNormalize(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["FFN"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class Conversion(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["FCON"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class FloatingLessThanNormalized(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["FLN"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


class FloatingNotEqualNormalized(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, opcode=OPCODES["FNN"],
                                        sequence=sequence,
                                        a=a, b=b, c=c)


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
class AlphanumericConstant(instruction.Constant):

    def __init__(self, data):
        instruction.Constant.__init__(self, mnemonic="ALF", data=data)


# DEC: Fixed Decimal Constant
class DecimalConstant(instruction.Constant):

    def __init__(self, data):
        instruction.Constant.__init__(self, mnemonic="DEC", data=data)


# EBC: Extended Binary Constant
class ExtendedBinaryConstant(instruction.Constant):

    def __init__(self, data):
        instruction.Constant.__init__(self, mnemonic="EBC", data=data)


# FLBIN: Floating-Point Binary Constant
class FloatingBinaryConstant(instruction.Constant):

    def __init__(self, data):
        instruction.Constant.__init__(self, mnemonic="FLBIN", data=data)


# FLDEC: Floating-Point Decimal Constant
class FloatingDecimalConstant(instruction.Constant):

    def __init__(self, data):
        instruction.Constant.__init__(self, mnemonic="FLDEC", data=data)


# FXBIN: Decimal to Fixed Binary Translation
class FixedBinaryConstant(instruction.Constant):

    def __init__(self, data):
        instruction.Constant.__init__(self, mnemonic="FXBIN", data=data)


# OCT: Octal Constant
class OctalConstant(instruction.Constant):

    def __init__(self, data):
        instruction.Constant.__init__(self, mnemonic="OCT", data=data)


# Control Constants.

# SPEC: Special Address Constant
class SpecialAddressConstant(instruction.Constant):

    def __init__(self, data):
        instruction.Constant.__init__(self, mnemonic="SPEC", data=data)


# CAC: Complete Address Constant
class CompleteAddressConstant(instruction.Constant):

    def __init__(self, data):
        instruction.Constant.__init__(self, mnemonic="CAC", data=data)


# MASKBASE: Mask Base Address Constant
class MaskBaseAddressConstant(instruction.Constant):

    def __init__(self, data):
        instruction.Constant.__init__(self, mnemonic="MASKBASE", data=data)


# PCON: Program Control Constant
class ProgramControlConstant(instruction.Constant):

    def __init__(self, data):
        instruction.Constant.__init__(self, mnemonic="CONTROL", data=data)


# M: Mixed Constant
class MixedConstant(instruction.Constant):

    def __init__(self, data):
        instruction.Constant.__init__(self, mnemonic="M", data=data)


# TAC: Tape Address Constant
class TapeAddressConstant(instruction.Constant):

    def __init__(self, data):
        instruction.Constant.__init__(self, mnemonic="TAC", data=data)


# LINK: Linkage Constant
class LinkageConstant(instruction.Constant):

    def __init__(self, data):
        instruction.Constant.__init__(self, mnemonic="LINK", data=data)


# SEGNAME: Segment Name Constant
class SegmentNameConstant(instruction.Constant):

    def __init__(self, data):
        instruction.Constant.__init__(self, mnemonic="SEGNAME", data=data)


# SUBCALL: Subroutine Call Constant
class SubroutineCallConstant(instruction.Constant):

    def __init__(self, data):
        instruction.Constant.__init__(self, mnemonic="SUBCALL", data=data)


# Extended Instructions.

# "CSCON": 0,                     # Turn On Programs, Use Cosequence Counters
# "DOFF":  0,                     # Turn Off Programs
# "DON":   0,                     # Turn On Programs
# "PRA":   0o06,                  # Print Alphanumeric
# "PRD":   0o06,                  # Print Decimal
# "PRO":   0o06,                  # Print Octal
# "SCON":  0,                     # Turn On Programs, Use Sequence Counters
# "SPCR":  0,                     # Save PCR
# "STOP":  0,                     # Stop Current Program


# Miscellaneous Instructions.
# "COREDUMP": 0,                  # ?
# "DUMP":     0                   # ?

def print_instructions():
    # Generate all possible instruction codes and look for duplicates.
    opcodes = {}
    for mnemonic in OPCODES:
        opcodes[mnemonic] = []
        o = OPCODES[mnemonic]
        if o.type == "maskable":
            for i in range(2):
                for j in range(32):
                    opcodes[mnemonic].append(
                        make_masked_opcode(mnemonic, i, j))
        elif o.type == "unmasked":
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        for l in range(2):
                            opcodes[mnemonic].append(
                                make_unmasked_opcode(mnemonic, i, j, k, l))
        elif o.type == "peripheral":
            for i in range(64):
                opcodes[mnemonic].append(make_peripheral_opcode(mnemonic, i))
        elif o.type == "print":
            # Note: PRA, PRD and PRO all generate the same range of opcodes.
            # Only count once.
            if mnemonic == "PRD":
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            for l in range(2):
                                opcodes[mnemonic].append(
                                    make_print_opcode(mnemonic, i, j, k, l))
        elif o.type == "simulator":
            opcodes[mnemonic].append(0o0007)
            opcodes[mnemonic].append(0o4007)
        else:
            assert False, "Invalid instruction type!"
    opmap = {}
    for mnemonic in opcodes:
        opvals = sorted(opcodes[mnemonic])
        for opval in opvals:
            opmap[opval] = mnemonic
    for opval in sorted(opmap):
        print "0o%04o %s" % (opval, opmap[opval])


if __name__ == "__main__":
    print_instructions()
