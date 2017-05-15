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

class Word(object):
    """H-x800 word class."""
    def __init__(self, command, a, b, c):
        self._command = command                 # Command code.
        self._a = a                             # A address group.
        self._b = b                             # B address group.
        self._c = c                             # C address group.
        # TODO: form the resulting memory word.
        pass
