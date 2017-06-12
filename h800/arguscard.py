#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# ARGUS Punch-Card Classes
# ========================
#
# ARGUS-format punch-card support for the H800.

from __future__ import print_function
import sys

import punchcard


_WIDTH = 120
_FIELDS = [1, 2, 8, 9, 20, 33, 47, 61, 76, 81]
_FIELDNAMES = ["column1", "lognum", "column8", "label", "operation", "operand1", "operand2", "operand3", "misc", "remarks"]


class Card(punchcard.PunchCard):
    """A simple class to represent an ARGUS punch card."""
    def __init__(self, line, width=_WIDTH, fields=_FIELDS, fieldnames=_FIELDNAMES, filename=None, linenum=0, verbose=False):
        super(Card, self).__init__(line, width=width, fields=fields, fieldnames=fieldnames, filename=filename, linenum=linenum, verbose=verbose)
        if self.column1 == 'P' or self.column1 == 'R' or self.column1 == 'L':
            self._record["label"] = None
            self._record["operation"] = None
            self._record["operand1"] = None
            self._record["operand2"] = None
            self._record["operand3"] = None
            self._record["misc"] = None
            self._record["remarks"] = self._line[9:].strip()
        if self.column1 == 'L':
            self._record["remarks"] = self._line[9:].strip()
        self._record["instruction"] = self._record["operation"]
        if self._record["operation"] and ',' in self._record["operation"]:
            self._record["instruction"] = self._record["operation"].split(',')[0]

    @property
    def column1(self):
        return self._record["column1"]

    @property
    def lognum(self):
        return self._record["lognum"]

    @property
    def column8(self):
        return self._record["column8"]

    @property
    def label(self):
        return self._record["label"]

    @property
    def location(self):
        return self._record["label"]

    @property
    def operation(self):
        return self._record["operation"]

    @property
    def operand1(self):
        return self._record["operand1"]

    @property
    def addressa(self):
        return self._record["operand1"]

    @property
    def operand2(self):
        return self._record["operand2"]

    @property
    def addressb(self):
        return self._record["operand2"]

    @property
    def operand3(self):
        return self._record["operand3"]

    @property
    def addressc(self):
        return self._record["operand3"]

    @property
    def sequence(self):
        return self._record["misc"]

    @property
    def remarks(self):
        return self._record["remarks"]

    @property
    def instruction(self):
        return self._record["instruction"]

    def parse(self):
        pass


class Deck(punchcard.Deck):
    """A simple class to represent a deck of ARGUS punch-cards."""
    def __init__(self, lines=None, file=None, width=_WIDTH, fields=_FIELDS, cardclass=Card, verbose=False):
        super(Deck, self).__init__(lines=lines, file=file, width=width, fields=fields, cardclass=cardclass, verbose=verbose)
        self._logSection = None
        self._logSectionCol8 = None
        for card in self._cards:
            if card.record["column1"] == 'L':
                # This will only recognise the first log section in a deck.
                self._logSection = card.line[8:81].strip()
                self._logSectionCol8 = card.record["column8"]
                break

    @property
    def log_section(self):
        return self._logSection

    @property
    def log_section_col8(self):
        return self._logSectionCol8
