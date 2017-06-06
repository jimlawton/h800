#!/usr/bin/env python

from h800.instructions import *


def my_assert(value, good):
    assert value == good, "Value is 0o%o, should be 0o%o" % (value, good)


def run_tests(message, testdata):
    print message
    for t in testdata:
        if t[0].__name__.endswith("Masked"):
            i = t[0](sequence=t[1], mask=t[2])
            my_assert(i.value, t[3])
        else:
            i = t[0](sequence=t[1], a=t[2], b=t[3], c=t[4])
            my_assert(i.value, t[5])


def run_exception_tests(message, testdata):
    print message
    for t in testdata:
        gotexc = False
        try:
            if t[0].__name__.endswith("Masked"):
                i = t[0](sequence=t[1], mask=t[2])
            else:
                i = t[0](sequence=t[1], a=t[2], b=t[3], c=t[4])
        except ValueError:
            gotexc = True
        else:
            raise
        assert gotexc == True, "Invalid value should have thrown an exception!"


def test_BA_masked_simple():
    print "TEST: BA (masked): simple"
    i = BinaryAddMasked(sequence=0, mask=0)
    my_assert(i.value, 0o51)


def test_BA_masked_invalid_args():
    print "TEST: BA (masked): invalid args"
    gotexc = False
    try:
        i = BinaryAddMasked(sequence=0, mask=32)
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"
    gotexc = False
    try:
        i = BinaryAddMasked(sequence=2, mask=0)
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"


def test_BA_masked_args_range():
    print "TEST: BA (masked): args range"
    i = BinaryAddMasked(sequence=1, mask=0)
    my_assert(i.value, 0o4051)
    i = BinaryAddMasked(sequence=0, mask=31)
    my_assert(i.value, 0o3751)
    i = BinaryAddMasked(sequence=1, mask=31)
    my_assert(i.value, 0o7751)


def test_BA_unmasked_simple():
    print "TEST: BA (unmasked): simple"
    i = BinaryAddUnmasked(sequence=0, a=0, b=0, c=0)
    my_assert(i.value, 0o2011)


def test_BA_unmasked_invalid_args():
    print "TEST: BA (unmasked): invalid args"
    gotexc = False
    try:
        i = BinaryAddUnmasked(sequence=2, a=0, b=0, c=0)
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"
    gotexc = False
    try:
        i = BinaryAddUnmasked(sequence=0, a=2, b=0, c=0)
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"
    gotexc = False
    try:
        i = BinaryAddUnmasked(sequence=0, a=-1, b=2, c=3)
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"


def test_BA_unmasked_args_range():
    print "TEST: BA (unmasked): args range"
    i = BinaryAddUnmasked(sequence=0, a=0, b=0, c=0)
    my_assert(i.value, 0o2011)
    i = BinaryAddUnmasked(sequence=0, a=0, b=0, c=1)
    my_assert(i.value, 0o2111)
    i = BinaryAddUnmasked(sequence=0, a=0, b=1, c=0)
    my_assert(i.value, 0o2211)
    i = BinaryAddUnmasked(sequence=0, a=0, b=1, c=1)
    my_assert(i.value, 0o2311)
    i = BinaryAddUnmasked(sequence=0, a=1, b=0, c=0)
    my_assert(i.value, 0o2411)
    i = BinaryAddUnmasked(sequence=0, a=1, b=0, c=1)
    my_assert(i.value, 0o2511)
    i = BinaryAddUnmasked(sequence=0, a=1, b=1, c=0)
    my_assert(i.value, 0o2611)
    i = BinaryAddUnmasked(sequence=0, a=1, b=1, c=1)
    my_assert(i.value, 0o2711)
    i = BinaryAddUnmasked(sequence=1, a=0, b=0, c=0)
    my_assert(i.value, 0o6011)
    i = BinaryAddUnmasked(sequence=1, a=0, b=0, c=1)
    my_assert(i.value, 0o6111)
    i = BinaryAddUnmasked(sequence=1, a=0, b=1, c=0)
    my_assert(i.value, 0o6211)
    i = BinaryAddUnmasked(sequence=1, a=0, b=1, c=1)
    my_assert(i.value, 0o6311)
    i = BinaryAddUnmasked(sequence=1, a=1, b=0, c=0)
    my_assert(i.value, 0o6411)
    i = BinaryAddUnmasked(sequence=1, a=1, b=0, c=1)
    my_assert(i.value, 0o6511)
    i = BinaryAddUnmasked(sequence=1, a=1, b=1, c=0)
    my_assert(i.value, 0o6611)
    i = BinaryAddUnmasked(sequence=1, a=1, b=1, c=1)
    my_assert(i.value, 0o6711)
