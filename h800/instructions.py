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
# BA  masked    | s mmmmm  1 01001 |
# BA  unmasked  | s 10 abc 0 01001 |
# DA  masked    | s mmmmm  1 00001 |
# DA  unmasked  | s 10 abc 0 00001 |
# WA  masked    | s mmmmm  1 01101 |
# WA  unmasked  | s 10 abc 0 01101 |
# BS  masked    | s mmmmm  1 11001 |
# BS  unmasked  | s 10 abc 0 11001 |
# DS  masked    | s mmmmm  1 10001 |
# DS  unmasked  | s 10 abc 0 10001 |
# WD  masked    | s mmmmm  1 11101 |
# WD  unmasked  | s 10 abc 0 11101 |
# NA  masked    | s mmmmm  1 01100 |
# NA  unmasked  | s 10 abc 0 01100 |
# NN  masked    | s mmmmm  1 01000 |
# NN  unmasked  | s 10 abc 0 01000 |
# LA  masked    | s mmmmm  1 11100 |
# LA  unmasked  | s 10 abc 0 11100 |
# LN  masked    | s mmmmm  1 11000 |
# LN  unmasked  | s 10 abc 0 11000 |
# TX  masked    | s mmmmm  1 10000 |
# TX  unmasked  | s 10 abc 0 10000 |
# TS  masked    | s mmmmm  1 00100 |
# TS  unmasked  | s 10 abc 0 00100 |
# HA  masked    | s mmmmm  1 10101 |
# HA  unmasked  | s 10 abc 0 10101 |
# SM  masked    | s mmmmm  1 00101 |
# SM  unmasked  | s 10 abc 0 00101 |
# CP  masked    | s mmmmm  1 10100 |
# CP  unmasked  | s 10 abc 0 10100 |
# BM            | s 00 abc 0 01011 |
# DM            | s 00 abc 0 00011 |
# BT            | s 10 abc 0 01011 |
# DT            | s 10 abc 0 00011 |
# MT            | s 00 abc 0 10000 |
# TN            | s 01 abc 0 10000 |
# CC            | s 01 abc 0 01000 |
# IT            | s 01 abc 0 11000 |
# EBA           | s 11 abc 0 01011 |
# EBS           | s 11 abc 0 11011 |
# RT            | s 11 abc 0 11000 |
# MPC           | s 10 abc 0 00000 |
# PR            | x 000 xx 0 00110 |
# SWS           | s 10 abc 0 00110 |
# SPS           | s 10 abc 0 00010 |
# SWE           | s 10 abc 0 01110 |
# SPE           | s 10 abc 0 01010 |
# SSL           | s 10 abc 0 10110 |
# SS            | s 00 abc 0 00110 |
# EX            | s 00 abc 0 01110 |
# RF            | pppppp   1 11010 |
# RB            | pppppp   1 01010 |
# WF            | pppppp   1 01110 |
# RW            | pppppp   1 00010 |
# PRA           | s xx abc 1 00110 |
# PRD           | s xx abc 1 00110 |
# PRO           | s xx abc 1 00110 |
# S   direct    | 0 xxxxxx  xx 110 |
# S   indexed   | 1 xxxxxx  xx 110 |
# FBA           | s 01 abc 0 00001 |
# FDA           | s 01 abc 0 10001 |
# FBS           | s 01 abc 0 01001 |
# FDS           | s 01 abc 0 11001 |
# FBD           | s 01 abc 0 00101 |
# FDD           | s 01 abc 0 10101 |
# FBAU          | s 11 abc 0 00001 |
# FDAU          | s 11 abc 0 10001 |
# FBSU          | s 11 abc 0 01001 |
# FDSU          | s 11 abc 0 11001 |
# FBM           | s 11 abc 0 00101 |
# FDM           | s 11 abc 0 10101 |
# ULD           | s 11 abc 0 01101 |
# FBAE          | s 00 abc 0 00001 |
# FBSE          | s 00 abc 0 01001 |
# BD            | s 00 abc 0 00101 |
# DD            | s 00 abc 0 10101 |
# FFN           | s 00 abc 0 01101 |
# FCON          | s 00 abc 0 11101 |
# FLN           | s 00 abc 0 11000 |
# FNN           | s 10 abc 0 01100 |

MACHINE_INSTRUCTIONS = {
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

INSTRUCTIONS = dict(MACHINE_INSTRUCTIONS.items() + CONTROL_INSTRUCTIONS.items() +
                    DATA_CONSTANTS.items() + CONTROL_CONSTANTS.items() +
                    EXTENDED_INSTRUCTIONS.items() + MISC_INSTRUCTIONS.items())
