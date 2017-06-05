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
# BA  masked    | s mmmmm  1 01001 |    101 001
# BA  unmasked  | s 10 abc 0 01001 | 10 001 001
# DA  masked    | s mmmmm  1 00001 |    100 001
# DA  unmasked  | s 10 abc 0 00001 | 10 000 001
# WA  masked    | s mmmmm  1 01101 |    101 101
# WA  unmasked  | s 10 abc 0 01101 | 10 001 101
# BS  masked    | s mmmmm  1 11001 |    111 001
# BS  unmasked  | s 10 abc 0 11001 | 10 011 001
# DS  masked    | s mmmmm  1 10001 |    110 001
# DS  unmasked  | s 10 abc 0 10001 | 10 010 001
# WD  masked    | s mmmmm  1 11101 |    111 101
# WD  unmasked  | s 10 abc 0 11101 | 10 011 101
# NA  masked    | s mmmmm  1 01100 |    101 100
# NA  unmasked  | s 10 abc 0 01100 | 10 001 100
# NN  masked    | s mmmmm  1 01000 |    101 000
# NN  unmasked  | s 10 abc 0 01000 | 10 001 000
# LA  masked    | s mmmmm  1 11100 |    111 100
# LA  unmasked  | s 10 abc 0 11100 | 10 011 100
# LN  masked    | s mmmmm  1 11000 |    111 000
# LN  unmasked  | s 10 abc 0 11000 | 10 011 000
# TX  masked    | s mmmmm  1 10000 |    110 000
# TX  unmasked  | s 10 abc 0 10000 | 10 010 000
# TS  masked    | s mmmmm  1 00100 |    100 100
# TS  unmasked  | s 10 abc 0 00100 | 10 000 100
# HA  masked    | s mmmmm  1 10101 |    110 101
# HA  unmasked  | s 10 abc 0 10101 | 10 010 101
# SM  masked    | s mmmmm  1 00101 |    100 101
# SM  unmasked  | s 10 abc 0 00101 | 10 000 101
# CP  masked    | s mmmmm  1 10100 |    110 100
# CP  unmasked  | s 10 abc 0 10100 | 10 010 100
# BM            | s 00 abc 0 01011 | 00 001 011
# DM            | s 00 abc 0 00011 | 00 000 011
# BT            | s 10 abc 0 01011 | 10 001 011
# DT            | s 10 abc 0 00011 | 10 000 011
# MT            | s 00 abc 0 10000 | 00 010 000
# TN            | s 01 abc 0 10000 | 01 010 000
# CC            | s 01 abc 0 01000 | 01 001 000
# IT            | s 01 abc 0 11000 | 01 011 000
# EBA           | s 11 abc 0 01011 | 11 001 011
# EBS           | s 11 abc 0 11011 | 11 011 011
# RT            | s 11 abc 0 11000 | 11 011 000
# MPC           | s 10 abc 0 00000 | 10 000 000
# PR            | x 000 xx 0 00110 | 00 000 110 *
# SWS           | s 10 abc 0 00110 | 10 000 110
# SPS           | s 10 abc 0 00010 | 10 000 010
# SWE           | s 10 abc 0 01110 | 10 001 110
# SPE           | s 10 abc 0 01010 | 10 001 010
# SSL           | s 10 abc 0 10110 | 10 010 110
# SS            | s 00 abc 0 00110 | 00 000 110
# EX            | s 00 abc 0 01110 | 00 001 110
# RF            | pppppp   1 11010 |    111 010
# RB            | pppppp   1 01010 |    101 010
# WF            | pppppp   1 01110 |    101 110
# RW            | pppppp   1 00010 |    100 010
# PRA           | s xx abc 1 00110 | xx 100 110
# PRD           | s xx abc 1 00110 | xx 100 110
# PRO           | s xx abc 1 00110 | xx 100 110
# S   direct    | 0 xx xxx x xx110 | xx xxx 110 ?
# S   indexed   | 1 xx xxx x xx110 | xx xxx 110 ?
# FBA           | s 01 abc 0 00001 | 01 000 001
# FDA           | s 01 abc 0 10001 | 01 010 001
# FBS           | s 01 abc 0 01001 | 01 001 001
# FDS           | s 01 abc 0 11001 | 01 011 001
# FBD           | s 01 abc 0 00101 | 01 000 101
# FDD           | s 01 abc 0 10101 | 01 010 101
# FBAU          | s 11 abc 0 00001 | 11 000 001
# FDAU          | s 11 abc 0 10001 | 11 010 001
# FBSU          | s 11 abc 0 01001 | 11 001 001
# FDSU          | s 11 abc 0 11001 | 11 011 001
# FBM           | s 11 abc 0 00101 | 11 000 101
# FDM           | s 11 abc 0 10101 | 11 010 101
# ULD           | s 11 abc 0 01101 | 11 001 101
# FBAE          | s 00 abc 0 00001 | 00 000 001
# FBSE          | s 00 abc 0 01001 | 00 001 001
# BD            | s 00 abc 0 00101 | 00 000 101
# DD            | s 00 abc 0 10101 | 00 010 101
# FFN           | s 00 abc 0 01101 | 00 001 101
# FCON          | s 00 abc 0 11101 | 00 011 101
# FLN           | s 00 abc 0 11000 | 00 011 000
# FNN           | s 10 abc 0 01100 | 10 001 100

from instruction import *


OPCODES = {
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

INSTRUCTIONS = dict(OPCODES.items() + CONTROL_INSTRUCTIONS.items() +
                    DATA_CONSTANTS.items() + CONTROL_CONSTANTS.items() +
                    EXTENDED_INSTRUCTIONS.items() + MISC_INSTRUCTIONS.items())


class NotImplemented(Exception):
    raise NotImplemented


# General, masked or unmasked.

# "BA":   0o11,                   # Binary Add
# "DA":   0o01,                   # Decimal Add
# "WA":   0o15,                   # Word Add
# "BS":   0o31,                   # Binary Subtract
# "DS":   0o21,                   # Decimal Subtract
# "WD":   0o35,                   # Word Difference
# "NA":   0o16,                   # Not equal, Alphabetic
# "NN":   0o10,                   # Not equal, Numeric
# "LA":   0o36,                   # Less than or equal, Alphabetic
# "LN":   0o30,                   # Less than or equal, Numeric
# "TX":   0o20,                   # Transfer A to C
# "TS":   0o06,                   # Transfer A to B and go to C
# "HA":   0o25,                   # Half Add (mod 2)
# "SM":   0o05,                   # Superimpose
# "CP":   0o26,                   # Check Parity

class BinaryAddMasked(GeneralMasked):

    def __init__(self, sequence, mask):
        GeneralMasked.__init__(self, mnemonic="BA", sequence=sequence,
                               mask=mask, group=1,
                               opcode=OPCODES["BA"])


class BinaryAddUnmasked(GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        GeneralUnmasked.__init__(self, mnemonic="BA", sequence=sequence,
                                 group=0, a=a, b=b, c=c,
                                 opcode=OPCODES["BA"])


class DecimalAddMasked(GeneralMasked):

    def __init__(self, sequence, mask):
        GeneralMasked.__init__(self, mnemonic="DA", sequence=sequence,
                               mask=mask, group=1,
                               opcode=OPCODES["DA"])


class DecimalAddUnmasked(GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        GeneralUnmasked.__init__(self, mnemonic="DA", sequence=sequence, group=0, a=a, b=b, c=c, opcode=OPCODES["DA"])


class WordAddMasked(GeneralMasked):

    def __init__(self, sequence, mask):
        GeneralMasked.__init__(self, mnemonic="WA", sequence=sequence, mask=mask, group=1, opcode=OPCODES["WA"])


class WordAddUnmasked(GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        GeneralUnmasked.__init__(self, mnemonic="WA", sequence=sequence, group=0, a=a, b=b, c=c, opcode=OPCODES["WA"])


class BinarySubtractMasked(GeneralMasked):

    def __init__(self, sequence, mask):
        GeneralMasked.__init__(self, mnemonic="BS", sequence=sequence, mask=mask, group=1, opcode=OPCODES["BS"])


class BinarySubtractUnmasked(GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        GeneralUnmasked.__init__(self, mnemonic="BS", sequence=sequence, group=0, a=a, b=b, c=c, opcode=OPCODES["BS"])


class DecimalSubtractMasked(GeneralMasked):

    def __init__(self, sequence, mask):
        GeneralMasked.__init__(self, mnemonic="DS", sequence=sequence, mask=mask, group=1, opcode=OPCODES["DS"])


class DecimalSubtractUnmasked(GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        GeneralUnmasked.__init__(self, mnemonic="DS", sequence=sequence, group=0, a=a, b=b, c=c, opcode=OPCODES["DS"])


class WordDifferenceMasked(GeneralMasked):

    def __init__(self, sequence, mask):
        GeneralMasked.__init__(self, mnemonic="WD", sequence=sequence, mask=mask, group=1, opcode=OPCODES["WD"])


class WordDifferenceUnmasked(GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        GeneralUnmasked.__init__(self, mnemonic="WD", sequence=sequence, group=0, a=a, b=b, c=c, opcode=OPCODES["WD"])


class NotEqualAlphabeticMasked(GeneralMasked):

    def __init__(self, sequence, mask):
        GeneralMasked.__init__(self, mnemonic="NA", sequence=sequence, mask=mask, group=1, opcode=OPCODES["NA"])


class NotEqualAlphabeticUnmasked(GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        GeneralUnmasked.__init__(self, mnemonic="NA", sequence=sequence, group=0, a=a, b=b, c=c, opcode=OPCODES["NA"])


class NotEqualNumericMasked(GeneralMasked):

    def __init__(self, sequence, mask):
        GeneralMasked.__init__(self, mnemonic="NN", sequence=sequence, mask=mask, group=1, opcode=OPCODES["NN"])


class NotEqualNumericUnmasked(GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        GeneralUnmasked.__init__(self, mnemonic="NN", sequence=sequence, group=0, a=a, b=b, c=c, opcode=OPCODES["NN"])


class LessThanOrEqualAlphabeticMasked(GeneralMasked):

    def __init__(self, sequence, mask):
        GeneralMasked.__init__(self, mnemonic="LA", sequence=sequence, mask=mask, group=1, opcode=OPCODES["LA"])


class LessThanOrEqualAlphabeticUnmasked(GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        GeneralUnmasked.__init__(self, mnemonic="LA", sequence=sequence, group=0, a=a, b=b, c=c, opcode=OPCODES["LA"])


class LessThanOrEqualNumericMasked(GeneralMasked):

    def __init__(self, sequence, mask):
        GeneralMasked.__init__(self, mnemonic="LN", sequence=sequence, mask=mask, group=1, opcode=OPCODES["LN"])


class LessThanOrEqualNumericUnmasked(GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        GeneralUnmasked.__init__(self, mnemonic="LN", sequence=sequence, group=0, a=a, b=b, c=c, opcode=OPCODES["LN"])


class TransferMasked(GeneralMasked):

    def __init__(self, sequence, mask):
        GeneralMasked.__init__(self, mnemonic="TX", sequence=sequence, mask=mask, group=1, opcode=OPCODES["TX"])


class TransferUnmasked(GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        GeneralUnmasked.__init__(self, mnemonic="TX", sequence=sequence, group=0, a=a, b=b, c=c, opcode=OPCODES["TX"])


class TransferChangeSequenceMasked(GeneralMasked):

    def __init__(self, sequence, mask):
        GeneralMasked.__init__(self, mnemonic="TS", sequence=sequence, mask=mask, group=1, opcode=OPCODES["TS"])


class TransferChangeSequenceUnmasked(GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        GeneralUnmasked.__init__(self, mnemonic="TS", sequence=sequence, group=0, a=a, b=b, c=c, opcode=OPCODES["TS"])


class HalfAddMasked(GeneralMasked):

    def __init__(self, sequence, mask):
        GeneralMasked.__init__(self, mnemonic="HA", sequence=sequence, mask=mask, group=1, opcode=OPCODES["HA"])


class HalfAddUnmasked(GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        GeneralUnmasked.__init__(self, mnemonic="HA", sequence=sequence, group=0, a=a, b=b, c=c, opcode=OPCODES["HA"])


class SuperimposeMasked(GeneralMasked):

    def __init__(self, sequence, mask):
        GeneralMasked.__init__(self, mnemonic="SM", sequence=sequence, mask=mask, group=1, opcode=OPCODES["SM"])


class SuperimposeUnmasked(GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        GeneralUnmasked.__init__(self, mnemonic="SM", sequence=sequence, group=0, a=a, b=b, c=c, opcode=OPCODES["SM"])


class CheckParityMasked(GeneralMasked):

    def __init__(self, sequence, mask):
        GeneralMasked.__init__(self, mnemonic="CP", sequence=sequence, mask=mask, group=1, opcode=OPCODES["CP"])


class CheckParityUnmasked(GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        GeneralUnmasked.__init__(self, mnemonic="CP", sequence=sequence, group=0, a=a, b=b, c=c, opcode=OPCODES["CP"])


# General, unmasked.

class BinaryMultiply(GeneralUnmasked):

    def __init__(self, sequence, a, b, c):
        GeneralUnmasked.__init__(self, mnemonic="BM", sequence=sequence, group=0, a=a, b=b, c=c, opcode=OPCODES["BM"])


class DecimalMultiply(GeneralUnmasked):
    raise NotImplemented


class BinaryAccumulate(GeneralUnmasked):
    raise NotImplemented


class DecimalAccumulate(GeneralUnmasked):
    raise NotImplemented


class MultipleTransfer(GeneralUnmasked):
    raise NotImplemented


class TransferNWords(GeneralUnmasked):
    raise NotImplemented


class ComputeOrthocount(GeneralUnmasked):
    raise NotImplemented


class ItemTransfer(GeneralUnmasked):
    raise NotImplemented


class ExtendedBinaryAdd(GeneralUnmasked):
    raise NotImplemented


class ExtendedBinarySubtract(GeneralUnmasked):
    raise NotImplemented


class RecordTransfer(GeneralUnmasked):
    raise NotImplemented


class ControlProgram(GeneralUnmasked):
    raise NotImplemented


class Proceed(GeneralUnmasked):
    raise NotImplemented


# # Inherent mask.

class ShiftWordAndSubstitute(GeneralUnmasked):
    raise NotImplemented


class ShiftPreservingSignAndSubstitute(GeneralUnmasked):
    raise NotImplemented


class ShiftWordAndExtract(GeneralUnmasked):
    raise NotImplemented


class ShiftPreservingSignAndExtract(GeneralUnmasked):
    raise NotImplemented


class ShiftAndSelect(GeneralUnmasked):
    raise NotImplemented


class Substitute(GeneralUnmasked):
    raise NotImplemented


class Extract(GeneralUnmasked):
    raise NotImplemented


# Peripheral and print.

class ReadForward(Peripheral):
    raise NotImplemented


class ReadBackward(Peripheral):
    raise NotImplemented


class WriteForward(Peripheral):
    raise NotImplemented


class Rewind(Peripheral):
    raise NotImplemented


# Simulator.
# "S":    0o07,                   # Simulate

class Simulator(Simulator):
    raise NotImplemented


# Scientific.

# "FBA":  0o01,                   # Floating Binary Add

class FloatingBinaryAdd(Scientific):
    raise NotImplemented


# "FDA":  0o21,                   # Floating Decimal Add
class FloatingDecimalAdd(Scientific):
    raise NotImplemented


# "FBS":  0o11,                   # Floating Binary Subtract
class FloatingBinarySubtract(Scientific):
    raise NotImplemented


# "FDS":  0o31,                   # Floating Decimal Subtract
class FloatingDecimalSubtract(Scientific):
    raise NotImplemented


# "FBD":  0o05,                   # Floating Binary Divide
class FloatingBinaryDivide(Scientific):
    raise NotImplemented


# "FDD":  0o25,                   # Floating Decimal Divide
class FloatingDecimalDivide(Scientific):
    raise NotImplemented


# "FBAU": 0o01,                   # Floating Binary Add, Unnormalized
class FloatingBinaryAddUnnormalized(Scientific):
    raise NotImplemented


# "FDAU": 0o21,                   # Floating Decimal Add, Unnormalized
class FloatingDecimalAddUnnormalized(Scientific):
    raise NotImplemented


# "FBSU": 0o11,                   # Floating Binary Subtract, Unnormalized
class FloatingBinarySubtractUnnormalized(Scientific):
    raise NotImplemented


# "FDSU": 0o31,                   # Floating Decimal Subtract, Unnormalized
class FloatingDecimalSubtractUnnormalized(Scientific):
    raise NotImplemented


# "FBM":  0o05,                   # Floating Binary Multiply
class FloatingBinaryMultiply(Scientific):
    raise NotImplemented


# "FDM":  0o25,                   # Floating Decimal Multiply
class FloatingDecimalMultiply(Scientific):
    raise NotImplemented


# "ULD":  0o15,                   # Multiple Unload
class MultipleUnload(Scientific):
    raise NotImplemented


# "FBAE": 0o01,                   # Floating Binary Add, Extended precision
class FloatingBinaryAddExtendedPrecision(Scientific):
    raise NotImplemented


# "FBSE": 0o11,                   # Floating Binary Subtract, Extended precision
class FloatingBinarySubtractExtendedPrecision(Scientific):
    raise NotImplemented


# "BD":   0o05,                   # Fixed Binary Divide
class FixedBinaryDivide(Scientific):
    raise NotImplemented


# "DD":   0o25,                   # Fixed Decimal Divide
class FixedDecimalDivide(Scientific):
    raise NotImplemented


# "FFN":  0o15,                   # Fixed-to-Floating Normalize
class FixedToFloatingNormalize(Scientific):
    raise NotImplemented


# "FCON": 0o35,                   # Conversion
class Conversion(Scientific):
    raise NotImplemented


# "FLN":  0o30,                   # Floating Less than, Normalized
class FloatingLessThanNormalized(Scientific):
    raise NotImplemented


# "FNN":  0o16,                   # Floating Not equal, Normalized
class FloatingNotEqualNormalized(Scientific):
    raise NotImplemented


# Control Instructions.

# "ASSIGN":   0,                  # Assign Tag to Complex Address
class AssignTag(AssemblyControl):
    raise NotImplemented


# "END":      0,                  # Specify Information for Executive
class End(AssemblyControl):
    raise NotImplemented


# "EQUALS":   0,                  # Assign Value to Tag
class Equals(AssemblyControl):
    raise NotImplemented


# "EVEN":     0,                  # Set Location Counter to Next Even Address
class Even(AssemblyControl):
    raise NotImplemented


# "MASKGRP":  0,                  # Assign Shift and Field Group Numbers
class MaskGroup(AssemblyControl):
    raise NotImplemented


# "MODLOC":   0,                  # Set Location Counter Modulo-N.
class SetLocationCounterModuloN(AssemblyControl):
    raise NotImplemented


# "RESERVE":  0,                  # Reserve N Words of Memory
class Reserve(AssemblyControl):
    raise NotImplemented


# "SETLOC":   0,                  # Set Location Counter
class SetLocationCounter(AssemblyControl):
    raise NotImplemented


# "SIMULATE": 0,                  # Start of Simulator Routine
class Simulate(AssemblyControl):
    raise NotImplemented


# "TAS":      0                   # Temporarily Assign Tag to Complex Address
class TemporarilyAssignTag(AssemblyControl):
    raise NotImplemented


# Data Constants.

# "ALF":   0,                     # Alphanumeric Constant
class AlphanumericConstant(Constant):
    raise NotImplemented


# "DEC":   0,                     # Fixed Decimal Constant
class DecimalConstant(Constant):
    raise NotImplemented


# "EBC":   0,                     # Extended Binary Constant
class ExtendedBinaryConstant(Constant):
    raise NotImplemented


# "FLBIN": 0,                     # Floating-Point Binary Constant
class FloatingBinaryConstant(Constant):
    raise NotImplemented


# "FLDEC": 0,                     # Floating-Point Decimal Constant
class FloatingDecimalConstant(Constant):
    raise NotImplemented


# "FXBIN": 0,                     # Decimal to Fixed Binary Translation
class FixedBinaryConstant(Constant):
    raise NotImplemented


# "OCT":   0                      # Octal Constant
class OctalConstant(Constant):
    raise NotImplemented


# Control Constants.

# "SPEC":     0,                  # Special Address Constant
class SpecialAddressConstant(Constant):
    raise NotImplemented


# "CAC":      0,                  # Complete Address Constant
class CompleteAddressConstant(Constant):
    raise NotImplemented


# "MASKBASE": 0,                  # Mask Base Address Constant
class MaskBaseAddressConstant(Constant):
    raise NotImplemented


# "CONTROL":  0,                  # Program Control Constant
class ProgramControlConstant(Constant):
    raise NotImplemented


# "M":        0,                  # Mixed Constant
class MixedConstant(Constant):
    raise NotImplemented


# "TAC":      0,                  # Tape Address Constant
class TapeAddressConstant(Constant):
    raise NotImplemented


# "LINK":     0,                  # Linkage Constant
class LinkageConstant(Constant):
    raise NotImplemented


# "SEGNAME":  0,                  # Segment Name Constant
class SegmentNameConstant(Constant):
    raise NotImplemented


# "SUBCALL":  0                   # Subroutine Call Constant
class SubroutineCallConstant(Constant):
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
