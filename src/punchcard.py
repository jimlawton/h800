#!/usr/bin/env python

# Punch-Card Utility classes
# ==========================
#
# Punch cards are column-delimited lines of text.
#
# The default field layout, unless overridden is:
#
# 0        0         0         0         0         0         0         0         0         0         1         1         1
# 0        1         2         3         4         5         6         7         8         9         0         1         2
# 123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
# ABBBBBBCDDDDDDDDDDDEEEEEEEEEEEEEFFFFFFFFFFFFFFGGGGGGGGGGGGGGHHHHHHHHHHHHHHHIIIIIJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ
#
# where A, B, C, ..., J represent separate text fields in the card. This layout
# is represented by a list of starting columns:
#    A  B  C  D  E   F   G   H   I   J
#   [1, 2, 8, 9, 20, 33, 47, 61, 76, 81]
#
# These classes take input in the form of strings representing lines of text
# and split it into fields, as defined by the layout.


_DEFAULT_WIDTH = 120
_DEFAULT_FIELDS = [1, 2, 8, 9, 20, 33, 47, 61, 76, 81]

class PunchCard(object):
    """A simple class to represent a punch card."""
    def __init__(self, line, width=_DEFAULT_WIDTH, fields=_DEFAULT_FIELDS):
        self._line = line
        self._fields = fields
        pass


class Deck(object):
    """A simple class to represent a deck of punch-cards."""
    def __init__(self, lines, width=_DEFAULT_WIDTH, fields=_DEFAULT_FIELDS):
        self._lines = lines
        self._cards = []
        for line in lines:
            self._cards.append(PunchCard(lines, width=width, fields=fields))

