#!/usr/bin/env python

# Generic bit-field class.
#
# This implements a class for representing generalized bit-fields:
#  - bit-fields can be of arbitrary width
#  - support either left-to-right or right-to-left bit ordering
#  - support both 0- and 1-based bit numbering schemes
#
# NOTE: BitField indices are inclusive, unlike Python slices.
# E.g.:
#   [7:3] of an 8-bit MSB-left field means bits 7,6,5,4,3.
#   [4:6] of an 8-bit MSB-right field means bits 4,5,6.
# Think logic circuit bit notation.
#
# The combinations of the supported ordering and numbering schemes are shown
# below, along with the actual Python element index for each bit.:
#
# The bit-field width is N.
#
# BIT_ORDER_MSB_LEFT, BIT_SCHEME_LSB_0:
#
#  MSB                                                     LSB
# +----+----+----+----+----+----+----+----+----+----+----+----+
# | N-1| N-2| N-3|                                  |  1 |  0 |
# +----+----+----+----+----+----+----+----+----+----+----+----+
#    0    1    2                                           N-1
#
# BIT_ORDER_MSB_LEFT, BIT_SCHEME_LSB_1:
#
#  MSB                                                     LSB
# +----+----+----+----+----+----+----+----+----+----+----+----+
# | N  | N-1| N-2|                                  |  2 |  1 |
# +----+----+----+----+----+----+----+----+----+----+----+----+
#    0    1    2                                           N-1
#
# BIT_ORDER_MSB_LEFT, BIT_SCHEME_MSB_0:
#
#  MSB                                                     LSB
# +----+----+----+----+----+----+----+----+----+----+----+----+
# |  0 |  1 |  2 |                                  | N-2| N-1|
# +----+----+----+----+----+----+----+----+----+----+----+----+
#    0    1    2                                           N-1
#
# BIT_ORDER_MSB_LEFT, BIT_SCHEME_MSB_1:
#
#  MSB                                                     LSB
# +----+----+----+----+----+----+----+----+----+----+----+----+
# |  1 |  2 |  3 |                                  | N-1| N  |
# +----+----+----+----+----+----+----+----+----+----+----+----+
#    0    1    2                                           N-1
#
# BIT_ORDER_LSB_LEFT, BIT_SCHEME_LSB_0:
#
#  LSB                                                     MSB
# +----+----+----+----+----+----+----+----+----+----+----+----+
# |  0 |  1 |  2 |                                  | N-2| N-1|
# +----+----+----+----+----+----+----+----+----+----+----+----+
#    0    1    2                                           N-1
#
# BIT_ORDER_LSB_LEFT, BIT_SCHEME_LSB_1:
#
#  LSB                                                     MSB
# +----+----+----+----+----+----+----+----+----+----+----+----+
# |  1 |  2 |  3 |                                  | N-1| N  |
# +----+----+----+----+----+----+----+----+----+----+----+----+
#    0    1    2                                           N-1
#
# BIT_ORDER_LSB_LEFT, BIT_SCHEME_MSB_0:
#
#  LSB                                                     MSB
# +----+----+----+----+----+----+----+----+----+----+----+----+
# | N-1| N-2| N-3|                                  |  1 |  0 |
# +----+----+----+----+----+----+----+----+----+----+----+----+
#    0    1    2                                           N-1
#
# BIT_ORDER_LSB_LEFT, BIT_SCHEME_MSB_1:
#
#  LSB                                                     MSB
# +----+----+----+----+----+----+----+----+----+----+----+----+
# | N  | N-1| N-2|                                  |  2 |  1 |
# +----+----+----+----+----+----+----+----+----+----+----+----+
#    0    1    2                                           N-1


class BitField(object):

    DEFAULT_WIDTH = 8
    # TODO: what is max value allowed for size?
    MAX_WIDTH = 64

    # The bit numbering scheme (0/1..N or N..1/0).
    #  - LSB 0
    #  - LSB 1
    #  - MSB 0
    #  - MSB 1
    BIT_SCHEME_LSB_0 = 0        # Bit 0 is LSB.
    BIT_SCHEME_LSB_1 = 1        # Bit 1 is LSB.
    BIT_SCHEME_MSB_0 = 2        # Bit 0 is MSB.
    BIT_SCHEME_MSB_1 = 3        # Bit 1 is MSB.

    # Bit ordering.
    BIT_ORDER_MSB_LEFT = BIT_ORDER_LSB_RIGHT = 0    # MSB ... LSB
    BIT_ORDER_LSB_LEFT = BIT_ORDER_MSB_RIGHT = 1    # LSB ... MSB

    def __init__(self, value=0,
                 width=DEFAULT_WIDTH,
                 numbering=BIT_SCHEME_LSB_0, order=BIT_ORDER_MSB_RIGHT):
        """Class constructor."""
        self._width = width
        if width > self.MAX_WIDTH:
            raise ValueError("Width is greater than maximum allowed!")
        self._maxval = 2L ** width - 1
        self._value = value
        if self._value > self._maxval:
            raise ValueError("Value is greater than maximum allowed by bit-field width!")
        self._numbering = numbering
        if numbering not in (self.BIT_SCHEME_LSB_0, self.BIT_SCHEME_LSB_1,
                             self.BIT_SCHEME_MSB_0, self.BIT_SCHEME_MSB_1):
            raise ValueError("Invalid bit numbering scheme!")
        self._order = order
        if order not in (self.BIT_ORDER_MSB_LEFT, self.BIT_ORDER_MSB_RIGHT):
            raise ValueError("Invalid bit order, must be left or right!")

    @property
    def width(self):
        "Return the width of the bit-field (in bits)."
        return self._width

    @property
    def maxval(self):
        "Return the maximum integer value supported by this bit-field."
        return self._maxval

    @property
    def numbering(self):
        "Return the bit numbering scheme (LSB 0, LSB 1, MSB 0, MSB 1)."
        return self._numbering

    @property
    def order(self):
        "Return the bit order (left-to-right or right-to-left)."
        return self._order

    @property
    def value(self):
        "Return the current integer value of the bit-field."
        return int(self._value)

    @value.setter
    def value(self, value):
        "Set the bit-field to the specified integer value."
        self._checkValue(value)
        self._value = int(value)

    @property
    def indices(self):
        "Return a list of the bit indices of the bit-field."
        indices = []
        for i in range(0, self._width):
            indices.append(self._index(i))
        return indices

    @property
    def lsb(self):
        "Return the index of the LSB in the bit-field."
        if self._order == self.BIT_ORDER_LSB_LEFT:
            return self.indices[0]
        else:
            return self.indices[-1]

    @property
    def msb(self):
        "Return the index of the MSB in the bit-field."
        if self._order == self.BIT_ORDER_MSB_LEFT:
            return self.indices[0]
        else:
            return self.indices[-1]

    # Calculating real indexes from supplied virtual index.
    # ("V" is the supplied virtual index, "W" is the width)
    #
    # Order                 Scheme              Real Index
    # BIT_ORDER_MSB_LEFT    BIT_SCHEME_LSB_0    R = W - (V + 1)
    # BIT_ORDER_MSB_LEFT    BIT_SCHEME_LSB_1    R = W - V
    # BIT_ORDER_MSB_LEFT    BIT_SCHEME_MSB_0    R = V
    # BIT_ORDER_MSB_LEFT    BIT_SCHEME_MSB_1    R = V - 1
    # BIT_ORDER_LSB_LEFT    BIT_SCHEME_LSB_0    R = V
    # BIT_ORDER_LSB_LEFT    BIT_SCHEME_LSB_1    R = V - 1
    # BIT_ORDER_LSB_LEFT    BIT_SCHEME_MSB_0    R = W - (V + 1)
    # BIT_ORDER_LSB_LEFT    BIT_SCHEME_MSB_1    R = W - V
    def _rindex(self, index, width=None):
        if width is None:
            width = self._width
        if self._order == self.BIT_ORDER_MSB_LEFT:
            if self._numbering == self.BIT_SCHEME_LSB_0:
                return width - (index + 1)
            elif self._numbering == self.BIT_SCHEME_LSB_1:
                return width - index
            elif self._numbering == self.BIT_SCHEME_MSB_0:
                return index
            elif self._numbering == self.BIT_SCHEME_MSB_1:
                return index - 1
        else:
            if self._numbering == self.BIT_SCHEME_LSB_0:
                return index
            elif self._numbering == self.BIT_SCHEME_LSB_1:
                return index - 1
            elif self._numbering == self.BIT_SCHEME_MSB_0:
                return width - (index + 1)
            elif self._numbering == self.BIT_SCHEME_MSB_1:
                return width - index

    # Calculate virtual index from supplied real index.
    # This is the inverse of the _rindex method above.
    # ("R" is the supplied real index, "W" is the width)
    #
    # Order                 Scheme              Virtual Index
    # BIT_ORDER_MSB_LEFT    BIT_SCHEME_LSB_0    V = W - (R + 1)
    # BIT_ORDER_MSB_LEFT    BIT_SCHEME_LSB_1    V = W - R
    # BIT_ORDER_MSB_LEFT    BIT_SCHEME_MSB_0    V = R
    # BIT_ORDER_MSB_LEFT    BIT_SCHEME_MSB_1    V = R + 1
    # BIT_ORDER_LSB_LEFT    BIT_SCHEME_LSB_0    V = R
    # BIT_ORDER_LSB_LEFT    BIT_SCHEME_LSB_1    V = R + 1
    # BIT_ORDER_LSB_LEFT    BIT_SCHEME_MSB_0    V = W - (R + 1)
    # BIT_ORDER_LSB_LEFT    BIT_SCHEME_MSB_1    V = W - R
    def _vindex(self, index, width=None):
        if width is None:
            width = self._width
        if self._order == self.BIT_ORDER_MSB_LEFT:
            if self._numbering == self.BIT_SCHEME_LSB_0:
                return width - (index + 1)
            elif self._numbering == self.BIT_SCHEME_LSB_1:
                return width - index
            elif self._numbering == self.BIT_SCHEME_MSB_0:
                return index
            elif self._numbering == self.BIT_SCHEME_MSB_1:
                return index + 1
        else:
            if self._numbering == self.BIT_SCHEME_LSB_0:
                return index
            elif self._numbering == self.BIT_SCHEME_LSB_1:
                return index + 1
            elif self._numbering == self.BIT_SCHEME_MSB_0:
                return width - (index + 1)
            elif self._numbering == self.BIT_SCHEME_MSB_1:
                return width - index

    def _shift(self, index):
        # Given a bit index, return the shift required to get it to the zeroth
        # position.
        # print "_shift: index=%d width=%d" % (index, self._width)
        if self._order == self.BIT_ORDER_MSB_LEFT:
            #print "ML S:%d" % (self._width - index - 1)
            return self._width - index - 1
        else:
            # print "MR S:%d" % (index)
            return index

    def _lsbIndex(self, start, end):
        # Given a bit range, return the index of the LSB of the range.
        if self._order == self.BIT_ORDER_MSB_LEFT:
            return max(start, end)
        else:
            return min(start, end)

    def _msbIndex(self, start, end):
        # Given a bit range, return the index of the MSB of the range.
        if self._order == self.BIT_ORDER_MSB_LEFT:
            return min(start, end)
        else:
            return max(start, end)

    def _checkIndex(self, index):
        rindex = self._index(index)
        if rindex < 0 or rindex >= self._width:
            raise ValueError("Invalid index for %d-bit bit-field!" % self._width)

    def _checkRange(self, start, end):
        self._checkIndex(start)
        self._checkIndex(end)
        if self._order == self.BIT_ORDER_MSB_LEFT:
            if self._numbering in (self.BIT_SCHEME_LSB_0, self.BIT_SCHEME_LSB_1):
                # LSB low, right, e.g. [7:0].
                if start < end:
                    raise ValueError("Invalid bit range for MSB...LSB bit-field!")
            else:
                # MSB low, left, e.g. [0:7].
                if start > end:
                    raise ValueError("Invalid bit range for MSB...LSB bit-field!")
        else:
            if self._numbering in (self.BIT_SCHEME_LSB_0, self.BIT_SCHEME_LSB_1):
                # LSB low, left, e.g. [0:7].
                if start > end:
                    raise ValueError("Invalid bit range for MSB...LSB bit-field!")
            else:
                # MSB low, right, e.g. [7:0].
                if start < end:
                    raise ValueError("Invalid bit range for MSB...LSB bit-field!")

    def _getRange(self, start, end):
        self._checkRange(start, end)
        rstart = self._index(start)
        rend = self._index(end)
        return (rstart, rend)

    def _checkValue(self, value, width=None):
        if width is None:
            width = self.width
        if width < 0 or width > self.maxval:
            raise ValueError("Illegal bit-field width %d!" % self.width)
        if value > 2 ** width:
            raise ValueError("Value is greater than allowed for %d-bit field!" % width)

    def _bitmask(self, start, end):
        self._checkRange(start, end)
        rstart, rend = self._getRange(start, end)
        return 2L ** (rend - rstart + 1) - 1

    def _getBitValue(self, index, value, width):
        "Get the value of the specified bit index in the supplied value."
        self._checkValue(value, width=width)
        rindex = self._index(index, width=width)
        shift = self._shift(rindex)
        return (value >> shift) & 1L

    def __getitem__(self, key):
        if isinstance(key, slice):
            start = key.start
            end = key.stop
            self._checkRange(start, end)
            rstart, rend = self._getRange(start, end)
            bitmask = self._bitmask(start, end)
            shift = self._shift(self._lsbIndex(rstart, rend))
        else:
            index = key
            self._checkIndex(index)
            rindex = self._index(index)
            bitmask = 1L
            shift = self._shift(rindex)
        # print "K=%s | B=%d | S=%d | v=%d->%d" % (key, bitmask, shift, self._value, (self._value >> shift) & bitmask)
        return (self._value >> shift) & bitmask

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            start = key.start
            end = key.stop
            self._checkRange(start, end)
            rstart, rend = self._getRange(start, end)
            bitmask = self._bitmask(start, end)
            shift = self._shift(self._lsbIndex(rstart, rend))
            newvalue = (((self._value >> shift) & ~bitmask) | value) << shift
            # print "%d:%d,%d | %d:%d | B=0x%x | S=%d | v=%d->%d" % \
            #     (start, end, value, rstart, rend, bitmask, shift, self._value, newvalue)
        else:
            index = key
            self._checkIndex(index)
            self._checkValue(value)
            rindex = self._index(index)
            shift = self._shift(rindex)
            value = (value & 1L) << shift
            bitmask = (1L) << shift
            newvalue = (self._value & ~bitmask) | value
            # print "%d,%d | %d | B=%d | S=%d | v=%d->%d" % \
            #     (index, value, rindex, bitmask, shift, self._value, newvalue)
        self._value = newvalue

    def __len__(self):
        return self._width

    def __int__(self):
        return self._value

    def __index__(self):
        return self._value

    def __repr__(self):
        return '{{:{0}>{1}}}'.format(0, self._width).format(bin(self._value)[2:])

    def set(self, index=None):
        "Set the specified bit (or all bits if not specified) to 1."
        if index:
            self._checkIndex(index)
            self.__setitem__(index, 1)
        else:
            self._value = self._maxval

    def clear(self, index=None):
        "Set the specified bit (or all bits if not specified) to 0."
        if index:
            self._checkIndex(index)
            self.__setitem__(index, 0)
        else:
            self._value = 0

    def isBit(self, index, value):
        "Return True if the specified bit has the specified value."
        self._checkIndex(index)
        return self.__getitem__(index) == value

    def isBitSet(self, index):
        "Return True if the specified bit is 1."
        return self.isBit(index, 1)

    def isBitClr(self, index):
        "Return True if the specified bit is 0."
        return not self.isBitSet(index)

    def isRange(self, start, end, value):
        "Return True if the specified range of bits has the specified value."
        self._checkRange(start, end)
        if value not in (0, 1):
            raise ValueError("Bit-field Value must be 0 or 1!")
        subfield = self.__getitem__(slice(start, end))
        bitmask = self._bitmask(start, end)
        if value == 0:
            return True if subfield == 0 else False
        else:
            setval = int(bitmask)
            return True if subfield == setval else False

    def isRangeSet(self, start, end):
        "Return True if the specified range of bits are all 1."
        return self.isRange(start, end, 1)

    def isRangeClr(self, start, end):
        "Return True if the specified range of bits are all 0."
        return not self.isRangeSet(start, end)
