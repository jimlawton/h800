#!/usr/bin/env python

# H-800/H-1800 Word Format
# ===============================
#
# From the PRM, Section III:
#   The 48 bits of a Honeywell 1800 instruction word are interpreted as four
#   groups of 12 bits each.  Bits 1-12 represent the command code; bits 13-24,
#   25-36, and 37-48 are designated as the A address group, B address group,
#   and C address group, respectively.  The address portions of instructions
#   normally are used to designate the locations of operands and results, but
#   in certain instructions they may contain special information such as the
#   number of words to be moved, the number of bits to be shifted, a change of
#   sequence counter, and so forth.
#
#  MSB                                                             LSB
# +----------------+----------------+----------------+----------------+
# | 1           12 | 13          24 | 25          36 | 37          48 |
# +----------------+----------------+----------------+----------------+
# | COMMAND        |   A ADDRESS    |   B ADDRESS    |   C ADDRESS    |
# +----------------+----------------+----------------+----------------+

from bitfield import BitField


class Word(object):
    """H-x800 word class."""
    def __init__(self, command=0, a=0, b=0, c=0):
        self.data = BitField(0, width=48,
                             numbering=BitField.BIT_SCHEME_MSB_1,
                             order=BitField.BIT_ORDER_MSB_LEFT)
        self.data[1:12] = self._command = command   # Command code.
        self.data[13:24] = self._a = a              # A address group.
        self.data[25:36] = self._b = b              # B address group.
        self.data[37:48] = self._c = c              # C address group.

    @property
    def value(self):
        return int(self.data)

    @value.setter
    def value(self, value):
        self.data.value = value

    @property
    def command(self):
        return self.data[1:12]

    @command.setter
    def command(self, value):
        self._command = self.data[1:12] = value

    @property
    def a(self):
        return self.data[13:24]

    @a.setter
    def a(self, value):
        self._a = self.data[13:24] = value

    @property
    def b(self):
        return self.data[25:36]

    @b.setter
    def b(self, value):
        self._b = self.data[25:36] = value

    @property
    def c(self):
        return self.data[37:48]

    @c.setter
    def c(self, value):
        self._c = self.data[37:48] = value

    def emit(self):
        "Emit binary output."
        # TODO
        pass
