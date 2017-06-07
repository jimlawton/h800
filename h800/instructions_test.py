#!/usr/bin/env python

from h800.instructions import *


def my_assert(value, good):
    assert value == good, "Value is 0o%o, should be 0o%o" % (value, good)


def run_test(testdata):
    print testdata
    if len(testdata[1]) == 4:
        # Unmasked instructions.
        i = testdata[0](sequence=testdata[1][0], a=testdata[1][1], b=testdata[1][2], c=testdata[1][3])
    elif len(testdata[1]) == 3:
        assert False, "Illegal argument length!"
    elif len(testdata[1]) == 2:
        # Masked instructions.
        i = testdata[0](sequence=testdata[1][0], mask=testdata[1][1])
    elif len(testdata[1]) == 1:
        # Peripheral or misc instructions, or constant.
        if testdata[0].__name__.endswith("Constant"):
            # Constants.
            i = testdata[0](data=testdata[1][0])
        elif testdata[0].__name__ == "Simulator":
            i = testdata[0](sequence=testdata[1][0])
        else:
            i = testdata[0](paddr=testdata[1][0])
    elif len(testdata[1]) == 0:
        # Instructions with no args, e.g. Proceed.
        i = testdata[0]()
    else:
        assert False, "Illegal argument length!"
    my_assert(i.value, testdata[2])


def run_tests(message, testdata):
    print message
    for t in testdata:
        run_test(t)


def run_exception_tests(message, testdata):
    print message
    for t in testdata:
        gotexc = False
        try:
            run_test(t)
        except ValueError:
            gotexc = True
        else:
            raise
        assert gotexc == True, "Invalid value should have thrown an exception!"


# ######## BA ########

def test_BA_masked_simple():
    testdata = [[BinaryAddMasked, [0, 0], 0o51]]
    run_tests("TEST: BA (masked): simple", testdata)


def test_BA_masked_invalid_args():
    testdata = [
        [BinaryAddMasked, [0, 32], 0],
        [BinaryAddMasked, [2, 0], 0]
    ]
    run_exception_tests("TEST: BA (masked): invalid args", testdata)


def test_BA_masked_args_range():
    testdata = [
        [BinaryAddMasked, [1, 0], 0o4051],
        [BinaryAddMasked, [0, 31], 0o3751],
        [BinaryAddMasked, [1, 31], 0o7751]
    ]
    run_tests("TEST: BA (masked): args range", testdata)


def test_BA_unmasked_simple():
    testdata = [[BinaryAddUnmasked, [0, 0, 0, 0], 0o2011]]
    run_tests("TEST: BA (unmasked): simple", testdata)


def test_BA_unmasked_invalid_args():
    testdata = [
        [BinaryAddUnmasked, [2, 0, 0, 0], 0],
        [BinaryAddUnmasked, [0, 2, 0, 0], 0],
        [BinaryAddUnmasked, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: BA (unmasked): invalid args", testdata)


def test_BA_unmasked_args_range():
    testdata = [
        [BinaryAddUnmasked, [0, 0, 0, 0], 0o2011],
        [BinaryAddUnmasked, [0, 0, 0, 1], 0o2111],
        [BinaryAddUnmasked, [0, 0, 1, 0], 0o2211],
        [BinaryAddUnmasked, [0, 0, 1, 1], 0o2311],
        [BinaryAddUnmasked, [0, 1, 0, 0], 0o2411],
        [BinaryAddUnmasked, [0, 1, 0, 1], 0o2511],
        [BinaryAddUnmasked, [0, 1, 1, 0], 0o2611],
        [BinaryAddUnmasked, [0, 1, 1, 1], 0o2711],
        [BinaryAddUnmasked, [1, 0, 0, 0], 0o6011],
        [BinaryAddUnmasked, [1, 0, 0, 1], 0o6111],
        [BinaryAddUnmasked, [1, 0, 1, 0], 0o6211],
        [BinaryAddUnmasked, [1, 0, 1, 1], 0o6311],
        [BinaryAddUnmasked, [1, 1, 0, 0], 0o6411],
        [BinaryAddUnmasked, [1, 1, 0, 1], 0o6511],
        [BinaryAddUnmasked, [1, 1, 1, 0], 0o6611],
        [BinaryAddUnmasked, [1, 1, 1, 1], 0o6711]
    ]
    run_tests("TEST: BA (unmasked): args range", testdata)


# ######## DA ########

def test_DA_masked_simple():
    testdata = [[DecimalAddMasked, [0, 0], 0o41]]
    run_tests("TEST: DA (masked): simple", testdata)


def test_DA_masked_invalid_args():
    testdata = [
        [DecimalAddMasked, [0, 32], 0],
        [DecimalAddMasked, [2, 0], 0]
    ]
    run_exception_tests("TEST: DA (masked): invalid args", testdata)


def test_DA_masked_args_range():
    testdata = [
        [DecimalAddMasked, [1, 0], 0o4041],
        [DecimalAddMasked, [0, 31], 0o3741],
        [DecimalAddMasked, [1, 31], 0o7741]
    ]
    run_tests("TEST: DA (masked): args range", testdata)


def test_DA_unmasked_simple():
    testdata = [[DecimalAddUnmasked, [0, 0, 0, 0], 0o2001]]
    run_tests("TEST: DA (unmasked): simple", testdata)


def test_DA_unmasked_invalid_args():
    testdata = [
        [DecimalAddUnmasked, [2, 0, 0, 0], 0],
        [DecimalAddUnmasked, [0, 2, 0, 0], 0],
        [DecimalAddUnmasked, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: DA (unmasked): invalid args", testdata)


def test_DA_unmasked_args_range():
    testdata = [
        [DecimalAddUnmasked, [0, 0, 0, 0], 0o2001],
        [DecimalAddUnmasked, [0, 0, 0, 1], 0o2101],
        [DecimalAddUnmasked, [0, 0, 1, 0], 0o2201],
        [DecimalAddUnmasked, [0, 0, 1, 1], 0o2301],
        [DecimalAddUnmasked, [0, 1, 0, 0], 0o2401],
        [DecimalAddUnmasked, [0, 1, 0, 1], 0o2501],
        [DecimalAddUnmasked, [0, 1, 1, 0], 0o2601],
        [DecimalAddUnmasked, [0, 1, 1, 1], 0o2701],
        [DecimalAddUnmasked, [1, 0, 0, 0], 0o6001],
        [DecimalAddUnmasked, [1, 0, 0, 1], 0o6101],
        [DecimalAddUnmasked, [1, 0, 1, 0], 0o6201],
        [DecimalAddUnmasked, [1, 0, 1, 1], 0o6301],
        [DecimalAddUnmasked, [1, 1, 0, 0], 0o6401],
        [DecimalAddUnmasked, [1, 1, 0, 1], 0o6501],
        [DecimalAddUnmasked, [1, 1, 1, 0], 0o6601],
        [DecimalAddUnmasked, [1, 1, 1, 1], 0o6701]
    ]
    run_tests("TEST: DA (unmasked): args range", testdata)


# ######## WA ########

def test_WA_masked_simple():
    testdata = [[WordAddMasked, [0, 0], 0o55]]
    run_tests("TEST: WA (masked): simple", testdata)


def test_WA_masked_invalid_args():
    testdata = [
        [WordAddMasked, [0, 32], 0],
        [WordAddMasked, [2, 0], 0]
    ]
    run_exception_tests("TEST: WA (masked): invalid args", testdata)


def test_WA_masked_args_range():
    testdata = [
        [WordAddMasked, [1, 0], 0o4055],
        [WordAddMasked, [0, 31], 0o3755],
        [WordAddMasked, [1, 31], 0o7755]
    ]
    run_tests("TEST: WA (masked): args range", testdata)


def test_WA_unmasked_simple():
    testdata = [[WordAddUnmasked, [0, 0, 0, 0], 0o2015]]
    run_tests("TEST: WA (unmasked): simple", testdata)


def test_WA_unmasked_invalid_args():
    testdata = [
        [WordAddUnmasked, [2, 0, 0, 0], 0],
        [WordAddUnmasked, [0, 2, 0, 0], 0],
        [WordAddUnmasked, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: WA (unmasked): invalid args", testdata)


def test_WA_unmasked_args_range():
    testdata = [
        [WordAddUnmasked, [0, 0, 0, 0], 0o2015],
        [WordAddUnmasked, [0, 0, 0, 1], 0o2115],
        [WordAddUnmasked, [0, 0, 1, 0], 0o2215],
        [WordAddUnmasked, [0, 0, 1, 1], 0o2315],
        [WordAddUnmasked, [0, 1, 0, 0], 0o2415],
        [WordAddUnmasked, [0, 1, 0, 1], 0o2515],
        [WordAddUnmasked, [0, 1, 1, 0], 0o2615],
        [WordAddUnmasked, [0, 1, 1, 1], 0o2715],
        [WordAddUnmasked, [1, 0, 0, 0], 0o6015],
        [WordAddUnmasked, [1, 0, 0, 1], 0o6115],
        [WordAddUnmasked, [1, 0, 1, 0], 0o6215],
        [WordAddUnmasked, [1, 0, 1, 1], 0o6315],
        [WordAddUnmasked, [1, 1, 0, 0], 0o6415],
        [WordAddUnmasked, [1, 1, 0, 1], 0o6515],
        [WordAddUnmasked, [1, 1, 1, 0], 0o6615],
        [WordAddUnmasked, [1, 1, 1, 1], 0o6715]
    ]
    run_tests("TEST: WA (unmasked): args range", testdata)


# ######## BS ########

def test_BS_masked_simple():
    testdata = [[BinarySubtractMasked, [0, 0], 0o71]]
    run_tests("TEST: BA (masked): simple", testdata)


def test_BS_masked_invalid_args():
    testdata = [
        [BinarySubtractMasked, [0, 32], 0],
        [BinarySubtractMasked, [2, 0], 0]
    ]
    run_exception_tests("TEST: BA (masked): invalid args", testdata)


def test_BS_masked_args_range():
    testdata = [
        [BinarySubtractMasked, [1, 0], 0o4071],
        [BinarySubtractMasked, [0, 31], 0o3771],
        [BinarySubtractMasked, [1, 31], 0o7771]
    ]
    run_tests("TEST: BA (masked): args range", testdata)


def test_BS_unmasked_simple():
    testdata = [[BinarySubtractUnmasked, [0, 0, 0, 0], 0o2031]]
    run_tests("TEST: BA (unmasked): simple", testdata)


def test_BS_unmasked_invalid_args():
    testdata = [
        [BinarySubtractUnmasked, [2, 0, 0, 0], 0],
        [BinarySubtractUnmasked, [0, 2, 0, 0], 0],
        [BinarySubtractUnmasked, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: BA (unmasked): invalid args", testdata)


def test_BS_unmasked_args_range():
    testdata = [
        [BinarySubtractUnmasked, [0, 0, 0, 0], 0o2031],
        [BinarySubtractUnmasked, [0, 0, 0, 1], 0o2131],
        [BinarySubtractUnmasked, [0, 0, 1, 0], 0o2231],
        [BinarySubtractUnmasked, [0, 0, 1, 1], 0o2331],
        [BinarySubtractUnmasked, [0, 1, 0, 0], 0o2431],
        [BinarySubtractUnmasked, [0, 1, 0, 1], 0o2531],
        [BinarySubtractUnmasked, [0, 1, 1, 0], 0o2631],
        [BinarySubtractUnmasked, [0, 1, 1, 1], 0o2731],
        [BinarySubtractUnmasked, [1, 0, 0, 0], 0o6031],
        [BinarySubtractUnmasked, [1, 0, 0, 1], 0o6131],
        [BinarySubtractUnmasked, [1, 0, 1, 0], 0o6231],
        [BinarySubtractUnmasked, [1, 0, 1, 1], 0o6331],
        [BinarySubtractUnmasked, [1, 1, 0, 0], 0o6431],
        [BinarySubtractUnmasked, [1, 1, 0, 1], 0o6531],
        [BinarySubtractUnmasked, [1, 1, 1, 0], 0o6631],
        [BinarySubtractUnmasked, [1, 1, 1, 1], 0o6731]
    ]
    run_tests("TEST: BA (unmasked): args range", testdata)


# ######## DS ########

def test_DS_masked_simple():
    testdata = [[DecimalSubtractMasked, [0, 0], 0o61]]
    run_tests("TEST: DA (masked): simple", testdata)


def test_DS_masked_invalid_args():
    testdata = [
        [DecimalSubtractMasked, [0, 32], 0],
        [DecimalSubtractMasked, [2, 0], 0]
    ]
    run_exception_tests("TEST: DA (masked): invalid args", testdata)


def test_DS_masked_args_range():
    testdata = [
        [DecimalSubtractMasked, [1, 0], 0o4061],
        [DecimalSubtractMasked, [0, 31], 0o3761],
        [DecimalSubtractMasked, [1, 31], 0o7761]
    ]
    run_tests("TEST: DA (masked): args range", testdata)


def test_DS_unmasked_simple():
    testdata = [[DecimalSubtractUnmasked, [0, 0, 0, 0], 0o2021]]
    run_tests("TEST: DA (unmasked): simple", testdata)


def test_DS_unmasked_invalid_args():
    testdata = [
        [DecimalSubtractUnmasked, [2, 0, 0, 0], 0],
        [DecimalSubtractUnmasked, [0, 2, 0, 0], 0],
        [DecimalSubtractUnmasked, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: DA (unmasked): invalid args", testdata)


def test_DS_unmasked_args_range():
    testdata = [
        [DecimalSubtractUnmasked, [0, 0, 0, 0], 0o2021],
        [DecimalSubtractUnmasked, [0, 0, 0, 1], 0o2121],
        [DecimalSubtractUnmasked, [0, 0, 1, 0], 0o2221],
        [DecimalSubtractUnmasked, [0, 0, 1, 1], 0o2321],
        [DecimalSubtractUnmasked, [0, 1, 0, 0], 0o2421],
        [DecimalSubtractUnmasked, [0, 1, 0, 1], 0o2521],
        [DecimalSubtractUnmasked, [0, 1, 1, 0], 0o2621],
        [DecimalSubtractUnmasked, [0, 1, 1, 1], 0o2721],
        [DecimalSubtractUnmasked, [1, 0, 0, 0], 0o6021],
        [DecimalSubtractUnmasked, [1, 0, 0, 1], 0o6121],
        [DecimalSubtractUnmasked, [1, 0, 1, 0], 0o6221],
        [DecimalSubtractUnmasked, [1, 0, 1, 1], 0o6321],
        [DecimalSubtractUnmasked, [1, 1, 0, 0], 0o6421],
        [DecimalSubtractUnmasked, [1, 1, 0, 1], 0o6521],
        [DecimalSubtractUnmasked, [1, 1, 1, 0], 0o6621],
        [DecimalSubtractUnmasked, [1, 1, 1, 1], 0o6721]
    ]
    run_tests("TEST: DA (unmasked): args range", testdata)


# ######## WD ########

def test_WD_masked_simple():
    testdata = [[WordDifferenceMasked, [0, 0], 0o75]]
    run_tests("TEST: WA (masked): simple", testdata)


def test_WD_masked_invalid_args():
    testdata = [
        [WordDifferenceMasked, [0, 32], 0],
        [WordDifferenceMasked, [2, 0], 0]
    ]
    run_exception_tests("TEST: WA (masked): invalid args", testdata)


def test_WD_masked_args_range():
    testdata = [
        [WordDifferenceMasked, [1, 0], 0o4075],
        [WordDifferenceMasked, [0, 31], 0o3775],
        [WordDifferenceMasked, [1, 31], 0o7775]
    ]
    run_tests("TEST: WA (masked): args range", testdata)


def test_WD_unmasked_simple():
    testdata = [[WordDifferenceUnmasked, [0, 0, 0, 0], 0o2035]]
    run_tests("TEST: WA (unmasked): simple", testdata)


def test_WD_unmasked_invalid_args():
    testdata = [
        [WordDifferenceUnmasked, [2, 0, 0, 0], 0],
        [WordDifferenceUnmasked, [0, 2, 0, 0], 0],
        [WordDifferenceUnmasked, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: WA (unmasked): invalid args", testdata)


def test_WD_unmasked_args_range():
    testdata = [
        [WordDifferenceUnmasked, [0, 0, 0, 0], 0o2035],
        [WordDifferenceUnmasked, [0, 0, 0, 1], 0o2135],
        [WordDifferenceUnmasked, [0, 0, 1, 0], 0o2235],
        [WordDifferenceUnmasked, [0, 0, 1, 1], 0o2335],
        [WordDifferenceUnmasked, [0, 1, 0, 0], 0o2435],
        [WordDifferenceUnmasked, [0, 1, 0, 1], 0o2535],
        [WordDifferenceUnmasked, [0, 1, 1, 0], 0o2635],
        [WordDifferenceUnmasked, [0, 1, 1, 1], 0o2735],
        [WordDifferenceUnmasked, [1, 0, 0, 0], 0o6035],
        [WordDifferenceUnmasked, [1, 0, 0, 1], 0o6135],
        [WordDifferenceUnmasked, [1, 0, 1, 0], 0o6235],
        [WordDifferenceUnmasked, [1, 0, 1, 1], 0o6335],
        [WordDifferenceUnmasked, [1, 1, 0, 0], 0o6435],
        [WordDifferenceUnmasked, [1, 1, 0, 1], 0o6535],
        [WordDifferenceUnmasked, [1, 1, 1, 0], 0o6635],
        [WordDifferenceUnmasked, [1, 1, 1, 1], 0o6735]
    ]
    run_tests("TEST: WA (unmasked): args range", testdata)


# ######## NA ########

def test_NA_masked_simple():
    testdata = [[NotEqualAlphabeticMasked, [0, 0], 0o54]]
    run_tests("TEST: NA (masked): simple", testdata)


def test_NA_masked_invalid_args():
    testdata = [
        [NotEqualAlphabeticMasked, [0, 32], 0],
        [NotEqualAlphabeticMasked, [2, 0], 0]
    ]
    run_exception_tests("TEST: NA (masked): invalid args", testdata)


def test_NA_masked_args_range():
    testdata = [
        [NotEqualAlphabeticMasked, [1, 0], 0o4054],
        [NotEqualAlphabeticMasked, [0, 31], 0o3754],
        [NotEqualAlphabeticMasked, [1, 31], 0o7754]
    ]
    run_tests("TEST: NA (masked): args range", testdata)


def test_NA_unmasked_simple():
    testdata = [[NotEqualAlphabeticUnmasked, [0, 0, 0, 0], 0o2014]]
    run_tests("TEST: NA (unmasked): simple", testdata)


def test_NA_unmasked_invalid_args():
    testdata = [
        [NotEqualAlphabeticUnmasked, [2, 0, 0, 0], 0],
        [NotEqualAlphabeticUnmasked, [0, 2, 0, 0], 0],
        [NotEqualAlphabeticUnmasked, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: NA (unmasked): invalid args", testdata)


def test_NA_unmasked_args_range():
    testdata = [
        [NotEqualAlphabeticUnmasked, [0, 0, 0, 0], 0o2014],
        [NotEqualAlphabeticUnmasked, [0, 0, 0, 1], 0o2114],
        [NotEqualAlphabeticUnmasked, [0, 0, 1, 0], 0o2214],
        [NotEqualAlphabeticUnmasked, [0, 0, 1, 1], 0o2314],
        [NotEqualAlphabeticUnmasked, [0, 1, 0, 0], 0o2414],
        [NotEqualAlphabeticUnmasked, [0, 1, 0, 1], 0o2514],
        [NotEqualAlphabeticUnmasked, [0, 1, 1, 0], 0o2614],
        [NotEqualAlphabeticUnmasked, [0, 1, 1, 1], 0o2714],
        [NotEqualAlphabeticUnmasked, [1, 0, 0, 0], 0o6014],
        [NotEqualAlphabeticUnmasked, [1, 0, 0, 1], 0o6114],
        [NotEqualAlphabeticUnmasked, [1, 0, 1, 0], 0o6214],
        [NotEqualAlphabeticUnmasked, [1, 0, 1, 1], 0o6314],
        [NotEqualAlphabeticUnmasked, [1, 1, 0, 0], 0o6414],
        [NotEqualAlphabeticUnmasked, [1, 1, 0, 1], 0o6514],
        [NotEqualAlphabeticUnmasked, [1, 1, 1, 0], 0o6614],
        [NotEqualAlphabeticUnmasked, [1, 1, 1, 1], 0o6714]
    ]
    run_tests("TEST: NA (unmasked): args range", testdata)


# ######## NN ########

def test_NN_masked_simple():
    testdata = [[NotEqualNumericMasked, [0, 0], 0o50]]
    run_tests("TEST: NN (masked): simple", testdata)


def test_NN_masked_invalid_args():
    testdata = [
        [NotEqualNumericMasked, [0, 32], 0],
        [NotEqualNumericMasked, [2, 0], 0]
    ]
    run_exception_tests("TEST: NN (masked): invalid args", testdata)


def test_NN_masked_args_range():
    testdata = [
        [NotEqualNumericMasked, [1, 0], 0o4050],
        [NotEqualNumericMasked, [0, 31], 0o3750],
        [NotEqualNumericMasked, [1, 31], 0o7750]
    ]
    run_tests("TEST: NN (masked): args range", testdata)


def test_NN_unmasked_simple():
    testdata = [[NotEqualNumericUnmasked, [0, 0, 0, 0], 0o2010]]
    run_tests("TEST: NN (unmasked): simple", testdata)


def test_NN_unmasked_invalid_args():
    testdata = [
        [NotEqualNumericUnmasked, [2, 0, 0, 0], 0],
        [NotEqualNumericUnmasked, [0, 2, 0, 0], 0],
        [NotEqualNumericUnmasked, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: NN (unmasked): invalid args", testdata)


def test_NN_unmasked_args_range():
    testdata = [
        [NotEqualNumericUnmasked, [0, 0, 0, 0], 0o2010],
        [NotEqualNumericUnmasked, [0, 0, 0, 1], 0o2110],
        [NotEqualNumericUnmasked, [0, 0, 1, 0], 0o2210],
        [NotEqualNumericUnmasked, [0, 0, 1, 1], 0o2310],
        [NotEqualNumericUnmasked, [0, 1, 0, 0], 0o2410],
        [NotEqualNumericUnmasked, [0, 1, 0, 1], 0o2510],
        [NotEqualNumericUnmasked, [0, 1, 1, 0], 0o2610],
        [NotEqualNumericUnmasked, [0, 1, 1, 1], 0o2710],
        [NotEqualNumericUnmasked, [1, 0, 0, 0], 0o6010],
        [NotEqualNumericUnmasked, [1, 0, 0, 1], 0o6110],
        [NotEqualNumericUnmasked, [1, 0, 1, 0], 0o6210],
        [NotEqualNumericUnmasked, [1, 0, 1, 1], 0o6310],
        [NotEqualNumericUnmasked, [1, 1, 0, 0], 0o6410],
        [NotEqualNumericUnmasked, [1, 1, 0, 1], 0o6510],
        [NotEqualNumericUnmasked, [1, 1, 1, 0], 0o6610],
        [NotEqualNumericUnmasked, [1, 1, 1, 1], 0o6710]
    ]
    run_tests("TEST: NN (unmasked): args range", testdata)


# ######## LA ########

def test_LA_masked_simple():
    testdata = [[LessThanOrEqualAlphabeticMasked, [0, 0], 0o74]]
    run_tests("TEST: LA (masked): simple", testdata)


def test_LA_masked_invalid_args():
    testdata = [
        [LessThanOrEqualAlphabeticMasked, [0, 32], 0],
        [LessThanOrEqualAlphabeticMasked, [2, 0], 0]
    ]
    run_exception_tests("TEST: LA (masked): invalid args", testdata)


def test_LA_masked_args_range():
    testdata = [
        [LessThanOrEqualAlphabeticMasked, [1, 0], 0o4074],
        [LessThanOrEqualAlphabeticMasked, [0, 31], 0o3774],
        [LessThanOrEqualAlphabeticMasked, [1, 31], 0o7774]
    ]
    run_tests("TEST: LA (masked): args range", testdata)


def test_LA_unmasked_simple():
    testdata = [[LessThanOrEqualAlphabeticUnmasked, [0, 0, 0, 0], 0o2034]]
    run_tests("TEST: LA (unmasked): simple", testdata)


def test_LA_unmasked_invalid_args():
    testdata = [
        [LessThanOrEqualAlphabeticUnmasked, [2, 0, 0, 0], 0],
        [LessThanOrEqualAlphabeticUnmasked, [0, 2, 0, 0], 0],
        [LessThanOrEqualAlphabeticUnmasked, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: LA (unmasked): invalid args", testdata)


def test_LA_unmasked_args_range():
    testdata = [
        [LessThanOrEqualAlphabeticUnmasked, [0, 0, 0, 0], 0o2034],
        [LessThanOrEqualAlphabeticUnmasked, [0, 0, 0, 1], 0o2134],
        [LessThanOrEqualAlphabeticUnmasked, [0, 0, 1, 0], 0o2234],
        [LessThanOrEqualAlphabeticUnmasked, [0, 0, 1, 1], 0o2334],
        [LessThanOrEqualAlphabeticUnmasked, [0, 1, 0, 0], 0o2434],
        [LessThanOrEqualAlphabeticUnmasked, [0, 1, 0, 1], 0o2534],
        [LessThanOrEqualAlphabeticUnmasked, [0, 1, 1, 0], 0o2634],
        [LessThanOrEqualAlphabeticUnmasked, [0, 1, 1, 1], 0o2734],
        [LessThanOrEqualAlphabeticUnmasked, [1, 0, 0, 0], 0o6034],
        [LessThanOrEqualAlphabeticUnmasked, [1, 0, 0, 1], 0o6134],
        [LessThanOrEqualAlphabeticUnmasked, [1, 0, 1, 0], 0o6234],
        [LessThanOrEqualAlphabeticUnmasked, [1, 0, 1, 1], 0o6334],
        [LessThanOrEqualAlphabeticUnmasked, [1, 1, 0, 0], 0o6434],
        [LessThanOrEqualAlphabeticUnmasked, [1, 1, 0, 1], 0o6534],
        [LessThanOrEqualAlphabeticUnmasked, [1, 1, 1, 0], 0o6634],
        [LessThanOrEqualAlphabeticUnmasked, [1, 1, 1, 1], 0o6734]
    ]
    run_tests("TEST: LA (unmasked): args range", testdata)


# ######## LN ########

def test_LN_masked_simple():
    testdata = [[LessThanOrEqualNumericMasked, [0, 0], 0o70]]
    run_tests("TEST: LN (masked): simple", testdata)


def test_LN_masked_invalid_args():
    testdata = [
        [LessThanOrEqualNumericMasked, [0, 32], 0],
        [LessThanOrEqualNumericMasked, [2, 0], 0]
    ]
    run_exception_tests("TEST: LN (masked): invalid args", testdata)


def test_LN_masked_args_range():
    testdata = [
        [LessThanOrEqualNumericMasked, [1, 0], 0o4070],
        [LessThanOrEqualNumericMasked, [0, 31], 0o3770],
        [LessThanOrEqualNumericMasked, [1, 31], 0o7770]
    ]
    run_tests("TEST: LN (masked): args range", testdata)


def test_LN_unmasked_simple():
    testdata = [[LessThanOrEqualNumericUnmasked, [0, 0, 0, 0], 0o2030]]
    run_tests("TEST: LN (unmasked): simple", testdata)


def test_LN_unmasked_invalid_args():
    testdata = [
        [LessThanOrEqualNumericUnmasked, [2, 0, 0, 0], 0],
        [LessThanOrEqualNumericUnmasked, [0, 2, 0, 0], 0],
        [LessThanOrEqualNumericUnmasked, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: LN (unmasked): invalid args", testdata)


def test_LN_unmasked_args_range():
    testdata = [
        [LessThanOrEqualNumericUnmasked, [0, 0, 0, 0], 0o2030],
        [LessThanOrEqualNumericUnmasked, [0, 0, 0, 1], 0o2130],
        [LessThanOrEqualNumericUnmasked, [0, 0, 1, 0], 0o2230],
        [LessThanOrEqualNumericUnmasked, [0, 0, 1, 1], 0o2330],
        [LessThanOrEqualNumericUnmasked, [0, 1, 0, 0], 0o2430],
        [LessThanOrEqualNumericUnmasked, [0, 1, 0, 1], 0o2530],
        [LessThanOrEqualNumericUnmasked, [0, 1, 1, 0], 0o2630],
        [LessThanOrEqualNumericUnmasked, [0, 1, 1, 1], 0o2730],
        [LessThanOrEqualNumericUnmasked, [1, 0, 0, 0], 0o6030],
        [LessThanOrEqualNumericUnmasked, [1, 0, 0, 1], 0o6130],
        [LessThanOrEqualNumericUnmasked, [1, 0, 1, 0], 0o6230],
        [LessThanOrEqualNumericUnmasked, [1, 0, 1, 1], 0o6330],
        [LessThanOrEqualNumericUnmasked, [1, 1, 0, 0], 0o6430],
        [LessThanOrEqualNumericUnmasked, [1, 1, 0, 1], 0o6530],
        [LessThanOrEqualNumericUnmasked, [1, 1, 1, 0], 0o6630],
        [LessThanOrEqualNumericUnmasked, [1, 1, 1, 1], 0o6730]
    ]
    run_tests("TEST: LN (unmasked): args range", testdata)


# ######## TX ########

def test_TX_masked_simple():
    testdata = [[TransferMasked, [0, 0], 0o60]]
    run_tests("TEST: TX (masked): simple", testdata)


def test_TX_masked_invalid_args():
    testdata = [
        [TransferMasked, [0, 32], 0],
        [TransferMasked, [2, 0], 0]
    ]
    run_exception_tests("TEST: TX (masked): invalid args", testdata)


def test_TX_masked_args_range():
    testdata = [
        [TransferMasked, [1, 0], 0o4060],
        [TransferMasked, [0, 31], 0o3760],
        [TransferMasked, [1, 31], 0o7760]
    ]
    run_tests("TEST: TX (masked): args range", testdata)


def test_TX_unmasked_simple():
    testdata = [[TransferUnmasked, [0, 0, 0, 0], 0o2020]]
    run_tests("TEST: TX (unmasked): simple", testdata)


def test_TX_unmasked_invalid_args():
    testdata = [
        [TransferUnmasked, [2, 0, 0, 0], 0],
        [TransferUnmasked, [0, 2, 0, 0], 0],
        [TransferUnmasked, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: TX (unmasked): invalid args", testdata)


def test_TX_unmasked_args_range():
    testdata = [
        [TransferUnmasked, [0, 0, 0, 0], 0o2020],
        [TransferUnmasked, [0, 0, 0, 1], 0o2120],
        [TransferUnmasked, [0, 0, 1, 0], 0o2220],
        [TransferUnmasked, [0, 0, 1, 1], 0o2320],
        [TransferUnmasked, [0, 1, 0, 0], 0o2420],
        [TransferUnmasked, [0, 1, 0, 1], 0o2520],
        [TransferUnmasked, [0, 1, 1, 0], 0o2620],
        [TransferUnmasked, [0, 1, 1, 1], 0o2720],
        [TransferUnmasked, [1, 0, 0, 0], 0o6020],
        [TransferUnmasked, [1, 0, 0, 1], 0o6120],
        [TransferUnmasked, [1, 0, 1, 0], 0o6220],
        [TransferUnmasked, [1, 0, 1, 1], 0o6320],
        [TransferUnmasked, [1, 1, 0, 0], 0o6420],
        [TransferUnmasked, [1, 1, 0, 1], 0o6520],
        [TransferUnmasked, [1, 1, 1, 0], 0o6620],
        [TransferUnmasked, [1, 1, 1, 1], 0o6720]
    ]
    run_tests("TEST: TX (unmasked): args range", testdata)


# ######## TS ########

def test_TS_masked_simple():
    testdata = [[TransferChangeSequenceMasked, [0, 0], 0o44]]
    run_tests("TEST: TS (masked): simple", testdata)


def test_TS_masked_invalid_args():
    testdata = [
        [TransferChangeSequenceMasked, [0, 32], 0],
        [TransferChangeSequenceMasked, [2, 0], 0]
    ]
    run_exception_tests("TEST: TS (masked): invalid args", testdata)


def test_TS_masked_args_range():
    testdata = [
        [TransferChangeSequenceMasked, [1, 0], 0o4044],
        [TransferChangeSequenceMasked, [0, 31], 0o3744],
        [TransferChangeSequenceMasked, [1, 31], 0o7744]
    ]
    run_tests("TEST: TS (masked): args range", testdata)


def test_TS_unmasked_simple():
    testdata = [[TransferChangeSequenceUnmasked, [0, 0, 0, 0], 0o2004]]
    run_tests("TEST: TS (unmasked): simple", testdata)


def test_TS_unmasked_invalid_args():
    testdata = [
        [TransferChangeSequenceUnmasked, [2, 0, 0, 0], 0],
        [TransferChangeSequenceUnmasked, [0, 2, 0, 0], 0],
        [TransferChangeSequenceUnmasked, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: TS (unmasked): invalid args", testdata)


def test_TS_unmasked_args_range():
    testdata = [
        [TransferChangeSequenceUnmasked, [0, 0, 0, 0], 0o2004],
        [TransferChangeSequenceUnmasked, [0, 0, 0, 1], 0o2104],
        [TransferChangeSequenceUnmasked, [0, 0, 1, 0], 0o2204],
        [TransferChangeSequenceUnmasked, [0, 0, 1, 1], 0o2304],
        [TransferChangeSequenceUnmasked, [0, 1, 0, 0], 0o2404],
        [TransferChangeSequenceUnmasked, [0, 1, 0, 1], 0o2504],
        [TransferChangeSequenceUnmasked, [0, 1, 1, 0], 0o2604],
        [TransferChangeSequenceUnmasked, [0, 1, 1, 1], 0o2704],
        [TransferChangeSequenceUnmasked, [1, 0, 0, 0], 0o6004],
        [TransferChangeSequenceUnmasked, [1, 0, 0, 1], 0o6104],
        [TransferChangeSequenceUnmasked, [1, 0, 1, 0], 0o6204],
        [TransferChangeSequenceUnmasked, [1, 0, 1, 1], 0o6304],
        [TransferChangeSequenceUnmasked, [1, 1, 0, 0], 0o6404],
        [TransferChangeSequenceUnmasked, [1, 1, 0, 1], 0o6504],
        [TransferChangeSequenceUnmasked, [1, 1, 1, 0], 0o6604],
        [TransferChangeSequenceUnmasked, [1, 1, 1, 1], 0o6704]
    ]
    run_tests("TEST: TS (unmasked): args range", testdata)


# ######## HA ########

def test_HA_masked_simple():
    testdata = [[HalfAddMasked, [0, 0], 0o65]]
    run_tests("TEST: HA (masked): simple", testdata)


def test_HA_masked_invalid_args():
    testdata = [
        [HalfAddMasked, [0, 32], 0],
        [HalfAddMasked, [2, 0], 0]
    ]
    run_exception_tests("TEST: HA (masked): invalid args", testdata)


def test_HA_masked_args_range():
    testdata = [
        [HalfAddMasked, [1, 0], 0o4065],
        [HalfAddMasked, [0, 31], 0o3765],
        [HalfAddMasked, [1, 31], 0o7765]
    ]
    run_tests("TEST: HA (masked): args range", testdata)


def test_HA_unmasked_simple():
    testdata = [[HalfAddUnmasked, [0, 0, 0, 0], 0o2025]]
    run_tests("TEST: HA (unmasked): simple", testdata)


def test_HA_unmasked_invalid_args():
    testdata = [
        [HalfAddUnmasked, [2, 0, 0, 0], 0],
        [HalfAddUnmasked, [0, 2, 0, 0], 0],
        [HalfAddUnmasked, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: HA (unmasked): invalid args", testdata)


def test_HA_unmasked_args_range():
    testdata = [
        [HalfAddUnmasked, [0, 0, 0, 0], 0o2025],
        [HalfAddUnmasked, [0, 0, 0, 1], 0o2125],
        [HalfAddUnmasked, [0, 0, 1, 0], 0o2225],
        [HalfAddUnmasked, [0, 0, 1, 1], 0o2325],
        [HalfAddUnmasked, [0, 1, 0, 0], 0o2425],
        [HalfAddUnmasked, [0, 1, 0, 1], 0o2525],
        [HalfAddUnmasked, [0, 1, 1, 0], 0o2625],
        [HalfAddUnmasked, [0, 1, 1, 1], 0o2725],
        [HalfAddUnmasked, [1, 0, 0, 0], 0o6025],
        [HalfAddUnmasked, [1, 0, 0, 1], 0o6125],
        [HalfAddUnmasked, [1, 0, 1, 0], 0o6225],
        [HalfAddUnmasked, [1, 0, 1, 1], 0o6325],
        [HalfAddUnmasked, [1, 1, 0, 0], 0o6425],
        [HalfAddUnmasked, [1, 1, 0, 1], 0o6525],
        [HalfAddUnmasked, [1, 1, 1, 0], 0o6625],
        [HalfAddUnmasked, [1, 1, 1, 1], 0o6725]
    ]
    run_tests("TEST: HA (unmasked): args range", testdata)


# ######## SM ########

def test_SM_masked_simple():
    testdata = [[SuperimposeMasked, [0, 0], 0o45]]
    run_tests("TEST: SM (masked): simple", testdata)


def test_SM_masked_invalid_args():
    testdata = [
        [SuperimposeMasked, [0, 32], 0],
        [SuperimposeMasked, [2, 0], 0]
    ]
    run_exception_tests("TEST: SM (masked): invalid args", testdata)


def test_SM_masked_args_range():
    testdata = [
        [SuperimposeMasked, [1, 0], 0o4045],
        [SuperimposeMasked, [0, 31], 0o3745],
        [SuperimposeMasked, [1, 31], 0o7745]
    ]
    run_tests("TEST: SM (masked): args range", testdata)


def test_SM_unmasked_simple():
    testdata = [[SuperimposeUnmasked, [0, 0, 0, 0], 0o2005]]
    run_tests("TEST: SM (unmasked): simple", testdata)


def test_SM_unmasked_invalid_args():
    testdata = [
        [SuperimposeUnmasked, [2, 0, 0, 0], 0],
        [SuperimposeUnmasked, [0, 2, 0, 0], 0],
        [SuperimposeUnmasked, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: SM (unmasked): invalid args", testdata)


def test_SM_unmasked_args_range():
    testdata = [
        [SuperimposeUnmasked, [0, 0, 0, 0], 0o2005],
        [SuperimposeUnmasked, [0, 0, 0, 1], 0o2105],
        [SuperimposeUnmasked, [0, 0, 1, 0], 0o2205],
        [SuperimposeUnmasked, [0, 0, 1, 1], 0o2305],
        [SuperimposeUnmasked, [0, 1, 0, 0], 0o2405],
        [SuperimposeUnmasked, [0, 1, 0, 1], 0o2505],
        [SuperimposeUnmasked, [0, 1, 1, 0], 0o2605],
        [SuperimposeUnmasked, [0, 1, 1, 1], 0o2705],
        [SuperimposeUnmasked, [1, 0, 0, 0], 0o6005],
        [SuperimposeUnmasked, [1, 0, 0, 1], 0o6105],
        [SuperimposeUnmasked, [1, 0, 1, 0], 0o6205],
        [SuperimposeUnmasked, [1, 0, 1, 1], 0o6305],
        [SuperimposeUnmasked, [1, 1, 0, 0], 0o6405],
        [SuperimposeUnmasked, [1, 1, 0, 1], 0o6505],
        [SuperimposeUnmasked, [1, 1, 1, 0], 0o6605],
        [SuperimposeUnmasked, [1, 1, 1, 1], 0o6705]
    ]
    run_tests("TEST: SM (unmasked): args range", testdata)


# ######## CP ########

def test_CP_masked_simple():
    testdata = [[CheckParityMasked, [0, 0], 0o64]]
    run_tests("TEST: CP (masked): simple", testdata)


def test_CP_masked_invalid_args():
    testdata = [
        [CheckParityMasked, [0, 32], 0],
        [CheckParityMasked, [2, 0], 0]
    ]
    run_exception_tests("TEST: CP (masked): invalid args", testdata)


def test_CP_masked_args_range():
    testdata = [
        [CheckParityMasked, [1, 0], 0o4064],
        [CheckParityMasked, [0, 31], 0o3764],
        [CheckParityMasked, [1, 31], 0o7764]
    ]
    run_tests("TEST: CP (masked): args range", testdata)


def test_CP_unmasked_simple():
    testdata = [[CheckParityUnmasked, [0, 0, 0, 0], 0o2024]]
    run_tests("TEST: CP (unmasked): simple", testdata)


def test_CP_unmasked_invalid_args():
    testdata = [
        [CheckParityUnmasked, [2, 0, 0, 0], 0],
        [CheckParityUnmasked, [0, 2, 0, 0], 0],
        [CheckParityUnmasked, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: CP (unmasked): invalid args", testdata)


def test_CP_unmasked_args_range():
    testdata = [
        [CheckParityUnmasked, [0, 0, 0, 0], 0o2024],
        [CheckParityUnmasked, [0, 0, 0, 1], 0o2124],
        [CheckParityUnmasked, [0, 0, 1, 0], 0o2224],
        [CheckParityUnmasked, [0, 0, 1, 1], 0o2324],
        [CheckParityUnmasked, [0, 1, 0, 0], 0o2424],
        [CheckParityUnmasked, [0, 1, 0, 1], 0o2524],
        [CheckParityUnmasked, [0, 1, 1, 0], 0o2624],
        [CheckParityUnmasked, [0, 1, 1, 1], 0o2724],
        [CheckParityUnmasked, [1, 0, 0, 0], 0o6024],
        [CheckParityUnmasked, [1, 0, 0, 1], 0o6124],
        [CheckParityUnmasked, [1, 0, 1, 0], 0o6224],
        [CheckParityUnmasked, [1, 0, 1, 1], 0o6324],
        [CheckParityUnmasked, [1, 1, 0, 0], 0o6424],
        [CheckParityUnmasked, [1, 1, 0, 1], 0o6524],
        [CheckParityUnmasked, [1, 1, 1, 0], 0o6624],
        [CheckParityUnmasked, [1, 1, 1, 1], 0o6724]
    ]
    run_tests("TEST: CP (unmasked): args range", testdata)


# ######## BM ########

def test_BM_simple():
    testdata = [[BinaryMultiply, [0, 0, 0, 0], 0o13]]
    run_tests("TEST: BM simple", testdata)


def test_BM_invalid_args():
    testdata = [
        [BinaryMultiply, [2, 0, 0, 0], 0],
        [BinaryMultiply, [0, 2, 0, 0], 0],
        [BinaryMultiply, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: BM invalid args", testdata)


def test_BM_args_range():
    testdata = [
        [BinaryMultiply, [0, 0, 0, 0], 0o0013],
        [BinaryMultiply, [0, 0, 0, 1], 0o0113],
        [BinaryMultiply, [0, 0, 1, 0], 0o0213],
        [BinaryMultiply, [0, 0, 1, 1], 0o0313],
        [BinaryMultiply, [0, 1, 0, 0], 0o0413],
        [BinaryMultiply, [0, 1, 0, 1], 0o0513],
        [BinaryMultiply, [0, 1, 1, 0], 0o0613],
        [BinaryMultiply, [0, 1, 1, 1], 0o0713],
        [BinaryMultiply, [1, 0, 0, 0], 0o4013],
        [BinaryMultiply, [1, 0, 0, 1], 0o4113],
        [BinaryMultiply, [1, 0, 1, 0], 0o4213],
        [BinaryMultiply, [1, 0, 1, 1], 0o4313],
        [BinaryMultiply, [1, 1, 0, 0], 0o4413],
        [BinaryMultiply, [1, 1, 0, 1], 0o4513],
        [BinaryMultiply, [1, 1, 1, 0], 0o4613],
        [BinaryMultiply, [1, 1, 1, 1], 0o4713]
    ]
    run_tests("TEST: BM args range", testdata)


# ######## DM ########

def test_DM_simple():
    testdata = [[DecimalMultiply, [0, 0, 0, 0], 0o03]]
    run_tests("TEST: DM simple", testdata)


def test_DM_invalid_args():
    testdata = [
        [DecimalMultiply, [2, 0, 0, 0], 0],
        [DecimalMultiply, [0, 2, 0, 0], 0],
        [DecimalMultiply, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: DM invalid args", testdata)


def test_DM_args_range():
    testdata = [
        [DecimalMultiply, [0, 0, 0, 0], 0o0003],
        [DecimalMultiply, [0, 0, 0, 1], 0o0103],
        [DecimalMultiply, [0, 0, 1, 0], 0o0203],
        [DecimalMultiply, [0, 0, 1, 1], 0o0303],
        [DecimalMultiply, [0, 1, 0, 0], 0o0403],
        [DecimalMultiply, [0, 1, 0, 1], 0o0503],
        [DecimalMultiply, [0, 1, 1, 0], 0o0603],
        [DecimalMultiply, [0, 1, 1, 1], 0o0703],
        [DecimalMultiply, [1, 0, 0, 0], 0o4003],
        [DecimalMultiply, [1, 0, 0, 1], 0o4103],
        [DecimalMultiply, [1, 0, 1, 0], 0o4203],
        [DecimalMultiply, [1, 0, 1, 1], 0o4303],
        [DecimalMultiply, [1, 1, 0, 0], 0o4403],
        [DecimalMultiply, [1, 1, 0, 1], 0o4503],
        [DecimalMultiply, [1, 1, 1, 0], 0o4603],
        [DecimalMultiply, [1, 1, 1, 1], 0o4703]
    ]
    run_tests("TEST: DM args range", testdata)


# ######## BT ########

def test_BT_simple():
    testdata = [[BinaryAccumulate, [0, 0, 0, 0], 0o2013]]
    run_tests("TEST: BT simple", testdata)


def test_BT_invalid_args():
    testdata = [
        [BinaryAccumulate, [2, 0, 0, 0], 0],
        [BinaryAccumulate, [0, 2, 0, 0], 0],
        [BinaryAccumulate, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: BT invalid args", testdata)


def test_BT_args_range():
    testdata = [
        [BinaryAccumulate, [0, 0, 0, 0], 0o2013],
        [BinaryAccumulate, [0, 0, 0, 1], 0o2113],
        [BinaryAccumulate, [0, 0, 1, 0], 0o2213],
        [BinaryAccumulate, [0, 0, 1, 1], 0o2313],
        [BinaryAccumulate, [0, 1, 0, 0], 0o2413],
        [BinaryAccumulate, [0, 1, 0, 1], 0o2513],
        [BinaryAccumulate, [0, 1, 1, 0], 0o2613],
        [BinaryAccumulate, [0, 1, 1, 1], 0o2713],
        [BinaryAccumulate, [1, 0, 0, 0], 0o6013],
        [BinaryAccumulate, [1, 0, 0, 1], 0o6113],
        [BinaryAccumulate, [1, 0, 1, 0], 0o6213],
        [BinaryAccumulate, [1, 0, 1, 1], 0o6313],
        [BinaryAccumulate, [1, 1, 0, 0], 0o6413],
        [BinaryAccumulate, [1, 1, 0, 1], 0o6513],
        [BinaryAccumulate, [1, 1, 1, 0], 0o6613],
        [BinaryAccumulate, [1, 1, 1, 1], 0o6713]
    ]
    run_tests("TEST: BT args range", testdata)


# ######## DT ########

def test_DT_simple():
    testdata = [[DecimalAccumulate, [0, 0, 0, 0], 0o2003]]
    run_tests("TEST: DT simple", testdata)


def test_DT_invalid_args():
    testdata = [
        [DecimalAccumulate, [2, 0, 0, 0], 0],
        [DecimalAccumulate, [0, 2, 0, 0], 0],
        [DecimalAccumulate, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: DT invalid args", testdata)


def test_DT_args_range():
    testdata = [
        [DecimalAccumulate, [0, 0, 0, 0], 0o2003],
        [DecimalAccumulate, [0, 0, 0, 1], 0o2103],
        [DecimalAccumulate, [0, 0, 1, 0], 0o2203],
        [DecimalAccumulate, [0, 0, 1, 1], 0o2303],
        [DecimalAccumulate, [0, 1, 0, 0], 0o2403],
        [DecimalAccumulate, [0, 1, 0, 1], 0o2503],
        [DecimalAccumulate, [0, 1, 1, 0], 0o2603],
        [DecimalAccumulate, [0, 1, 1, 1], 0o2703],
        [DecimalAccumulate, [1, 0, 0, 0], 0o6003],
        [DecimalAccumulate, [1, 0, 0, 1], 0o6103],
        [DecimalAccumulate, [1, 0, 1, 0], 0o6203],
        [DecimalAccumulate, [1, 0, 1, 1], 0o6303],
        [DecimalAccumulate, [1, 1, 0, 0], 0o6403],
        [DecimalAccumulate, [1, 1, 0, 1], 0o6503],
        [DecimalAccumulate, [1, 1, 1, 0], 0o6603],
        [DecimalAccumulate, [1, 1, 1, 1], 0o6703]
    ]
    run_tests("TEST: DT args range", testdata)


# ######## MT ########

def test_MT_simple():
    testdata = [[MultipleTransfer, [0, 0, 0, 0], 0o0020]]
    run_tests("TEST: MT simple", testdata)


def test_MT_invalid_args():
    testdata = [
        [MultipleTransfer, [2, 0, 0, 0], 0],
        [MultipleTransfer, [0, 2, 0, 0], 0],
        [MultipleTransfer, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: MT invalid args", testdata)


def test_MT_args_range():
    testdata = [
        [MultipleTransfer, [0, 0, 0, 0], 0o0020],
        [MultipleTransfer, [0, 0, 0, 1], 0o0120],
        [MultipleTransfer, [0, 0, 1, 0], 0o0220],
        [MultipleTransfer, [0, 0, 1, 1], 0o0320],
        [MultipleTransfer, [0, 1, 0, 0], 0o0420],
        [MultipleTransfer, [0, 1, 0, 1], 0o0520],
        [MultipleTransfer, [0, 1, 1, 0], 0o0620],
        [MultipleTransfer, [0, 1, 1, 1], 0o0720],
        [MultipleTransfer, [1, 0, 0, 0], 0o4020],
        [MultipleTransfer, [1, 0, 0, 1], 0o4120],
        [MultipleTransfer, [1, 0, 1, 0], 0o4220],
        [MultipleTransfer, [1, 0, 1, 1], 0o4320],
        [MultipleTransfer, [1, 1, 0, 0], 0o4420],
        [MultipleTransfer, [1, 1, 0, 1], 0o4520],
        [MultipleTransfer, [1, 1, 1, 0], 0o4620],
        [MultipleTransfer, [1, 1, 1, 1], 0o4720]
    ]
    run_tests("TEST: MT args range", testdata)


# ######## TN ########

def test_TN_simple():
    testdata = [[TransferNWords, [0, 0, 0, 0], 0o1020]]
    run_tests("TEST: TN simple", testdata)


def test_TN_invalid_args():
    testdata = [
        [TransferNWords, [2, 0, 0, 0], 0],
        [TransferNWords, [0, 2, 0, 0], 0],
        [TransferNWords, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: TN invalid args", testdata)


def test_TN_args_range():
    testdata = [
        [TransferNWords, [0, 0, 0, 0], 0o1020],
        [TransferNWords, [0, 0, 0, 1], 0o1120],
        [TransferNWords, [0, 0, 1, 0], 0o1220],
        [TransferNWords, [0, 0, 1, 1], 0o1320],
        [TransferNWords, [0, 1, 0, 0], 0o1420],
        [TransferNWords, [0, 1, 0, 1], 0o1520],
        [TransferNWords, [0, 1, 1, 0], 0o1620],
        [TransferNWords, [0, 1, 1, 1], 0o1720],
        [TransferNWords, [1, 0, 0, 0], 0o5020],
        [TransferNWords, [1, 0, 0, 1], 0o5120],
        [TransferNWords, [1, 0, 1, 0], 0o5220],
        [TransferNWords, [1, 0, 1, 1], 0o5320],
        [TransferNWords, [1, 1, 0, 0], 0o5420],
        [TransferNWords, [1, 1, 0, 1], 0o5520],
        [TransferNWords, [1, 1, 1, 0], 0o5620],
        [TransferNWords, [1, 1, 1, 1], 0o5720]
    ]
    run_tests("TEST: TN args range", testdata)


# ######## CC ########

def test_CC_simple():
    testdata = [[ComputeOrthocount, [0, 0, 0, 0], 0o1010]]
    run_tests("TEST: CC simple", testdata)


def test_CC_invalid_args():
    testdata = [
        [ComputeOrthocount, [2, 0, 0, 0], 0],
        [ComputeOrthocount, [0, 2, 0, 0], 0],
        [ComputeOrthocount, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: CC invalid args", testdata)


def test_CC_args_range():
    testdata = [
        [ComputeOrthocount, [0, 0, 0, 0], 0o1010],
        [ComputeOrthocount, [0, 0, 0, 1], 0o1110],
        [ComputeOrthocount, [0, 0, 1, 0], 0o1210],
        [ComputeOrthocount, [0, 0, 1, 1], 0o1310],
        [ComputeOrthocount, [0, 1, 0, 0], 0o1410],
        [ComputeOrthocount, [0, 1, 0, 1], 0o1510],
        [ComputeOrthocount, [0, 1, 1, 0], 0o1610],
        [ComputeOrthocount, [0, 1, 1, 1], 0o1710],
        [ComputeOrthocount, [1, 0, 0, 0], 0o5010],
        [ComputeOrthocount, [1, 0, 0, 1], 0o5110],
        [ComputeOrthocount, [1, 0, 1, 0], 0o5210],
        [ComputeOrthocount, [1, 0, 1, 1], 0o5310],
        [ComputeOrthocount, [1, 1, 0, 0], 0o5410],
        [ComputeOrthocount, [1, 1, 0, 1], 0o5510],
        [ComputeOrthocount, [1, 1, 1, 0], 0o5610],
        [ComputeOrthocount, [1, 1, 1, 1], 0o5710]
    ]
    run_tests("TEST: CC args range", testdata)


# ######## IT ########

def test_IT_simple():
    testdata = [[ItemTransfer, [0, 0, 0, 0], 0o1030]]
    run_tests("TEST: IT simple", testdata)


def test_IT_invalid_args():
    testdata = [
        [ItemTransfer, [2, 0, 0, 0], 0],
        [ItemTransfer, [0, 2, 0, 0], 0],
        [ItemTransfer, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: IT invalid args", testdata)


def test_IT_args_range():
    testdata = [
        [ItemTransfer, [0, 0, 0, 0], 0o1030],
        [ItemTransfer, [0, 0, 0, 1], 0o1130],
        [ItemTransfer, [0, 0, 1, 0], 0o1230],
        [ItemTransfer, [0, 0, 1, 1], 0o1330],
        [ItemTransfer, [0, 1, 0, 0], 0o1430],
        [ItemTransfer, [0, 1, 0, 1], 0o1530],
        [ItemTransfer, [0, 1, 1, 0], 0o1630],
        [ItemTransfer, [0, 1, 1, 1], 0o1730],
        [ItemTransfer, [1, 0, 0, 0], 0o5030],
        [ItemTransfer, [1, 0, 0, 1], 0o5130],
        [ItemTransfer, [1, 0, 1, 0], 0o5230],
        [ItemTransfer, [1, 0, 1, 1], 0o5330],
        [ItemTransfer, [1, 1, 0, 0], 0o5430],
        [ItemTransfer, [1, 1, 0, 1], 0o5530],
        [ItemTransfer, [1, 1, 1, 0], 0o5630],
        [ItemTransfer, [1, 1, 1, 1], 0o5730]
    ]
    run_tests("TEST: IT args range", testdata)


# ######## EBA ########

def test_EBA_simple():
    testdata = [[ExtendedBinaryAdd, [0, 0, 0, 0], 0o3013]]
    run_tests("TEST: EBA simple", testdata)


def test_EBA_invalid_args():
    testdata = [
        [ExtendedBinaryAdd, [2, 0, 0, 0], 0],
        [ExtendedBinaryAdd, [0, 2, 0, 0], 0],
        [ExtendedBinaryAdd, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: EBA invalid args", testdata)


def test_EBA_args_range():
    testdata = [
        [ExtendedBinaryAdd, [0, 0, 0, 0], 0o3013],
        [ExtendedBinaryAdd, [0, 0, 0, 1], 0o3113],
        [ExtendedBinaryAdd, [0, 0, 1, 0], 0o3213],
        [ExtendedBinaryAdd, [0, 0, 1, 1], 0o3313],
        [ExtendedBinaryAdd, [0, 1, 0, 0], 0o3413],
        [ExtendedBinaryAdd, [0, 1, 0, 1], 0o3513],
        [ExtendedBinaryAdd, [0, 1, 1, 0], 0o3613],
        [ExtendedBinaryAdd, [0, 1, 1, 1], 0o3713],
        [ExtendedBinaryAdd, [1, 0, 0, 0], 0o7013],
        [ExtendedBinaryAdd, [1, 0, 0, 1], 0o7113],
        [ExtendedBinaryAdd, [1, 0, 1, 0], 0o7213],
        [ExtendedBinaryAdd, [1, 0, 1, 1], 0o7313],
        [ExtendedBinaryAdd, [1, 1, 0, 0], 0o7413],
        [ExtendedBinaryAdd, [1, 1, 0, 1], 0o7513],
        [ExtendedBinaryAdd, [1, 1, 1, 0], 0o7613],
        [ExtendedBinaryAdd, [1, 1, 1, 1], 0o7713]
    ]
    run_tests("TEST: EBA args range", testdata)


# ######## EBS ########

def test_EBS_simple():
    testdata = [[ExtendedBinarySubtract, [0, 0, 0, 0], 0o3033]]
    run_tests("TEST: EBS simple", testdata)


def test_EBS_invalid_args():
    testdata = [
        [ExtendedBinarySubtract, [2, 0, 0, 0], 0],
        [ExtendedBinarySubtract, [0, 2, 0, 0], 0],
        [ExtendedBinarySubtract, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: EBS invalid args", testdata)


def test_EBS_args_range():
    testdata = [
        [ExtendedBinarySubtract, [0, 0, 0, 0], 0o3033],
        [ExtendedBinarySubtract, [0, 0, 0, 1], 0o3133],
        [ExtendedBinarySubtract, [0, 0, 1, 0], 0o3233],
        [ExtendedBinarySubtract, [0, 0, 1, 1], 0o3333],
        [ExtendedBinarySubtract, [0, 1, 0, 0], 0o3433],
        [ExtendedBinarySubtract, [0, 1, 0, 1], 0o3533],
        [ExtendedBinarySubtract, [0, 1, 1, 0], 0o3633],
        [ExtendedBinarySubtract, [0, 1, 1, 1], 0o3733],
        [ExtendedBinarySubtract, [1, 0, 0, 0], 0o7033],
        [ExtendedBinarySubtract, [1, 0, 0, 1], 0o7133],
        [ExtendedBinarySubtract, [1, 0, 1, 0], 0o7233],
        [ExtendedBinarySubtract, [1, 0, 1, 1], 0o7333],
        [ExtendedBinarySubtract, [1, 1, 0, 0], 0o7433],
        [ExtendedBinarySubtract, [1, 1, 0, 1], 0o7533],
        [ExtendedBinarySubtract, [1, 1, 1, 0], 0o7633],
        [ExtendedBinarySubtract, [1, 1, 1, 1], 0o7733]
    ]
    run_tests("TEST: EBS args range", testdata)


# ######## RT ########

def test_RT_simple():
    testdata = [[RecordTransfer, [0, 0, 0, 0], 0o3030]]
    run_tests("TEST: RT simple", testdata)


def test_RT_invalid_args():
    testdata = [
        [RecordTransfer, [2, 0, 0, 0], 0],
        [RecordTransfer, [0, 2, 0, 0], 0],
        [RecordTransfer, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: RT invalid args", testdata)


def test_RT_args_range():
    testdata = [
        [RecordTransfer, [0, 0, 0, 0], 0o3030],
        [RecordTransfer, [0, 0, 0, 1], 0o3130],
        [RecordTransfer, [0, 0, 1, 0], 0o3230],
        [RecordTransfer, [0, 0, 1, 1], 0o3330],
        [RecordTransfer, [0, 1, 0, 0], 0o3430],
        [RecordTransfer, [0, 1, 0, 1], 0o3530],
        [RecordTransfer, [0, 1, 1, 0], 0o3630],
        [RecordTransfer, [0, 1, 1, 1], 0o3730],
        [RecordTransfer, [1, 0, 0, 0], 0o7030],
        [RecordTransfer, [1, 0, 0, 1], 0o7130],
        [RecordTransfer, [1, 0, 1, 0], 0o7230],
        [RecordTransfer, [1, 0, 1, 1], 0o7330],
        [RecordTransfer, [1, 1, 0, 0], 0o7430],
        [RecordTransfer, [1, 1, 0, 1], 0o7530],
        [RecordTransfer, [1, 1, 1, 0], 0o7630],
        [RecordTransfer, [1, 1, 1, 1], 0o7730]
    ]
    run_tests("TEST: RT args range", testdata)


# ######## MPC ########

def test_MPC_simple():
    testdata = [[ControlProgram, [0, 0, 0, 0], 0o2000]]
    run_tests("TEST: MPC simple", testdata)


def test_MPC_invalid_args():
    testdata = [
        [ControlProgram, [2, 0, 0, 0], 0],
        [ControlProgram, [0, 2, 0, 0], 0],
        [ControlProgram, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: MPC invalid args", testdata)


def test_MPC_args_range():
    testdata = [
        [ControlProgram, [0, 0, 0, 0], 0o2000],
        [ControlProgram, [0, 0, 0, 1], 0o2100],
        [ControlProgram, [0, 0, 1, 0], 0o2200],
        [ControlProgram, [0, 0, 1, 1], 0o2300],
        [ControlProgram, [0, 1, 0, 0], 0o2400],
        [ControlProgram, [0, 1, 0, 1], 0o2500],
        [ControlProgram, [0, 1, 1, 0], 0o2600],
        [ControlProgram, [0, 1, 1, 1], 0o2700],
        [ControlProgram, [1, 0, 0, 0], 0o6000],
        [ControlProgram, [1, 0, 0, 1], 0o6100],
        [ControlProgram, [1, 0, 1, 0], 0o6200],
        [ControlProgram, [1, 0, 1, 1], 0o6300],
        [ControlProgram, [1, 1, 0, 0], 0o6400],
        [ControlProgram, [1, 1, 0, 1], 0o6500],
        [ControlProgram, [1, 1, 1, 0], 0o6600],
        [ControlProgram, [1, 1, 1, 1], 0o6700]
    ]
    run_tests("TEST: MPC args range", testdata)


# ######## PR ########

def test_PR_simple():
    testdata = [[Proceed, [], 0o0000]]
    run_tests("TEST: PR simple", testdata)


# ######## SWS ########

def test_SWS_simple():
    testdata = [[ShiftWordAndSubstitute, [0, 0, 0, 0], 0o2006]]
    run_tests("TEST: SWS simple", testdata)


def test_SWS_invalid_args():
    testdata = [
        [ShiftWordAndSubstitute, [2, 0, 0, 0], 0],
        [ShiftWordAndSubstitute, [0, 2, 0, 0], 0],
        [ShiftWordAndSubstitute, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: SWS invalid args", testdata)


def test_SWS_args_range():
    testdata = [
        [ShiftWordAndSubstitute, [0, 0, 0, 0], 0o2006],
        [ShiftWordAndSubstitute, [0, 0, 0, 1], 0o2106],
        [ShiftWordAndSubstitute, [0, 0, 1, 0], 0o2206],
        [ShiftWordAndSubstitute, [0, 0, 1, 1], 0o2306],
        [ShiftWordAndSubstitute, [0, 1, 0, 0], 0o2406],
        [ShiftWordAndSubstitute, [0, 1, 0, 1], 0o2506],
        [ShiftWordAndSubstitute, [0, 1, 1, 0], 0o2606],
        [ShiftWordAndSubstitute, [0, 1, 1, 1], 0o2706],
        [ShiftWordAndSubstitute, [1, 0, 0, 0], 0o6006],
        [ShiftWordAndSubstitute, [1, 0, 0, 1], 0o6106],
        [ShiftWordAndSubstitute, [1, 0, 1, 0], 0o6206],
        [ShiftWordAndSubstitute, [1, 0, 1, 1], 0o6306],
        [ShiftWordAndSubstitute, [1, 1, 0, 0], 0o6406],
        [ShiftWordAndSubstitute, [1, 1, 0, 1], 0o6506],
        [ShiftWordAndSubstitute, [1, 1, 1, 0], 0o6606],
        [ShiftWordAndSubstitute, [1, 1, 1, 1], 0o6706]
    ]
    run_tests("TEST: SWS args range", testdata)


# ######## SPS ########

def test_SPS_simple():
    testdata = [[ShiftPreservingSignAndSubstitute, [0, 0, 0, 0], 0o2002]]
    run_tests("TEST: SPS simple", testdata)


def test_SPS_invalid_args():
    testdata = [
        [ShiftPreservingSignAndSubstitute, [2, 0, 0, 0], 0],
        [ShiftPreservingSignAndSubstitute, [0, 2, 0, 0], 0],
        [ShiftPreservingSignAndSubstitute, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: SPS invalid args", testdata)


def test_SPS_args_range():
    testdata = [
        [ShiftPreservingSignAndSubstitute, [0, 0, 0, 0], 0o2002],
        [ShiftPreservingSignAndSubstitute, [0, 0, 0, 1], 0o2102],
        [ShiftPreservingSignAndSubstitute, [0, 0, 1, 0], 0o2202],
        [ShiftPreservingSignAndSubstitute, [0, 0, 1, 1], 0o2302],
        [ShiftPreservingSignAndSubstitute, [0, 1, 0, 0], 0o2402],
        [ShiftPreservingSignAndSubstitute, [0, 1, 0, 1], 0o2502],
        [ShiftPreservingSignAndSubstitute, [0, 1, 1, 0], 0o2602],
        [ShiftPreservingSignAndSubstitute, [0, 1, 1, 1], 0o2702],
        [ShiftPreservingSignAndSubstitute, [1, 0, 0, 0], 0o6002],
        [ShiftPreservingSignAndSubstitute, [1, 0, 0, 1], 0o6102],
        [ShiftPreservingSignAndSubstitute, [1, 0, 1, 0], 0o6202],
        [ShiftPreservingSignAndSubstitute, [1, 0, 1, 1], 0o6302],
        [ShiftPreservingSignAndSubstitute, [1, 1, 0, 0], 0o6402],
        [ShiftPreservingSignAndSubstitute, [1, 1, 0, 1], 0o6502],
        [ShiftPreservingSignAndSubstitute, [1, 1, 1, 0], 0o6602],
        [ShiftPreservingSignAndSubstitute, [1, 1, 1, 1], 0o6702]
    ]
    run_tests("TEST: SPS args range", testdata)


# ######## SWE ########

def test_SWE_simple():
    testdata = [[ShiftWordAndExtract, [0, 0, 0, 0], 0o2016]]
    run_tests("TEST: SWE simple", testdata)


def test_SWE_invalid_args():
    testdata = [
        [ShiftWordAndExtract, [2, 0, 0, 0], 0],
        [ShiftWordAndExtract, [0, 2, 0, 0], 0],
        [ShiftWordAndExtract, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: SWE invalid args", testdata)


def test_SWE_args_range():
    testdata = [
        [ShiftWordAndExtract, [0, 0, 0, 0], 0o2016],
        [ShiftWordAndExtract, [0, 0, 0, 1], 0o2116],
        [ShiftWordAndExtract, [0, 0, 1, 0], 0o2216],
        [ShiftWordAndExtract, [0, 0, 1, 1], 0o2316],
        [ShiftWordAndExtract, [0, 1, 0, 0], 0o2416],
        [ShiftWordAndExtract, [0, 1, 0, 1], 0o2516],
        [ShiftWordAndExtract, [0, 1, 1, 0], 0o2616],
        [ShiftWordAndExtract, [0, 1, 1, 1], 0o2716],
        [ShiftWordAndExtract, [1, 0, 0, 0], 0o6016],
        [ShiftWordAndExtract, [1, 0, 0, 1], 0o6116],
        [ShiftWordAndExtract, [1, 0, 1, 0], 0o6216],
        [ShiftWordAndExtract, [1, 0, 1, 1], 0o6316],
        [ShiftWordAndExtract, [1, 1, 0, 0], 0o6416],
        [ShiftWordAndExtract, [1, 1, 0, 1], 0o6516],
        [ShiftWordAndExtract, [1, 1, 1, 0], 0o6616],
        [ShiftWordAndExtract, [1, 1, 1, 1], 0o6716]
    ]
    run_tests("TEST: SWE args range", testdata)


# ######## SPE ########

def test_SPE_simple():
    testdata = [[ShiftPreservingSignAndExtract, [0, 0, 0, 0], 0o2012]]
    run_tests("TEST: SPE simple", testdata)


def test_SPE_invalid_args():
    testdata = [
        [ShiftPreservingSignAndExtract, [2, 0, 0, 0], 0],
        [ShiftPreservingSignAndExtract, [0, 2, 0, 0], 0],
        [ShiftPreservingSignAndExtract, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: SPE invalid args", testdata)


def test_SPE_args_range():
    testdata = [
        [ShiftPreservingSignAndExtract, [0, 0, 0, 0], 0o2012],
        [ShiftPreservingSignAndExtract, [0, 0, 0, 1], 0o2112],
        [ShiftPreservingSignAndExtract, [0, 0, 1, 0], 0o2212],
        [ShiftPreservingSignAndExtract, [0, 0, 1, 1], 0o2312],
        [ShiftPreservingSignAndExtract, [0, 1, 0, 0], 0o2412],
        [ShiftPreservingSignAndExtract, [0, 1, 0, 1], 0o2512],
        [ShiftPreservingSignAndExtract, [0, 1, 1, 0], 0o2612],
        [ShiftPreservingSignAndExtract, [0, 1, 1, 1], 0o2712],
        [ShiftPreservingSignAndExtract, [1, 0, 0, 0], 0o6012],
        [ShiftPreservingSignAndExtract, [1, 0, 0, 1], 0o6112],
        [ShiftPreservingSignAndExtract, [1, 0, 1, 0], 0o6212],
        [ShiftPreservingSignAndExtract, [1, 0, 1, 1], 0o6312],
        [ShiftPreservingSignAndExtract, [1, 1, 0, 0], 0o6412],
        [ShiftPreservingSignAndExtract, [1, 1, 0, 1], 0o6512],
        [ShiftPreservingSignAndExtract, [1, 1, 1, 0], 0o6612],
        [ShiftPreservingSignAndExtract, [1, 1, 1, 1], 0o6712]
    ]
    run_tests("TEST: SPE args range", testdata)


# ######## SSL ########

def test_SSL_simple():
    testdata = [[ShiftAndSelect, [0, 0, 0, 0], 0o2026]]
    run_tests("TEST: SSL simple", testdata)


def test_SSL_invalid_args():
    testdata = [
        [ShiftAndSelect, [2, 0, 0, 0], 0],
        [ShiftAndSelect, [0, 2, 0, 0], 0],
        [ShiftAndSelect, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: SSL invalid args", testdata)


def test_SSL_args_range():
    testdata = [
        [ShiftAndSelect, [0, 0, 0, 0], 0o2026],
        [ShiftAndSelect, [0, 0, 0, 1], 0o2126],
        [ShiftAndSelect, [0, 0, 1, 0], 0o2226],
        [ShiftAndSelect, [0, 0, 1, 1], 0o2326],
        [ShiftAndSelect, [0, 1, 0, 0], 0o2426],
        [ShiftAndSelect, [0, 1, 0, 1], 0o2526],
        [ShiftAndSelect, [0, 1, 1, 0], 0o2626],
        [ShiftAndSelect, [0, 1, 1, 1], 0o2726],
        [ShiftAndSelect, [1, 0, 0, 0], 0o6026],
        [ShiftAndSelect, [1, 0, 0, 1], 0o6126],
        [ShiftAndSelect, [1, 0, 1, 0], 0o6226],
        [ShiftAndSelect, [1, 0, 1, 1], 0o6326],
        [ShiftAndSelect, [1, 1, 0, 0], 0o6426],
        [ShiftAndSelect, [1, 1, 0, 1], 0o6526],
        [ShiftAndSelect, [1, 1, 1, 0], 0o6626],
        [ShiftAndSelect, [1, 1, 1, 1], 0o6726]
    ]
    run_tests("TEST: SSL args range", testdata)


# ######## SS ########

def test_SS_simple():
    testdata = [[Substitute, [0, 0, 0, 0], 0o0006]]
    run_tests("TEST: SS simple", testdata)


def test_SS_invalid_args():
    testdata = [
        [Substitute, [2, 0, 0, 0], 0],
        [Substitute, [0, 2, 0, 0], 0],
        [Substitute, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: SS invalid args", testdata)


def test_SS_args_range():
    testdata = [
        [Substitute, [0, 0, 0, 0], 0o0006],
        [Substitute, [0, 0, 0, 1], 0o0106],
        [Substitute, [0, 0, 1, 0], 0o0206],
        [Substitute, [0, 0, 1, 1], 0o0306],
        [Substitute, [0, 1, 0, 0], 0o0406],
        [Substitute, [0, 1, 0, 1], 0o0506],
        [Substitute, [0, 1, 1, 0], 0o0606],
        [Substitute, [0, 1, 1, 1], 0o0706],
        [Substitute, [1, 0, 0, 0], 0o4006],
        [Substitute, [1, 0, 0, 1], 0o4106],
        [Substitute, [1, 0, 1, 0], 0o4206],
        [Substitute, [1, 0, 1, 1], 0o4306],
        [Substitute, [1, 1, 0, 0], 0o4406],
        [Substitute, [1, 1, 0, 1], 0o4506],
        [Substitute, [1, 1, 1, 0], 0o4606],
        [Substitute, [1, 1, 1, 1], 0o4706]
    ]
    run_tests("TEST: SS args range", testdata)


# ######## EX ########

def test_EX_simple():
    testdata = [[Extract, [0, 0, 0, 0], 0o0016]]
    run_tests("TEST: EX simple", testdata)


def test_EX_invalid_args():
    testdata = [
        [Extract, [2, 0, 0, 0], 0],
        [Extract, [0, 2, 0, 0], 0],
        [Extract, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: EX invalid args", testdata)


def test_EX_args_range():
    testdata = [
        [Extract, [0, 0, 0, 0], 0o0016],
        [Extract, [0, 0, 0, 1], 0o0116],
        [Extract, [0, 0, 1, 0], 0o0216],
        [Extract, [0, 0, 1, 1], 0o0316],
        [Extract, [0, 1, 0, 0], 0o0416],
        [Extract, [0, 1, 0, 1], 0o0516],
        [Extract, [0, 1, 1, 0], 0o0616],
        [Extract, [0, 1, 1, 1], 0o0716],
        [Extract, [1, 0, 0, 0], 0o4016],
        [Extract, [1, 0, 0, 1], 0o4116],
        [Extract, [1, 0, 1, 0], 0o4216],
        [Extract, [1, 0, 1, 1], 0o4316],
        [Extract, [1, 1, 0, 0], 0o4416],
        [Extract, [1, 1, 0, 1], 0o4516],
        [Extract, [1, 1, 1, 0], 0o4616],
        [Extract, [1, 1, 1, 1], 0o4716]
    ]
    run_tests("TEST: EX args range", testdata)


# ######## RF ########

def test_RF_simple():
    testdata = [[ReadForward, [0], 0o0072]]
    run_tests("TEST: RF simple", testdata)


def test_RF_invalid_args():
    testdata = [
        [ReadForward, [-1], 0],
        [ReadForward, [64], 0]
    ]
    run_exception_tests("TEST: RF invalid args", testdata)


def test_RF_args_range():
    testdata = [
        [ReadForward, [0], 0o0072],
        [ReadForward, [1], 0o0172],
        [ReadForward, [2], 0o0272],
        [ReadForward, [3], 0o0372],
        [ReadForward, [4], 0o0472],
        [ReadForward, [5], 0o0572],
        [ReadForward, [6], 0o0672],
        [ReadForward, [7], 0o0772],
        [ReadForward, [8], 0o1072],
        [ReadForward, [9], 0o1172],
        [ReadForward, [10], 0o1272],
        [ReadForward, [11], 0o1372],
        [ReadForward, [12], 0o1472],
        [ReadForward, [13], 0o1572],
        [ReadForward, [14], 0o1672],
        [ReadForward, [15], 0o1772],
        [ReadForward, [16], 0o2072],
        [ReadForward, [17], 0o2172],
        [ReadForward, [18], 0o2272],
        [ReadForward, [19], 0o2372],
        [ReadForward, [20], 0o2472],
        [ReadForward, [21], 0o2572],
        [ReadForward, [22], 0o2672],
        [ReadForward, [23], 0o2772],
        [ReadForward, [24], 0o3072],
        [ReadForward, [25], 0o3172],
        [ReadForward, [26], 0o3272],
        [ReadForward, [27], 0o3372],
        [ReadForward, [28], 0o3472],
        [ReadForward, [29], 0o3572],
        [ReadForward, [30], 0o3672],
        [ReadForward, [31], 0o3772],
        [ReadForward, [32], 0o4072],
        [ReadForward, [33], 0o4172],
        [ReadForward, [34], 0o4272],
        [ReadForward, [35], 0o4372],
        [ReadForward, [36], 0o4472],
        [ReadForward, [37], 0o4572],
        [ReadForward, [38], 0o4672],
        [ReadForward, [39], 0o4772],
        [ReadForward, [40], 0o5072],
        [ReadForward, [41], 0o5172],
        [ReadForward, [42], 0o5272],
        [ReadForward, [43], 0o5372],
        [ReadForward, [44], 0o5472],
        [ReadForward, [45], 0o5572],
        [ReadForward, [46], 0o5672],
        [ReadForward, [47], 0o5772],
        [ReadForward, [48], 0o6072],
        [ReadForward, [49], 0o6172],
        [ReadForward, [50], 0o6272],
        [ReadForward, [51], 0o6372],
        [ReadForward, [52], 0o6472],
        [ReadForward, [53], 0o6572],
        [ReadForward, [54], 0o6672],
        [ReadForward, [55], 0o6772],
        [ReadForward, [56], 0o7072],
        [ReadForward, [57], 0o7172],
        [ReadForward, [58], 0o7272],
        [ReadForward, [59], 0o7372],
        [ReadForward, [60], 0o7472],
        [ReadForward, [61], 0o7572],
        [ReadForward, [62], 0o7672],
        [ReadForward, [63], 0o7772]
    ]
    run_tests("TEST: RF args range", testdata)


# ######## RB ########

def test_RB_simple():
    testdata = [[ReadBackward, [0], 0o0052]]
    run_tests("TEST: RB simple", testdata)


def test_RB_invalid_args():
    testdata = [
        [ReadBackward, [-1], 0],
        [ReadBackward, [64], 0]
    ]
    run_exception_tests("TEST: RB invalid args", testdata)


def test_RB_args_range():
    testdata = [
        [ReadBackward, [0], 0o0052],
        [ReadBackward, [1], 0o0152],
        [ReadBackward, [2], 0o0252],
        [ReadBackward, [3], 0o0352],
        [ReadBackward, [4], 0o0452],
        [ReadBackward, [5], 0o0552],
        [ReadBackward, [6], 0o0652],
        [ReadBackward, [7], 0o0752],
        [ReadBackward, [8], 0o1052],
        [ReadBackward, [9], 0o1152],
        [ReadBackward, [10], 0o1252],
        [ReadBackward, [11], 0o1352],
        [ReadBackward, [12], 0o1452],
        [ReadBackward, [13], 0o1552],
        [ReadBackward, [14], 0o1652],
        [ReadBackward, [15], 0o1752],
        [ReadBackward, [16], 0o2052],
        [ReadBackward, [17], 0o2152],
        [ReadBackward, [18], 0o2252],
        [ReadBackward, [19], 0o2352],
        [ReadBackward, [20], 0o2452],
        [ReadBackward, [21], 0o2552],
        [ReadBackward, [22], 0o2652],
        [ReadBackward, [23], 0o2752],
        [ReadBackward, [24], 0o3052],
        [ReadBackward, [25], 0o3152],
        [ReadBackward, [26], 0o3252],
        [ReadBackward, [27], 0o3352],
        [ReadBackward, [28], 0o3452],
        [ReadBackward, [29], 0o3552],
        [ReadBackward, [30], 0o3652],
        [ReadBackward, [31], 0o3752],
        [ReadBackward, [32], 0o4052],
        [ReadBackward, [33], 0o4152],
        [ReadBackward, [34], 0o4252],
        [ReadBackward, [35], 0o4352],
        [ReadBackward, [36], 0o4452],
        [ReadBackward, [37], 0o4552],
        [ReadBackward, [38], 0o4652],
        [ReadBackward, [39], 0o4752],
        [ReadBackward, [40], 0o5052],
        [ReadBackward, [41], 0o5152],
        [ReadBackward, [42], 0o5252],
        [ReadBackward, [43], 0o5352],
        [ReadBackward, [44], 0o5452],
        [ReadBackward, [45], 0o5552],
        [ReadBackward, [46], 0o5652],
        [ReadBackward, [47], 0o5752],
        [ReadBackward, [48], 0o6052],
        [ReadBackward, [49], 0o6152],
        [ReadBackward, [50], 0o6252],
        [ReadBackward, [51], 0o6352],
        [ReadBackward, [52], 0o6452],
        [ReadBackward, [53], 0o6552],
        [ReadBackward, [54], 0o6652],
        [ReadBackward, [55], 0o6752],
        [ReadBackward, [56], 0o7052],
        [ReadBackward, [57], 0o7152],
        [ReadBackward, [58], 0o7252],
        [ReadBackward, [59], 0o7352],
        [ReadBackward, [60], 0o7452],
        [ReadBackward, [61], 0o7552],
        [ReadBackward, [62], 0o7652],
        [ReadBackward, [63], 0o7752]
    ]
    run_tests("TEST: RB args range", testdata)


# ######## WF ########

def test_WF_simple():
    testdata = [[WriteForward, [0], 0o0056]]
    run_tests("TEST: WF simple", testdata)


def test_WF_invalid_args():
    testdata = [
        [WriteForward, [-1], 0],
        [WriteForward, [64], 0]
    ]
    run_exception_tests("TEST: WF invalid args", testdata)


def test_WF_args_range():
    testdata = [
        [WriteForward, [0], 0o0056],
        [WriteForward, [1], 0o0156],
        [WriteForward, [2], 0o0256],
        [WriteForward, [3], 0o0356],
        [WriteForward, [4], 0o0456],
        [WriteForward, [5], 0o0556],
        [WriteForward, [6], 0o0656],
        [WriteForward, [7], 0o0756],
        [WriteForward, [8], 0o1056],
        [WriteForward, [9], 0o1156],
        [WriteForward, [10], 0o1256],
        [WriteForward, [11], 0o1356],
        [WriteForward, [12], 0o1456],
        [WriteForward, [13], 0o1556],
        [WriteForward, [14], 0o1656],
        [WriteForward, [15], 0o1756],
        [WriteForward, [16], 0o2056],
        [WriteForward, [17], 0o2156],
        [WriteForward, [18], 0o2256],
        [WriteForward, [19], 0o2356],
        [WriteForward, [20], 0o2456],
        [WriteForward, [21], 0o2556],
        [WriteForward, [22], 0o2656],
        [WriteForward, [23], 0o2756],
        [WriteForward, [24], 0o3056],
        [WriteForward, [25], 0o3156],
        [WriteForward, [26], 0o3256],
        [WriteForward, [27], 0o3356],
        [WriteForward, [28], 0o3456],
        [WriteForward, [29], 0o3556],
        [WriteForward, [30], 0o3656],
        [WriteForward, [31], 0o3756],
        [WriteForward, [32], 0o4056],
        [WriteForward, [33], 0o4156],
        [WriteForward, [34], 0o4256],
        [WriteForward, [35], 0o4356],
        [WriteForward, [36], 0o4456],
        [WriteForward, [37], 0o4556],
        [WriteForward, [38], 0o4656],
        [WriteForward, [39], 0o4756],
        [WriteForward, [40], 0o5056],
        [WriteForward, [41], 0o5156],
        [WriteForward, [42], 0o5256],
        [WriteForward, [43], 0o5356],
        [WriteForward, [44], 0o5456],
        [WriteForward, [45], 0o5556],
        [WriteForward, [46], 0o5656],
        [WriteForward, [47], 0o5756],
        [WriteForward, [48], 0o6056],
        [WriteForward, [49], 0o6156],
        [WriteForward, [50], 0o6256],
        [WriteForward, [51], 0o6356],
        [WriteForward, [52], 0o6456],
        [WriteForward, [53], 0o6556],
        [WriteForward, [54], 0o6656],
        [WriteForward, [55], 0o6756],
        [WriteForward, [56], 0o7056],
        [WriteForward, [57], 0o7156],
        [WriteForward, [58], 0o7256],
        [WriteForward, [59], 0o7356],
        [WriteForward, [60], 0o7456],
        [WriteForward, [61], 0o7556],
        [WriteForward, [62], 0o7656],
        [WriteForward, [63], 0o7756]
    ]
    run_tests("TEST: WF args range", testdata)


# ######## RW ########

def test_RW_simple():
    testdata = [[Rewind, [0], 0o0042]]
    run_tests("TEST: RW simple", testdata)


def test_RW_invalid_args():
    testdata = [
        [Rewind, [-1], 0],
        [Rewind, [64], 0]
    ]
    run_exception_tests("TEST: RW invalid args", testdata)


def test_RW_args_range():
    testdata = [
        [Rewind, [0], 0o0042],
        [Rewind, [1], 0o0142],
        [Rewind, [2], 0o0242],
        [Rewind, [3], 0o0342],
        [Rewind, [4], 0o0442],
        [Rewind, [5], 0o0542],
        [Rewind, [6], 0o0642],
        [Rewind, [7], 0o0742],
        [Rewind, [8], 0o1042],
        [Rewind, [9], 0o1142],
        [Rewind, [10], 0o1242],
        [Rewind, [11], 0o1342],
        [Rewind, [12], 0o1442],
        [Rewind, [13], 0o1542],
        [Rewind, [14], 0o1642],
        [Rewind, [15], 0o1742],
        [Rewind, [16], 0o2042],
        [Rewind, [17], 0o2142],
        [Rewind, [18], 0o2242],
        [Rewind, [19], 0o2342],
        [Rewind, [20], 0o2442],
        [Rewind, [21], 0o2542],
        [Rewind, [22], 0o2642],
        [Rewind, [23], 0o2742],
        [Rewind, [24], 0o3042],
        [Rewind, [25], 0o3142],
        [Rewind, [26], 0o3242],
        [Rewind, [27], 0o3342],
        [Rewind, [28], 0o3442],
        [Rewind, [29], 0o3542],
        [Rewind, [30], 0o3642],
        [Rewind, [31], 0o3742],
        [Rewind, [32], 0o4042],
        [Rewind, [33], 0o4142],
        [Rewind, [34], 0o4242],
        [Rewind, [35], 0o4342],
        [Rewind, [36], 0o4442],
        [Rewind, [37], 0o4542],
        [Rewind, [38], 0o4642],
        [Rewind, [39], 0o4742],
        [Rewind, [40], 0o5042],
        [Rewind, [41], 0o5142],
        [Rewind, [42], 0o5242],
        [Rewind, [43], 0o5342],
        [Rewind, [44], 0o5442],
        [Rewind, [45], 0o5542],
        [Rewind, [46], 0o5642],
        [Rewind, [47], 0o5742],
        [Rewind, [48], 0o6042],
        [Rewind, [49], 0o6142],
        [Rewind, [50], 0o6242],
        [Rewind, [51], 0o6342],
        [Rewind, [52], 0o6442],
        [Rewind, [53], 0o6542],
        [Rewind, [54], 0o6642],
        [Rewind, [55], 0o6742],
        [Rewind, [56], 0o7042],
        [Rewind, [57], 0o7142],
        [Rewind, [58], 0o7242],
        [Rewind, [59], 0o7342],
        [Rewind, [60], 0o7442],
        [Rewind, [61], 0o7542],
        [Rewind, [62], 0o7642],
        [Rewind, [63], 0o7742]
    ]
    run_tests("TEST: RW args range", testdata)


# ######## PRA ########

def test_PRA_simple():
    testdata = [[PrintAlphabetic, [0, 0, 0, 0], 0o0046]]
    run_tests("TEST: PRA simple", testdata)


def test_PRA_invalid_args():
    testdata = [
        [PrintAlphabetic, [2, 0, 0, 0], 0],
        [PrintAlphabetic, [0, 2, 0, 0], 0],
        [PrintAlphabetic, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: PRA invalid args", testdata)


def test_PRA_args_range():
    testdata = [
        [PrintAlphabetic, [0, 0, 0, 0], 0o0046],
        [PrintAlphabetic, [0, 0, 0, 1], 0o0146],
        [PrintAlphabetic, [0, 0, 1, 0], 0o0246],
        [PrintAlphabetic, [0, 0, 1, 1], 0o0346],
        [PrintAlphabetic, [0, 1, 0, 0], 0o0446],
        [PrintAlphabetic, [0, 1, 0, 1], 0o0546],
        [PrintAlphabetic, [0, 1, 1, 0], 0o0646],
        [PrintAlphabetic, [0, 1, 1, 1], 0o0746],
        [PrintAlphabetic, [1, 0, 0, 0], 0o4046],
        [PrintAlphabetic, [1, 0, 0, 1], 0o4146],
        [PrintAlphabetic, [1, 0, 1, 0], 0o4246],
        [PrintAlphabetic, [1, 0, 1, 1], 0o4346],
        [PrintAlphabetic, [1, 1, 0, 0], 0o4446],
        [PrintAlphabetic, [1, 1, 0, 1], 0o4546],
        [PrintAlphabetic, [1, 1, 1, 0], 0o4646],
        [PrintAlphabetic, [1, 1, 1, 1], 0o4746]
    ]
    run_tests("TEST: PRA args range", testdata)


# ######## PRD ########

def test_PRD_simple():
    testdata = [[PrintDecimal, [0, 0, 0, 0], 0o0046]]
    run_tests("TEST: PRD simple", testdata)


def test_PRD_invalid_args():
    testdata = [
        [PrintDecimal, [2, 0, 0, 0], 0],
        [PrintDecimal, [0, 2, 0, 0], 0],
        [PrintDecimal, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: PRD invalid args", testdata)


def test_PRD_args_range():
    testdata = [
        [PrintDecimal, [0, 0, 0, 0], 0o0046],
        [PrintDecimal, [0, 0, 0, 1], 0o0146],
        [PrintDecimal, [0, 0, 1, 0], 0o0246],
        [PrintDecimal, [0, 0, 1, 1], 0o0346],
        [PrintDecimal, [0, 1, 0, 0], 0o0446],
        [PrintDecimal, [0, 1, 0, 1], 0o0546],
        [PrintDecimal, [0, 1, 1, 0], 0o0646],
        [PrintDecimal, [0, 1, 1, 1], 0o0746],
        [PrintDecimal, [1, 0, 0, 0], 0o4046],
        [PrintDecimal, [1, 0, 0, 1], 0o4146],
        [PrintDecimal, [1, 0, 1, 0], 0o4246],
        [PrintDecimal, [1, 0, 1, 1], 0o4346],
        [PrintDecimal, [1, 1, 0, 0], 0o4446],
        [PrintDecimal, [1, 1, 0, 1], 0o4546],
        [PrintDecimal, [1, 1, 1, 0], 0o4646],
        [PrintDecimal, [1, 1, 1, 1], 0o4746]
    ]
    run_tests("TEST: PRD args range", testdata)


# ######## PRO ########

def test_PRO_simple():
    testdata = [[PrintOctal, [0, 0, 0, 0], 0o0046]]
    run_tests("TEST: PRO simple", testdata)


def test_PRO_invalid_args():
    testdata = [
        [PrintOctal, [2, 0, 0, 0], 0],
        [PrintOctal, [0, 2, 0, 0], 0],
        [PrintOctal, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: PRO invalid args", testdata)


def test_PRO_args_range():
    testdata = [
        [PrintOctal, [0, 0, 0, 0], 0o0046],
        [PrintOctal, [0, 0, 0, 1], 0o0146],
        [PrintOctal, [0, 0, 1, 0], 0o0246],
        [PrintOctal, [0, 0, 1, 1], 0o0346],
        [PrintOctal, [0, 1, 0, 0], 0o0446],
        [PrintOctal, [0, 1, 0, 1], 0o0546],
        [PrintOctal, [0, 1, 1, 0], 0o0646],
        [PrintOctal, [0, 1, 1, 1], 0o0746],
        [PrintOctal, [1, 0, 0, 0], 0o4046],
        [PrintOctal, [1, 0, 0, 1], 0o4146],
        [PrintOctal, [1, 0, 1, 0], 0o4246],
        [PrintOctal, [1, 0, 1, 1], 0o4346],
        [PrintOctal, [1, 1, 0, 0], 0o4446],
        [PrintOctal, [1, 1, 0, 1], 0o4546],
        [PrintOctal, [1, 1, 1, 0], 0o4646],
        [PrintOctal, [1, 1, 1, 1], 0o4746]
    ]
    run_tests("TEST: PRO args range", testdata)


# ######## S ########

def test_S_simple():
    testdata = [[Simulator, [0], 0o0007]]
    run_tests("TEST: S simple", testdata)


def test_S_invalid_args():
    testdata = [
        [Simulator, [2], 0]
    ]
    run_exception_tests("TEST: S invalid args", testdata)


def test_S_args_range():
    testdata = [
        [Simulator, [0], 0o0007],
        [Simulator, [1], 0o4007]
    ]
    run_tests("TEST: S args range", testdata)


# ######## FBA ########

def test_FBA_simple():
    testdata = [[FloatingBinaryAdd, [0, 0, 0, 0], 0o1001]]
    run_tests("TEST: FBA simple", testdata)


def test_FBA_invalid_args():
    testdata = [
        [FloatingBinaryAdd, [2, 0, 0, 0], 0],
        [FloatingBinaryAdd, [0, 2, 0, 0], 0],
        [FloatingBinaryAdd, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FBA invalid args", testdata)


def test_FBA_args_range():
    testdata = [
        [FloatingBinaryAdd, [0, 0, 0, 0], 0o1001],
        [FloatingBinaryAdd, [0, 0, 0, 1], 0o1101],
        [FloatingBinaryAdd, [0, 0, 1, 0], 0o1201],
        [FloatingBinaryAdd, [0, 0, 1, 1], 0o1301],
        [FloatingBinaryAdd, [0, 1, 0, 0], 0o1401],
        [FloatingBinaryAdd, [0, 1, 0, 1], 0o1501],
        [FloatingBinaryAdd, [0, 1, 1, 0], 0o1601],
        [FloatingBinaryAdd, [0, 1, 1, 1], 0o1701],
        [FloatingBinaryAdd, [1, 0, 0, 0], 0o5001],
        [FloatingBinaryAdd, [1, 0, 0, 1], 0o5101],
        [FloatingBinaryAdd, [1, 0, 1, 0], 0o5201],
        [FloatingBinaryAdd, [1, 0, 1, 1], 0o5301],
        [FloatingBinaryAdd, [1, 1, 0, 0], 0o5401],
        [FloatingBinaryAdd, [1, 1, 0, 1], 0o5501],
        [FloatingBinaryAdd, [1, 1, 1, 0], 0o5601],
        [FloatingBinaryAdd, [1, 1, 1, 1], 0o5701]
    ]
    run_tests("TEST: FBA args range", testdata)


# ######## FDA ########

def test_FDA_simple():
    testdata = [[FloatingDecimalAdd, [0, 0, 0, 0], 0o1021]]
    run_tests("TEST: FDA simple", testdata)


def test_FDA_invalid_args():
    testdata = [
        [FloatingDecimalAdd, [2, 0, 0, 0], 0],
        [FloatingDecimalAdd, [0, 2, 0, 0], 0],
        [FloatingDecimalAdd, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FDA invalid args", testdata)


def test_FDA_args_range():
    testdata = [
        [FloatingDecimalAdd, [0, 0, 0, 0], 0o1021],
        [FloatingDecimalAdd, [0, 0, 0, 1], 0o1121],
        [FloatingDecimalAdd, [0, 0, 1, 0], 0o1221],
        [FloatingDecimalAdd, [0, 0, 1, 1], 0o1321],
        [FloatingDecimalAdd, [0, 1, 0, 0], 0o1421],
        [FloatingDecimalAdd, [0, 1, 0, 1], 0o1521],
        [FloatingDecimalAdd, [0, 1, 1, 0], 0o1621],
        [FloatingDecimalAdd, [0, 1, 1, 1], 0o1721],
        [FloatingDecimalAdd, [1, 0, 0, 0], 0o5021],
        [FloatingDecimalAdd, [1, 0, 0, 1], 0o5121],
        [FloatingDecimalAdd, [1, 0, 1, 0], 0o5221],
        [FloatingDecimalAdd, [1, 0, 1, 1], 0o5321],
        [FloatingDecimalAdd, [1, 1, 0, 0], 0o5421],
        [FloatingDecimalAdd, [1, 1, 0, 1], 0o5521],
        [FloatingDecimalAdd, [1, 1, 1, 0], 0o5621],
        [FloatingDecimalAdd, [1, 1, 1, 1], 0o5721]
    ]
    run_tests("TEST: FDA args range", testdata)


# ######## FBS ########

def test_FBS_simple():
    testdata = [[FloatingBinarySubtract, [0, 0, 0, 0], 0o1011]]
    run_tests("TEST: FBS simple", testdata)


def test_FBS_invalid_args():
    testdata = [
        [FloatingBinarySubtract, [2, 0, 0, 0], 0],
        [FloatingBinarySubtract, [0, 2, 0, 0], 0],
        [FloatingBinarySubtract, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FBS invalid args", testdata)


def test_FBS_args_range():
    testdata = [
        [FloatingBinarySubtract, [0, 0, 0, 0], 0o1011],
        [FloatingBinarySubtract, [0, 0, 0, 1], 0o1111],
        [FloatingBinarySubtract, [0, 0, 1, 0], 0o1211],
        [FloatingBinarySubtract, [0, 0, 1, 1], 0o1311],
        [FloatingBinarySubtract, [0, 1, 0, 0], 0o1411],
        [FloatingBinarySubtract, [0, 1, 0, 1], 0o1511],
        [FloatingBinarySubtract, [0, 1, 1, 0], 0o1611],
        [FloatingBinarySubtract, [0, 1, 1, 1], 0o1711],
        [FloatingBinarySubtract, [1, 0, 0, 0], 0o5011],
        [FloatingBinarySubtract, [1, 0, 0, 1], 0o5111],
        [FloatingBinarySubtract, [1, 0, 1, 0], 0o5211],
        [FloatingBinarySubtract, [1, 0, 1, 1], 0o5311],
        [FloatingBinarySubtract, [1, 1, 0, 0], 0o5411],
        [FloatingBinarySubtract, [1, 1, 0, 1], 0o5511],
        [FloatingBinarySubtract, [1, 1, 1, 0], 0o5611],
        [FloatingBinarySubtract, [1, 1, 1, 1], 0o5711]
    ]
    run_tests("TEST: FBS args range", testdata)


# ######## FDS ########

def test_FDS_simple():
    testdata = [[FloatingDecimalSubtract, [0, 0, 0, 0], 0o1031]]
    run_tests("TEST: FDS simple", testdata)


def test_FDS_invalid_args():
    testdata = [
        [FloatingDecimalSubtract, [2, 0, 0, 0], 0],
        [FloatingDecimalSubtract, [0, 2, 0, 0], 0],
        [FloatingDecimalSubtract, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FDS invalid args", testdata)


def test_FDS_args_range():
    testdata = [
        [FloatingDecimalSubtract, [0, 0, 0, 0], 0o1031],
        [FloatingDecimalSubtract, [0, 0, 0, 1], 0o1131],
        [FloatingDecimalSubtract, [0, 0, 1, 0], 0o1231],
        [FloatingDecimalSubtract, [0, 0, 1, 1], 0o1331],
        [FloatingDecimalSubtract, [0, 1, 0, 0], 0o1431],
        [FloatingDecimalSubtract, [0, 1, 0, 1], 0o1531],
        [FloatingDecimalSubtract, [0, 1, 1, 0], 0o1631],
        [FloatingDecimalSubtract, [0, 1, 1, 1], 0o1731],
        [FloatingDecimalSubtract, [1, 0, 0, 0], 0o5031],
        [FloatingDecimalSubtract, [1, 0, 0, 1], 0o5131],
        [FloatingDecimalSubtract, [1, 0, 1, 0], 0o5231],
        [FloatingDecimalSubtract, [1, 0, 1, 1], 0o5331],
        [FloatingDecimalSubtract, [1, 1, 0, 0], 0o5431],
        [FloatingDecimalSubtract, [1, 1, 0, 1], 0o5531],
        [FloatingDecimalSubtract, [1, 1, 1, 0], 0o5631],
        [FloatingDecimalSubtract, [1, 1, 1, 1], 0o5731]
    ]
    run_tests("TEST: FDS args range", testdata)


# ######## FBD ########

def test_FBD_simple():
    testdata = [[FloatingBinaryDivide, [0, 0, 0, 0], 0o1005]]
    run_tests("TEST: FBD simple", testdata)


def test_FBD_invalid_args():
    testdata = [
        [FloatingBinaryDivide, [2, 0, 0, 0], 0],
        [FloatingBinaryDivide, [0, 2, 0, 0], 0],
        [FloatingBinaryDivide, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FBD invalid args", testdata)


def test_FBD_args_range():
    testdata = [
        [FloatingBinaryDivide, [0, 0, 0, 0], 0o1005],
        [FloatingBinaryDivide, [0, 0, 0, 1], 0o1105],
        [FloatingBinaryDivide, [0, 0, 1, 0], 0o1205],
        [FloatingBinaryDivide, [0, 0, 1, 1], 0o1305],
        [FloatingBinaryDivide, [0, 1, 0, 0], 0o1405],
        [FloatingBinaryDivide, [0, 1, 0, 1], 0o1505],
        [FloatingBinaryDivide, [0, 1, 1, 0], 0o1605],
        [FloatingBinaryDivide, [0, 1, 1, 1], 0o1705],
        [FloatingBinaryDivide, [1, 0, 0, 0], 0o5005],
        [FloatingBinaryDivide, [1, 0, 0, 1], 0o5105],
        [FloatingBinaryDivide, [1, 0, 1, 0], 0o5205],
        [FloatingBinaryDivide, [1, 0, 1, 1], 0o5305],
        [FloatingBinaryDivide, [1, 1, 0, 0], 0o5405],
        [FloatingBinaryDivide, [1, 1, 0, 1], 0o5505],
        [FloatingBinaryDivide, [1, 1, 1, 0], 0o5605],
        [FloatingBinaryDivide, [1, 1, 1, 1], 0o5705]
    ]
    run_tests("TEST: FBD args range", testdata)


# ######## FDD ########

def test_FDD_simple():
    testdata = [[FloatingDecimalDivide, [0, 0, 0, 0], 0o1025]]
    run_tests("TEST: FDD simple", testdata)


def test_FDD_invalid_args():
    testdata = [
        [FloatingDecimalDivide, [2, 0, 0, 0], 0],
        [FloatingDecimalDivide, [0, 2, 0, 0], 0],
        [FloatingDecimalDivide, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FDD invalid args", testdata)


def test_FDD_args_range():
    testdata = [
        [FloatingDecimalDivide, [0, 0, 0, 0], 0o1025],
        [FloatingDecimalDivide, [0, 0, 0, 1], 0o1125],
        [FloatingDecimalDivide, [0, 0, 1, 0], 0o1225],
        [FloatingDecimalDivide, [0, 0, 1, 1], 0o1325],
        [FloatingDecimalDivide, [0, 1, 0, 0], 0o1425],
        [FloatingDecimalDivide, [0, 1, 0, 1], 0o1525],
        [FloatingDecimalDivide, [0, 1, 1, 0], 0o1625],
        [FloatingDecimalDivide, [0, 1, 1, 1], 0o1725],
        [FloatingDecimalDivide, [1, 0, 0, 0], 0o5025],
        [FloatingDecimalDivide, [1, 0, 0, 1], 0o5125],
        [FloatingDecimalDivide, [1, 0, 1, 0], 0o5225],
        [FloatingDecimalDivide, [1, 0, 1, 1], 0o5325],
        [FloatingDecimalDivide, [1, 1, 0, 0], 0o5425],
        [FloatingDecimalDivide, [1, 1, 0, 1], 0o5525],
        [FloatingDecimalDivide, [1, 1, 1, 0], 0o5625],
        [FloatingDecimalDivide, [1, 1, 1, 1], 0o5725]
    ]
    run_tests("TEST: FDD args range", testdata)


# ######## FBAU ########

def test_FBAU_simple():
    testdata = [[FloatingBinaryAddUnnormalized, [0, 0, 0, 0], 0o3001]]
    run_tests("TEST: FBAU simple", testdata)


def test_FBAU_invalid_args():
    testdata = [
        [FloatingBinaryAddUnnormalized, [2, 0, 0, 0], 0],
        [FloatingBinaryAddUnnormalized, [0, 2, 0, 0], 0],
        [FloatingBinaryAddUnnormalized, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FBAU invalid args", testdata)


def test_FBAU_args_range():
    testdata = [
        [FloatingBinaryAddUnnormalized, [0, 0, 0, 0], 0o3001],
        [FloatingBinaryAddUnnormalized, [0, 0, 0, 1], 0o3101],
        [FloatingBinaryAddUnnormalized, [0, 0, 1, 0], 0o3201],
        [FloatingBinaryAddUnnormalized, [0, 0, 1, 1], 0o3301],
        [FloatingBinaryAddUnnormalized, [0, 1, 0, 0], 0o3401],
        [FloatingBinaryAddUnnormalized, [0, 1, 0, 1], 0o3501],
        [FloatingBinaryAddUnnormalized, [0, 1, 1, 0], 0o3601],
        [FloatingBinaryAddUnnormalized, [0, 1, 1, 1], 0o3701],
        [FloatingBinaryAddUnnormalized, [1, 0, 0, 0], 0o7001],
        [FloatingBinaryAddUnnormalized, [1, 0, 0, 1], 0o7101],
        [FloatingBinaryAddUnnormalized, [1, 0, 1, 0], 0o7201],
        [FloatingBinaryAddUnnormalized, [1, 0, 1, 1], 0o7301],
        [FloatingBinaryAddUnnormalized, [1, 1, 0, 0], 0o7401],
        [FloatingBinaryAddUnnormalized, [1, 1, 0, 1], 0o7501],
        [FloatingBinaryAddUnnormalized, [1, 1, 1, 0], 0o7601],
        [FloatingBinaryAddUnnormalized, [1, 1, 1, 1], 0o7701]
    ]
    run_tests("TEST: FBAU args range", testdata)


# ######## FDAU ########

def test_FDAU_simple():
    testdata = [[FloatingDecimalAddUnnormalized, [0, 0, 0, 0], 0o3021]]
    run_tests("TEST: FDAU simple", testdata)


def test_FDAU_invalid_args():
    testdata = [
        [FloatingDecimalAddUnnormalized, [2, 0, 0, 0], 0],
        [FloatingDecimalAddUnnormalized, [0, 2, 0, 0], 0],
        [FloatingDecimalAddUnnormalized, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FDAU invalid args", testdata)


def test_FDAU_args_range():
    testdata = [
        [FloatingDecimalAddUnnormalized, [0, 0, 0, 0], 0o3021],
        [FloatingDecimalAddUnnormalized, [0, 0, 0, 1], 0o3121],
        [FloatingDecimalAddUnnormalized, [0, 0, 1, 0], 0o3221],
        [FloatingDecimalAddUnnormalized, [0, 0, 1, 1], 0o3321],
        [FloatingDecimalAddUnnormalized, [0, 1, 0, 0], 0o3421],
        [FloatingDecimalAddUnnormalized, [0, 1, 0, 1], 0o3521],
        [FloatingDecimalAddUnnormalized, [0, 1, 1, 0], 0o3621],
        [FloatingDecimalAddUnnormalized, [0, 1, 1, 1], 0o3721],
        [FloatingDecimalAddUnnormalized, [1, 0, 0, 0], 0o7021],
        [FloatingDecimalAddUnnormalized, [1, 0, 0, 1], 0o7121],
        [FloatingDecimalAddUnnormalized, [1, 0, 1, 0], 0o7221],
        [FloatingDecimalAddUnnormalized, [1, 0, 1, 1], 0o7321],
        [FloatingDecimalAddUnnormalized, [1, 1, 0, 0], 0o7421],
        [FloatingDecimalAddUnnormalized, [1, 1, 0, 1], 0o7521],
        [FloatingDecimalAddUnnormalized, [1, 1, 1, 0], 0o7621],
        [FloatingDecimalAddUnnormalized, [1, 1, 1, 1], 0o7721]
    ]
    run_tests("TEST: FDAU args range", testdata)


# ######## FBSU ########

def test_FBSU_simple():
    testdata = [[FloatingBinarySubtractUnnormalized, [0, 0, 0, 0], 0o3011]]
    run_tests("TEST: FBSU simple", testdata)


def test_FBSU_invalid_args():
    testdata = [
        [FloatingBinarySubtractUnnormalized, [2, 0, 0, 0], 0],
        [FloatingBinarySubtractUnnormalized, [0, 2, 0, 0], 0],
        [FloatingBinarySubtractUnnormalized, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FBSU invalid args", testdata)


def test_FBSU_args_range():
    testdata = [
        [FloatingBinarySubtractUnnormalized, [0, 0, 0, 0], 0o3011],
        [FloatingBinarySubtractUnnormalized, [0, 0, 0, 1], 0o3111],
        [FloatingBinarySubtractUnnormalized, [0, 0, 1, 0], 0o3211],
        [FloatingBinarySubtractUnnormalized, [0, 0, 1, 1], 0o3311],
        [FloatingBinarySubtractUnnormalized, [0, 1, 0, 0], 0o3411],
        [FloatingBinarySubtractUnnormalized, [0, 1, 0, 1], 0o3511],
        [FloatingBinarySubtractUnnormalized, [0, 1, 1, 0], 0o3611],
        [FloatingBinarySubtractUnnormalized, [0, 1, 1, 1], 0o3711],
        [FloatingBinarySubtractUnnormalized, [1, 0, 0, 0], 0o7011],
        [FloatingBinarySubtractUnnormalized, [1, 0, 0, 1], 0o7111],
        [FloatingBinarySubtractUnnormalized, [1, 0, 1, 0], 0o7211],
        [FloatingBinarySubtractUnnormalized, [1, 0, 1, 1], 0o7311],
        [FloatingBinarySubtractUnnormalized, [1, 1, 0, 0], 0o7411],
        [FloatingBinarySubtractUnnormalized, [1, 1, 0, 1], 0o7511],
        [FloatingBinarySubtractUnnormalized, [1, 1, 1, 0], 0o7611],
        [FloatingBinarySubtractUnnormalized, [1, 1, 1, 1], 0o7711]
    ]
    run_tests("TEST: FBSU args range", testdata)


# ######## FDSU ########

def test_FDSU_simple():
    testdata = [[FloatingDecimalSubtractUnnormalized, [0, 0, 0, 0], 0o3031]]
    run_tests("TEST: FDSU simple", testdata)


def test_FDSU_invalid_args():
    testdata = [
        [FloatingDecimalSubtractUnnormalized, [2, 0, 0, 0], 0],
        [FloatingDecimalSubtractUnnormalized, [0, 2, 0, 0], 0],
        [FloatingDecimalSubtractUnnormalized, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FDSU invalid args", testdata)


def test_FDSU_args_range():
    testdata = [
        [FloatingDecimalSubtractUnnormalized, [0, 0, 0, 0], 0o3031],
        [FloatingDecimalSubtractUnnormalized, [0, 0, 0, 1], 0o3131],
        [FloatingDecimalSubtractUnnormalized, [0, 0, 1, 0], 0o3231],
        [FloatingDecimalSubtractUnnormalized, [0, 0, 1, 1], 0o3331],
        [FloatingDecimalSubtractUnnormalized, [0, 1, 0, 0], 0o3431],
        [FloatingDecimalSubtractUnnormalized, [0, 1, 0, 1], 0o3531],
        [FloatingDecimalSubtractUnnormalized, [0, 1, 1, 0], 0o3631],
        [FloatingDecimalSubtractUnnormalized, [0, 1, 1, 1], 0o3731],
        [FloatingDecimalSubtractUnnormalized, [1, 0, 0, 0], 0o7031],
        [FloatingDecimalSubtractUnnormalized, [1, 0, 0, 1], 0o7131],
        [FloatingDecimalSubtractUnnormalized, [1, 0, 1, 0], 0o7231],
        [FloatingDecimalSubtractUnnormalized, [1, 0, 1, 1], 0o7331],
        [FloatingDecimalSubtractUnnormalized, [1, 1, 0, 0], 0o7431],
        [FloatingDecimalSubtractUnnormalized, [1, 1, 0, 1], 0o7531],
        [FloatingDecimalSubtractUnnormalized, [1, 1, 1, 0], 0o7631],
        [FloatingDecimalSubtractUnnormalized, [1, 1, 1, 1], 0o7731]
    ]
    run_tests("TEST: FDSU args range", testdata)


# ######## FBM ########

def test_FBM_simple():
    testdata = [[FloatingBinaryMultiply, [0, 0, 0, 0], 0o3005]]
    run_tests("TEST: FBM simple", testdata)


def test_FBM_invalid_args():
    testdata = [
        [FloatingBinaryMultiply, [2, 0, 0, 0], 0],
        [FloatingBinaryMultiply, [0, 2, 0, 0], 0],
        [FloatingBinaryMultiply, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FBM invalid args", testdata)


def test_FBM_args_range():
    testdata = [
        [FloatingBinaryMultiply, [0, 0, 0, 0], 0o3005],
        [FloatingBinaryMultiply, [0, 0, 0, 1], 0o3105],
        [FloatingBinaryMultiply, [0, 0, 1, 0], 0o3205],
        [FloatingBinaryMultiply, [0, 0, 1, 1], 0o3305],
        [FloatingBinaryMultiply, [0, 1, 0, 0], 0o3405],
        [FloatingBinaryMultiply, [0, 1, 0, 1], 0o3505],
        [FloatingBinaryMultiply, [0, 1, 1, 0], 0o3605],
        [FloatingBinaryMultiply, [0, 1, 1, 1], 0o3705],
        [FloatingBinaryMultiply, [1, 0, 0, 0], 0o7005],
        [FloatingBinaryMultiply, [1, 0, 0, 1], 0o7105],
        [FloatingBinaryMultiply, [1, 0, 1, 0], 0o7205],
        [FloatingBinaryMultiply, [1, 0, 1, 1], 0o7305],
        [FloatingBinaryMultiply, [1, 1, 0, 0], 0o7405],
        [FloatingBinaryMultiply, [1, 1, 0, 1], 0o7505],
        [FloatingBinaryMultiply, [1, 1, 1, 0], 0o7605],
        [FloatingBinaryMultiply, [1, 1, 1, 1], 0o7705]
    ]
    run_tests("TEST: FBM args range", testdata)


# ######## FDM ########

def test_FDM_simple():
    testdata = [[FloatingDecimalMultiply, [0, 0, 0, 0], 0o3025]]
    run_tests("TEST: FDM simple", testdata)


def test_FDM_invalid_args():
    testdata = [
        [FloatingDecimalMultiply, [2, 0, 0, 0], 0],
        [FloatingDecimalMultiply, [0, 2, 0, 0], 0],
        [FloatingDecimalMultiply, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FDM invalid args", testdata)


def test_FDM_args_range():
    testdata = [
        [FloatingDecimalMultiply, [0, 0, 0, 0], 0o3025],
        [FloatingDecimalMultiply, [0, 0, 0, 1], 0o3125],
        [FloatingDecimalMultiply, [0, 0, 1, 0], 0o3225],
        [FloatingDecimalMultiply, [0, 0, 1, 1], 0o3325],
        [FloatingDecimalMultiply, [0, 1, 0, 0], 0o3425],
        [FloatingDecimalMultiply, [0, 1, 0, 1], 0o3525],
        [FloatingDecimalMultiply, [0, 1, 1, 0], 0o3625],
        [FloatingDecimalMultiply, [0, 1, 1, 1], 0o3725],
        [FloatingDecimalMultiply, [1, 0, 0, 0], 0o7025],
        [FloatingDecimalMultiply, [1, 0, 0, 1], 0o7125],
        [FloatingDecimalMultiply, [1, 0, 1, 0], 0o7225],
        [FloatingDecimalMultiply, [1, 0, 1, 1], 0o7325],
        [FloatingDecimalMultiply, [1, 1, 0, 0], 0o7425],
        [FloatingDecimalMultiply, [1, 1, 0, 1], 0o7525],
        [FloatingDecimalMultiply, [1, 1, 1, 0], 0o7625],
        [FloatingDecimalMultiply, [1, 1, 1, 1], 0o7725]
    ]
    run_tests("TEST: FDM args range", testdata)


# ######## ULD ########

def test_ULD_simple():
    testdata = [[MultipleUnload, [0, 0, 0, 0], 0o3015]]
    run_tests("TEST: ULD simple", testdata)


def test_ULD_invalid_args():
    testdata = [
        [MultipleUnload, [2, 0, 0, 0], 0],
        [MultipleUnload, [0, 2, 0, 0], 0],
        [MultipleUnload, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: ULD invalid args", testdata)


def test_ULD_args_range():
    testdata = [
        [MultipleUnload, [0, 0, 0, 0], 0o3015],
        [MultipleUnload, [0, 0, 0, 1], 0o3115],
        [MultipleUnload, [0, 0, 1, 0], 0o3215],
        [MultipleUnload, [0, 0, 1, 1], 0o3315],
        [MultipleUnload, [0, 1, 0, 0], 0o3415],
        [MultipleUnload, [0, 1, 0, 1], 0o3515],
        [MultipleUnload, [0, 1, 1, 0], 0o3615],
        [MultipleUnload, [0, 1, 1, 1], 0o3715],
        [MultipleUnload, [1, 0, 0, 0], 0o7015],
        [MultipleUnload, [1, 0, 0, 1], 0o7115],
        [MultipleUnload, [1, 0, 1, 0], 0o7215],
        [MultipleUnload, [1, 0, 1, 1], 0o7315],
        [MultipleUnload, [1, 1, 0, 0], 0o7415],
        [MultipleUnload, [1, 1, 0, 1], 0o7515],
        [MultipleUnload, [1, 1, 1, 0], 0o7615],
        [MultipleUnload, [1, 1, 1, 1], 0o7715]
    ]
    run_tests("TEST: ULD args range", testdata)


# ######## FBAE ########

def test_FBAE_simple():
    testdata = [[FloatingBinaryAddExtendedPrecision, [0, 0, 0, 0], 0o0001]]
    run_tests("TEST: FBAE simple", testdata)


def test_FBAE_invalid_args():
    testdata = [
        [FloatingBinaryAddExtendedPrecision, [2, 0, 0, 0], 0],
        [FloatingBinaryAddExtendedPrecision, [0, 2, 0, 0], 0],
        [FloatingBinaryAddExtendedPrecision, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FBAE invalid args", testdata)


def test_FBAE_args_range():
    testdata = [
        [FloatingBinaryAddExtendedPrecision, [0, 0, 0, 0], 0o0001],
        [FloatingBinaryAddExtendedPrecision, [0, 0, 0, 1], 0o0101],
        [FloatingBinaryAddExtendedPrecision, [0, 0, 1, 0], 0o0201],
        [FloatingBinaryAddExtendedPrecision, [0, 0, 1, 1], 0o0301],
        [FloatingBinaryAddExtendedPrecision, [0, 1, 0, 0], 0o0401],
        [FloatingBinaryAddExtendedPrecision, [0, 1, 0, 1], 0o0501],
        [FloatingBinaryAddExtendedPrecision, [0, 1, 1, 0], 0o0601],
        [FloatingBinaryAddExtendedPrecision, [0, 1, 1, 1], 0o0701],
        [FloatingBinaryAddExtendedPrecision, [1, 0, 0, 0], 0o4001],
        [FloatingBinaryAddExtendedPrecision, [1, 0, 0, 1], 0o4101],
        [FloatingBinaryAddExtendedPrecision, [1, 0, 1, 0], 0o4201],
        [FloatingBinaryAddExtendedPrecision, [1, 0, 1, 1], 0o4301],
        [FloatingBinaryAddExtendedPrecision, [1, 1, 0, 0], 0o4401],
        [FloatingBinaryAddExtendedPrecision, [1, 1, 0, 1], 0o4501],
        [FloatingBinaryAddExtendedPrecision, [1, 1, 1, 0], 0o4601],
        [FloatingBinaryAddExtendedPrecision, [1, 1, 1, 1], 0o4701]
    ]
    run_tests("TEST: FBAE args range", testdata)


# ######## FBSE ########

def test_FBSE_simple():
    testdata = [[FloatingBinarySubtractExtendedPrecision, [0, 0, 0, 0], 0o0011]]
    run_tests("TEST: FBSE simple", testdata)


def test_FBSE_invalid_args():
    testdata = [
        [FloatingBinarySubtractExtendedPrecision, [2, 0, 0, 0], 0],
        [FloatingBinarySubtractExtendedPrecision, [0, 2, 0, 0], 0],
        [FloatingBinarySubtractExtendedPrecision, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FBSE invalid args", testdata)


def test_FBSE_args_range():
    testdata = [
        [FloatingBinarySubtractExtendedPrecision, [0, 0, 0, 0], 0o0011],
        [FloatingBinarySubtractExtendedPrecision, [0, 0, 0, 1], 0o0111],
        [FloatingBinarySubtractExtendedPrecision, [0, 0, 1, 0], 0o0211],
        [FloatingBinarySubtractExtendedPrecision, [0, 0, 1, 1], 0o0311],
        [FloatingBinarySubtractExtendedPrecision, [0, 1, 0, 0], 0o0411],
        [FloatingBinarySubtractExtendedPrecision, [0, 1, 0, 1], 0o0511],
        [FloatingBinarySubtractExtendedPrecision, [0, 1, 1, 0], 0o0611],
        [FloatingBinarySubtractExtendedPrecision, [0, 1, 1, 1], 0o0711],
        [FloatingBinarySubtractExtendedPrecision, [1, 0, 0, 0], 0o4011],
        [FloatingBinarySubtractExtendedPrecision, [1, 0, 0, 1], 0o4111],
        [FloatingBinarySubtractExtendedPrecision, [1, 0, 1, 0], 0o4211],
        [FloatingBinarySubtractExtendedPrecision, [1, 0, 1, 1], 0o4311],
        [FloatingBinarySubtractExtendedPrecision, [1, 1, 0, 0], 0o4411],
        [FloatingBinarySubtractExtendedPrecision, [1, 1, 0, 1], 0o4511],
        [FloatingBinarySubtractExtendedPrecision, [1, 1, 1, 0], 0o4611],
        [FloatingBinarySubtractExtendedPrecision, [1, 1, 1, 1], 0o4711]
    ]
    run_tests("TEST: FBSE args range", testdata)


# ######## BD ########

def test_BD_simple():
    testdata = [[FixedBinaryDivide, [0, 0, 0, 0], 0o0005]]
    run_tests("TEST: BD simple", testdata)


def test_BD_invalid_args():
    testdata = [
        [FixedBinaryDivide, [2, 0, 0, 0], 0],
        [FixedBinaryDivide, [0, 2, 0, 0], 0],
        [FixedBinaryDivide, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: BD invalid args", testdata)


def test_BD_args_range():
    testdata = [
        [FixedBinaryDivide, [0, 0, 0, 0], 0o0005],
        [FixedBinaryDivide, [0, 0, 0, 1], 0o0105],
        [FixedBinaryDivide, [0, 0, 1, 0], 0o0205],
        [FixedBinaryDivide, [0, 0, 1, 1], 0o0305],
        [FixedBinaryDivide, [0, 1, 0, 0], 0o0405],
        [FixedBinaryDivide, [0, 1, 0, 1], 0o0505],
        [FixedBinaryDivide, [0, 1, 1, 0], 0o0605],
        [FixedBinaryDivide, [0, 1, 1, 1], 0o0705],
        [FixedBinaryDivide, [1, 0, 0, 0], 0o4005],
        [FixedBinaryDivide, [1, 0, 0, 1], 0o4105],
        [FixedBinaryDivide, [1, 0, 1, 0], 0o4205],
        [FixedBinaryDivide, [1, 0, 1, 1], 0o4305],
        [FixedBinaryDivide, [1, 1, 0, 0], 0o4405],
        [FixedBinaryDivide, [1, 1, 0, 1], 0o4505],
        [FixedBinaryDivide, [1, 1, 1, 0], 0o4605],
        [FixedBinaryDivide, [1, 1, 1, 1], 0o4705]
    ]
    run_tests("TEST: BD args range", testdata)


# ######## DD ########

def test_DD_simple():
    testdata = [[FixedDecimalDivide, [0, 0, 0, 0], 0o0025]]
    run_tests("TEST: DD simple", testdata)


def test_DD_invalid_args():
    testdata = [
        [FixedDecimalDivide, [2, 0, 0, 0], 0],
        [FixedDecimalDivide, [0, 2, 0, 0], 0],
        [FixedDecimalDivide, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: DD invalid args", testdata)


def test_DD_args_range():
    testdata = [
        [FixedDecimalDivide, [0, 0, 0, 0], 0o0025],
        [FixedDecimalDivide, [0, 0, 0, 1], 0o0125],
        [FixedDecimalDivide, [0, 0, 1, 0], 0o0225],
        [FixedDecimalDivide, [0, 0, 1, 1], 0o0325],
        [FixedDecimalDivide, [0, 1, 0, 0], 0o0425],
        [FixedDecimalDivide, [0, 1, 0, 1], 0o0525],
        [FixedDecimalDivide, [0, 1, 1, 0], 0o0625],
        [FixedDecimalDivide, [0, 1, 1, 1], 0o0725],
        [FixedDecimalDivide, [1, 0, 0, 0], 0o4025],
        [FixedDecimalDivide, [1, 0, 0, 1], 0o4125],
        [FixedDecimalDivide, [1, 0, 1, 0], 0o4225],
        [FixedDecimalDivide, [1, 0, 1, 1], 0o4325],
        [FixedDecimalDivide, [1, 1, 0, 0], 0o4425],
        [FixedDecimalDivide, [1, 1, 0, 1], 0o4525],
        [FixedDecimalDivide, [1, 1, 1, 0], 0o4625],
        [FixedDecimalDivide, [1, 1, 1, 1], 0o4725]
    ]
    run_tests("TEST: DD args range", testdata)


# ######## FFN ########

def test_FFN_simple():
    testdata = [[FixedToFloatingNormalize, [0, 0, 0, 0], 0o0015]]
    run_tests("TEST: FFN simple", testdata)


def test_FFN_invalid_args():
    testdata = [
        [FixedToFloatingNormalize, [2, 0, 0, 0], 0],
        [FixedToFloatingNormalize, [0, 2, 0, 0], 0],
        [FixedToFloatingNormalize, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FFN invalid args", testdata)


def test_FFN_args_range():
    testdata = [
        [FixedToFloatingNormalize, [0, 0, 0, 0], 0o0015],
        [FixedToFloatingNormalize, [0, 0, 0, 1], 0o0115],
        [FixedToFloatingNormalize, [0, 0, 1, 0], 0o0215],
        [FixedToFloatingNormalize, [0, 0, 1, 1], 0o0315],
        [FixedToFloatingNormalize, [0, 1, 0, 0], 0o0415],
        [FixedToFloatingNormalize, [0, 1, 0, 1], 0o0515],
        [FixedToFloatingNormalize, [0, 1, 1, 0], 0o0615],
        [FixedToFloatingNormalize, [0, 1, 1, 1], 0o0715],
        [FixedToFloatingNormalize, [1, 0, 0, 0], 0o4015],
        [FixedToFloatingNormalize, [1, 0, 0, 1], 0o4115],
        [FixedToFloatingNormalize, [1, 0, 1, 0], 0o4215],
        [FixedToFloatingNormalize, [1, 0, 1, 1], 0o4315],
        [FixedToFloatingNormalize, [1, 1, 0, 0], 0o4415],
        [FixedToFloatingNormalize, [1, 1, 0, 1], 0o4515],
        [FixedToFloatingNormalize, [1, 1, 1, 0], 0o4615],
        [FixedToFloatingNormalize, [1, 1, 1, 1], 0o4715]
    ]
    run_tests("TEST: FFN args range", testdata)


# ######## FCON ########

def test_FCON_simple():
    testdata = [[Conversion, [0, 0, 0, 0], 0o0035]]
    run_tests("TEST: FCON simple", testdata)


def test_FCON_invalid_args():
    testdata = [
        [Conversion, [2, 0, 0, 0], 0],
        [Conversion, [0, 2, 0, 0], 0],
        [Conversion, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FCON invalid args", testdata)


def test_FCON_args_range():
    testdata = [
        [Conversion, [0, 0, 0, 0], 0o0035],
        [Conversion, [0, 0, 0, 1], 0o0135],
        [Conversion, [0, 0, 1, 0], 0o0235],
        [Conversion, [0, 0, 1, 1], 0o0335],
        [Conversion, [0, 1, 0, 0], 0o0435],
        [Conversion, [0, 1, 0, 1], 0o0535],
        [Conversion, [0, 1, 1, 0], 0o0635],
        [Conversion, [0, 1, 1, 1], 0o0735],
        [Conversion, [1, 0, 0, 0], 0o4035],
        [Conversion, [1, 0, 0, 1], 0o4135],
        [Conversion, [1, 0, 1, 0], 0o4235],
        [Conversion, [1, 0, 1, 1], 0o4335],
        [Conversion, [1, 1, 0, 0], 0o4435],
        [Conversion, [1, 1, 0, 1], 0o4535],
        [Conversion, [1, 1, 1, 0], 0o4635],
        [Conversion, [1, 1, 1, 1], 0o4735]
    ]
    run_tests("TEST: FCON args range", testdata)


# ######## FLN ########

def test_FLN_simple():
    testdata = [[FloatingLessThanNormalized, [0, 0, 0, 0], 0o0030]]
    run_tests("TEST: FLN simple", testdata)


def test_FLN_invalid_args():
    testdata = [
        [FloatingLessThanNormalized, [2, 0, 0, 0], 0],
        [FloatingLessThanNormalized, [0, 2, 0, 0], 0],
        [FloatingLessThanNormalized, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FLN invalid args", testdata)


def test_FLN_args_range():
    testdata = [
        [FloatingLessThanNormalized, [0, 0, 0, 0], 0o0030],
        [FloatingLessThanNormalized, [0, 0, 0, 1], 0o0130],
        [FloatingLessThanNormalized, [0, 0, 1, 0], 0o0230],
        [FloatingLessThanNormalized, [0, 0, 1, 1], 0o0330],
        [FloatingLessThanNormalized, [0, 1, 0, 0], 0o0430],
        [FloatingLessThanNormalized, [0, 1, 0, 1], 0o0530],
        [FloatingLessThanNormalized, [0, 1, 1, 0], 0o0630],
        [FloatingLessThanNormalized, [0, 1, 1, 1], 0o0730],
        [FloatingLessThanNormalized, [1, 0, 0, 0], 0o4030],
        [FloatingLessThanNormalized, [1, 0, 0, 1], 0o4130],
        [FloatingLessThanNormalized, [1, 0, 1, 0], 0o4230],
        [FloatingLessThanNormalized, [1, 0, 1, 1], 0o4330],
        [FloatingLessThanNormalized, [1, 1, 0, 0], 0o4430],
        [FloatingLessThanNormalized, [1, 1, 0, 1], 0o4530],
        [FloatingLessThanNormalized, [1, 1, 1, 0], 0o4630],
        [FloatingLessThanNormalized, [1, 1, 1, 1], 0o4730]
    ]
    run_tests("TEST: FLN args range", testdata)


# ######## FNN ########

def test_FNN_simple():
    testdata = [[FloatingNotEqualNormalized, [0, 0, 0, 0], 0o2014]]
    run_tests("TEST: FNN simple", testdata)


def test_FNN_invalid_args():
    testdata = [
        [FloatingNotEqualNormalized, [2, 0, 0, 0], 0],
        [FloatingNotEqualNormalized, [0, 2, 0, 0], 0],
        [FloatingNotEqualNormalized, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FNN invalid args", testdata)


def test_FNN_args_range():
    testdata = [
        [FloatingNotEqualNormalized, [0, 0, 0, 0], 0o2014],
        [FloatingNotEqualNormalized, [0, 0, 0, 1], 0o2114],
        [FloatingNotEqualNormalized, [0, 0, 1, 0], 0o2214],
        [FloatingNotEqualNormalized, [0, 0, 1, 1], 0o2314],
        [FloatingNotEqualNormalized, [0, 1, 0, 0], 0o2414],
        [FloatingNotEqualNormalized, [0, 1, 0, 1], 0o2514],
        [FloatingNotEqualNormalized, [0, 1, 1, 0], 0o2614],
        [FloatingNotEqualNormalized, [0, 1, 1, 1], 0o2714],
        [FloatingNotEqualNormalized, [1, 0, 0, 0], 0o6014],
        [FloatingNotEqualNormalized, [1, 0, 0, 1], 0o6114],
        [FloatingNotEqualNormalized, [1, 0, 1, 0], 0o6214],
        [FloatingNotEqualNormalized, [1, 0, 1, 1], 0o6314],
        [FloatingNotEqualNormalized, [1, 1, 0, 0], 0o6414],
        [FloatingNotEqualNormalized, [1, 1, 0, 1], 0o6514],
        [FloatingNotEqualNormalized, [1, 1, 1, 0], 0o6614],
        [FloatingNotEqualNormalized, [1, 1, 1, 1], 0o6714]
    ]
    run_tests("TEST: FNN args range", testdata)


# ######## ALF ########

def test_ALF_simple():
    testdata = [[AlphanumericConstant, [0], 0o0]]
    run_tests("TEST: ALF simple", testdata)


def test_ALF_invalid_args():
    testdata = [
        [AlphanumericConstant, [-1], 0],
        [AlphanumericConstant, [2 ** 48], 0]
    ]
    run_exception_tests("TEST: ALF invalid args", testdata)


def test_ALF_args_range():
    testdata = [
        [AlphanumericConstant, [0], 0],
        [AlphanumericConstant, [1], 1],
        [AlphanumericConstant, [4095], 4095],
        [AlphanumericConstant, [4096], 4096],
        [AlphanumericConstant, [2 ** 48 - 1], 2 ** 48 - 1],
    ]
    run_tests("TEST: ALF args range", testdata)

