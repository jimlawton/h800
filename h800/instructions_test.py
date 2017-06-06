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


# ######## NA ########

def test_NA_masked_simple():
    testdata = [[NotEqualAlphabeticMasked, 0, 0, 0o54]]
    run_tests("TEST: NA (masked): simple", testdata)


def test_NA_masked_invalid_args():
    testdata = [
        [NotEqualAlphabeticMasked, 0, 32, 0],
        [NotEqualAlphabeticMasked, 2, 0, 0]
    ]
    run_exception_tests("TEST: NA (masked): invalid args", testdata)


def test_NA_masked_args_range():
    testdata = [
        [NotEqualAlphabeticMasked, 1, 0, 0o4054],
        [NotEqualAlphabeticMasked, 0, 31, 0o3754],
        [NotEqualAlphabeticMasked, 1, 31, 0o7754]
    ]
    run_tests("TEST: NA (masked): args range", testdata)


def test_NA_unmasked_simple():
    testdata = [[NotEqualAlphabeticUnmasked, 0, 0, 0, 0, 0o2014]]
    run_tests("TEST: NA (unmasked): simple", testdata)


def test_NA_unmasked_invalid_args():
    testdata = [
        [NotEqualAlphabeticUnmasked, 2, 0, 0, 0, 0],
        [NotEqualAlphabeticUnmasked, 0, 2, 0, 0, 0],
        [NotEqualAlphabeticUnmasked, 0, 1, 2, 3, 0]
    ]
    run_exception_tests("TEST: NA (unmasked): invalid args", testdata)


def test_NA_unmasked_args_range():
    testdata = [
        [NotEqualAlphabeticUnmasked, 0, 0, 0, 0, 0o2014],
        [NotEqualAlphabeticUnmasked, 0, 0, 0, 1, 0o2114],
        [NotEqualAlphabeticUnmasked, 0, 0, 1, 0, 0o2214],
        [NotEqualAlphabeticUnmasked, 0, 0, 1, 1, 0o2314],
        [NotEqualAlphabeticUnmasked, 0, 1, 0, 0, 0o2414],
        [NotEqualAlphabeticUnmasked, 0, 1, 0, 1, 0o2514],
        [NotEqualAlphabeticUnmasked, 0, 1, 1, 0, 0o2614],
        [NotEqualAlphabeticUnmasked, 0, 1, 1, 1, 0o2714],
        [NotEqualAlphabeticUnmasked, 1, 0, 0, 0, 0o6014],
        [NotEqualAlphabeticUnmasked, 1, 0, 0, 1, 0o6114],
        [NotEqualAlphabeticUnmasked, 1, 0, 1, 0, 0o6214],
        [NotEqualAlphabeticUnmasked, 1, 0, 1, 1, 0o6314],
        [NotEqualAlphabeticUnmasked, 1, 1, 0, 0, 0o6414],
        [NotEqualAlphabeticUnmasked, 1, 1, 0, 1, 0o6514],
        [NotEqualAlphabeticUnmasked, 1, 1, 1, 0, 0o6614],
        [NotEqualAlphabeticUnmasked, 1, 1, 1, 1, 0o6714]
    ]
    run_tests("TEST: NA (unmasked): args range", testdata)


# ######## NN ########

def test_NN_masked_simple():
    testdata = [[NotEqualNumericMasked, 0, 0, 0o50]]
    run_tests("TEST: NN (masked): simple", testdata)


def test_NN_masked_invalid_args():
    testdata = [
        [NotEqualNumericMasked, 0, 32, 0],
        [NotEqualNumericMasked, 2, 0, 0]
    ]
    run_exception_tests("TEST: NN (masked): invalid args", testdata)


def test_NN_masked_args_range():
    testdata = [
        [NotEqualNumericMasked, 1, 0, 0o4050],
        [NotEqualNumericMasked, 0, 31, 0o3750],
        [NotEqualNumericMasked, 1, 31, 0o7750]
    ]
    run_tests("TEST: NN (masked): args range", testdata)


def test_NN_unmasked_simple():
    testdata = [[NotEqualNumericUnmasked, 0, 0, 0, 0, 0o2010]]
    run_tests("TEST: NN (unmasked): simple", testdata)


def test_NN_unmasked_invalid_args():
    testdata = [
        [NotEqualNumericUnmasked, 2, 0, 0, 0, 0],
        [NotEqualNumericUnmasked, 0, 2, 0, 0, 0],
        [NotEqualNumericUnmasked, 0, 1, 2, 3, 0]
    ]
    run_exception_tests("TEST: NN (unmasked): invalid args", testdata)


def test_NN_unmasked_args_range():
    testdata = [
        [NotEqualNumericUnmasked, 0, 0, 0, 0, 0o2010],
        [NotEqualNumericUnmasked, 0, 0, 0, 1, 0o2110],
        [NotEqualNumericUnmasked, 0, 0, 1, 0, 0o2210],
        [NotEqualNumericUnmasked, 0, 0, 1, 1, 0o2310],
        [NotEqualNumericUnmasked, 0, 1, 0, 0, 0o2410],
        [NotEqualNumericUnmasked, 0, 1, 0, 1, 0o2510],
        [NotEqualNumericUnmasked, 0, 1, 1, 0, 0o2610],
        [NotEqualNumericUnmasked, 0, 1, 1, 1, 0o2710],
        [NotEqualNumericUnmasked, 1, 0, 0, 0, 0o6010],
        [NotEqualNumericUnmasked, 1, 0, 0, 1, 0o6110],
        [NotEqualNumericUnmasked, 1, 0, 1, 0, 0o6210],
        [NotEqualNumericUnmasked, 1, 0, 1, 1, 0o6310],
        [NotEqualNumericUnmasked, 1, 1, 0, 0, 0o6410],
        [NotEqualNumericUnmasked, 1, 1, 0, 1, 0o6510],
        [NotEqualNumericUnmasked, 1, 1, 1, 0, 0o6610],
        [NotEqualNumericUnmasked, 1, 1, 1, 1, 0o6710]
    ]
    run_tests("TEST: NN (unmasked): args range", testdata)


# ######## LA ########

def test_LA_masked_simple():
    testdata = [[LessThanOrEqualAlphabeticMasked, 0, 0, 0o74]]
    run_tests("TEST: LA (masked): simple", testdata)


def test_LA_masked_invalid_args():
    testdata = [
        [LessThanOrEqualAlphabeticMasked, 0, 32, 0],
        [LessThanOrEqualAlphabeticMasked, 2, 0, 0]
    ]
    run_exception_tests("TEST: LA (masked): invalid args", testdata)


def test_LA_masked_args_range():
    testdata = [
        [LessThanOrEqualAlphabeticMasked, 1, 0, 0o4074],
        [LessThanOrEqualAlphabeticMasked, 0, 31, 0o3774],
        [LessThanOrEqualAlphabeticMasked, 1, 31, 0o7774]
    ]
    run_tests("TEST: LA (masked): args range", testdata)


def test_LA_unmasked_simple():
    testdata = [[LessThanOrEqualAlphabeticUnmasked, 0, 0, 0, 0, 0o2034]]
    run_tests("TEST: LA (unmasked): simple", testdata)


def test_LA_unmasked_invalid_args():
    testdata = [
        [LessThanOrEqualAlphabeticUnmasked, 2, 0, 0, 0, 0],
        [LessThanOrEqualAlphabeticUnmasked, 0, 2, 0, 0, 0],
        [LessThanOrEqualAlphabeticUnmasked, 0, 1, 2, 3, 0]
    ]
    run_exception_tests("TEST: LA (unmasked): invalid args", testdata)


def test_LA_unmasked_args_range():
    testdata = [
        [LessThanOrEqualAlphabeticUnmasked, 0, 0, 0, 0, 0o2034],
        [LessThanOrEqualAlphabeticUnmasked, 0, 0, 0, 1, 0o2134],
        [LessThanOrEqualAlphabeticUnmasked, 0, 0, 1, 0, 0o2234],
        [LessThanOrEqualAlphabeticUnmasked, 0, 0, 1, 1, 0o2334],
        [LessThanOrEqualAlphabeticUnmasked, 0, 1, 0, 0, 0o2434],
        [LessThanOrEqualAlphabeticUnmasked, 0, 1, 0, 1, 0o2534],
        [LessThanOrEqualAlphabeticUnmasked, 0, 1, 1, 0, 0o2634],
        [LessThanOrEqualAlphabeticUnmasked, 0, 1, 1, 1, 0o2734],
        [LessThanOrEqualAlphabeticUnmasked, 1, 0, 0, 0, 0o6034],
        [LessThanOrEqualAlphabeticUnmasked, 1, 0, 0, 1, 0o6134],
        [LessThanOrEqualAlphabeticUnmasked, 1, 0, 1, 0, 0o6234],
        [LessThanOrEqualAlphabeticUnmasked, 1, 0, 1, 1, 0o6334],
        [LessThanOrEqualAlphabeticUnmasked, 1, 1, 0, 0, 0o6434],
        [LessThanOrEqualAlphabeticUnmasked, 1, 1, 0, 1, 0o6534],
        [LessThanOrEqualAlphabeticUnmasked, 1, 1, 1, 0, 0o6634],
        [LessThanOrEqualAlphabeticUnmasked, 1, 1, 1, 1, 0o6734]
    ]
    run_tests("TEST: LA (unmasked): args range", testdata)


# ######## LN ########

def test_LN_masked_simple():
    testdata = [[LessThanOrEqualNumericMasked, 0, 0, 0o70]]
    run_tests("TEST: LN (masked): simple", testdata)


def test_LN_masked_invalid_args():
    testdata = [
        [LessThanOrEqualNumericMasked, 0, 32, 0],
        [LessThanOrEqualNumericMasked, 2, 0, 0]
    ]
    run_exception_tests("TEST: LN (masked): invalid args", testdata)


def test_LN_masked_args_range():
    testdata = [
        [LessThanOrEqualNumericMasked, 1, 0, 0o4070],
        [LessThanOrEqualNumericMasked, 0, 31, 0o3770],
        [LessThanOrEqualNumericMasked, 1, 31, 0o7770]
    ]
    run_tests("TEST: LN (masked): args range", testdata)


def test_LN_unmasked_simple():
    testdata = [[LessThanOrEqualNumericUnmasked, 0, 0, 0, 0, 0o2030]]
    run_tests("TEST: LN (unmasked): simple", testdata)


def test_LN_unmasked_invalid_args():
    testdata = [
        [LessThanOrEqualNumericUnmasked, 2, 0, 0, 0, 0],
        [LessThanOrEqualNumericUnmasked, 0, 2, 0, 0, 0],
        [LessThanOrEqualNumericUnmasked, 0, 1, 2, 3, 0]
    ]
    run_exception_tests("TEST: LN (unmasked): invalid args", testdata)


def test_LN_unmasked_args_range():
    testdata = [
        [LessThanOrEqualNumericUnmasked, 0, 0, 0, 0, 0o2030],
        [LessThanOrEqualNumericUnmasked, 0, 0, 0, 1, 0o2130],
        [LessThanOrEqualNumericUnmasked, 0, 0, 1, 0, 0o2230],
        [LessThanOrEqualNumericUnmasked, 0, 0, 1, 1, 0o2330],
        [LessThanOrEqualNumericUnmasked, 0, 1, 0, 0, 0o2430],
        [LessThanOrEqualNumericUnmasked, 0, 1, 0, 1, 0o2530],
        [LessThanOrEqualNumericUnmasked, 0, 1, 1, 0, 0o2630],
        [LessThanOrEqualNumericUnmasked, 0, 1, 1, 1, 0o2730],
        [LessThanOrEqualNumericUnmasked, 1, 0, 0, 0, 0o6030],
        [LessThanOrEqualNumericUnmasked, 1, 0, 0, 1, 0o6130],
        [LessThanOrEqualNumericUnmasked, 1, 0, 1, 0, 0o6230],
        [LessThanOrEqualNumericUnmasked, 1, 0, 1, 1, 0o6330],
        [LessThanOrEqualNumericUnmasked, 1, 1, 0, 0, 0o6430],
        [LessThanOrEqualNumericUnmasked, 1, 1, 0, 1, 0o6530],
        [LessThanOrEqualNumericUnmasked, 1, 1, 1, 0, 0o6630],
        [LessThanOrEqualNumericUnmasked, 1, 1, 1, 1, 0o6730]
    ]
    run_tests("TEST: LN (unmasked): args range", testdata)


# ######## TX ########

def test_TX_masked_simple():
    testdata = [[TransferMasked, 0, 0, 0o60]]
    run_tests("TEST: TX (masked): simple", testdata)


def test_TX_masked_invalid_args():
    testdata = [
        [TransferMasked, 0, 32, 0],
        [TransferMasked, 2, 0, 0]
    ]
    run_exception_tests("TEST: TX (masked): invalid args", testdata)


def test_TX_masked_args_range():
    testdata = [
        [TransferMasked, 1, 0, 0o4060],
        [TransferMasked, 0, 31, 0o3760],
        [TransferMasked, 1, 31, 0o7760]
    ]
    run_tests("TEST: TX (masked): args range", testdata)


def test_TX_unmasked_simple():
    testdata = [[TransferUnmasked, 0, 0, 0, 0, 0o2020]]
    run_tests("TEST: TX (unmasked): simple", testdata)


def test_TX_unmasked_invalid_args():
    testdata = [
        [TransferUnmasked, 2, 0, 0, 0, 0],
        [TransferUnmasked, 0, 2, 0, 0, 0],
        [TransferUnmasked, 0, 1, 2, 3, 0]
    ]
    run_exception_tests("TEST: TX (unmasked): invalid args", testdata)


def test_TX_unmasked_args_range():
    testdata = [
        [TransferUnmasked, 0, 0, 0, 0, 0o2020],
        [TransferUnmasked, 0, 0, 0, 1, 0o2120],
        [TransferUnmasked, 0, 0, 1, 0, 0o2220],
        [TransferUnmasked, 0, 0, 1, 1, 0o2320],
        [TransferUnmasked, 0, 1, 0, 0, 0o2420],
        [TransferUnmasked, 0, 1, 0, 1, 0o2520],
        [TransferUnmasked, 0, 1, 1, 0, 0o2620],
        [TransferUnmasked, 0, 1, 1, 1, 0o2720],
        [TransferUnmasked, 1, 0, 0, 0, 0o6020],
        [TransferUnmasked, 1, 0, 0, 1, 0o6120],
        [TransferUnmasked, 1, 0, 1, 0, 0o6220],
        [TransferUnmasked, 1, 0, 1, 1, 0o6320],
        [TransferUnmasked, 1, 1, 0, 0, 0o6420],
        [TransferUnmasked, 1, 1, 0, 1, 0o6520],
        [TransferUnmasked, 1, 1, 1, 0, 0o6620],
        [TransferUnmasked, 1, 1, 1, 1, 0o6720]
    ]
    run_tests("TEST: TX (unmasked): args range", testdata)


# ######## TS ########

def test_TS_masked_simple():
    testdata = [[TransferChangeSequenceMasked, 0, 0, 0o44]]
    run_tests("TEST: TS (masked): simple", testdata)


def test_TS_masked_invalid_args():
    testdata = [
        [TransferChangeSequenceMasked, 0, 32, 0],
        [TransferChangeSequenceMasked, 2, 0, 0]
    ]
    run_exception_tests("TEST: TS (masked): invalid args", testdata)


def test_TS_masked_args_range():
    testdata = [
        [TransferChangeSequenceMasked, 1, 0, 0o4044],
        [TransferChangeSequenceMasked, 0, 31, 0o3744],
        [TransferChangeSequenceMasked, 1, 31, 0o7744]
    ]
    run_tests("TEST: TS (masked): args range", testdata)


def test_TS_unmasked_simple():
    testdata = [[TransferChangeSequenceUnmasked, 0, 0, 0, 0, 0o2004]]
    run_tests("TEST: TS (unmasked): simple", testdata)


def test_TS_unmasked_invalid_args():
    testdata = [
        [TransferChangeSequenceUnmasked, 2, 0, 0, 0, 0],
        [TransferChangeSequenceUnmasked, 0, 2, 0, 0, 0],
        [TransferChangeSequenceUnmasked, 0, 1, 2, 3, 0]
    ]
    run_exception_tests("TEST: TS (unmasked): invalid args", testdata)


def test_TS_unmasked_args_range():
    testdata = [
        [TransferChangeSequenceUnmasked, 0, 0, 0, 0, 0o2004],
        [TransferChangeSequenceUnmasked, 0, 0, 0, 1, 0o2104],
        [TransferChangeSequenceUnmasked, 0, 0, 1, 0, 0o2204],
        [TransferChangeSequenceUnmasked, 0, 0, 1, 1, 0o2304],
        [TransferChangeSequenceUnmasked, 0, 1, 0, 0, 0o2404],
        [TransferChangeSequenceUnmasked, 0, 1, 0, 1, 0o2504],
        [TransferChangeSequenceUnmasked, 0, 1, 1, 0, 0o2604],
        [TransferChangeSequenceUnmasked, 0, 1, 1, 1, 0o2704],
        [TransferChangeSequenceUnmasked, 1, 0, 0, 0, 0o6004],
        [TransferChangeSequenceUnmasked, 1, 0, 0, 1, 0o6104],
        [TransferChangeSequenceUnmasked, 1, 0, 1, 0, 0o6204],
        [TransferChangeSequenceUnmasked, 1, 0, 1, 1, 0o6304],
        [TransferChangeSequenceUnmasked, 1, 1, 0, 0, 0o6404],
        [TransferChangeSequenceUnmasked, 1, 1, 0, 1, 0o6504],
        [TransferChangeSequenceUnmasked, 1, 1, 1, 0, 0o6604],
        [TransferChangeSequenceUnmasked, 1, 1, 1, 1, 0o6704]
    ]
    run_tests("TEST: TS (unmasked): args range", testdata)


# ######## HA ########

def test_HA_masked_simple():
    testdata = [[HalfAddMasked, 0, 0, 0o65]]
    run_tests("TEST: HA (masked): simple", testdata)


def test_HA_masked_invalid_args():
    testdata = [
        [HalfAddMasked, 0, 32, 0],
        [HalfAddMasked, 2, 0, 0]
    ]
    run_exception_tests("TEST: HA (masked): invalid args", testdata)


def test_HA_masked_args_range():
    testdata = [
        [HalfAddMasked, 1, 0, 0o4065],
        [HalfAddMasked, 0, 31, 0o3765],
        [HalfAddMasked, 1, 31, 0o7765]
    ]
    run_tests("TEST: HA (masked): args range", testdata)


def test_HA_unmasked_simple():
    testdata = [[HalfAddUnmasked, 0, 0, 0, 0, 0o2025]]
    run_tests("TEST: HA (unmasked): simple", testdata)


def test_HA_unmasked_invalid_args():
    testdata = [
        [HalfAddUnmasked, 2, 0, 0, 0, 0],
        [HalfAddUnmasked, 0, 2, 0, 0, 0],
        [HalfAddUnmasked, 0, 1, 2, 3, 0]
    ]
    run_exception_tests("TEST: HA (unmasked): invalid args", testdata)


def test_HA_unmasked_args_range():
    testdata = [
        [HalfAddUnmasked, 0, 0, 0, 0, 0o2025],
        [HalfAddUnmasked, 0, 0, 0, 1, 0o2125],
        [HalfAddUnmasked, 0, 0, 1, 0, 0o2225],
        [HalfAddUnmasked, 0, 0, 1, 1, 0o2325],
        [HalfAddUnmasked, 0, 1, 0, 0, 0o2425],
        [HalfAddUnmasked, 0, 1, 0, 1, 0o2525],
        [HalfAddUnmasked, 0, 1, 1, 0, 0o2625],
        [HalfAddUnmasked, 0, 1, 1, 1, 0o2725],
        [HalfAddUnmasked, 1, 0, 0, 0, 0o6025],
        [HalfAddUnmasked, 1, 0, 0, 1, 0o6125],
        [HalfAddUnmasked, 1, 0, 1, 0, 0o6225],
        [HalfAddUnmasked, 1, 0, 1, 1, 0o6325],
        [HalfAddUnmasked, 1, 1, 0, 0, 0o6425],
        [HalfAddUnmasked, 1, 1, 0, 1, 0o6525],
        [HalfAddUnmasked, 1, 1, 1, 0, 0o6625],
        [HalfAddUnmasked, 1, 1, 1, 1, 0o6725]
    ]
    run_tests("TEST: HA (unmasked): args range", testdata)


