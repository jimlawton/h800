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
    c = BinaryAddMasked
    testdata = [
        [c, [0, 0], 0o0051],
        [c, [0, 1], 0o0151]
    ]
    run_tests("TEST: BA (masked): simple", testdata)


def test_BA_masked_invalid_args():
    c = BinaryAddMasked
    testdata = [
        [c, [0, 32], 0],
        [c, [2, 0], 0]
    ]
    run_exception_tests("TEST: BA (masked): invalid args", testdata)


def test_BA_masked_args_range():
    c = BinaryAddMasked
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, [i, j], make_masked_opcode("BA", i, j)])
    run_tests("TEST: BA (masked): args range", testdata)


def test_BA_unmasked_simple():
    c = BinaryAddUnmasked
    testdata = [[c, [0, 0, 0, 0], make_unmasked_opcode("BA", 0, 0, 0, 0)]]
    run_tests("TEST: BA (unmasked): simple", testdata)


def test_BA_unmasked_invalid_args():
    c = BinaryAddUnmasked
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: BA (unmasked): invalid args", testdata)


def test_BA_unmasked_args_range():
    c = BinaryAddUnmasked
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("BA", i, j, k, l)])
    run_tests("TEST: BA (unmasked): args range", testdata)


# ######## DA ########

def test_DA_masked_simple():
    c = DecimalAddMasked
    testdata = [[c, [0, 0], 0o41]]
    run_tests("TEST: DA (masked): simple", testdata)


def test_DA_masked_invalid_args():
    c = DecimalAddMasked
    testdata = [
        [c, [0, 32], 0],
        [c, [2, 0], 0]
    ]
    run_exception_tests("TEST: DA (masked): invalid args", testdata)


def test_DA_masked_args_range():
    c = DecimalAddMasked
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, [i, j], make_masked_opcode("DA", i, j)])
    run_tests("TEST: DA (masked): args range", testdata)


def test_DA_unmasked_simple():
    c = DecimalAddUnmasked
    testdata = [[c, [0, 0, 0, 0], 0o2001]]
    run_tests("TEST: DA (unmasked): simple", testdata)


def test_DA_unmasked_invalid_args():
    c = DecimalAddUnmasked
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: DA (unmasked): invalid args", testdata)


def test_DA_unmasked_args_range():
    c = DecimalAddUnmasked
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("DA", i, j, k, l)])
    run_tests("TEST: DA (unmasked): args range", testdata)


# ######## WA ########

def test_WA_masked_simple():
    c = WordAddMasked
    testdata = [[c, [0, 0], 0o55]]
    run_tests("TEST: WA (masked): simple", testdata)


def test_WA_masked_invalid_args():
    c = WordAddMasked
    testdata = [
        [c, [0, 32], 0],
        [c, [2, 0], 0]
    ]
    run_exception_tests("TEST: WA (masked): invalid args", testdata)


def test_WA_masked_args_range():
    c = WordAddMasked
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, [i, j], make_masked_opcode("WA", i, j)])
    run_tests("TEST: WA (masked): args range", testdata)


def test_WA_unmasked_simple():
    c = WordAddUnmasked
    testdata = [[c, [0, 0, 0, 0], 0o2015]]
    run_tests("TEST: WA (unmasked): simple", testdata)


def test_WA_unmasked_invalid_args():
    c = WordAddUnmasked
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: WA (unmasked): invalid args", testdata)


def test_WA_unmasked_args_range():
    c = WordAddUnmasked
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("WA", i, j, k, l)])
    run_tests("TEST: WA (unmasked): args range", testdata)


# ######## BS ########

def test_BS_masked_simple():
    c = BinarySubtractMasked
    testdata = [[c, [0, 0], 0o71]]
    run_tests("TEST: BS (masked): simple", testdata)


def test_BS_masked_invalid_args():
    c = BinarySubtractMasked
    testdata = [
        [c, [0, 32], 0],
        [c, [2, 0], 0]
    ]
    run_exception_tests("TEST: BS (masked): invalid args", testdata)


def test_BS_masked_args_range():
    c = BinarySubtractMasked
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, [i, j], make_masked_opcode("BS", i, j)])
    run_tests("TEST: BS (masked): args range", testdata)


def test_BS_unmasked_simple():
    c = BinarySubtractUnmasked
    testdata = [[c, [0, 0, 0, 0], 0o2031]]
    run_tests("TEST: BS (unmasked): simple", testdata)


def test_BS_unmasked_invalid_args():
    c = BinarySubtractUnmasked
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: BS (unmasked): invalid args", testdata)


def test_BS_unmasked_args_range():
    c = BinarySubtractUnmasked
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("BS", i, j, k, l)])
    run_tests("TEST: BS (unmasked): args range", testdata)


# ######## DS ########

def test_DS_masked_simple():
    c = DecimalSubtractMasked
    testdata = [[c, [0, 0], 0o61]]
    run_tests("TEST: DS (masked): simple", testdata)


def test_DS_masked_invalid_args():
    c = DecimalSubtractMasked
    testdata = [
        [c, [0, 32], 0],
        [c, [2, 0], 0]
    ]
    run_exception_tests("TEST: DS (masked): invalid args", testdata)


def test_DS_masked_args_range():
    c = DecimalSubtractMasked
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, [i, j], make_masked_opcode("DS", i, j)])
    run_tests("TEST: DS (masked): args range", testdata)


def test_DS_unmasked_simple():
    c = DecimalSubtractUnmasked
    testdata = [[c, [0, 0, 0, 0], 0o2021]]
    run_tests("TEST: DS (unmasked): simple", testdata)


def test_DS_unmasked_invalid_args():
    c = DecimalSubtractUnmasked
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: DS (unmasked): invalid args", testdata)


def test_DS_unmasked_args_range():
    c = DecimalSubtractUnmasked
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("DS", i, j, k, l)])
    run_tests("TEST: DS (unmasked): args range", testdata)


# ######## WD ########

def test_WD_masked_simple():
    c = WordDifferenceMasked
    testdata = [[c, [0, 0], 0o75]]
    run_tests("TEST: WD (masked): simple", testdata)


def test_WD_masked_invalid_args():
    c = WordDifferenceMasked
    testdata = [
        [c, [0, 32], 0],
        [c, [2, 0], 0]
    ]
    run_exception_tests("TEST: WD (masked): invalid args", testdata)


def test_WD_masked_args_range():
    c = WordDifferenceMasked
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, [i, j], make_masked_opcode("WD", i, j)])
    run_tests("TEST: WD (masked): args range", testdata)


def test_WD_unmasked_simple():
    c = WordDifferenceUnmasked
    testdata = [[c, [0, 0, 0, 0], 0o2035]]
    run_tests("TEST: WD (unmasked): simple", testdata)


def test_WD_unmasked_invalid_args():
    c = WordDifferenceUnmasked
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: WD (unmasked): invalid args", testdata)


def test_WD_unmasked_args_range():
    c = WordDifferenceUnmasked
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("WD", i, j, k, l)])
    run_tests("TEST: WD (unmasked): args range", testdata)


# ######## NA ########

def test_NA_masked_simple():
    c = NotEqualAlphabeticMasked
    testdata = [[c, [0, 0], 0o54]]
    run_tests("TEST: NA (masked): simple", testdata)


def test_NA_masked_invalid_args():
    c = NotEqualAlphabeticMasked
    testdata = [
        [c, [0, 32], 0],
        [c, [2, 0], 0]
    ]
    run_exception_tests("TEST: NA (masked): invalid args", testdata)


def test_NA_masked_args_range():
    c = NotEqualAlphabeticMasked
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, [i, j], make_masked_opcode("NA", i, j)])
    run_tests("TEST: NA (masked): args range", testdata)


def test_NA_unmasked_simple():
    c = NotEqualAlphabeticUnmasked
    testdata = [[c, [0, 0, 0, 0], 0o2014]]
    run_tests("TEST: NA (unmasked): simple", testdata)


def test_NA_unmasked_invalid_args():
    c = NotEqualAlphabeticUnmasked
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: NA (unmasked): invalid args", testdata)


def test_NA_unmasked_args_range():
    c = NotEqualAlphabeticUnmasked
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("NA", i, j, k, l)])
    run_tests("TEST: NA (unmasked): args range", testdata)


# ######## NN ########

def test_NN_masked_simple():
    c = NotEqualNumericMasked
    testdata = [[c, [0, 0], 0o50]]
    run_tests("TEST: NN (masked): simple", testdata)


def test_NN_masked_invalid_args():
    c = NotEqualNumericMasked
    testdata = [
        [c, [0, 32], 0],
        [c, [2, 0], 0]
    ]
    run_exception_tests("TEST: NN (masked): invalid args", testdata)


def test_NN_masked_args_range():
    c = NotEqualNumericMasked
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, [i, j], make_masked_opcode("NN", i, j)])
    run_tests("TEST: NN (masked): args range", testdata)


def test_NN_unmasked_simple():
    c = NotEqualNumericUnmasked
    testdata = [[c, [0, 0, 0, 0], 0o2010]]
    run_tests("TEST: NN (unmasked): simple", testdata)


def test_NN_unmasked_invalid_args():
    c = NotEqualNumericUnmasked
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: NN (unmasked): invalid args", testdata)


def test_NN_unmasked_args_range():
    c = NotEqualNumericUnmasked
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("NN", i, j, k, l)])
    run_tests("TEST: NN (unmasked): args range", testdata)


# ######## LA ########

def test_LA_masked_simple():
    c = LessThanOrEqualAlphabeticMasked
    testdata = [[c, [0, 0], 0o74]]
    run_tests("TEST: LA (masked): simple", testdata)


def test_LA_masked_invalid_args():
    c = LessThanOrEqualAlphabeticMasked
    testdata = [
        [c, [0, 32], 0],
        [c, [2, 0], 0]
    ]
    run_exception_tests("TEST: LA (masked): invalid args", testdata)


def test_LA_masked_args_range():
    c = LessThanOrEqualAlphabeticMasked
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, [i, j], make_masked_opcode("LA", i, j)])
    run_tests("TEST: LA (masked): args range", testdata)


def test_LA_unmasked_simple():
    c = LessThanOrEqualAlphabeticUnmasked
    testdata = [[c, [0, 0, 0, 0], 0o2034]]
    run_tests("TEST: LA (unmasked): simple", testdata)


def test_LA_unmasked_invalid_args():
    c = LessThanOrEqualAlphabeticUnmasked
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: LA (unmasked): invalid args", testdata)


def test_LA_unmasked_args_range():
    c = LessThanOrEqualAlphabeticUnmasked
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("LA", i, j, k, l)])
    run_tests("TEST: LA (unmasked): args range", testdata)


# ######## LN ########

def test_LN_masked_simple():
    c = LessThanOrEqualNumericMasked
    testdata = [[c, [0, 0], 0o70]]
    run_tests("TEST: LN (masked): simple", testdata)


def test_LN_masked_invalid_args():
    c = LessThanOrEqualNumericMasked
    testdata = [
        [c, [0, 32], 0],
        [c, [2, 0], 0]
    ]
    run_exception_tests("TEST: LN (masked): invalid args", testdata)


def test_LN_masked_args_range():
    c = LessThanOrEqualNumericMasked
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, [i, j], make_masked_opcode("LN", i, j)])
    run_tests("TEST: LN (masked): args range", testdata)


def test_LN_unmasked_simple():
    c = LessThanOrEqualNumericUnmasked
    testdata = [[c, [0, 0, 0, 0], 0o2030]]
    run_tests("TEST: LN (unmasked): simple", testdata)


def test_LN_unmasked_invalid_args():
    c = LessThanOrEqualNumericUnmasked
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: LN (unmasked): invalid args", testdata)


def test_LN_unmasked_args_range():
    c = LessThanOrEqualNumericUnmasked
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("LN", i, j, k, l)])
    run_tests("TEST: LN (unmasked): args range", testdata)


# ######## TX ########

def test_TX_masked_simple():
    c = TransferMasked
    testdata = [[c, [0, 0], 0o60]]
    run_tests("TEST: TX (masked): simple", testdata)


def test_TX_masked_invalid_args():
    c = TransferMasked
    testdata = [
        [c, [0, 32], 0],
        [c, [2, 0], 0]
    ]
    run_exception_tests("TEST: TX (masked): invalid args", testdata)


def test_TX_masked_args_range():
    c = TransferMasked
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, [i, j], make_masked_opcode("TX", i, j)])
    run_tests("TEST: TX (masked): args range", testdata)


def test_TX_unmasked_simple():
    c = TransferUnmasked
    testdata = [[c, [0, 0, 0, 0], 0o2020]]
    run_tests("TEST: TX (unmasked): simple", testdata)


def test_TX_unmasked_invalid_args():
    c = TransferUnmasked
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: TX (unmasked): invalid args", testdata)


def test_TX_unmasked_args_range():
    c = TransferUnmasked
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("TX", i, j, k, l)])
    run_tests("TEST: TX (unmasked): args range", testdata)


# ######## TS ########

def test_TS_masked_simple():
    c = TransferChangeSequenceMasked
    testdata = [[c, [0, 0], 0o44]]
    run_tests("TEST: TS (masked): simple", testdata)


def test_TS_masked_invalid_args():
    c = TransferChangeSequenceMasked
    testdata = [
        [c, [0, 32], 0],
        [c, [2, 0], 0]
    ]
    run_exception_tests("TEST: TS (masked): invalid args", testdata)


def test_TS_masked_args_range():
    c = TransferChangeSequenceMasked
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, [i, j], make_masked_opcode("TS", i, j)])
    run_tests("TEST: TS (masked): args range", testdata)


def test_TS_unmasked_simple():
    c = TransferChangeSequenceUnmasked
    testdata = [[c, [0, 0, 0, 0], 0o2004]]
    run_tests("TEST: TS (unmasked): simple", testdata)


def test_TS_unmasked_invalid_args():
    c = TransferChangeSequenceUnmasked
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: TS (unmasked): invalid args", testdata)


def test_TS_unmasked_args_range():
    c = TransferChangeSequenceUnmasked
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("TS", i, j, k, l)])
    run_tests("TEST: TS (unmasked): args range", testdata)


# ######## HA ########

def test_HA_masked_simple():
    c = HalfAddMasked
    testdata = [[c, [0, 0], 0o65]]
    run_tests("TEST: HA (masked): simple", testdata)


def test_HA_masked_invalid_args():
    c = HalfAddMasked
    testdata = [
        [c, [0, 32], 0],
        [c, [2, 0], 0]
    ]
    run_exception_tests("TEST: HA (masked): invalid args", testdata)


def test_HA_masked_args_range():
    c = HalfAddMasked
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, [i, j], make_masked_opcode("HA", i, j)])
    run_tests("TEST: HA (masked): args range", testdata)


def test_HA_unmasked_simple():
    c = HalfAddUnmasked
    testdata = [[c, [0, 0, 0, 0], 0o2025]]
    run_tests("TEST: HA (unmasked): simple", testdata)


def test_HA_unmasked_invalid_args():
    c = HalfAddUnmasked
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: HA (unmasked): invalid args", testdata)


def test_HA_unmasked_args_range():
    c = HalfAddUnmasked
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("HA", i, j, k, l)])
    run_tests("TEST: HA (unmasked): args range", testdata)


# ######## SM ########

def test_SM_masked_simple():
    c = SuperimposeMasked
    testdata = [[c, [0, 0], 0o45]]
    run_tests("TEST: SM (masked): simple", testdata)


def test_SM_masked_invalid_args():
    c = SuperimposeMasked
    testdata = [
        [c, [0, 32], 0],
        [c, [2, 0], 0]
    ]
    run_exception_tests("TEST: SM (masked): invalid args", testdata)


def test_SM_masked_args_range():
    c = SuperimposeMasked
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, [i, j], make_masked_opcode("SM", i, j)])
    run_tests("TEST: SM (masked): args range", testdata)


def test_SM_unmasked_simple():
    c = SuperimposeUnmasked
    testdata = [[c, [0, 0, 0, 0], 0o2005]]
    run_tests("TEST: SM (unmasked): simple", testdata)


def test_SM_unmasked_invalid_args():
    c = SuperimposeUnmasked
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: SM (unmasked): invalid args", testdata)


def test_SM_unmasked_args_range():
    c = SuperimposeUnmasked
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("SM", i, j, k, l)])
    run_tests("TEST: SM (unmasked): args range", testdata)


# ######## CP ########

def test_CP_masked_simple():
    c = CheckParityMasked
    testdata = [[c, [0, 0], 0o64]]
    run_tests("TEST: CP (masked): simple", testdata)


def test_CP_masked_invalid_args():
    c = CheckParityMasked
    testdata = [
        [c, [0, 32], 0],
        [c, [2, 0], 0]
    ]
    run_exception_tests("TEST: CP (masked): invalid args", testdata)


def test_CP_masked_args_range():
    c = CheckParityMasked
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, [i, j], make_masked_opcode("CP", i, j)])
    run_tests("TEST: CP (masked): args range", testdata)


def test_CP_unmasked_simple():
    c = CheckParityUnmasked
    testdata = [[c, [0, 0, 0, 0], 0o2024]]
    run_tests("TEST: CP (unmasked): simple", testdata)


def test_CP_unmasked_invalid_args():
    c = CheckParityUnmasked
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: CP (unmasked): invalid args", testdata)


def test_CP_unmasked_args_range():
    c = CheckParityUnmasked
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("CP", i, j, k, l)])
    run_tests("TEST: CP (unmasked): args range", testdata)


# ######## BM ########

def test_BM_simple():
    c = BinaryMultiply
    testdata = [[c, [0, 0, 0, 0], 0o13]]
    run_tests("TEST: BM simple", testdata)


def test_BM_invalid_args():
    c = BinaryMultiply
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: BM invalid args", testdata)


def test_BM_args_range():
    c = BinaryMultiply
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("BM", i, j, k, l, bits23=0b00)])
    run_tests("TEST: BM args range", testdata)


# ######## DM ########

def test_DM_simple():
    c = DecimalMultiply
    testdata = [[c, [0, 0, 0, 0], 0o03]]
    run_tests("TEST: DM simple", testdata)


def test_DM_invalid_args():
    c = DecimalMultiply
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: DM invalid args", testdata)


def test_DM_args_range():
    c = DecimalMultiply
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("DM", i, j, k, l, bits23=0b00)])
    run_tests("TEST: DM args range", testdata)


# ######## BT ########

def test_BT_simple():
    c = BinaryAccumulate
    testdata = [[c, [0, 0, 0, 0], 0o2013]]
    run_tests("TEST: BT simple", testdata)


def test_BT_invalid_args():
    c = BinaryAccumulate
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: BT invalid args", testdata)


def test_BT_args_range():
    c = BinaryAccumulate
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("BT", i, j, k, l)])
    run_tests("TEST: BT args range", testdata)


# ######## DT ########

def test_DT_simple():
    c = DecimalAccumulate
    testdata = [[c, [0, 0, 0, 0], 0o2003]]
    run_tests("TEST: DT simple", testdata)


def test_DT_invalid_args():
    c = DecimalAccumulate
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: DT invalid args", testdata)


def test_DT_args_range():
    c = DecimalAccumulate
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("DT", i, j, k, l)])
    run_tests("TEST: DT args range", testdata)


# ######## MT ########

def test_MT_simple():
    c = MultipleTransfer
    testdata = [[c, [0, 0, 0, 0], 0o0020]]
    run_tests("TEST: MT simple", testdata)


def test_MT_invalid_args():
    c = MultipleTransfer
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: MT invalid args", testdata)


def test_MT_args_range():
    c = MultipleTransfer
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("MT", i, j, k, l, bits23=0b00)])
    run_tests("TEST: MT args range", testdata)


# ######## TN ########

def test_TN_simple():
    c = TransferNWords
    testdata = [[c, [0, 0, 0, 0], 0o1020]]
    run_tests("TEST: TN simple", testdata)


def test_TN_invalid_args():
    c = TransferNWords
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: TN invalid args", testdata)


def test_TN_args_range():
    c = TransferNWords
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("TN", i, j, k, l, bits23=0b01)])
    run_tests("TEST: TN args range", testdata)


# ######## CC ########

def test_CC_simple():
    c = ComputeOrthocount
    testdata = [[c, [0, 0, 0, 0], 0o1010]]
    run_tests("TEST: CC simple", testdata)


def test_CC_invalid_args():
    c = ComputeOrthocount
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: CC invalid args", testdata)


def test_CC_args_range():
    c = ComputeOrthocount
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("CC", i, j, k, l, bits23=0b01)])
    run_tests("TEST: CC args range", testdata)


# ######## IT ########

def test_IT_simple():
    c = ItemTransfer
    testdata = [[c, [0, 0, 0, 0], 0o1030]]
    run_tests("TEST: IT simple", testdata)


def test_IT_invalid_args():
    c = ItemTransfer
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: IT invalid args", testdata)


def test_IT_args_range():
    c = ItemTransfer
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("IT", i, j, k, l, bits23=0b01)])
    run_tests("TEST: IT args range", testdata)


# ######## EBA ########

def test_EBA_simple():
    c = ExtendedBinaryAdd
    testdata = [[c, [0, 0, 0, 0], 0o3013]]
    run_tests("TEST: EBA simple", testdata)


def test_EBA_invalid_args():
    c = ExtendedBinaryAdd
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: EBA invalid args", testdata)


def test_EBA_args_range():
    c = ExtendedBinaryAdd
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("EBA", i, j, k, l, bits23=0b11)])
    run_tests("TEST: EBA args range", testdata)


# ######## EBS ########

def test_EBS_simple():
    c = ExtendedBinarySubtract
    testdata = [[c, [0, 0, 0, 0], 0o3033]]
    run_tests("TEST: EBS simple", testdata)


def test_EBS_invalid_args():
    c = ExtendedBinarySubtract
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: EBS invalid args", testdata)


def test_EBS_args_range():
    c = ExtendedBinarySubtract
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("EBS", i, j, k, l, bits23=0b11)])
    run_tests("TEST: EBS args range", testdata)


# ######## RT ########

def test_RT_simple():
    c = RecordTransfer
    testdata = [[c, [0, 0, 0, 0], 0o3030]]
    run_tests("TEST: RT simple", testdata)


def test_RT_invalid_args():
    c = RecordTransfer
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: RT invalid args", testdata)


def test_RT_args_range():
    c = RecordTransfer
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("RT", i, j, k, l, bits23=0b11)])
    run_tests("TEST: RT args range", testdata)


# ######## MPC ########

def test_MPC_simple():
    c = ControlProgram
    testdata = [[c, [0, 0, 0, 0], 0o2000]]
    run_tests("TEST: MPC simple", testdata)


def test_MPC_invalid_args():
    c = ControlProgram
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: MPC invalid args", testdata)


def test_MPC_args_range():
    c = ControlProgram
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("MPC", i, j, k, l)])
    run_tests("TEST: MPC args range", testdata)


# ######## PR ########

def test_PR_simple():
    c = Proceed
    testdata = [[c, [], 0o0000]]
    run_tests("TEST: PR simple", testdata)


# ######## SWS ########

def test_SWS_simple():
    c = ShiftWordAndSubstitute
    testdata = [[c, [0, 0, 0, 0], 0o2006]]
    run_tests("TEST: SWS simple", testdata)


def test_SWS_invalid_args():
    c = ShiftWordAndSubstitute
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: SWS invalid args", testdata)


def test_SWS_args_range():
    c = ShiftWordAndSubstitute
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("SWS", i, j, k, l)])
    run_tests("TEST: SWS args range", testdata)


# ######## SPS ########

def test_SPS_simple():
    c = ShiftPreservingSignAndSubstitute
    testdata = [[c, [0, 0, 0, 0], 0o2002]]
    run_tests("TEST: SPS simple", testdata)


def test_SPS_invalid_args():
    c = ShiftPreservingSignAndSubstitute
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: SPS invalid args", testdata)


def test_SPS_args_range():
    c = ShiftPreservingSignAndSubstitute
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("SPS", i, j, k, l)])
    run_tests("TEST: SPS args range", testdata)


# ######## SWE ########

def test_SWE_simple():
    c = ShiftWordAndExtract
    testdata = [[c, [0, 0, 0, 0], 0o2016]]
    run_tests("TEST: SWE simple", testdata)


def test_SWE_invalid_args():
    c = ShiftWordAndExtract
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: SWE invalid args", testdata)


def test_SWE_args_range():
    c = ShiftWordAndExtract
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("SWE", i, j, k, l)])
    run_tests("TEST: SWE args range", testdata)


# ######## SPE ########

def test_SPE_simple():
    c = ShiftPreservingSignAndExtract
    testdata = [[c, [0, 0, 0, 0], 0o2012]]
    run_tests("TEST: SPE simple", testdata)


def test_SPE_invalid_args():
    c = ShiftPreservingSignAndExtract
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: SPE invalid args", testdata)


def test_SPE_args_range():
    c = ShiftPreservingSignAndExtract
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("SPE", i, j, k, l)])
    run_tests("TEST: SPE args range", testdata)


# ######## SSL ########

def test_SSL_simple():
    c = ShiftAndSelect
    testdata = [[c, [0, 0, 0, 0], 0o2026]]
    run_tests("TEST: SSL simple", testdata)


def test_SSL_invalid_args():
    c = ShiftAndSelect
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: SSL invalid args", testdata)


def test_SSL_args_range():
    c = ShiftAndSelect
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("SSL", i, j, k, l)])
    run_tests("TEST: SSL args range", testdata)


# ######## SS ########

def test_SS_simple():
    c = Substitute
    testdata = [[c, [0, 0, 0, 0], 0o0006]]
    run_tests("TEST: SS simple", testdata)


def test_SS_invalid_args():
    c = Substitute
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: SS invalid args", testdata)


def test_SS_args_range():
    c = Substitute
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("SS", i, j, k, l, bits23=0b00)])
    run_tests("TEST: SS args range", testdata)


# ######## EX ########

def test_EX_simple():
    c = Extract
    testdata = [[c, [0, 0, 0, 0], 0o0016]]
    run_tests("TEST: EX simple", testdata)


def test_EX_invalid_args():
    c = Extract
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: EX invalid args", testdata)


def test_EX_args_range():
    c = Extract
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("EX", i, j, k, l, bits23=0b00)])
    run_tests("TEST: EX args range", testdata)


# ######## RF ########

def test_RF_simple():
    c = ReadForward
    testdata = [[c, [0], 0o0072]]
    run_tests("TEST: RF simple", testdata)


def test_RF_invalid_args():
    c = ReadForward
    testdata = [
        [c, [-1], 0],
        [c, [64], 0]
    ]
    run_exception_tests("TEST: RF invalid args", testdata)


def test_RF_args_range():
    c = ReadForward
    testdata = []
    for p in range(64):
        testdata.append([c, [p], make_peripheral_opcode("RF", p)])
    run_tests("TEST: RF args range", testdata)


# ######## RB ########

def test_RB_simple():
    c = ReadBackward
    testdata = [[c, [0], 0o0052]]
    run_tests("TEST: RB simple", testdata)


def test_RB_invalid_args():
    c = ReadBackward
    testdata = [
        [c, [-1], 0],
        [c, [64], 0]
    ]
    run_exception_tests("TEST: RB invalid args", testdata)


def test_RB_args_range():
    c = ReadBackward
    testdata = []
    for p in range(64):
        testdata.append([c, [p], make_peripheral_opcode("RB", p)])
    run_tests("TEST: RB args range", testdata)


# ######## WF ########

def test_WF_simple():
    c = WriteForward
    testdata = [[c, [0], 0o0056]]
    run_tests("TEST: WF simple", testdata)


def test_WF_invalid_args():
    c = WriteForward
    testdata = [
        [c, [-1], 0],
        [c, [64], 0]
    ]
    run_exception_tests("TEST: WF invalid args", testdata)


def test_WF_args_range():
    c = WriteForward
    testdata = []
    for p in range(64):
        testdata.append([c, [p], make_peripheral_opcode("WF", p)])
    run_tests("TEST: WF args range", testdata)


# ######## RW ########

def test_RW_simple():
    c = Rewind
    testdata = [[c, [0], 0o0042]]
    run_tests("TEST: RW simple", testdata)


def test_RW_invalid_args():
    c = Rewind
    testdata = [
        [c, [-1], 0],
        [c, [64], 0]
    ]
    run_exception_tests("TEST: RW invalid args", testdata)


def test_RW_args_range():
    c = Rewind
    testdata = []
    for p in range(64):
        testdata.append([c, [p], make_peripheral_opcode("RW", p)])
    run_tests("TEST: RW args range", testdata)


# ######## PRA ########

def test_PRA_simple():
    c = PrintAlphabetic
    testdata = [[c, [0, 0, 0, 0], 0o0046]]
    run_tests("TEST: PRA simple", testdata)


def test_PRA_invalid_args():
    c = PrintAlphabetic
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: PRA invalid args", testdata)


def test_PRA_args_range():
    c = PrintAlphabetic
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_print_opcode("PRA", i, j, k, l)])
    run_tests("TEST: PRA args range", testdata)


# ######## PRD ########

def test_PRD_simple():
    c = PrintDecimal
    testdata = [[c, [0, 0, 0, 0], 0o0046]]
    run_tests("TEST: PRD simple", testdata)


def test_PRD_invalid_args():
    c = PrintDecimal
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: PRD invalid args", testdata)


def test_PRD_args_range():
    c = PrintDecimal
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_print_opcode("PRD", i, j, k, l)])
    run_tests("TEST: PRD args range", testdata)


# ######## PRO ########

def test_PRO_simple():
    c = PrintOctal
    testdata = [[c, [0, 0, 0, 0], 0o0046]]
    run_tests("TEST: PRO simple", testdata)


def test_PRO_invalid_args():
    c = PrintOctal
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: PRO invalid args", testdata)


def test_PRO_args_range():
    c = PrintOctal
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_print_opcode("PRO", i, j, k, l)])
    run_tests("TEST: PRO args range", testdata)


# ######## S ########

def test_S_simple():
    c = Simulator
    testdata = [[c, [0], 0o0007]]
    run_tests("TEST: S simple", testdata)


def test_S_invalid_args():
    c = Simulator
    testdata = [
        [c, [2], 0]
    ]
    run_exception_tests("TEST: S invalid args", testdata)


def test_S_args_range():
    c = Simulator
    testdata = [
        [c, [0], 0o0007],
        [c, [1], 0o4007]
    ]
    run_tests("TEST: S args range", testdata)


# ######## FBA ########

def test_FBA_simple():
    c = FloatingBinaryAdd
    testdata = [[c, [0, 0, 0, 0], 0o1001]]
    run_tests("TEST: FBA simple", testdata)


def test_FBA_invalid_args():
    c = FloatingBinaryAdd
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FBA invalid args", testdata)


def test_FBA_args_range():
    c = FloatingBinaryAdd
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("FBA", i, j, k, l, bits23=0b01)])
    run_tests("TEST: FBA args range", testdata)


# ######## FDA ########

def test_FDA_simple():
    c = FloatingDecimalAdd
    testdata = [[c, [0, 0, 0, 0], 0o1021]]
    run_tests("TEST: FDA simple", testdata)


def test_FDA_invalid_args():
    c = FloatingDecimalAdd
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FDA invalid args", testdata)


def test_FDA_args_range():
    c = FloatingDecimalAdd
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("FDA", i, j, k, l, bits23=0b01)])
    run_tests("TEST: FDA args range", testdata)


# ######## FBS ########

def test_FBS_simple():
    c = FloatingBinarySubtract
    testdata = [[c, [0, 0, 0, 0], 0o1011]]
    run_tests("TEST: FBS simple", testdata)


def test_FBS_invalid_args():
    c = FloatingBinarySubtract
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FBS invalid args", testdata)


def test_FBS_args_range():
    c = FloatingBinarySubtract
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("FBS", i, j, k, l, bits23=0b01)])
    run_tests("TEST: FBS args range", testdata)


# ######## FDS ########

def test_FDS_simple():
    c = FloatingDecimalSubtract
    testdata = [[c, [0, 0, 0, 0], 0o1031]]
    run_tests("TEST: FDS simple", testdata)


def test_FDS_invalid_args():
    c = FloatingDecimalSubtract
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FDS invalid args", testdata)


def test_FDS_args_range():
    c = FloatingDecimalSubtract
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("FDS", i, j, k, l, bits23=0b01)])
    run_tests("TEST: FDS args range", testdata)


# ######## FBD ########

def test_FBD_simple():
    c = FloatingBinaryDivide
    testdata = [[c, [0, 0, 0, 0], 0o1005]]
    run_tests("TEST: FBD simple", testdata)


def test_FBD_invalid_args():
    c = FloatingBinaryDivide
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FBD invalid args", testdata)


def test_FBD_args_range():
    c = FloatingBinaryDivide
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("FBD", i, j, k, l, bits23=0b01)])
    run_tests("TEST: FBD args range", testdata)


# ######## FDD ########

def test_FDD_simple():
    c = FloatingDecimalDivide
    testdata = [[c, [0, 0, 0, 0], 0o1025]]
    run_tests("TEST: FDD simple", testdata)


def test_FDD_invalid_args():
    c = FloatingDecimalDivide
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FDD invalid args", testdata)


def test_FDD_args_range():
    c = FloatingDecimalDivide
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("FDD", i, j, k, l, bits23=0b01)])
    run_tests("TEST: FDD args range", testdata)


# ######## FBAU ########

def test_FBAU_simple():
    c = FloatingBinaryAddUnnormalized
    testdata = [[c, [0, 0, 0, 0], 0o3001]]
    run_tests("TEST: FBAU simple", testdata)


def test_FBAU_invalid_args():
    c = FloatingBinaryAddUnnormalized
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FBAU invalid args", testdata)


def test_FBAU_args_range():
    c = FloatingBinaryAddUnnormalized
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("FBAU", i, j, k, l, bits23=0b11)])
    run_tests("TEST: FBAU args range", testdata)


# ######## FDAU ########

def test_FDAU_simple():
    c = FloatingDecimalAddUnnormalized
    testdata = [[c, [0, 0, 0, 0], 0o3021]]
    run_tests("TEST: FDAU simple", testdata)


def test_FDAU_invalid_args():
    c = FloatingDecimalAddUnnormalized
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FDAU invalid args", testdata)


def test_FDAU_args_range():
    c = FloatingDecimalAddUnnormalized
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("FDAU", i, j, k, l, bits23=0b11)])
    run_tests("TEST: FDAU args range", testdata)


# ######## FBSU ########

def test_FBSU_simple():
    c = FloatingBinarySubtractUnnormalized
    testdata = [[c, [0, 0, 0, 0], 0o3011]]
    run_tests("TEST: FBSU simple", testdata)


def test_FBSU_invalid_args():
    c = FloatingBinarySubtractUnnormalized
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FBSU invalid args", testdata)


def test_FBSU_args_range():
    c = FloatingBinarySubtractUnnormalized
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("FBSU", i, j, k, l, bits23=0b11)])
    run_tests("TEST: FBSU args range", testdata)


# ######## FDSU ########

def test_FDSU_simple():
    c = FloatingDecimalSubtractUnnormalized
    testdata = [[c, [0, 0, 0, 0], 0o3031]]
    run_tests("TEST: FDSU simple", testdata)


def test_FDSU_invalid_args():
    c = FloatingDecimalSubtractUnnormalized
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FDSU invalid args", testdata)


def test_FDSU_args_range():
    c = FloatingDecimalSubtractUnnormalized
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("FDSU", i, j, k, l, bits23=0b11)])
    run_tests("TEST: FDSU args range", testdata)


# ######## FBM ########

def test_FBM_simple():
    c = FloatingBinaryMultiply
    testdata = [[c, [0, 0, 0, 0], 0o3005]]
    run_tests("TEST: FBM simple", testdata)


def test_FBM_invalid_args():
    c = FloatingBinaryMultiply
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FBM invalid args", testdata)


def test_FBM_args_range():
    c = FloatingBinaryMultiply
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("FBM", i, j, k, l, bits23=0b11)])
    run_tests("TEST: FBM args range", testdata)


# ######## FDM ########

def test_FDM_simple():
    c = FloatingDecimalMultiply
    testdata = [[c, [0, 0, 0, 0], 0o3025]]
    run_tests("TEST: FDM simple", testdata)


def test_FDM_invalid_args():
    c = FloatingDecimalMultiply
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FDM invalid args", testdata)


def test_FDM_args_range():
    c = FloatingDecimalMultiply
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("FDM", i, j, k, l, bits23=0b11)])
    run_tests("TEST: FDM args range", testdata)


# ######## ULD ########

def test_ULD_simple():
    c = MultipleUnload
    testdata = [[c, [0, 0, 0, 0], 0o3015]]
    run_tests("TEST: ULD simple", testdata)


def test_ULD_invalid_args():
    c = MultipleUnload
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: ULD invalid args", testdata)


def test_ULD_args_range():
    c = MultipleUnload
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("ULD", i, j, k, l, bits23=0b11)])
    run_tests("TEST: ULD args range", testdata)


# ######## FBAE ########

def test_FBAE_simple():
    c = FloatingBinaryAddExtendedPrecision
    testdata = [[c, [0, 0, 0, 0], 0o0001]]
    run_tests("TEST: FBAE simple", testdata)


def test_FBAE_invalid_args():
    c = FloatingBinaryAddExtendedPrecision
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FBAE invalid args", testdata)


def test_FBAE_args_range():
    c = FloatingBinaryAddExtendedPrecision
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("FBAE", i, j, k, l, bits23=0b00)])
    run_tests("TEST: FBAE args range", testdata)


# ######## FBSE ########

def test_FBSE_simple():
    c = FloatingBinarySubtractExtendedPrecision
    testdata = [[c, [0, 0, 0, 0], 0o0011]]
    run_tests("TEST: FBSE simple", testdata)


def test_FBSE_invalid_args():
    c = FloatingBinarySubtractExtendedPrecision
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FBSE invalid args", testdata)


def test_FBSE_args_range():
    c = FloatingBinarySubtractExtendedPrecision
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("FBSE", i, j, k, l, bits23=0b00)])
    run_tests("TEST: FBSE args range", testdata)


# ######## BD ########

def test_BD_simple():
    c = FixedBinaryDivide
    testdata = [[c, [0, 0, 0, 0], 0o0005]]
    run_tests("TEST: BD simple", testdata)


def test_BD_invalid_args():
    c = FixedBinaryDivide
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: BD invalid args", testdata)


def test_BD_args_range():
    c = FixedBinaryDivide
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("BD", i, j, k, l, bits23=0b00)])
    run_tests("TEST: BD args range", testdata)


# ######## DD ########

def test_DD_simple():
    c = FixedDecimalDivide
    testdata = [[c, [0, 0, 0, 0], 0o0025]]
    run_tests("TEST: DD simple", testdata)


def test_DD_invalid_args():
    c = FixedDecimalDivide
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: DD invalid args", testdata)


def test_DD_args_range():
    c = FixedDecimalDivide
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("DD", i, j, k, l, bits23=0b00)])
    run_tests("TEST: DD args range", testdata)


# ######## FFN ########

def test_FFN_simple():
    c = FixedToFloatingNormalize
    testdata = [[c, [0, 0, 0, 0], 0o0015]]
    run_tests("TEST: FFN simple", testdata)


def test_FFN_invalid_args():
    c = FixedToFloatingNormalize
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FFN invalid args", testdata)


def test_FFN_args_range():
    c = FixedToFloatingNormalize
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("FFN", i, j, k, l, bits23=0b00)])
    run_tests("TEST: FFN args range", testdata)


# ######## FCON ########

def test_FCON_simple():
    c = Conversion
    testdata = [[c, [0, 0, 0, 0], 0o0035]]
    run_tests("TEST: FCON simple", testdata)


def test_FCON_invalid_args():
    c = Conversion
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FCON invalid args", testdata)


def test_FCON_args_range():
    c = Conversion
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("FCON", i, j, k, l, bits23=0b00)])
    run_tests("TEST: FCON args range", testdata)


# ######## FLN ########

def test_FLN_simple():
    c = FloatingLessThanNormalized
    testdata = [[c, [0, 0, 0, 0], 0o0030]]
    run_tests("TEST: FLN simple", testdata)


def test_FLN_invalid_args():
    c = FloatingLessThanNormalized
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FLN invalid args", testdata)


def test_FLN_args_range():
    c = FloatingLessThanNormalized
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("FLN", i, j, k, l, bits23=0b00)])
    run_tests("TEST: FLN args range", testdata)


# ######## FNN ########

def test_FNN_simple():
    c = FloatingNotEqualNormalized
    testdata = [[c, [0, 0, 0, 0], 0o2014]]
    run_tests("TEST: FNN simple", testdata)


def test_FNN_invalid_args():
    c = FloatingNotEqualNormalized
    testdata = [
        [c, [2, 0, 0, 0], 0],
        [c, [0, 2, 0, 0], 0],
        [c, [0, 1, 2, 3], 0]
    ]
    run_exception_tests("TEST: FNN invalid args", testdata)


def test_FNN_args_range():
    c = FloatingNotEqualNormalized
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, [i, j, k, l], make_unmasked_opcode("FNN", i, j, k, l, bits23=0b10)])
    run_tests("TEST: FNN args range", testdata)


# ######## ALF ########

def test_ALF_simple():
    c = AlphanumericConstant
    testdata = [[c, [0], 0o0]]
    run_tests("TEST: ALF simple", testdata)


def test_ALF_invalid_args():
    c = AlphanumericConstant
    testdata = [
        [c, [-1], 0],
        [c, [2 ** 48], 0]
    ]
    run_exception_tests("TEST: ALF invalid args", testdata)


def test_ALF_args_range():
    c = AlphanumericConstant
    testdata = [
        [c, [0], 0],
        [c, [1], 1],
        [c, [4095], 4095],
        [c, [4096], 4096],
        [c, [2 ** 48 - 1], 2 ** 48 - 1],
    ]
    run_tests("TEST: ALF args range", testdata)


# ######## DEC ########

def test_DEC_simple():
    c = DecimalConstant
    testdata = [[c, [0], 0o0]]
    run_tests("TEST: DEC simple", testdata)


def test_DEC_invalid_args():
    c = DecimalConstant
    testdata = [
        [c, [-1], 0],
        [c, [2 ** 48], 0]
    ]
    run_exception_tests("TEST: DEC invalid args", testdata)


def test_DEC_args_range():
    c = DecimalConstant
    testdata = [
        [c, [0], 0],
        [c, [1], 1],
        [c, [4095], 4095],
        [c, [4096], 4096],
        [c, [2 ** 48 - 1], 2 ** 48 - 1],
    ]
    run_tests("TEST: DEC args range", testdata)


# ######## EBC ########

def test_EBC_simple():
    c = ExtendedBinaryConstant
    testdata = [[c, [0], 0o0]]
    run_tests("TEST: EBC simple", testdata)


def test_EBC_invalid_args():
    c = ExtendedBinaryConstant
    testdata = [
        [c, [-1], 0],
        [c, [2 ** 48], 0]
    ]
    run_exception_tests("TEST: EBC invalid args", testdata)


def test_EBC_args_range():
    c = ExtendedBinaryConstant
    testdata = [
        [c, [0], 0],
        [c, [1], 1],
        [c, [4095], 4095],
        [c, [4096], 4096],
        [c, [2 ** 48 - 1], 2 ** 48 - 1],
    ]
    run_tests("TEST: EBC args range", testdata)


# ######## FLBIN ########

def test_FLBIN_simple():
    c = FloatingBinaryConstant
    testdata = [[c, [0], 0o0]]
    run_tests("TEST: FLBIN simple", testdata)


def test_FLBIN_invalid_args():
    c = FloatingBinaryConstant
    testdata = [
        [c, [-1], 0],
        [c, [2 ** 48], 0]
    ]
    run_exception_tests("TEST: FLBIN invalid args", testdata)


def test_FLBIN_args_range():
    c = FloatingBinaryConstant
    testdata = [
        [c, [0], 0],
        [c, [1], 1],
        [c, [4095], 4095],
        [c, [4096], 4096],
        [c, [2 ** 48 - 1], 2 ** 48 - 1],
    ]
    run_tests("TEST: FLBIN args range", testdata)


# ######## FLDEC ########

def test_FLDEC_simple():
    c = FloatingDecimalConstant
    testdata = [[c, [0], 0o0]]
    run_tests("TEST: FLDEC simple", testdata)


def test_FLDEC_invalid_args():
    c = FloatingDecimalConstant
    testdata = [
        [c, [-1], 0],
        [c, [2 ** 48], 0]
    ]
    run_exception_tests("TEST: FLDEC invalid args", testdata)


def test_FLDEC_args_range():
    c = FloatingDecimalConstant
    testdata = [
        [c, [0], 0],
        [c, [1], 1],
        [c, [4095], 4095],
        [c, [4096], 4096],
        [c, [2 ** 48 - 1], 2 ** 48 - 1],
    ]
    run_tests("TEST: FLDEC args range", testdata)


# ######## FXBIN ########

def test_FXBIN_simple():
    c = FixedBinaryConstant
    testdata = [[c, [0], 0o0]]
    run_tests("TEST: FXBIN simple", testdata)


def test_FXBIN_invalid_args():
    c = FixedBinaryConstant
    testdata = [
        [c, [-1], 0],
        [c, [2 ** 48], 0]
    ]
    run_exception_tests("TEST: FXBIN invalid args", testdata)


def test_FXBIN_args_range():
    c = FixedBinaryConstant
    testdata = [
        [c, [0], 0],
        [c, [1], 1],
        [c, [4095], 4095],
        [c, [4096], 4096],
        [c, [2 ** 48 - 1], 2 ** 48 - 1],
    ]
    run_tests("TEST: FXBIN args range", testdata)


# ######## OCT ########

def test_OCT_simple():
    c = OctalConstant
    testdata = [[c, [0], 0o0]]
    run_tests("TEST: OCT simple", testdata)


def test_OCT_invalid_args():
    c = OctalConstant
    testdata = [
        [c, [-1], 0],
        [c, [2 ** 48], 0]
    ]
    run_exception_tests("TEST: OCT invalid args", testdata)


def test_OCT_args_range():
    c = OctalConstant
    testdata = [
        [c, [0], 0],
        [c, [1], 1],
        [c, [4095], 4095],
        [c, [4096], 4096],
        [c, [2 ** 48 - 1], 2 ** 48 - 1],
    ]
    run_tests("TEST: OCT args range", testdata)


def test_machine_instructions():
    # Generate all possible instruction codes and look for duplicates.
    opcodes = []
    #run_tests("TEST: machine instructions check", testdata)
