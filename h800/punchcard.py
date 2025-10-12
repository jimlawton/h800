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

import os
import os.path
import sys

_DEFAULT_WIDTH = 120
_DEFAULT_FIELDS = [1, 2, 8, 9, 20, 33, 47, 61, 76, 81]
_DEFAULT_FIELDNAMES = [
    "column1",
    "lognum",
    "column8",
    "label",
    "operation",
    "operand1",
    "operand2",
    "operand3",
    "misc",
    "remarks",
]


class PunchCard:
    """A simple class to represent a punch card."""

    def __init__(
        self,
        line,
        width=_DEFAULT_WIDTH,
        fields=_DEFAULT_FIELDS,
        fieldnames=_DEFAULT_FIELDNAMES,
        filename=None,
        linenum=0,
        verbose=False,
    ):
        self._line = line.replace("\n", "")
        self._layout = []
        self._filename = filename
        self._linenum = linenum
        self._verbose = verbose
        self._comment = line.startswith("#")
        if not self._comment:
            for i, col in enumerate(fields):
                fstart = col
                if i == len(fields) - 1:
                    fwidth = width - col + 1
                else:
                    fwidth = fields[i + 1] - col
                self._layout.append((fstart, fwidth))
            self._fields = []
            for s, w in self._layout:
                self._fields.append(line[s - 1 : s - 1 + w])
            self._stripped_fields = []
            self._record = {}
            if linenum != 0:
                self._record["linenum"] = linenum
            for i, field in enumerate(self._fields):
                if field.strip() == "":
                    self._stripped_fields.append(None)
                    self._record[fieldnames[i]] = None
                else:
                    self._stripped_fields.append(field.strip())
                    self._record[fieldnames[i]] = field.strip()
        else:
            # Comment card: initialize empty field containers so attribute access is safe.
            self._fields = []
            self._stripped_fields = []
            self._record = {}
            if linenum != 0:
                # Optionally include line number metadata even for comments.
                self._record["linenum"] = linenum

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
    def stripped_fields(self):
        return self._stripped_fields

    @property
    def record(self):
        return self._record

    @property
    def filename(self):
        return self._filename

    @property
    def linenum(self):
        return self._linenum

    @property
    def is_comment(self):
        return self._comment

    @property
    def comment(self):
        if self.is_comment:
            return self._line
        else:
            return None

    def __str__(self):
        return str(self._line)


class Deck:
    """A simple class to represent a deck of punch-cards."""

    def __init__(
        self,
        lines=None,
        file=None,
        width=_DEFAULT_WIDTH,
        fields=_DEFAULT_FIELDS,
        cardclass=PunchCard,
        verbose=False,
    ):
        self._width = width
        self._fields = fields
        self._cardclass = cardclass
        self._verbose = verbose
        if lines is None and file is None:
            sys.exit("ERROR: no input supplied to class constructor!")
        self._cards = []
        if file:
            self._cards = self._read_source(file)
            self._lines = [card.line for card in self._cards]
        else:
            self._lines = lines
            for i, line in enumerate(self._lines):
                if line.startswith("#"):
                    if self._verbose:
                        print(f"Skipping meta-comment, file {file}, line {i + 1}")
                    continue
                self._cards.append(
                    cardclass(
                        line,
                        width=width,
                        fields=fields,
                        filename=file,
                        linenum=i + 1,
                        verbose=verbose,
                    )
                )
        self._fields = []
        self._stripped_fields = []
        self._records = []
        for card in self._cards:
            self._fields.append(card.fields)
            self._stripped_fields.append(card.stripped_fields)
            self._records.append(card.record)

    @property
    def lines(self):
        return self._lines

    @property
    def cards(self):
        return self._cards

    @property
    def fields(self):
        return self._fields

    @property
    def stripped_fields(self):
        return self._stripped_fields

    @property
    def records(self):
        return self._records

    def __str__(self):
        lines = []
        for card in self._cards:
            lines.append(str(card))
        return "\n".join(lines)

    def _read_source(self, filename, recurse=True):
        """Read an ARGUS source file. If the file includes $ directives,
        include those files recursively into the deck."""
        cards = []
        if not os.path.isfile(filename):
            sys.exit(f'ERROR: File "{filename}" does not exist!')
        lines = []
        with open(filename) as f:
            if self._verbose:
                print(f"Reading {filename}...")
            lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith("#"):
                if self._verbose:
                    print(f"Skipping meta-comment, file {filename}, line {i + 1}")
                continue
            if line.startswith("$"):
                incname = line[1:].split()[0]
                if not os.path.isfile(incname):
                    sys.exit(f'File "{incname}" does not exist')
                if recurse:
                    icards = self._readSource(incname)
                    cards.extend(icards)
                else:
                    cards.append(
                        self._cardclass(
                            line,
                            width=self._width,
                            fields=self._fields,
                            filename=filename,
                            linenum=i + 1,
                            verbose=self._verbose,
                        )
                    )
            else:
                cards.append(
                    self._cardclass(
                        line,
                        width=self._width,
                        fields=self._fields,
                        filename=filename,
                        linenum=i + 1,
                        verbose=self._verbose,
                    )
                )
        return cards
