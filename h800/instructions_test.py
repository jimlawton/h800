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


# ######## BA ########

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


# ######## DA ########

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


# ######## WA ########

def test_WA_masked_simple():
    testdata = [[WordAddMasked, 0, 0, 0o55]]
    run_tests("TEST: WA (masked): simple", testdata)


def test_WA_masked_invalid_args():
    testdata = [
        [WordAddMasked, 0, 32, 0],
        [WordAddMasked, 2, 0, 0]
    ]
    run_exception_tests("TEST: WA (masked): invalid args", testdata)


def test_WA_masked_args_range():
    testdata = [
        [WordAddMasked, 1, 0, 0o4055],
        [WordAddMasked, 0, 31, 0o3755],
        [WordAddMasked, 1, 31, 0o7755]
    ]
    run_tests("TEST: WA (masked): args range", testdata)


def test_WA_unmasked_simple():
    testdata = [[WordAddUnmasked, 0, 0, 0, 0, 0o2015]]
    run_tests("TEST: WA (unmasked): simple", testdata)


def test_WA_unmasked_invalid_args():
    testdata = [
        [WordAddUnmasked, 2, 0, 0, 0, 0],
        [WordAddUnmasked, 0, 2, 0, 0, 0],
        [WordAddUnmasked, 0, 1, 2, 3, 0]
    ]
    run_exception_tests("TEST: WA (unmasked): invalid args", testdata)


def test_WA_unmasked_args_range():
    testdata = [
        [WordAddUnmasked, 0, 0, 0, 0, 0o2015],
        [WordAddUnmasked, 0, 0, 0, 1, 0o2115],
        [WordAddUnmasked, 0, 0, 1, 0, 0o2215],
        [WordAddUnmasked, 0, 0, 1, 1, 0o2315],
        [WordAddUnmasked, 0, 1, 0, 0, 0o2415],
        [WordAddUnmasked, 0, 1, 0, 1, 0o2515],
        [WordAddUnmasked, 0, 1, 1, 0, 0o2615],
        [WordAddUnmasked, 0, 1, 1, 1, 0o2715],
        [WordAddUnmasked, 1, 0, 0, 0, 0o6015],
        [WordAddUnmasked, 1, 0, 0, 1, 0o6115],
        [WordAddUnmasked, 1, 0, 1, 0, 0o6215],
        [WordAddUnmasked, 1, 0, 1, 1, 0o6315],
        [WordAddUnmasked, 1, 1, 0, 0, 0o6415],
        [WordAddUnmasked, 1, 1, 0, 1, 0o6515],
        [WordAddUnmasked, 1, 1, 1, 0, 0o6615],
        [WordAddUnmasked, 1, 1, 1, 1, 0o6715]
    ]
    run_tests("TEST: WA (unmasked): args range", testdata)


# ######## BS ########

def test_BS_masked_simple():
    testdata = [[BinarySubtractMasked, 0, 0, 0o71]]
    run_tests("TEST: BA (masked): simple", testdata)


def test_BS_masked_invalid_args():
    testdata = [
        [BinarySubtractMasked, 0, 32, 0],
        [BinarySubtractMasked, 2, 0, 0]
    ]
    run_exception_tests("TEST: BA (masked): invalid args", testdata)


def test_BS_masked_args_range():
    testdata = [
        [BinarySubtractMasked, 1, 0, 0o4071],
        [BinarySubtractMasked, 0, 31, 0o3771],
        [BinarySubtractMasked, 1, 31, 0o7771]
    ]
    run_tests("TEST: BA (masked): args range", testdata)


def test_BS_unmasked_simple():
    testdata = [[BinarySubtractUnmasked, 0, 0, 0, 0, 0o2031]]
    run_tests("TEST: BA (unmasked): simple", testdata)


def test_BS_unmasked_invalid_args():
    testdata = [
        [BinarySubtractUnmasked, 2, 0, 0, 0, 0],
        [BinarySubtractUnmasked, 0, 2, 0, 0, 0],
        [BinarySubtractUnmasked, 0, 1, 2, 3, 0]
    ]
    run_exception_tests("TEST: BA (unmasked): invalid args", testdata)


def test_BS_unmasked_args_range():
    testdata = [
        [BinarySubtractUnmasked, 0, 0, 0, 0, 0o2031],
        [BinarySubtractUnmasked, 0, 0, 0, 1, 0o2131],
        [BinarySubtractUnmasked, 0, 0, 1, 0, 0o2231],
        [BinarySubtractUnmasked, 0, 0, 1, 1, 0o2331],
        [BinarySubtractUnmasked, 0, 1, 0, 0, 0o2431],
        [BinarySubtractUnmasked, 0, 1, 0, 1, 0o2531],
        [BinarySubtractUnmasked, 0, 1, 1, 0, 0o2631],
        [BinarySubtractUnmasked, 0, 1, 1, 1, 0o2731],
        [BinarySubtractUnmasked, 1, 0, 0, 0, 0o6031],
        [BinarySubtractUnmasked, 1, 0, 0, 1, 0o6131],
        [BinarySubtractUnmasked, 1, 0, 1, 0, 0o6231],
        [BinarySubtractUnmasked, 1, 0, 1, 1, 0o6331],
        [BinarySubtractUnmasked, 1, 1, 0, 0, 0o6431],
        [BinarySubtractUnmasked, 1, 1, 0, 1, 0o6531],
        [BinarySubtractUnmasked, 1, 1, 1, 0, 0o6631],
        [BinarySubtractUnmasked, 1, 1, 1, 1, 0o6731]
    ]
    run_tests("TEST: BA (unmasked): args range", testdata)


# ######## DS ########

def test_DS_masked_simple():
    testdata = [[DecimalSubtractMasked, 0, 0, 0o61]]
    run_tests("TEST: DA (masked): simple", testdata)


def test_DS_masked_invalid_args():
    testdata = [
        [DecimalSubtractMasked, 0, 32, 0],
        [DecimalSubtractMasked, 2, 0, 0]
    ]
    run_exception_tests("TEST: DA (masked): invalid args", testdata)


def test_DS_masked_args_range():
    testdata = [
        [DecimalSubtractMasked, 1, 0, 0o4061],
        [DecimalSubtractMasked, 0, 31, 0o3761],
        [DecimalSubtractMasked, 1, 31, 0o7761]
    ]
    run_tests("TEST: DA (masked): args range", testdata)


def test_DS_unmasked_simple():
    testdata = [[DecimalSubtractUnmasked, 0, 0, 0, 0, 0o2021]]
    run_tests("TEST: DA (unmasked): simple", testdata)


def test_DS_unmasked_invalid_args():
    testdata = [
        [DecimalSubtractUnmasked, 2, 0, 0, 0, 0],
        [DecimalSubtractUnmasked, 0, 2, 0, 0, 0],
        [DecimalSubtractUnmasked, 0, 1, 2, 3, 0]
    ]
    run_exception_tests("TEST: DA (unmasked): invalid args", testdata)


def test_DS_unmasked_args_range():
    testdata = [
        [DecimalSubtractUnmasked, 0, 0, 0, 0, 0o2021],
        [DecimalSubtractUnmasked, 0, 0, 0, 1, 0o2121],
        [DecimalSubtractUnmasked, 0, 0, 1, 0, 0o2221],
        [DecimalSubtractUnmasked, 0, 0, 1, 1, 0o2321],
        [DecimalSubtractUnmasked, 0, 1, 0, 0, 0o2421],
        [DecimalSubtractUnmasked, 0, 1, 0, 1, 0o2521],
        [DecimalSubtractUnmasked, 0, 1, 1, 0, 0o2621],
        [DecimalSubtractUnmasked, 0, 1, 1, 1, 0o2721],
        [DecimalSubtractUnmasked, 1, 0, 0, 0, 0o6021],
        [DecimalSubtractUnmasked, 1, 0, 0, 1, 0o6121],
        [DecimalSubtractUnmasked, 1, 0, 1, 0, 0o6221],
        [DecimalSubtractUnmasked, 1, 0, 1, 1, 0o6321],
        [DecimalSubtractUnmasked, 1, 1, 0, 0, 0o6421],
        [DecimalSubtractUnmasked, 1, 1, 0, 1, 0o6521],
        [DecimalSubtractUnmasked, 1, 1, 1, 0, 0o6621],
        [DecimalSubtractUnmasked, 1, 1, 1, 1, 0o6721]
    ]
    run_tests("TEST: DA (unmasked): args range", testdata)


# ######## WD ########

def test_WD_masked_simple():
    testdata = [[WordDifferenceMasked, 0, 0, 0o75]]
    run_tests("TEST: WA (masked): simple", testdata)


def test_WD_masked_invalid_args():
    testdata = [
        [WordDifferenceMasked, 0, 32, 0],
        [WordDifferenceMasked, 2, 0, 0]
    ]
    run_exception_tests("TEST: WA (masked): invalid args", testdata)


def test_WD_masked_args_range():
    testdata = [
        [WordDifferenceMasked, 1, 0, 0o4075],
        [WordDifferenceMasked, 0, 31, 0o3775],
        [WordDifferenceMasked, 1, 31, 0o7775]
    ]
    run_tests("TEST: WA (masked): args range", testdata)


def test_WD_unmasked_simple():
    testdata = [[WordDifferenceUnmasked, 0, 0, 0, 0, 0o2035]]
    run_tests("TEST: WA (unmasked): simple", testdata)


def test_WD_unmasked_invalid_args():
    testdata = [
        [WordDifferenceUnmasked, 2, 0, 0, 0, 0],
        [WordDifferenceUnmasked, 0, 2, 0, 0, 0],
        [WordDifferenceUnmasked, 0, 1, 2, 3, 0]
    ]
    run_exception_tests("TEST: WA (unmasked): invalid args", testdata)


def test_WD_unmasked_args_range():
    testdata = [
        [WordDifferenceUnmasked, 0, 0, 0, 0, 0o2035],
        [WordDifferenceUnmasked, 0, 0, 0, 1, 0o2135],
        [WordDifferenceUnmasked, 0, 0, 1, 0, 0o2235],
        [WordDifferenceUnmasked, 0, 0, 1, 1, 0o2335],
        [WordDifferenceUnmasked, 0, 1, 0, 0, 0o2435],
        [WordDifferenceUnmasked, 0, 1, 0, 1, 0o2535],
        [WordDifferenceUnmasked, 0, 1, 1, 0, 0o2635],
        [WordDifferenceUnmasked, 0, 1, 1, 1, 0o2735],
        [WordDifferenceUnmasked, 1, 0, 0, 0, 0o6035],
        [WordDifferenceUnmasked, 1, 0, 0, 1, 0o6135],
        [WordDifferenceUnmasked, 1, 0, 1, 0, 0o6235],
        [WordDifferenceUnmasked, 1, 0, 1, 1, 0o6335],
        [WordDifferenceUnmasked, 1, 1, 0, 0, 0o6435],
        [WordDifferenceUnmasked, 1, 1, 0, 1, 0o6535],
        [WordDifferenceUnmasked, 1, 1, 1, 0, 0o6635],
        [WordDifferenceUnmasked, 1, 1, 1, 1, 0o6735]
    ]
    run_tests("TEST: WA (unmasked): args range", testdata)
