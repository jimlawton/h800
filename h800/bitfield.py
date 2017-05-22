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

    # Calculating real indexes from supplied virtual indexes:
    # ("I" is the supplied virtual index)
    #
    # Order                 Scheme              Real Index
    # BIT_ORDER_MSB_LEFT    BIT_SCHEME_LSB_0    N - (I + 1)
    # BIT_ORDER_MSB_LEFT    BIT_SCHEME_LSB_1    N - I
    # BIT_ORDER_MSB_LEFT    BIT_SCHEME_MSB_0    I
    # BIT_ORDER_MSB_LEFT    BIT_SCHEME_MSB_1    I - 1
    # BIT_ORDER_LSB_LEFT    BIT_SCHEME_LSB_0    I
    # BIT_ORDER_LSB_LEFT    BIT_SCHEME_LSB_1    I - 1
    # BIT_ORDER_LSB_LEFT    BIT_SCHEME_MSB_0    N - (I + 1)
    # BIT_ORDER_LSB_LEFT    BIT_SCHEME_MSB_1    N - I
    def _index(self, index):
        if self._order == self.BIT_ORDER_MSB_LEFT:
            if self._numbering == self.BIT_SCHEME_LSB_0:
                return self._width - (index + 1)
            elif self._numbering == self.BIT_SCHEME_LSB_1:
                return self._width - index
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
                return self._width - (index + 1)
            elif self._numbering == self.BIT_SCHEME_MSB_1:
                return self._width - index

    def _shift(self, index):
        # Given a bit index, return the shift required to get it to the zeroth
        # position.
        # print "_shift: index=%d width=%d" % (index, self._width)
        if self._order == self.BIT_ORDER_MSB_LEFT:
            # print "ML S:%d" % (self._width - index - 1)
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

    def _checkValue(self, value):
        if value > self.maxval:
            raise ValueError("Value is greater than allowed for %d-bit field!" % self.width)

    def _bitmask(self, start, end):
        self._checkRange(start, end)
        rstart, rend = self._getRange(start, end)
        return 2L ** (rend - rstart + 1) - 1

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
            bitmask = 1
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


def main():
    print "\nTESTSUITE: simple default case."
    b = BitField()
    print "TEST: check initial value"
    assert b.value == 0, "Value is %d, should be 0" % b.value
    print "TEST: check maxval"
    assert b.maxval == 255, "Maxval is %d, should be 255" % b.maxval
    print "TEST: check width"
    assert b.width == 8, "Width is %d, should be 8" % b.width
    print "TEST: check length"
    assert len(b) == 8, "Length is %d, should be 8" % len(b)

    print "\nTESTSUITE: default width, initial value, msb-left."
    b = BitField(8, order=BitField.BIT_ORDER_MSB_LEFT)
    print "TEST: check initial value"
    assert b.value == 8, "Value is %d, should be 0" % b.value
    print "TEST: check maxval"
    assert b.maxval == 255, "Maxval is %d, should be 255" % b.maxval
    print "TEST: check width"
    assert b.width == 8, "Width is %d, should be 8" % b.width
    print "TEST: check length"
    assert len(b) == 8, "Length is %d, should be 8" % len(b)
    print "TEST: set slice [7:3] = 5"
    b[7:3] = 0b0101
    assert b.value == 40, "Value is %d, should be 40" % b.value
    assert b[3] == 1
    assert b.isBitSet(3) == True
    assert b[5] == 1
    assert b.isBitSet(5) == True
    print "TEST: set bit 7 = 1"
    b[7] = 1
    assert b[7] == 1
    assert b.isBitSet(7) == True
    assert b.value == 168, "Value is %d, should be 168" % b.value
    print "TEST: set slice [7:0] = 255"
    b[7:0] = 255
    assert b.value == 255, "Value is %d, should be 168" % b.value
    assert b.isBitSet(7) == True
    assert b.isBitClr(7) == False
    assert b.isBitSet(6) == True
    assert b.isBitClr(6) == False
    assert b.isBitSet(5) == True
    assert b.isBitClr(5) == False
    assert b.isBitSet(4) == True
    assert b.isBitClr(4) == False
    assert b.isBitSet(3) == True
    assert b.isBitClr(3) == False
    assert b.isBitSet(2) == True
    assert b.isBitClr(2) == False
    assert b.isBitSet(1) == True
    assert b.isBitClr(1) == False
    assert b.isBitSet(0) == True
    assert b.isBitClr(0) == False
    assert b.value == 255, "Value is %d, should be 255" % b.value
    assert b.isRange(7, 0, 1) == True
    assert b.isRangeSet(7, 0) == True
    assert b.isRangeClr(7, 0) == False

    print "\nTESTSUITE: default width, initial value, msb-left."
    b = BitField(15, order=BitField.BIT_ORDER_MSB_LEFT)
    print "TEST: check initial value"
    assert b.value == 15, "Value is %d, should be 0" % b.value
    print "TEST: check maxval"
    assert b.maxval == 255, "Maxval is %d, should be 255" % b.maxval
    print "TEST: check width"
    assert b.width == 8, "Width is %d, should be 8" % b.width
    print "TEST: check bit 7 clear"
    assert b[7] == 0
    assert b.isBitSet(7) == False
    assert b.isBitClr(7) == True
    print "TEST: check bit 6 clear"
    assert b[6] == 0
    assert b.isBitSet(6) == False
    assert b.isBitClr(6) == True
    print "TEST: check bit 5 clear"
    assert b[5] == 0
    assert b.isBitSet(5) == False
    assert b.isBitClr(5) == True
    print "TEST: check bit 4 clear"
    assert b[4] == 0
    assert b.isBitSet(4) == False
    assert b.isBitClr(4) == True
    print "TEST: check bit 3 set"
    assert b[3] == 1
    assert b.isBitSet(3) == True
    assert b.isBitClr(3) == False
    print "TEST: check bit 2 set"
    assert b[2] == 1
    assert b.isBitSet(2) == True
    assert b.isBitClr(2) == False
    print "TEST: check bit 1 set"
    assert b[1] == 1
    assert b.isBitSet(1) == True
    assert b.isBitClr(1) == False
    print "TEST: check bit 0 set"
    assert b[0] == 1
    assert b.isBitSet(0) == True
    assert b.isBitClr(0) == False

    print "\nTESTSUITE: default width, initial value, msb-right."
    b = BitField(8, order=BitField.BIT_ORDER_MSB_RIGHT)
    print "TEST: check initial value"
    assert b.value == 8, "Value is %d, should be 0" % b.value
    print "TEST: check maxval"
    assert b.maxval == 255, "Maxval is %d, should be 255" % b.maxval
    print "TEST: check width"
    assert b.width == 8, "Width is %d, should be 8" % b.width
    print "TEST: set slice [7:3] = 5"
    b[3:7] = 0b0101
    assert b.value == 40, "Value is %d, should be 40" % b.value
    assert b[3] == 1
    assert b.isBitSet(3) == True
    assert b.isBitClr(3) == False
    assert b[5] == 1
    assert b.isBitSet(5) == True
    assert b.isBitClr(5) == False
    print "TEST: set bit 7 = 1"
    b[7] = 1
    assert b[7] == 1
    assert b.isBitSet(7) == True
    assert b.isBitClr(7) == False
    assert b.value == 168, "Value is %d, should be 168" % b.value
    print "TEST: set slice [0:7] = 255"
    b[0:7] = 255
    assert b.isBitSet(0) == True
    assert b.isBitClr(0) == False
    assert b.isBitSet(1) == True
    assert b.isBitClr(1) == False
    assert b.isBitSet(2) == True
    assert b.isBitClr(2) == False
    assert b.isBitSet(3) == True
    assert b.isBitClr(3) == False
    assert b.isBitSet(4) == True
    assert b.isBitClr(4) == False
    assert b.isBitSet(5) == True
    assert b.isBitClr(5) == False
    assert b.isBitSet(6) == True
    assert b.isBitClr(6) == False
    assert b.isBitSet(7) == True
    assert b.isBitClr(7) == False
    assert b.value == 255, "Value is %d, should be 255" % b.value

    print "\nTESTSUITE: invalid width, invalid initial value, msb-right."
    gotexc = False
    try:
        print "TEST: test invalid width"
        b = BitField(256, width=65, order=BitField.BIT_ORDER_MSB_RIGHT)
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"

    gotexc = False
    try:
        print "TEST: test invalid initial value for width"
        b = BitField(256, width=8, order=BitField.BIT_ORDER_MSB_RIGHT)
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"

    print "\nTESTSUITE: width=48, initial value, msb-left, msb-1 scheme."
    b = BitField(0, width=48, numbering=BitField.BIT_SCHEME_MSB_1,
                 order=BitField.BIT_ORDER_MSB_LEFT)
    print "TEST: check initial value"
    assert b.value == 0, "Value is %d, should be 0" % b.value
    print "TEST: check maxval"
    assert b.maxval == 2L ** 48 - 1, "Maxval is %d, should be 255" % b.maxval
    print "TEST: check width"
    assert b.width == 48, "Width is %d, should be 8" % b.width
    print "TEST: check length"
    assert len(b) == 48, "Length is %d, should be 8" % len(b)
    print "TEST: set slice [33:48] = 65535"
    b[33:48] = 0b1111111111111111
    assert b.value == 65535, "Value is %d, should be 65535" % b.value
    print "TEST: set value to zero"
    b[1:48] = 0
    assert b.value == 0, "Value is %d, should be 0" % b.value
    print "TEST: set value to all ones using slice"
    b[1:48] = b.maxval
    assert b.value == 2 ** 48 - 1, "Value is %d, should be %d" % (b.value, b.maxval)
    print "TEST: set value to all zeros using slice"
    b[1:48] = 0
    assert b.value == 0, "Value is %d, should be %d" % (b.value, 0)
    print "TEST: set value to all ones using set"
    b.set()
    assert b.value == 2 ** 48 - 1, "Value is %d, should be %d" % (b.value, b.maxval)
    print "TEST: set value to all zeros using clear"
    b.clear()
    assert b.value == 0, "Value is %d, should be %d" % (b.value, 0)
    print "TEST: set high 12 bits to test-pattern"
    b[1:12] = 0b101010101010
    assert b.value == 187604171489280, "Value is %d, should be %d" % (b.value, 187604171489280)
    print "TEST: set value to all zeros using clear"
    b.clear()
    assert b.value == 0, "Value is %d, should be %d" % (b.value, 0)
    print "TEST: set 2nd 12 bits to test-pattern"
    b[13:24] = 0b101010101010
    assert b.value == 45801799680, "Value is %d, should be %d" % (b.value, 45801799680)
    print "TEST: set value to all zeros using clear"
    b.clear()
    assert b.value == 0, "Value is %d, should be %d" % (b.value, 0)
    print "TEST: set 3rd 12 bits to test-pattern"
    b[25:36] = 0b101010101010
    assert b.value == 11182080, "Value is %d, should be %d" % (b.value, 11182080)
    print "TEST: set value to all zeros using clear"
    b.clear()
    assert b.value == 0, "Value is %d, should be %d" % (b.value, 0)
    print "TEST: set low 12 bits to test-pattern"
    b[37:48] = 0b101010101010
    assert b.value == 2730, "Value is %d, should be %d" % (b.value, 2730)
    print "TEST: set value to all zeros using clear"
    b.clear()
    assert b.value == 0, "Value is %d, should be %d" % (b.value, 0)

    print "\nPASS"


if __name__ == '__main__':
    main()
