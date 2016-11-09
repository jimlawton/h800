# H-800/H-1800 Instruction Format
# ===============================
#
#   S       Sequence/cosequence bit, 0=sequence, 1=cosequence. [? TODO]
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

class Instruction(object):
    """Base opcode class."""
    def __init__(self, mnemonic, sequence, mask, group, a, b, c, paddr, opcode):
        self._mnemonic = mnemonic               # Mnemonic string.
        self._sequence = sequence               # Sequence/cosequence code.
        self._mask = mask                       # Mask.
        self._group = group                     # Group code.
        self._a = a                             # A register active.
        self._b = b                             # B register active.
        self._c = c                             # C register active.
        self._paddr = paddr                     # Peripheral address (6 bits).
        self._opcode = opcode                   # Opcode binary.
        # TODO: form the resulting machine code.
        pass


class GeneralMasked(Instruction):
    """General masked instruction class."""
    def __init__(self, mnemonic, sequence, mask, opcode):
        Instruction.__init__(self, mnemonic, sequence, mask, None, None, None, None, None, opcode)


class GeneralUnmasked(Instruction):
    """General unmasked instruction class."""
    def __init__(self, mnemonic, sequence, group, a, b, c, opcode):
        Instruction.__init__(self, mnemonic, sequence, None, group, a, b, c, None, opcode)


class Peripheral(Instruction):
    """Peripheral instruction class."""
    def __init__(self, mnemonic, paddr, opcode):
        Instruction.__init__(self, mnemonic, None, None, None, None, None, None, paddr, opcode)


class Simulator(Instruction):
    """Simulator instruction class."""
    def __init__(self, mnemonic, sequence, opcode):
        Instruction.__init__(self, mnemonic, sequence, None, None, None, None, None, None, 7)


class Scientific(Instruction):
    """Scientific instruction class."""
    def __init__(self, mnemonic, sequence, group, a, b, c, opcode):
        Instruction.__init__(self, mnemonic, sequence, None, group, a, b, c, None, opcode)
