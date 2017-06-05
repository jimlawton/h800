#!/usr/bin/env python

from h800.instructions import *


def test_BA_masked_simple():
    print "TEST: BA (masked): simple"
    i = BinaryAddMasked(sequence=0, mask=0)
    assert i.value == 0o51, "Value is 0o%o, should be 0o51" % i.value


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
    assert i.value == 0o4051, "Value is 0o%o, should be 0o4051" % i.value
    i = BinaryAddMasked(sequence=0, mask=31)
    assert i.value == 0o3751, "Value is 0o%o, should be 0o6051" % i.value
    i = BinaryAddMasked(sequence=1, mask=31)
    assert i.value == 0o7751, "Value is 0o%o, should be 0o7751" % i.value


def test_BA_unmasked_simple():
    print "TEST: BA (unmasked): simple"
    i = BinaryAddUnmasked(sequence=0, a=0, b=0, c=0)
    assert i.value == 0o2011, "Value is 0o%o, should be 0o2011" % i.value


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
    assert i.value == 0o2011, "Value is 0o%o, should be 0o2011" % i.value
    i = BinaryAddUnmasked(sequence=0, a=0, b=0, c=1)
    assert i.value == 0o3711, "Value is 0o%o, should be 0o6051" % i.value
    i = BinaryAddUnmasked(sequence=0, a=0, b=1, c=0)
    assert i.value == 0o3711, "Value is 0o%o, should be 0o6051" % i.value
    i = BinaryAddUnmasked(sequence=0, a=0, b=1, c=1)
    assert i.value == 0o3711, "Value is 0o%o, should be 0o6051" % i.value
    i = BinaryAddUnmasked(sequence=0, a=1, b=0, c=0)
    assert i.value == 0o3711, "Value is 0o%o, should be 0o6051" % i.value
    i = BinaryAddUnmasked(sequence=0, a=1, b=0, c=1)
    assert i.value == 0o3711, "Value is 0o%o, should be 0o6051" % i.value
    i = BinaryAddUnmasked(sequence=0, a=1, b=1, c=0)
    assert i.value == 0o3711, "Value is 0o%o, should be 0o6051" % i.value
    i = BinaryAddUnmasked(sequence=0, a=1, b=1, c=1)
    assert i.value == 0o3711, "Value is 0o%o, should be 0o6051" % i.value
    i = BinaryAddUnmasked(sequence=1, a=0, b=0, c=0)
    assert i.value == 0o2011, "Value is 0o%o, should be 0o2051" % i.value
    i = BinaryAddUnmasked(sequence=1, a=0, b=0, c=1)
    assert i.value == 0o3711, "Value is 0o%o, should be 0o6051" % i.value
    i = BinaryAddUnmasked(sequence=1, a=0, b=1, c=0)
    assert i.value == 0o3711, "Value is 0o%o, should be 0o6051" % i.value
    i = BinaryAddUnmasked(sequence=1, a=0, b=1, c=1)
    assert i.value == 0o3711, "Value is 0o%o, should be 0o6051" % i.value
    i = BinaryAddUnmasked(sequence=1, a=1, b=0, c=0)
    assert i.value == 0o3711, "Value is 0o%o, should be 0o6051" % i.value
    i = BinaryAddUnmasked(sequence=1, a=1, b=0, c=1)
    assert i.value == 0o3711, "Value is 0o%o, should be 0o6051" % i.value
    i = BinaryAddUnmasked(sequence=1, a=1, b=1, c=0)
    assert i.value == 0o3711, "Value is 0o%o, should be 0o6051" % i.value
    i = BinaryAddUnmasked(sequence=1, a=1, b=1, c=1)
    assert i.value == 0o3711, "Value is 0o%o, should be 0o6051" % i.value
