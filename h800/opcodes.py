#!/usr/bin/env python

OPCODES = {

    # General, masked or unmasked.
    "BA":   0o13,                   # Binary Add
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
    "HA":   0o23,                   # Half Add (mod 2)
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
    "SWE":  0o36,                   # Shift Word and Extract
    "SPE":  0o12,                   # Shift Preserving sign and Extract
    "SSL":  0o26,                   # Shift and Select
    "SS":   0o06,                   # Substitute
    "EX":   0o16,                   # Extract

    # Peripheral and print.
    "RF":   0o32,                   # Read Forward
    "RB":   0o00,                   # Read Backward
    "WF":   0o00,                   # Write Forward
    "RW":   0o00,                   # Rewind
    "PRA":  0o00,                   # Print Alphanumeric
    "PRD":  0o00,                   # Print Decimal
    "PRO":  0o00,                   # Print Octal

    # Simulator.
    "S":    0o00,                   # Simulate

    # Scientific.
    "FBA":  0o00,                   # Floating Binary Add
    "FDA":  0o00,                   # Floating Decimal Add
    "FBS":  0o00,                   # Floating Binary Subtract
    "FDS":  0o00,                   # Floating Decimal Subtract
    "FBD":  0o00,                   # Floating Binary Divide
    "FDD":  0o00,                   # Floating Decimal Divide
    "FBAU": 0o00,                   # Floating Binary Add, Unnormalized
    "FDAU": 0o00,                   # Floating Decimal Add, Unnormalized
    "FBSU": 0o00,                   # Floating Binary Subtract, Unnormalized
    "FDSU": 0o00,                   # Floating Decimal Subtract, Unnormalized
    "FBM":  0o00,                   # Floating Binary Multiply
    "FDM":  0o00,                   # Floating Decimal Multiply
    "ULD":  0o00,                   # Multiple Unload
    "FBAE": 0o00,                   # Floating Binary Add, Extended precision
    "FBSE": 0o00,                   # Floating Binary Subtract, Extended precision
    "BD":   0o00,                   # Fixed Binary Divide
    "DD":   0o00,                   # Fixed Decimal Divide
    "FFN":  0o00,                   # Fixed-to-Floating Normalize
    "FCON": 0o00,                   # Conversion
    "FLN":  0o00,                   # Floating Less than, Normalized
    "FNN":  0o00,                   # Floating Not equal, Normalized

}
