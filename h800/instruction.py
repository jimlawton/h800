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
from word import Word


class Instruction(object):
    """Base opcode class."""
    def __init__(self, opcode, sequence=None, mask=None, a=None, b=None, c=None, paddr=None, pseudo=False):
        print "opcode:%s sequence:%s mask:%s a=%s b=%s c=%s paddr=%s" % (opcode, sequence, mask, a, b, c, paddr)
        self._opcode = opcode               # Opcode object.
        self._sequence = sequence           # Sequence/cosequence code.
        self._mask = mask                   # Mask.
        self._a = a                         # A register active.
        self._b = b                         # B register active.
        self._c = c                         # C register active.
        self._paddr = paddr                 # Peripheral address (6 bits).
        self._pseudo = pseudo               # Pseudo-instructions generate no code.
        self._mnemonic = opcode.m           # Mnemonic string.
        self._bits23 = opcode.b23           # Bits 2,3.
        self._bit7 = opcode.b7              # Bit 7 (1 for masked, 0 for unmasked).
        self._op = opcode.op                # Opcode binary.
        self._maskable = opcode.maskable    # Is the instruction maskable?
        self.data = BitField(0, width=12,
                             numbering=BitField.BIT_SCHEME_MSB_1,
                             order=BitField.BIT_ORDER_MSB_LEFT)
        if sequence is not None:
            if paddr:
                raise ValueError("Conflicting arguments!")
            if sequence not in (0, 1, True, False):
                raise ValueError("Sequence must be boolean!")
            self.data[1] = sequence
        if mask is not None:
            if not self._maskable:
                raise ValueError("Mask supplied to an instruction that is not maskable!")
            if a is not None or b is not None or c is not None or paddr is not None:
                raise ValueError("Conflicting arguments!")
            if mask < 0 or mask > 31:
                raise ValueError("Mask must be in the range 0..31!")
            self.data[2:6] = mask
            if self._bit7 is not None:
                self.data[7] = (self._bit7 & 1)
        else:
            if self._bits23 is not None:
                self.data[2:3] = (self._bits23 & 3)
            if not self._maskable:
                if self._bit7 is not None:
                    self.data[7] = (self._bit7 & 1)
        if a is not None:
            if a not in (0, 1, True, False):
                raise ValueError("A must be boolean!")
            self._a = 1 if a else 0
            self.data[4] = self._a
        if b is not None:
            if b not in (0, 1, True, False):
                raise ValueError("B must be boolean!")
            self._b = 1 if b else 0
            self.data[5] = self._b
        if c is not None:
            if c not in (0, 1, True, False):
                raise ValueError("C must be boolean!")
            self._c = 1 if c else 0
            self.data[6] = self._c
        if paddr is not None:
            if sequence is not None or mask is not None or a is not None or b is not None or c is not None:
                raise ValueError("Conflicting arguments!")
            if paddr < 0 or paddr > 63:
                raise ValueError("Peripheral address must be in the range 0..63!")
            self.data[1:6] = self._paddr
            if self._bit7 is not None:
                self.data[7] = (self._bit7 & 1)
        if self._op < 0 or self._op > 31:
            raise ValueError("Opcode must be in the range 0..31!")
        self.data[8:12] = self._op & 31

    @property
    def value(self):
        "Return the current integer value of the opcode bitfield."
        return int(self.data)


class GeneralMasked(Instruction):
    """General masked instruction class."""
    def __init__(self, opcode, sequence, mask):
        Instruction.__init__(self, opcode=opcode, sequence=sequence, mask=mask)

class GeneralUnmasked(Instruction):
    """General unmasked instruction class."""
    def __init__(self, opcode, sequence, a, b, c):
        Instruction.__init__(self, opcode=opcode, sequence=sequence, a=a, b=b, c=c)


class Peripheral(Instruction):
    """Peripheral instruction class."""
    def __init__(self, opcode, paddr):
        Instruction.__init__(self, opcode=opcode, paddr=paddr)


class Simulator(Instruction):
    """Simulator instruction class."""
    def __init__(self, opcode, sequence):
        Instruction.__init__(self, opcode=opcode, sequence=sequence)


class Scientific(Instruction):
    """Scientific instruction class."""
    def __init__(self, opcode, sequence, a, b, c):
        Instruction.__init__(self, opcode=opcode, sequence=sequence, a=a, b=b, c=c)


class Constant(Word):
    """Constant instruction class."""
    def __init__(self, mnemonic, data):
        if data < 0 or data > 2 ** 48 - 1:
            raise ValueError("Opcode must be in the range 0..%d!" % (2 ** 48 - 1))
        Word.__init__(self, data=data)


class PseudoInstruction(Instruction):
    """Pseudo-instruction class. No code is generated."""
    def __init__(self, mnemonic, a, b, c):
        Instruction.__init__(self, mnemonic=mnemonic, a=a, b=b, c=c, pseudo=True)


class AssemblyControl(PseudoInstruction):
    """Assembly control instruction class."""
    def __init__(self, mnemonic, a, b, c):
        PseudoInstruction.__init__(self, mnemonic=mnemonic, a=a, b=b, c=c)
