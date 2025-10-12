from h800 import instruction
from h800.opcodes import (
    OPCODES,
    make_masked_opcode,
    make_peripheral_opcode,
    make_print_opcode,
    make_unmasked_opcode,
)

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


class NotImplementedError(Exception):
    def __init__(self):
        super().__init__("This feature is not yet implemented!")


class GeneralMasked(instruction.Instruction):
    """General masked instruction class."""

    def __init__(self, opcode, sequence, mask):
        super().__init__(opcode=opcode, sequence=sequence, mask=mask)


class GeneralUnmasked(instruction.Instruction):
    """General unmasked instruction class."""

    def __init__(self, opcode, sequence, a, b, c):
        super().__init__(opcode=opcode, sequence=sequence, a=a, b=b, c=c)


class Peripheral(instruction.Instruction):
    """Peripheral instruction class."""

    def __init__(self, opcode, paddr):
        super().__init__(opcode=opcode, paddr=paddr)


class Simulator(instruction.Instruction):
    """Simulator instruction class."""

    def __init__(self, opcode, sequence):
        super().__init__(opcode=opcode, sequence=sequence)


class Scientific(instruction.Instruction):
    """Scientific instruction class."""

    def __init__(self, opcode, sequence, a, b, c):
        super().__init__(opcode=opcode, sequence=sequence, a=a, b=b, c=c)


class PseudoInstruction(instruction.Instruction):
    """Pseudo-instruction class. No code is generated."""

    def __init__(self, mnemonic, a, b, c):
        super().__init__(mnemonic=mnemonic, a=a, b=b, c=c, pseudo=True)


class AssemblyControl(PseudoInstruction):
    """Assembly control instruction class."""

    def __init__(self, mnemonic, a, b, c):
        super().__init__(mnemonic=mnemonic, a=a, b=b, c=c)


# ASSIGN: Assign Tag to Complex Address
class AssignTag(AssemblyControl):
    pass


# END: Specify Information for Executive
class End(AssemblyControl):
    pass


# EQUALS: Assign Value to Tag
class Equals(AssemblyControl):
    pass


# EVEN: Set Location Counter to Next Even Address
class Even(AssemblyControl):
    pass


# MASKGRP: Assign Shift and Field Group Numbers
class MaskGroup(AssemblyControl):
    pass


# MODLOC: Set Location Counter Modulo-N.
class SetLocationCounterModuloN(AssemblyControl):
    pass


# RESERVE: Reserve N Words of Memory
class Reserve(AssemblyControl):
    pass


# SETLOC: Set Location Counter
class SetLocationCounter(AssemblyControl):
    pass


# SIMULATE: Start of Simulator Routine
class Simulate(AssemblyControl):
    pass


# TAS: Temporarily Assign Tag to Complex Address
class TemporarilyAssignTag(AssemblyControl):
    pass


# ALF: Alphanumeric Constant
def build_constant(mnemonic: str, value: int):
    """Unified constant factory replacing individual constant facade classes."""
    return instruction.Constant(mnemonic=mnemonic, value=value)


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
    "build_constant",
    "print_instructions",
]

if __name__ == "__main__":
    print_instructions()
