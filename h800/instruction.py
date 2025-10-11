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

# Constants for field validation
MASK_MAX = 31
PADDR_MAX = 63
BITS23_MAX = 3
OPCODE_MAX = 31
WORD_48_MAX = 2**48 - 1


class Instruction:
    """Base opcode class."""

    def __init__(
        self, opcode, sequence=None, mask=None, a=None, b=None, c=None, paddr=None, pseudo=False
    ):
        print(f"opcode:{opcode} sequence:{sequence} mask:{mask} a={a} b={b} c={c} paddr={paddr}")
        self._opcode = opcode  # Opcode object
        self._sequence = sequence  # Sequence/cosequence code
        self._mask = mask  # Mask
        self._a = a  # A register active
        self._b = b  # B register active
        self._c = c  # C register active
        self._paddr = paddr  # Peripheral address (6 bits)
        self._pseudo = pseudo  # Generate no binary code
        self._mnemonic = opcode.m  # Mnemonic string
        self._bits23 = opcode.b23  # Bits 2,3
        self._bit7 = opcode.b7  # Bit 7 (1 masked, 0 unmasked)
        self._op = opcode.op  # Opcode binary
        self._type = opcode.type  # Instruction type
        self.data = BitField(
            0, width=12, numbering=BitField.BIT_SCHEME_MSB_1, order=BitField.BIT_ORDER_MSB_LEFT
        )
        self._check()
        # print("1 0o%04o" % self.data)
        if self._sequence is not None:
            # print("*** setting sequence to %d" % self._sequence)
            self.data[1] = self._sequence
        # print("2 0o%04o" % self.data)
        if self._type in ("maskable", "peripheral", "print"):
            if (self._type == "maskable" and self._mask is not None) or self._type != "maskable":
                if self._bit7 is not None:
                    # print("*** setting bit7 to %d" % self._bit7)
                    self.data[7] = self._bit7
        # print("3 0o%04o" % self.data)
        if self._mask is not None:
            # print("*** setting mask to 0o%05o" % self._mask)
            self.data[2:6] = self._mask
        elif self._bits23 is not None:
            # print("*** setting bits 2,3 to %d" % self._bits23)
            self.data[2:3] = self._bits23
        # print("4 0o%04o" % self.data)
        if self._a is not None:
            # print("*** a: %d" % 1 if self._a else 0)
            self.data[4] = 1 if self._a else 0
        # print("5 0o%04o" % self.data)
        if b is not None:
            # print("*** b: %d" % 1 if self._b else 0)
            self.data[5] = 1 if self._b else 0
        # print("6 0o%04o" % self.data)
        if c is not None:
            # print("*** c: %d" % 1 if self._c else 0)
            self.data[6] = 1 if self._c else 0
        # print("7 0o%04o" % self.data)
        if paddr is not None:
            self.data[1:6] = self._paddr
            # print("*** paddr: %d" % self._paddr)
        # print("8 0o%04o" % self.data)
        self.data[8:12] = self._op

    def _check(self):
        """Validate instruction field combinations."""
        # Sequence vs peripheral address are mutually exclusive.
        if self._sequence is not None and self._paddr is not None:
            raise ValueError("Cannot specify sequence and peripheral address together.")
        if self._sequence is not None and self._sequence not in (0, 1, True, False):
            raise ValueError("Sequence must be boolean (0/1).")

        # Mask validation.
        if self._mask is not None:
            if self._type != "maskable":
                raise ValueError("Mask supplied to a non-maskable instruction.")
            if any(x is not None for x in (self._a, self._b, self._c, self._paddr)):
                raise ValueError("Cannot specify A, B, C, or peripheral address with mask.")
            if not (0 <= self._mask <= MASK_MAX):
                raise ValueError(f"Mask must be in the range 0..{MASK_MAX}.")

        # Operand flag validation.
        for flag_name, flag_value in (("A", self._a), ("B", self._b), ("C", self._c)):
            if flag_value is not None and flag_value not in (0, 1, True, False):
                raise ValueError(f"{flag_name} must be boolean (0/1).")

        # Peripheral address constraints.
        if self._paddr is not None:
            if any(x is not None for x in (self._sequence, self._mask, self._a, self._b, self._c)):
                raise ValueError(
                    "Cannot specify sequence, mask, A, B, or C with peripheral address."
                )
            if not (0 <= self._paddr <= PADDR_MAX):
                raise ValueError(f"Peripheral address must be in the range 0..{PADDR_MAX}.")

        # Bit 7 (masked/unmasked indicator) range.
        if self._bit7 is not None and not (0 <= self._bit7 <= 1):
            raise ValueError("Bit 7 must be in the range 0..1.")

        # Bits 2-3 range.
        if self._bits23 is not None and not (0 <= self._bits23 <= BITS23_MAX):
            raise ValueError(f"Bits 2-3 must be in the range 0..{BITS23_MAX}.")

        # Opcode range.
        if not (0 <= self._op <= OPCODE_MAX):
            raise ValueError(f"Opcode must be in the range 0..{OPCODE_MAX}.")

    @property
    def value(self):
        "Return the current integer value of the opcode bitfield."
        return int(self.data)


class GeneralMasked(Instruction):
    """General masked instruction class."""

    def __init__(self, opcode, sequence, mask):
        super().__init__(opcode=opcode, sequence=sequence, mask=mask)


class GeneralUnmasked(Instruction):
    """General unmasked instruction class."""

    def __init__(self, opcode, sequence, a, b, c):
        super().__init__(opcode=opcode, sequence=sequence, a=a, b=b, c=c)


class Peripheral(Instruction):
    """Peripheral instruction class."""

    def __init__(self, opcode, paddr):
        super().__init__(opcode=opcode, paddr=paddr)


class Simulator(Instruction):
    """Simulator instruction class."""

    def __init__(self, opcode, sequence):
        super().__init__(opcode=opcode, sequence=sequence)


class Scientific(Instruction):
    """Scientific instruction class."""

    def __init__(self, opcode, sequence, a, b, c):
        super().__init__(opcode=opcode, sequence=sequence, a=a, b=b, c=c)


class Constant(Word):
    """Constant instruction class."""

    def __init__(self, mnemonic, data):
        if data < 0 or data > WORD_48_MAX:
            raise ValueError(f"Opcode must be in the range 0..{WORD_48_MAX}!")
        super().__init__(data=data)


class PseudoInstruction(Instruction):
    """Pseudo-instruction class. No code is generated."""

    def __init__(self, mnemonic, a, b, c):
        super().__init__(mnemonic=mnemonic, a=a, b=b, c=c, pseudo=True)


class AssemblyControl(PseudoInstruction):
    """Assembly control instruction class."""

    def __init__(self, mnemonic, a, b, c):
        super().__init__(mnemonic=mnemonic, a=a, b=b, c=c)
