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

import instruction


# Base opcodes (bits 8-12 of the command code). These are modified by the
# value of bit 7 (0 for unmasked, or 1 for masked), and bits 2-3 for unmasked
# instructions.

BASE_OPCODES = {
    # General, masked or unmasked.
    "BA":   0o11,                   # Binary Add
    "DA":   0o01,                   # Decimal Add
    "WA":   0o15,                   # Word Add
    "BS":   0o31,                   # Binary Subtract
    "DS":   0o21,                   # Decimal Subtract
    "WD":   0o35,                   # Word Difference
    "NA":   0o16,                   # Not equal, Alphabetic
    "NN":   0o10,                   # Not equal, Numeric
    "LA":   0o36,                   # Less than or equal, Alphabetic
    "LN":   0o30,                   # Less than or equal, Numeric
    "TX":   0o20,                   # Transfer A to C
    "TS":   0o06,                   # Transfer A to B and go to C
    "HA":   0o25,                   # Half Add (mod 2)
    "SM":   0o05,                   # Superimpose
    "CP":   0o26,                   # Check Parity

    # General, unmasked.
    "BM":   0o13,                   # Binary Multiply
    "DM":   0o03,                   # Decimal Multiply
    "BT":   0o13,                   # Binary Accumulate
    "DT":   0o03,                   # Decimal Accumulate
    "MT":   0o20,                   # Multiple Transfer
    "TN":   0o20,                   # Transfer N words
    "CC":   0o10,                   # Compute Orthocount
    "IT":   0o30,                   # Item Transfer
    "EBA":  0o13,                   # Extended Binary Add
    "EBS":  0o33,                   # Extended Binary Subtract
    "RT":   0o30,                   # Record Transfer
    "MPC":  0o00,                   # Control Program
    "PR":   0o00,                   # Proceed

    # Inherent mask.
    "SWS":  0o06,                   # Shift Word and Substitute
    "SPS":  0o02,                   # Shift Preserving sign and Substitute
    "SWE":  0o16,                   # Shift Word and Extract
    "SPE":  0o12,                   # Shift Preserving sign and Extract
    "SSL":  0o26,                   # Shift and Select
    "SS":   0o06,                   # Substitute
    "EX":   0o16,                   # Extract

    # Peripheral and print.
    "RF":   0o32,                   # Read Forward
    "RB":   0o12,                   # Read Backward
    "WF":   0o16,                   # Write Forward
    "RW":   0o02,                   # Rewind
    "PRA":  0o46,                   # Print Alphabetic
    "PRD":  0o46,                   # Print Decimal
    "PRO":  0o46,                   # Print OCtal

    # Simulator.
    "S":    0o07,                   # Simulate

    # Scientific.
    "FBA":  0o01,                   # Floating Binary Add
    "FDA":  0o21,                   # Floating Decimal Add
    "FBS":  0o11,                   # Floating Binary Subtract
    "FDS":  0o31,                   # Floating Decimal Subtract
    "FBD":  0o05,                   # Floating Binary Divide
    "FDD":  0o25,                   # Floating Decimal Divide
    "FBAU": 0o01,                   # Floating Binary Add, Unnormalized
    "FDAU": 0o21,                   # Floating Decimal Add, Unnormalized
    "FBSU": 0o11,                   # Floating Binary Subtract, Unnormalized
    "FDSU": 0o31,                   # Floating Decimal Subtract, Unnormalized
    "FBM":  0o05,                   # Floating Binary Multiply
    "FDM":  0o25,                   # Floating Decimal Multiply
    "ULD":  0o15,                   # Multiple Unload
    "FBAE": 0o01,                   # Floating Binary Add, Extended precision
    "FBSE": 0o11,                   # Floating Binary Subtract, Extended precision
    "BD":   0o05,                   # Fixed Binary Divide
    "DD":   0o25,                   # Fixed Decimal Divide
    "FFN":  0o15,                   # Fixed-to-Floating Normalize
    "FCON": 0o35,                   # Conversion
    "FLN":  0o30,                   # Floating Less than, Normalized
    "FNN":  0o16,                   # Floating Not equal, Normalized
}

# The remaining instructions are pseudo-instructions of various types.

CONTROL_INSTRUCTIONS = {
    "ASSIGN":   0,                  # Assign Tag to Complex Address
    "END":      0,                  # Specify Information for Executive
    "EQUALS":   0,                  # Assign Value to Tag
    "EVEN":     0,                  # Set Location Counter to Next Even Address
    "MASKGRP":  0,                  # Assign Shift and Field Group Numbers
    "MODLOC":   0,                  # Set Location Counter Modulo-N.
    "RESERVE":  0,                  # Reserve N Words of Memory
    "SETLOC":   0,                  # Set Location Counter
    "SIMULATE": 0,                  # Start of Simulator Routine
    "TAS":      0                   # Temporarily Assign Tag to Complex Address
}

DATA_CONSTANTS = {
    "ALF":   0,                     # Alphanumeric Constant
    "DEC":   0,                     # Fixed Decimal Constant
    "EBC":   0,                     # Extended Binary Constant
    "FLBIN": 0,                     # Floating-Point Binary Constant
    "FLDEC": 0,                     # Floating-Point Decimal Constant
    "FXBIN": 0,                     # Decimal to Fixed Binary Translation
    "OCT":   0                      # Octal Constant
}

CONTROL_CONSTANTS = {
    "SPEC":     0,                  # Special Address Constant
    "CAC":      0,                  # Complete Address Constant
    "MASKBASE": 0,                  # Mask Base Address Constant
    "CONTROL":  0,                  # Program Control Constant
    "M":        0,                  # Mixed Constant
    "TAC":      0,                  # Tape Address Constant
    "LINK":     0,                  # Linkage Constant
    "SEGNAME":  0,                  # Segment Name Constant
    "SUBCALL":  0                   # Subroutine Call Constant
}

EXTENDED_INSTRUCTIONS = {
    "CSCON": 0,                     # Turn On Programs, Use Cosequence Counters
    "DOFF":  0,                     # Turn Off Programs
    "DON":   0,                     # Turn On Programs
    "PRA":   0o06,                  # Print Alphanumeric
    "PRD":   0o06,                  # Print Decimal
    "PRO":   0o06,                  # Print Octal
    "SCON":  0,                     # Turn On Programs, Use Sequence Counters
    "SPCR":  0,                     # Save PCR
    "STOP":  0,                     # Stop Current Program
}

MISC_INSTRUCTIONS = {
    "COREDUMP": 0,                  # ?
    "DUMP":     0                   # ?
}

INSTRUCTIONS = dict(BASE_OPCODES.items() + CONTROL_INSTRUCTIONS.items() +
                    DATA_CONSTANTS.items() + CONTROL_CONSTANTS.items() +
                    EXTENDED_INSTRUCTIONS.items() + MISC_INSTRUCTIONS.items())


# These are just convenient representations of bits 2 and 3 of the command code.
BITS23_00 = 0o000
BITS23_01 = 0o100
BITS23_10 = 0o200
BITS23_11 = 0o300

# These are just convenient representations of bit 7 of the command code.
BIT7_0 = 0o00
BIT7_1 = 0o40


class NotImplementedException(Exception):

    def __init__(self):
        super(NotImplementedException, self).__init__("This feature is not yet implemented!")


# General, masked or unmasked.

class BinaryAddMasked(instruction.GeneralMasked):

    def __init__(self, sequence, mask):
        instruction.GeneralMasked.__init__(self, mnemonic="BA",
                                           sequence=sequence,
                                           mask=mask,
                                           opcode=BIT7_1+BASE_OPCODES["BA"])


class BinaryAddUnmasked(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="BA",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["BA"])


class DecimalAddMasked(instruction.GeneralMasked):

    def __init__(self, sequence, mask):
        instruction.GeneralMasked.__init__(self, mnemonic="DA",
                                           sequence=sequence,
                                           mask=mask,
                                           opcode=BIT7_1+BASE_OPCODES["DA"])


class DecimalAddUnmasked(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="DA",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["DA"])


class WordAddMasked(instruction.GeneralMasked):

    def __init__(self, sequence, mask):
        instruction.GeneralMasked.__init__(self, mnemonic="WA",
                                           sequence=sequence,
                                           mask=mask,
                                           opcode=BIT7_1+BASE_OPCODES["WA"])


class WordAddUnmasked(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="WA",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["WA"])


class BinarySubtractMasked(instruction.GeneralMasked):

    def __init__(self, sequence, mask):
        instruction.GeneralMasked.__init__(self, mnemonic="BS",
                                           sequence=sequence,
                                           mask=mask,
                                           opcode=BIT7_1+BASE_OPCODES["BS"])


class BinarySubtractUnmasked(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="BS",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["BS"])


class DecimalSubtractMasked(instruction.GeneralMasked):

    def __init__(self, sequence, mask):
        instruction.GeneralMasked.__init__(self, mnemonic="DS",
                                           sequence=sequence,
                                           mask=mask,
                                           opcode=BIT7_1+BASE_OPCODES["DS"])


class DecimalSubtractUnmasked(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="DS",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["DS"])


class WordDifferenceMasked(instruction.GeneralMasked):

    def __init__(self, sequence, mask):
        instruction.GeneralMasked.__init__(self, mnemonic="WD",
                                           sequence=sequence,
                                           mask=mask,
                                           opcode=BIT7_1+BASE_OPCODES["WD"])


class WordDifferenceUnmasked(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="WD",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["WD"])


class NotEqualAlphabeticMasked(instruction.GeneralMasked):

    def __init__(self, sequence, mask):
        instruction.GeneralMasked.__init__(self, mnemonic="NA",
                                           sequence=sequence,
                                           mask=mask,
                                           opcode=BIT7_1+BASE_OPCODES["NA"])


class NotEqualAlphabeticUnmasked(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="NA",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["NA"])


class NotEqualNumericMasked(instruction.GeneralMasked):

    def __init__(self, sequence, mask):
        instruction.GeneralMasked.__init__(self, mnemonic="NN",
                                           sequence=sequence,
                                           mask=mask,
                                           opcode=BIT7_1+BASE_OPCODES["NN"])


class NotEqualNumericUnmasked(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="NN",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["NN"])


class LessThanOrEqualAlphabeticMasked(instruction.GeneralMasked):

    def __init__(self, sequence, mask):
        instruction.GeneralMasked.__init__(self, mnemonic="LA",
                                           sequence=sequence,
                                           mask=mask,
                                           opcode=BIT7_1+BASE_OPCODES["LA"])


class LessThanOrEqualAlphabeticUnmasked(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="LA",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["LA"])


class LessThanOrEqualNumericMasked(instruction.GeneralMasked):

    def __init__(self, sequence, mask):
        instruction.GeneralMasked.__init__(self, mnemonic="LN",
                                           sequence=sequence,
                                           mask=mask,
                                           opcode=BIT7_1+BASE_OPCODES["LN"])


class LessThanOrEqualNumericUnmasked(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="LN",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["LN"])


class TransferMasked(instruction.GeneralMasked):

    def __init__(self, sequence, mask):
        instruction.GeneralMasked.__init__(self, mnemonic="TX",
                                           sequence=sequence,
                                           mask=mask,
                                           opcode=BIT7_1+BASE_OPCODES["TX"])


class TransferUnmasked(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="TX",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["TX"])


class TransferChangeSequenceMasked(instruction.GeneralMasked):

    def __init__(self, sequence, mask):
        instruction.GeneralMasked.__init__(self, mnemonic="TS",
                                           sequence=sequence,
                                           mask=mask,
                                           opcode=BIT7_1+BASE_OPCODES["TS"])


class TransferChangeSequenceUnmasked(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="TS",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["TS"])


class HalfAddMasked(instruction.GeneralMasked):

    def __init__(self, sequence, mask):
        instruction.GeneralMasked.__init__(self, mnemonic="HA",
                                           sequence=sequence,
                                           mask=mask,
                                           opcode=BIT7_1+BASE_OPCODES["HA"])


class HalfAddUnmasked(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="HA",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["HA"])


class SuperimposeMasked(instruction.GeneralMasked):

    def __init__(self, sequence, mask):
        instruction.GeneralMasked.__init__(self, mnemonic="SM",
                                           sequence=sequence,
                                           mask=mask,
                                           opcode=BIT7_1+BASE_OPCODES["SM"])


class SuperimposeUnmasked(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="SM",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["SM"])


class CheckParityMasked(instruction.GeneralMasked):

    def __init__(self, sequence, mask):
        instruction.GeneralMasked.__init__(self, mnemonic="CP",
                                           sequence=sequence,
                                           mask=mask,
                                           opcode=BIT7_1+BASE_OPCODES["CP"])


class CheckParityUnmasked(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="CP",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["CP"])


# General, unmasked.

class BinaryMultiply(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="BM",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_00+BASE_OPCODES["BM"])


class DecimalMultiply(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="DM",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_00+BASE_OPCODES["DM"])


class BinaryAccumulate(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="BT",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["BT"])


class DecimalAccumulate(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="DT",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["DT"])


class MultipleTransfer(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="MT",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_00+BASE_OPCODES["MT"])


class TransferNWords(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="TN",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_01+BASE_OPCODES["TN"])


class ComputeOrthocount(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="CC",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_01+BASE_OPCODES["CC"])


class ItemTransfer(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="IT",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_01+BASE_OPCODES["IT"])


class ExtendedBinaryAdd(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="EBA",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_11+BASE_OPCODES["EBA"])


class ExtendedBinarySubtract(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="EBS",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_11+BASE_OPCODES["EBS"])


class RecordTransfer(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="RT",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_11+BASE_OPCODES["RT"])


class ControlProgram(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="MPC",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["MPC"])


class Proceed(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="PR",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_00+BASE_OPCODES["PR"])


# # Inherent mask.

class ShiftWordAndSubstitute(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="SWS",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["SWS"])


class ShiftPreservingSignAndSubstitute(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="SPS",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["SPS"])


class ShiftWordAndExtract(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="SWE",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["SWE"])


class ShiftPreservingSignAndExtract(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="SPE",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["SPE"])


class ShiftAndSelect(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="SSL",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_10+BASE_OPCODES["SSL"])


class Substitute(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="SS",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_00+BASE_OPCODES["SS"])


class Extract(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="EX",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BITS23_00+BASE_OPCODES["EX"])


# Peripheral and print.

class ReadForward(instruction.Peripheral):

    def __init__(self, paddr):
        instruction.Peripheral.__init__(self, mnemonic="RF",
                                        paddr=paddr,
                                        opcode=BIT7_1+BASE_OPCODES["RF"])


class ReadBackward(instruction.Peripheral):

    def __init__(self, paddr):
        instruction.Peripheral.__init__(self, mnemonic="RB",
                                        paddr=paddr,
                                        opcode=BIT7_1+BASE_OPCODES["RB"])


class WriteForward(instruction.Peripheral):

    def __init__(self, paddr):
        instruction.Peripheral.__init__(self, mnemonic="WF",
                                        paddr=paddr,
                                        opcode=BIT7_1+BASE_OPCODES["WF"])


class Rewind(instruction.Peripheral):

    def __init__(self, paddr):
        instruction.Peripheral.__init__(self, mnemonic="RW",
                                        paddr=paddr,
                                        opcode=BIT7_1+BASE_OPCODES["RW"])


class PrintAlphabetic(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="PRA",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BIT7_1+BASE_OPCODES["PRA"])


class PrintDecimal(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="PRD",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BIT7_1+BASE_OPCODES["PRD"])


class PrintOctal(instruction.GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        instruction.GeneralUnmasked.__init__(self, mnemonic="PRO",
                                             sequence=sequence,
                                             a=a, b=b, c=c,
                                             opcode=BIT7_1+BASE_OPCODES["PRO"])


# Simulator.

class Simulator(instruction.Simulator):

    def __init__(self, sequence):
        instruction.Simulator.__init__(self, mnemonic="S",
                                       sequence=sequence,
                                       opcode=BASE_OPCODES["S"])


# Scientific.

class FloatingBinaryAdd(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="FBA",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_01+BASE_OPCODES["FBA"])


class FloatingDecimalAdd(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="FDA",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_01+BASE_OPCODES["FDA"])


class FloatingBinarySubtract(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="FBS",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_01+BASE_OPCODES["FBS"])


class FloatingDecimalSubtract(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="FDS",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_01+BASE_OPCODES["FDS"])


class FloatingBinaryDivide(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="FBD",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_01+BASE_OPCODES["FBD"])


class FloatingDecimalDivide(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="FDD",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_01+BASE_OPCODES["FDD"])


class FloatingBinaryAddUnnormalized(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="FBAU",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_11+BASE_OPCODES["FBAU"])


class FloatingDecimalAddUnnormalized(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="FDAU",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_11+BASE_OPCODES["FDAU"])


class FloatingBinarySubtractUnnormalized(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="FBSU",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_11+BASE_OPCODES["FBSU"])


class FloatingDecimalSubtractUnnormalized(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="FDSU",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_11+BASE_OPCODES["FDSU"])


class FloatingBinaryMultiply(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="FBM",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_11+BASE_OPCODES["FBM"])


class FloatingDecimalMultiply(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="FDM",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_11+BASE_OPCODES["FDM"])


class MultipleUnload(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="ULD",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_11+BASE_OPCODES["ULD"])


class FloatingBinaryAddExtendedPrecision(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="FBAE",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_00+BASE_OPCODES["FBAE"])


class FloatingBinarySubtractExtendedPrecision(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="FBSE",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_00+BASE_OPCODES["FBSE"])


class FixedBinaryDivide(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="BD",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_00+BASE_OPCODES["BD"])


class FixedDecimalDivide(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="DD",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_00+BASE_OPCODES["DD"])


class FixedToFloatingNormalize(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="FFN",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_00+BASE_OPCODES["FFN"])


class Conversion(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="FCON",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_00+BASE_OPCODES["FCON"])


class FloatingLessThanNormalized(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="FLN",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_00+BASE_OPCODES["FLN"])


class FloatingNotEqualNormalized(instruction.Scientific):

    def __init__(self, sequence, a, b, c):
        instruction.Scientific.__init__(self, mnemonic="FNN",
                                        sequence=sequence,
                                        a=a, b=b, c=c,
                                        opcode=BITS23_10+BASE_OPCODES["FNN"])


# Control Instructions.

# Assign Tag to Complex Address
class AssignTag(instruction.AssemblyControl):
    raise NotImplemented


# Specify Information for Executive
class End(instruction.AssemblyControl):
    raise NotImplemented


# Assign Value to Tag
class Equals(instruction.AssemblyControl):
    raise NotImplemented


# Set Location Counter to Next Even Address
class Even(instruction.AssemblyControl):
    raise NotImplemented


# Assign Shift and Field Group Numbers
class MaskGroup(instruction.AssemblyControl):
    raise NotImplemented


# Set Location Counter Modulo-N.
class SetLocationCounterModuloN(instruction.AssemblyControl):
    raise NotImplemented


# Reserve N Words of Memory
class Reserve(instruction.AssemblyControl):
    raise NotImplemented


# Set Location Counter
class SetLocationCounter(instruction.AssemblyControl):
    raise NotImplemented


# Start of Simulator Routine
class Simulate(instruction.AssemblyControl):
    raise NotImplemented


# Temporarily Assign Tag to Complex Address
class TemporarilyAssignTag(instruction.AssemblyControl):
    raise NotImplemented


# Data Constants.

# Alphanumeric Constant
class AlphanumericConstant(instruction.Constant):
    raise NotImplemented


# Fixed Decimal Constant
class DecimalConstant(instruction.Constant):
    raise NotImplemented


# Extended Binary Constant
class ExtendedBinaryConstant(instruction.Constant):
    raise NotImplemented


# Floating-Point Binary Constant
class FloatingBinaryConstant(instruction.Constant):
    raise NotImplemented


# Floating-Point Decimal Constant
class FloatingDecimalConstant(instruction.Constant):
    raise NotImplemented


# Decimal to Fixed Binary Translation
class FixedBinaryConstant(instruction.Constant):
    raise NotImplemented


# Octal Constant
class OctalConstant(instruction.Constant):
    raise NotImplemented


# Control Constants.

# Special Address Constant
class SpecialAddressConstant(instruction.Constant):
    raise NotImplemented


# Complete Address Constant
class CompleteAddressConstant(instruction.Constant):
    raise NotImplemented


# Mask Base Address Constant
class MaskBaseAddressConstant(instruction.Constant):
    raise NotImplemented


# Program Control Constant
class ProgramControlConstant(instruction.Constant):
    raise NotImplemented


# Mixed Constant
class MixedConstant(instruction.Constant):
    raise NotImplemented


# Tape Address Constant
class TapeAddressConstant(instruction.Constant):
    raise NotImplemented


# Linkage Constant
class LinkageConstant(instruction.Constant):
    raise NotImplemented


# Segment Name Constant
class SegmentNameConstant(instruction.Constant):
    raise NotImplemented


# Subroutine Call Constant
class SubroutineCallConstant(instruction.Constant):
    raise NotImplemented


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


def main():
    # Tester goes here.
    print "TEST: TBD."
    # TODO
    print "PASS"


if __name__ == '__main__':
    main()
