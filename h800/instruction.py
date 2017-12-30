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

from .bitfield import BitField
from .word import Word


class Instruction:
    """Base opcode class."""
    def __init__(self, opcode, sequence=None, mask=None, a=None, b=None,
                 c=None, paddr=None, pseudo=False):
        print(("opcode:%s sequence:%s mask:%s a=%s b=%s c=%s paddr=%s" %
              (opcode, sequence, mask, a, b, c, paddr)))
        self._opcode = opcode               # Opcode object
        self._sequence = sequence           # Sequence/cosequence code
        self._mask = mask                   # Mask
        self._a = a                         # A register active
        self._b = b                         # B register active
        self._c = c                         # C register active
        self._paddr = paddr                 # Peripheral address (6 bits)
        self._pseudo = pseudo               # Generate no binary code
        self._mnemonic = opcode.m           # Mnemonic string
        self._bits23 = opcode.b23           # Bits 2,3
        self._bit7 = opcode.b7              # Bit 7 (1 masked, 0 unmasked)
        self._op = opcode.op                # Opcode binary
        self._type = opcode.type            # Instruction type
        self.data = BitField(0, width=12,
                             numbering=BitField.BIT_SCHEME_MSB_1,
                             order=BitField.BIT_ORDER_MSB_LEFT)
        self._check()
        print("1 0o%04o" % self.data)
        if self._sequence is not None:
            print("*** setting sequence to %d" % self._sequence)
            self.data[1] = self._sequence
        print("2 0o%04o" % self.data)
        if self._type in ("maskable", "peripheral", "print"):
            if (self._type == "maskable" and self._mask is not None) or \
                    self._type != "maskable":
                if self._bit7 is not None:
                    print("*** setting bit7 to %d" % self._bit7)
                    self.data[7] = self._bit7
        print("3 0o%04o" % self.data)
        if self._mask is not None:
            print("*** setting mask to 0o%05o" % self._mask)
            self.data[2:6] = self._mask
        else:
            if self._bits23 is not None:
                print("*** setting bits 2,3 to %d" % self._bits23)
                self.data[2:3] = self._bits23
        print("4 0o%04o" % self.data)
        if self._a is not None:
            print("*** a: %d" % 1 if self._a else 0)
            self.data[4] = 1 if self._a else 0
        print("5 0o%04o" % self.data)
        if b is not None:
            print("*** b: %d" % 1 if self._b else 0)
            self.data[5] = 1 if self._b else 0
        print("6 0o%04o" % self.data)
        if c is not None:
            print("*** c: %d" % 1 if self._c else 0)
            self.data[6] = 1 if self._c else 0
        print("7 0o%04o" % self.data)
        if paddr is not None:
            self.data[1:6] = self._paddr
            print("*** paddr: %d" % self._paddr)
        print("8 0o%04o" % self.data)
        self.data[8:12] = self._op
        print("9 0o%04o" % self.data)

    def _check(self):
        "Check the instruction for correctness."
        if self._sequence is not None:
            if self._paddr:
                raise ValueError("Cannot specify sequence and peripheral "
                                 "address!")
            if self._sequence not in (0, 1, True, False):
                raise ValueError("Sequence must be boolean!")
        if self._mask is not None:
            if self._type != "maskable":
                raise ValueError("Mask supplied to an instruction that is not "
                                 "maskable!")
            if self._a is not None or self._b is not None or \
                    self._c is not None or self._paddr is not None:
                raise ValueError("Cannot specify A, B, C, or peripheral "
                                 "address with mask!")
            if self._mask < 0 or self._mask > 31:
                raise ValueError("Mask must be in the range 0..31!")
        if self._a is not None:
            if self._a not in (0, 1, True, False):
                raise ValueError("A must be boolean!")
        if self._b is not None:
            if self._b not in (0, 1, True, False):
                raise ValueError("B must be boolean!")
        if self._c is not None:
            if self._c not in (0, 1, True, False):
                raise ValueError("C must be boolean!")
        if self._paddr is not None:
            if self._sequence is not None or self._mask is not None or \
                    self._a is not None or self._b is not None or \
                    self._c is not None:
                raise ValueError("Cannot specify sequence, mask, A, B, or C "
                                 "with peripheral address!")
            if self._paddr < 0 or self._paddr > 63:
                raise ValueError("Peripheral address must be in the range "
                                 "0..63!")
        if self._bit7 is not None:
            if self._bit7 < 0 or self._bit7 > 1:
                raise ValueError("Bit 7 must be in the range 0..1!")
        if self._bits23 is not None:
            if self._bits23 < 0 or self._bits23 > 3:
                raise ValueError("Bits 2-3 must be in the range 0..3!")
        if self._op < 0 or self._op > 31:
            raise ValueError("Opcode must be in the range 0..31!")

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
        Instruction.__init__(self, opcode=opcode, sequence=sequence,
                             a=a, b=b, c=c)


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
        Instruction.__init__(self, opcode=opcode, sequence=sequence,
                             a=a, b=b, c=c)


class Constant(Word):
    """Constant instruction class."""
    def __init__(self, mnemonic, data):
        if data < 0 or data > 2 ** 48 - 1:
            raise ValueError("Opcode must be in the range 0..%d!" %
                             (2 ** 48 - 1))
        Word.__init__(self, data=data)


class PseudoInstruction(Instruction):
    """Pseudo-instruction class. No code is generated."""
    def __init__(self, mnemonic, a, b, c):
        Instruction.__init__(self, mnemonic=mnemonic,
                             a=a, b=b, c=c, pseudo=True)


class AssemblyControl(PseudoInstruction):
    """Assembly control instruction class."""
    def __init__(self, mnemonic, a, b, c):
        PseudoInstruction.__init__(self, mnemonic=mnemonic, a=a, b=b, c=c)
