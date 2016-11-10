#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

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
# The default field start columns and widths are then:
# [(1, 1), (2, 6), (8, 1), (9, 11), (20, 13), (33, 14), (47, 14), (61, 15), (76, 5), (81, 40)]
#
# These classes take input in the form of strings representing lines of text
# and split it into fields, as defined by the layout.


_DEFAULT_WIDTH = 120
_DEFAULT_FIELDS = [1, 2, 8, 9, 20, 33, 47, 61, 76, 81]


class PunchCard(object):
    """A simple class to represent a punch card."""
    def __init__(self, line, width=_DEFAULT_WIDTH, fields=_DEFAULT_FIELDS):
        self._line = line
        self._layout = []
        for i, col in enumerate(fields):
            fstart = col
            if i == len(fields) - 1:
                fwidth = width - col + 1
            else:
                fwidth = fields[i+1] - col
            self._layout.append((fstart, fwidth))
        self._fields = []
        for s, w in self._layout:
            self._fields.append(line[s-1:s-1+w])
        self._strippedFields = []
        for field in self._fields:
            if field.rstrip() == "":
                self._strippedFields.append(None)
            else:
                self._strippedFields.append(field.rstrip())

    @property
    def line(self):
        return self._line

    @property
    def layout(self):
        return self._layout

    @property
    def fields(self):
        return self._fields

    @property
    def strippedFields(self):
        return self._strippedFields


class Deck(object):
    """A simple class to represent a deck of punch-cards."""
    def __init__(self, lines, width=_DEFAULT_WIDTH, fields=_DEFAULT_FIELDS):
        self._lines = lines
        self._cards = []
        for line in lines:
            self._cards.append(PunchCard(lines, width=width, fields=fields))

