#!/usr/bin/env python

# H-800/H-1800 Memory
# ===================

from bitfield import BitField
from word import Word


class MemoryBank(object):
    """H-x800 memory bank class."""

    MEMORY_WIDTH = 48       # 48 data, 6 parity.
    BANK_SIZE = 2048

    def __init__(self):
        self._data = {}
        for addr in range(self.BANK_SIZE):
            self._data[addr] = Word(0)
        self._width = self.MEMORY_WIDTH
        self._current = 0

    def _checkValue(self, value):
        if value < 0 or value > (2 ** self._width - 1):
            raise ValueError("Invalid value for %d-bit word!" % self._width)

    def _checkAddress(self, address):
        if address < 0 or address > 2047:
            raise ValueError("Invalid value for address!")

    @property
    def value(self, address, parity=False):
        # TODO: support parity.
        self._checkAddress(address)
        return int(self._data[address])

    @value.setter
    def value(self, address, value, parity=False):
        # TODO: support parity.
        self._checkAddress(address)
        self._checkValue(value)
        if value < 0 or value > (2 ** self._width - 1):
            raise ValueError("Invalid value for %d-bit word!" % self._width)
        self._data[address][1:self._width] = value

    @property
    def width(self):
        return int(self._width)

    def __getitem__(self, key):
        if isinstance(key, slice):
            values = []
            for i in range(key.start, key.stop):
                values.append(self._data[i].value)
        else:
            return self._data[key].value

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            for i in range(key.start, key.stop):
                self._data[i].value = value
        else:
            self._data[key].value = value

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return self

    def next(self):
        if self._current >= len(self._data):
            raise StopIteration
        else:
            self._current += 1
            return self._data[self._current - 1]

    def __repr__(self):
        text = ""
        for addr in self._data:
            text += "0o%016o " % self._data[addr].value
        return text

    def clear(self):
        for addr in self._data:
            self._data[addr].value = 0

