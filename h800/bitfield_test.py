#!/usr/bin/env python

from h800.bitfield import BitField


def my_assert(value, good):
    assert value == good, "Value is %s, should be %s" % (value, good)


# Tester for generic bit-field class.

def test_simple():
    b = BitField()
    print("TEST: check initial value")
    my_assert(b.value, 0)
    print("TEST: check maxval")
    my_assert(b.maxval, 255)
    print("TEST: check width")
    my_assert(b.width, 8)
    print("TEST: check length")
    my_assert(len(b), 8)


def test_msb_left_8bit():
    b = BitField(8, order=BitField.BIT_ORDER_MSB_LEFT)
    print("TEST: indices=", b.indices)
    print("TEST: check initial value")
    my_assert(b.value, 8)
    print("TEST: check maxval")
    my_assert(b.maxval, 255)
    print("TEST: check width")
    my_assert(b.width, 8)
    print("TEST: check length")
    my_assert(len(b), 8)
    print("TEST: set slice [7:3] = 5")
    b[7:3] = 0b0101
    my_assert(b.value, 40)
    my_assert(b[3], 1)
    my_assert(b.isBitSet(3), True)
    my_assert(b[5], 1)
    my_assert(b.isBitSet(5), True)
    print("TEST: set bit 7 = 1")
    b[7] = 1
    my_assert(b[7], 1)
    my_assert(b.isBitSet(7), True)
    my_assert(b.value, 168)
    print("TEST: set slice [7:0] = 255")
    b[7:0] = 255
    my_assert(b.value, 255)
    my_assert(b.isBitSet(7), True)
    my_assert(b.isBitClr(7), False)
    my_assert(b.isBitSet(6), True)
    my_assert(b.isBitClr(6), False)
    my_assert(b.isBitSet(5), True)
    my_assert(b.isBitClr(5), False)
    my_assert(b.isBitSet(4), True)
    my_assert(b.isBitClr(4), False)
    my_assert(b.isBitSet(3), True)
    my_assert(b.isBitClr(3), False)
    my_assert(b.isBitSet(2), True)
    my_assert(b.isBitClr(2), False)
    my_assert(b.isBitSet(1), True)
    my_assert(b.isBitClr(1), False)
    my_assert(b.isBitSet(0), True)
    my_assert(b.isBitClr(0), False)
    my_assert(b.value, 255)
    my_assert(b.isRange(7, 0, 1), True)
    my_assert(b.isRangeSet(7, 0), True)
    my_assert(b.isRangeClr(7, 0), False)


def test_msb_left_15bit():
    b = BitField(15, order=BitField.BIT_ORDER_MSB_LEFT)
    print("TEST: check initial value")
    my_assert(b.value, 15)
    print("TEST: check maxval")
    my_assert(b.maxval, 255)
    print("TEST: check width")
    my_assert(b.width, 8)
    print("TEST: check bit 7 clear")
    my_assert(b[7], 0)
    my_assert(b.isBitSet(7), False)
    my_assert(b.isBitClr(7), True)
    print("TEST: check bit 6 clear")
    my_assert(b[6], 0)
    my_assert(b.isBitSet(6), False)
    my_assert(b.isBitClr(6), True)
    print("TEST: check bit 5 clear")
    my_assert(b[5], 0)
    my_assert(b.isBitSet(5), False)
    my_assert(b.isBitClr(5), True)
    print("TEST: check bit 4 clear")
    my_assert(b[4], 0)
    my_assert(b.isBitSet(4), False)
    my_assert(b.isBitClr(4), True)
    print("TEST: check bit 3 set")
    my_assert(b[3], 1)
    my_assert(b.isBitSet(3), True)
    my_assert(b.isBitClr(3), False)
    print("TEST: check bit 2 set")
    my_assert(b[2], 1)
    my_assert(b.isBitSet(2), True)
    my_assert(b.isBitClr(2), False)
    print("TEST: check bit 1 set")
    my_assert(b[1], 1)
    my_assert(b.isBitSet(1), True)
    my_assert(b.isBitClr(1), False)
    print("TEST: check bit 0 set")
    my_assert(b[0], 1)
    my_assert(b.isBitSet(0), True)
    my_assert(b.isBitClr(0), False)


def test_msb_right_8bit():
    b = BitField(8, order=BitField.BIT_ORDER_MSB_RIGHT)
    print("TEST: check initial value")
    my_assert(b.value, 8)
    print("TEST: check maxval")
    my_assert(b.maxval, 255)
    print("TEST: check width")
    my_assert(b.width, 8)
    print("TEST: set slice [7:3] = 5")
    b[3:7] = 0b0101
    my_assert(b.value, 40)
    my_assert(b[3], 1)
    my_assert(b.isBitSet(3), True)
    my_assert(b.isBitClr(3), False)
    my_assert(b[5], 1)
    my_assert(b.isBitSet(5), True)
    my_assert(b.isBitClr(5), False)
    print("TEST: set bit 7 = 1")
    b[7] = 1
    my_assert(b[7], 1)
    my_assert(b.isBitSet(7), True)
    my_assert(b.isBitClr(7), False)
    my_assert(b.value, 168)
    print("TEST: set slice [0:7] = 255")
    b[0:7] = 255
    my_assert(b.isBitSet(0), True)
    my_assert(b.isBitClr(0), False)
    my_assert(b.isBitSet(1), True)
    my_assert(b.isBitClr(1), False)
    my_assert(b.isBitSet(2), True)
    my_assert(b.isBitClr(2), False)
    my_assert(b.isBitSet(3), True)
    my_assert(b.isBitClr(3), False)
    my_assert(b.isBitSet(4), True)
    my_assert(b.isBitClr(4), False)
    my_assert(b.isBitSet(5), True)
    my_assert(b.isBitClr(5), False)
    my_assert(b.isBitSet(6), True)
    my_assert(b.isBitClr(6), False)
    my_assert(b.isBitSet(7), True)
    my_assert(b.isBitClr(7), False)
    my_assert(b.value, 255)


def test_invalid_args():
    gotexc = False
    try:
        print("TEST: test invalid width")
        b = BitField(256, width=65, order=BitField.BIT_ORDER_MSB_RIGHT)
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc is True, "Invalid value should have thrown an exception!"

    gotexc = False
    try:
        print("TEST: test invalid initial value for width")
        b = BitField(256, width=8, order=BitField.BIT_ORDER_MSB_RIGHT)
        assert b is not None
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc is True, "Invalid value should have thrown an exception!"


def test_msb_left_msb1_48bit():
    b = BitField(0, width=48, numbering=BitField.BIT_SCHEME_MSB_1,
                 order=BitField.BIT_ORDER_MSB_LEFT)
    print("TEST: check initial value")
    my_assert(b.value, 0)
    print("TEST: check maxval")
    my_assert(b.maxval, 2 ** 48 - 1)
    print("TEST: check width")
    my_assert(b.width, 48)
    print("TEST: check length")
    my_assert(len(b), 48)
    print("TEST: set slice [33:48] = 65535")
    b[33:48] = 0b1111111111111111
    my_assert(b.value, 65535)
    print("TEST: set value to zero")
    b[1:48] = 0
    my_assert(b.value, 0)
    print("TEST: set value to all ones using slice")
    b[1:48] = b.maxval
    my_assert(b.value, 2 ** 48 - 1)
    print("TEST: set value to all zeros using slice")
    b[1:48] = 0
    my_assert(b.value, 0)
    print("TEST: set value to all ones using set")
    b.set()
    my_assert(b.value, 2 ** 48 - 1)
    print("TEST: set value to all zeros using clear")
    b.clear()
    my_assert(b.value, 0)
    print("TEST: set high 12 bits to test-pattern")
    b[1:12] = 0b101010101010
    my_assert(b.value, 187604171489280)
    print("TEST: set value to all zeros using clear")
    b.clear()
    my_assert(b.value, 0)
    print("TEST: set 2nd 12 bits to test-pattern")
    b[13:24] = 0b101010101010
    my_assert(b.value, 45801799680)
    print("TEST: set value to all zeros using clear")
    b.clear()
    my_assert(b.value, 0)
    print("TEST: set 3rd 12 bits to test-pattern")
    b[25:36] = 0b101010101010
    my_assert(b.value, 11182080)
    print("TEST: set value to all zeros using clear")
    b.clear()
    my_assert(b.value, 0)
    print("TEST: set low 12 bits to test-pattern")
    b[37:48] = 0b101010101010
    my_assert(b.value, 2730)
    print("TEST: set value to all zeros using clear")
    b.clear()
    my_assert(b.value, 0)


def test_msb_left_msb1_12bit():
    b = BitField(0, width=12, numbering=BitField.BIT_SCHEME_MSB_1,
                 order=BitField.BIT_ORDER_MSB_LEFT)
    print("TEST: check initial value")
    my_assert(b.value, 0)
    print("TEST: indices=", b.indices)
    print("TEST: check maxval")
    my_assert(b.maxval, 4095)
    print("TEST: check width")
    my_assert(b.width, 12)
    print("TEST: check length")
    my_assert(len(b), 12)
    print("TEST: set slice [9:12] = 15")
    b[9:12] = 0b1111
    my_assert(b.value, 15)
    print("TEST: set value to zero")
    b[1:12] = 0
    my_assert(b.value, 0)
    print("TEST: set value to all ones using slice")
    b[1:12] = b.maxval
    my_assert(b.value, 4095)
    print("TEST: set value to all zeros using slice")
    b[1:12] = 0
    my_assert(b.value, 0)
    print("TEST: set value to all ones using set")
    b.set()
    my_assert(b.value, 4095)
    print("TEST: set value to all zeros using clear")
    b.clear()
    my_assert(b.value, 0)
    print("TEST: set high 6 bits to test-pattern")
    b[1:6] = 0b101010
    my_assert(b.value, 2688)
    print("TEST: set value to all zeros using clear")
    b.clear()
    my_assert(b.value, 0)
    print("TEST: set low 6 bits to test-pattern")
    b[7:12] = 0b101010
    my_assert(b.value, 42)
    print("TEST: set value to all zeros using clear")
    b.clear()
    my_assert(b.value, 0)
    print("TEST: ripple a one right")
    for i in range(12):
        b.set(i + 1)
        my_assert(b.value, 2 ** (12 - i - 1))
        b.clear(i + 1)
        my_assert(b.value, 0)
    print("TEST: ripple a one left")
    for i in range(12):
        b.set(12 - i)
        my_assert(b.value, 2 ** i)
        b.clear(12 - i)
        my_assert(b.value, 0)
    print("TEST: shift a one right, filling")
    good = 0
    for i in range(12):
        b.set(i + 1)
        good += 2 ** (12 - i - 1)
        my_assert(b.value, good)
    b.clear()
    my_assert(b.value, 0)
    print("TEST: shift a one left, filling")
    good = 0
    for i in range(12):
        b.set(12 - i)
        good += 2 ** i
        my_assert(b.value, good)
    b.clear()
    my_assert(b.value, 0)


def test_misc_12bit():
    b = BitField(0, width=12, numbering=BitField.BIT_SCHEME_MSB_1,
                 order=BitField.BIT_ORDER_MSB_LEFT)
    print("TEST: check initial value")
    my_assert(b.value, 0)
    print("TEST: set bit 1")
    b[1] = 1
    my_assert(b.value, 2 ** 11)
    print("TEST: set bit 7")
    b[7] = 1
    my_assert(b.value, 2 ** 11 + 2 ** 5)
    print("TEST: clear bits 1:6")
    b[1:6] = 0
    my_assert(b.value, 2 ** 5)
    print("TEST: set bits 8:12 to 00101")
    b[8:12] = 5
    my_assert(b.value, 2 ** 5 + 5)
