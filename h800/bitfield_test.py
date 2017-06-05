#!/usr/bin/env python

from h800.bitfield import *


# Tester for generic bit-field class.

def test_simple():
    b = BitField()
    print "TEST: check initial value"
    assert b.value == 0, "Value is %d, should be 0" % b.value
    print "TEST: check maxval"
    assert b.maxval == 255, "Maxval is %d, should be 255" % b.maxval
    print "TEST: check width"
    assert b.width == 8, "Width is %d, should be 8" % b.width
    print "TEST: check length"
    assert len(b) == 8, "Length is %d, should be 8" % len(b)


def test_msb_left_8bit():
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


def test_msb_left_15bit():
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


def test_msb_right_8bit():
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


def test_invalid_args():
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


def test_msb_left_msb1_48bit():
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
