#!/usr/bin/env python

# H-800/H-1800 Instruction Format
# ===============================
#
# From the PRM, Section III:
#   Machine instructions fall into five major categories: general instructions,
#   unmasked and masked; inherent mask instructions; peripheral and print
#   instructions; simulator instructions; and scientific instructions.
#
#   The masked general instructions and the peripheral and print instructions
#   are uniquely designated by six-bits - bits 7 through 12 of the instruction
#   word.
#
#   The unmasked general instructions, the inherent mask instructions, and the
#   scientific instructions are uniquely designated by eight bits - bits 7
#   through 12, plus bits 2 and 3.
#
#   The simulator instructions are uniquely defined by only three bits - bits
#   10 through 12.
#
#   These groups of bits which uniquely specify the operation to be performed
#   are called the operation code.  The bits of the command code which are not
#   used for the operation code serve various other purposes
#
# Key:
#   S       Sequence/cosequence bit, 0=sequence, 1=cosequence.
#   MASK    5-bit mask.
#   OPCODE  5-bit opcode.
#   A       A address active if 1.
#   B       B address active if 1.
#   C       C address active if 1.
#   PADDR   6-bit peripheral address.
#
#
# Masked instructions:
#
#  MSB                                                     LSB
# +----+----+----+----+----+----+----+----+----+----+----+----+
# |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 |
# +----+----+----+----+----+----+----+----+----+----+----+----+
# |  S |          MASK          |  1 |         OPCODE         |
# +----+----+----+----+----+----+----+----+----+----+----+----+
#
#
# Unmasked instructions:
#
#  MSB                                                     LSB
# +----+----+----+----+----+----+----+----+----+----+----+----+
# |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 |
# +----+----+----+----+----+----+----+----+----+----+----+----+
# |  S |  x |  x |  A |  B |  C |  0 |         OPCODE         |
# +----+----+----+----+----+----+----+----+----+----+----+----+
#
#
# Peripheral instructions:
#
#  MSB                                                     LSB
# +----+----+----+----+----+----+----+----+----+----+----+----+
# |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 |
# +----+----+----+----+----+----+----+----+----+----+----+----+
# |            PADDRESS         |  1 |         OPCODE         |
# +----+----+----+----+----+----+----+----+----+----+----+----+

from bitfield import BitField


class Instruction(object):
    """Base opcode class."""
    def __init__(self, mnemonic, sequence=None, mask=None, a=0, b=0, c=0, paddr=None, opcode=0, pseudo=False):
        self._mnemonic = mnemonic       # Mnemonic string.
        self._sequence = sequence       # Sequence/cosequence code.
        self._mask = mask               # Mask.
        self._a = a                     # A register active.
        self._b = b                     # B register active.
        self._c = c                     # C register active.
        self._paddr = paddr             # Peripheral address (6 bits).
        self._opcode = opcode           # Opcode binary.
        self._pseudo = pseudo           # Pseudo-instructions generate no code.
        self.data = BitField(0, width=12,
                             numbering=BitField.BIT_SCHEME_MSB_1,
                             order=BitField.BIT_ORDER_MSB_LEFT)
        if sequence:
            if paddr:
                raise ValueError("Conflicting arguments!")
            if sequence not in (0, 1, True, False):
                raise ValueError("Sequence must be boolean!")
            self.data[1] = sequence
        if mask:
            if a or b or c or paddr:
                raise ValueError("Conflicting arguments!")
            if mask < 0 or mask > 31:
                raise ValueError("Mask must be in the range 0..31!")
            self.data[2:6] = mask
        else:
            self.data[2:3] = (opcode >> 9) & 3
        if a:
            if a not in (0, 1, True, False):
                raise ValueError("A must be boolean!")
            self._a = 1 if a is True else 0
            self.data[4] = self._a
        if b:
            if b not in (0, 1, True, False):
                raise ValueError("B must be boolean!")
            self._b = 1 if b is True else 0
            self.data[5] = self._b
        if c:
            if c not in (0, 1, True, False):
                raise ValueError("C must be boolean!")
            self._c = 1 if c is True else 0
            self.data[6] = self._c
        if paddr:
            if sequence or mask or a or b or c:
                raise ValueError("Conflicting arguments!")
            if paddr < 0 or paddr > 63:
                raise ValueError("Peripheral address must be in the range 0..63!")
            self.data[1:6] = self._paddr
        if opcode < 0 or opcode > 255:
            raise ValueError("Opcode must be in the range 0..31!")
        self.data[7:12] = opcode & 63

    @property
    def value(self):
        "Return the current integer value of the opcode bitfield."
        return int(self.data)


class GeneralMasked(Instruction):
    """General masked instruction class."""
    def __init__(self, mnemonic, sequence, mask, opcode):
        Instruction.__init__(self, mnemonic=mnemonic, sequence=sequence, mask=mask, opcode=opcode)

class GeneralUnmasked(Instruction):
    """General unmasked instruction class."""
    def __init__(self, mnemonic, sequence, a, b, c, opcode):
        Instruction.__init__(self, mnemonic=mnemonic, sequence=sequence, a=a, b=b, c=c, opcode=opcode)


class Peripheral(Instruction):
    """Peripheral instruction class."""
    def __init__(self, mnemonic, paddr, opcode):
        Instruction.__init__(self, mnemonic=mnemonic, paddr=paddr, opcode=opcode)


class Simulator(Instruction):
    """Simulator instruction class."""
    def __init__(self, mnemonic, sequence, opcode):
        Instruction.__init__(self, mnemonic=mnemonic, sequence=sequence, opcode=7)


class Scientific(Instruction):
    """Scientific instruction class."""
    def __init__(self, mnemonic, sequence, a, b, c, opcode):
        Instruction.__init__(self, mnemonic=mnemonic, sequence=sequence, a=a, b=b, c=c, opcode=opcode)


class Constant(Instruction):
    """Constant instruction class."""
    def __init__(self, mnemonic, a, b, c):
        Instruction.__init__(self, mnemonic=mnemonic, a=a, b=b, c=c)


class PseudoInstruction(Instruction):
    """Pseudo-instruction class. No code is generated."""
    def __init__(self, mnemonic, a, b, c):
        Instruction.__init__(self, mnemonic=mnemonic, a=a, b=b, c=c, pseudo=True)


class AssemblyControl(PseudoInstruction):
    """Assembly control instruction class."""
    def __init__(self, mnemonic, a, b, c):
        PseudoInstruction.__init__(self, mnemonic=mnemonic, a=a, b=b, c=c)


def main():
    # Tester goes here.
    print "TEST: TBD."
    # TODO
    print "PASS"


if __name__ == '__main__':
    main()
