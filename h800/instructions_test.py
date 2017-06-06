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
    testdata = [[BinaryAddMasked, 0, 0, 0o51]]
    run_tests("TEST: BA (masked): simple", testdata)


def test_BA_masked_invalid_args():
    testdata = [
        [BinaryAddMasked, 0, 32, 0],
        [BinaryAddMasked, 2, 0, 0]
    ]
    run_exception_tests("TEST: BA (masked): invalid args", testdata)


def test_BA_masked_args_range():
    testdata = [
        [BinaryAddMasked, 1, 0, 0o4051],
        [BinaryAddMasked, 0, 31, 0o3751],
        [BinaryAddMasked, 1, 31, 0o7751]
    ]
    run_tests("TEST: BA (masked): args range", testdata)


def test_BA_unmasked_simple():
    testdata = [[BinaryAddUnmasked, 0, 0, 0, 0, 0o2011]]
    run_tests("TEST: BA (unmasked): simple", testdata)


def test_BA_unmasked_invalid_args():
    testdata = [
        [BinaryAddUnmasked, 2, 0, 0, 0, 0],
        [BinaryAddUnmasked, 0, 2, 0, 0, 0],
        [BinaryAddUnmasked, 0, 1, 2, 3, 0]
    ]
    run_exception_tests("TEST: BA (unmasked): invalid args", testdata)


def test_BA_unmasked_args_range():
    testdata = [
        [BinaryAddUnmasked, 0, 0, 0, 0, 0o2011],
        [BinaryAddUnmasked, 0, 0, 0, 1, 0o2111],
        [BinaryAddUnmasked, 0, 0, 1, 0, 0o2211],
        [BinaryAddUnmasked, 0, 0, 1, 1, 0o2311],
        [BinaryAddUnmasked, 0, 1, 0, 0, 0o2411],
        [BinaryAddUnmasked, 0, 1, 0, 1, 0o2511],
        [BinaryAddUnmasked, 0, 1, 1, 0, 0o2611],
        [BinaryAddUnmasked, 0, 1, 1, 1, 0o2711],
        [BinaryAddUnmasked, 1, 0, 0, 0, 0o6011],
        [BinaryAddUnmasked, 1, 0, 0, 1, 0o6111],
        [BinaryAddUnmasked, 1, 0, 1, 0, 0o6211],
        [BinaryAddUnmasked, 1, 0, 1, 1, 0o6311],
        [BinaryAddUnmasked, 1, 1, 0, 0, 0o6411],
        [BinaryAddUnmasked, 1, 1, 0, 1, 0o6511],
        [BinaryAddUnmasked, 1, 1, 1, 0, 0o6611],
        [BinaryAddUnmasked, 1, 1, 1, 1, 0o6711]
    ]
    run_tests("TEST: BA (unmasked): args range", testdata)


def test_DA_masked_simple():
    testdata = [[DecimalAddMasked, 0, 0, 0o41]]
    run_tests("TEST: DA (masked): simple", testdata)


def test_DA_masked_invalid_args():
    testdata = [
        [DecimalAddMasked, 0, 32, 0],
        [DecimalAddMasked, 2, 0, 0]
    ]
    run_exception_tests("TEST: DA (masked): invalid args", testdata)


def test_DA_masked_args_range():
    testdata = [
        [DecimalAddMasked, 1, 0, 0o4041],
        [DecimalAddMasked, 0, 31, 0o3741],
        [DecimalAddMasked, 1, 31, 0o7741]
    ]
    run_tests("TEST: DA (masked): args range", testdata)


def test_DA_unmasked_simple():
    testdata = [[DecimalAddUnmasked, 0, 0, 0, 0, 0o2001]]
    run_tests("TEST: DA (unmasked): simple", testdata)


def test_DA_unmasked_invalid_args():
    testdata = [
        [DecimalAddUnmasked, 2, 0, 0, 0, 0],
        [DecimalAddUnmasked, 0, 2, 0, 0, 0],
        [DecimalAddUnmasked, 0, 1, 2, 3, 0]
    ]
    run_exception_tests("TEST: DA (unmasked): invalid args", testdata)


def test_DA_unmasked_args_range():
    testdata = [
        [DecimalAddUnmasked, 0, 0, 0, 0, 0o2001],
        [DecimalAddUnmasked, 0, 0, 0, 1, 0o2101],
        [DecimalAddUnmasked, 0, 0, 1, 0, 0o2201],
        [DecimalAddUnmasked, 0, 0, 1, 1, 0o2301],
        [DecimalAddUnmasked, 0, 1, 0, 0, 0o2401],
        [DecimalAddUnmasked, 0, 1, 0, 1, 0o2501],
        [DecimalAddUnmasked, 0, 1, 1, 0, 0o2601],
        [DecimalAddUnmasked, 0, 1, 1, 1, 0o2701],
        [DecimalAddUnmasked, 1, 0, 0, 0, 0o6001],
        [DecimalAddUnmasked, 1, 0, 0, 1, 0o6101],
        [DecimalAddUnmasked, 1, 0, 1, 0, 0o6201],
        [DecimalAddUnmasked, 1, 0, 1, 1, 0o6301],
        [DecimalAddUnmasked, 1, 1, 0, 0, 0o6401],
        [DecimalAddUnmasked, 1, 1, 0, 1, 0o6501],
        [DecimalAddUnmasked, 1, 1, 1, 0, 0o6601],
        [DecimalAddUnmasked, 1, 1, 1, 1, 0o6701]
    ]
    run_tests("TEST: DA (unmasked): args range", testdata)
