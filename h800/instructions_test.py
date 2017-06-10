#!/usr/bin/env python

from collections import namedtuple

from instructions import *


def my_assert(value, good):
    assert value == good, "Value is 0o%o, should be 0o%o" % (value, good)


MaskedTestData = namedtuple('MaskedTestData', ['sequence', 'mask'])
UnmaskedTestData = namedtuple('UnmaskedTestData', ['sequence', 'a', 'b', 'c'])
SimulatorTestData = namedtuple('SimulatorTestData', ['sequence'])
PeripheralTestData = namedtuple('PeripheralTestData', ['paddr'])
ConstantTestData = namedtuple('ConstantTestData', ['data'])


def run_test(testdata):
    print testdata
    c = testdata[0]
    t = testdata[1]
    good = testdata[2]
    if isinstance(t, UnmaskedTestData):
        # Unmasked instructions.
        i = c(sequence=t.sequence, a=t.a, b=t.b, c=t.c)
    elif isinstance(t, MaskedTestData):
        # Masked instructions.
        i = c(sequence=t.sequence, mask=t.mask)
    elif isinstance(t, ConstantTestData):
        # Constant.
        i = c(data=t.data)
    elif isinstance(t, SimulatorTestData):
        # Simulator instruction.
        i = c(sequence=t.sequence)
    elif isinstance(t, PeripheralTestData):
        # Peripheral instructions.
        i = c(paddr=t.paddr)
    elif t is None:
        # Instructions with no args, e.g. Proceed.
        i = c()
    else:
        assert False, "Invalid test data!"
    my_assert(i.value, good)


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
    c = BinaryAdd
    testdata = [
        [c, MaskedTestData(0, 0), 0o0051],
        [c, MaskedTestData(0, 1), 0o0151]
    ]
    run_tests("TEST: BA (masked): simple", testdata)


def test_BA_masked_invalid_args():
    c = BinaryAdd
    testdata = [
        [c, MaskedTestData(0, 32), 0],
        [c, MaskedTestData(2, 0), 0]
    ]
    run_exception_tests("TEST: BA (masked): invalid args", testdata)


def test_BA_masked_args_range():
    c = BinaryAdd
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, MaskedTestData(i, j), make_masked_opcode("BA", i, j)])
    run_tests("TEST: BA (masked): args range", testdata)


def test_BA_unmasked_simple():
    c = BinaryAdd
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), make_unmasked_opcode("BA", 0, 0, 0, 0)]]
    run_tests("TEST: BA (unmasked): simple", testdata)


def test_BA_unmasked_invalid_args():
    c = BinaryAdd
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: BA (unmasked): invalid args", testdata)


def test_BA_unmasked_args_range():
    c = BinaryAdd
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("BA", i, j, k, l)])
    run_tests("TEST: BA (unmasked): args range", testdata)


# ######## DA ########

def test_DA_masked_simple():
    c = DecimalAdd
    testdata = [[c, MaskedTestData(0, 0), 0o41]]
    run_tests("TEST: DA (masked): simple", testdata)


def test_DA_masked_invalid_args():
    c = DecimalAdd
    testdata = [
        [c, MaskedTestData(0, 32), 0],
        [c, MaskedTestData(2, 0), 0]
    ]
    run_exception_tests("TEST: DA (masked): invalid args", testdata)


def test_DA_masked_args_range():
    c = DecimalAdd
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, MaskedTestData(i, j), make_masked_opcode("DA", i, j)])
    run_tests("TEST: DA (masked): args range", testdata)


def test_DA_unmasked_simple():
    c = DecimalAdd
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2001]]
    run_tests("TEST: DA (unmasked): simple", testdata)


def test_DA_unmasked_invalid_args():
    c = DecimalAdd
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: DA (unmasked): invalid args", testdata)


def test_DA_unmasked_args_range():
    c = DecimalAdd
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("DA", i, j, k, l)])
    run_tests("TEST: DA (unmasked): args range", testdata)


# ######## WA ########

def test_WA_masked_simple():
    c = WordAdd
    testdata = [[c, MaskedTestData(0, 0), 0o55]]
    run_tests("TEST: WA (masked): simple", testdata)


def test_WA_masked_invalid_args():
    c = WordAdd
    testdata = [
        [c, MaskedTestData(0, 32), 0],
        [c, MaskedTestData(2, 0), 0]
    ]
    run_exception_tests("TEST: WA (masked): invalid args", testdata)


def test_WA_masked_args_range():
    c = WordAdd
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, MaskedTestData(i, j), make_masked_opcode("WA", i, j)])
    run_tests("TEST: WA (masked): args range", testdata)


def test_WA_unmasked_simple():
    c = WordAdd
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2015]]
    run_tests("TEST: WA (unmasked): simple", testdata)


def test_WA_unmasked_invalid_args():
    c = WordAdd
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: WA (unmasked): invalid args", testdata)


def test_WA_unmasked_args_range():
    c = WordAdd
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("WA", i, j, k, l)])
    run_tests("TEST: WA (unmasked): args range", testdata)


# ######## BS ########

def test_BS_masked_simple():
    c = BinarySubtract
    testdata = [[c, MaskedTestData(0, 0), 0o71]]
    run_tests("TEST: BS (masked): simple", testdata)


def test_BS_masked_invalid_args():
    c = BinarySubtract
    testdata = [
        [c, MaskedTestData(0, 32), 0],
        [c, MaskedTestData(2, 0), 0]
    ]
    run_exception_tests("TEST: BS (masked): invalid args", testdata)


def test_BS_masked_args_range():
    c = BinarySubtract
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, MaskedTestData(i, j), make_masked_opcode("BS", i, j)])
    run_tests("TEST: BS (masked): args range", testdata)


def test_BS_unmasked_simple():
    c = BinarySubtract
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2031]]
    run_tests("TEST: BS (unmasked): simple", testdata)


def test_BS_unmasked_invalid_args():
    c = BinarySubtract
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: BS (unmasked): invalid args", testdata)


def test_BS_unmasked_args_range():
    c = BinarySubtract
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("BS", i, j, k, l)])
    run_tests("TEST: BS (unmasked): args range", testdata)


# ######## DS ########

def test_DS_masked_simple():
    c = DecimalSubtract
    testdata = [[c, MaskedTestData(0, 0), 0o61]]
    run_tests("TEST: DS (masked): simple", testdata)


def test_DS_masked_invalid_args():
    c = DecimalSubtract
    testdata = [
        [c, MaskedTestData(0, 32), 0],
        [c, MaskedTestData(2, 0), 0]
    ]
    run_exception_tests("TEST: DS (masked): invalid args", testdata)


def test_DS_masked_args_range():
    c = DecimalSubtract
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, MaskedTestData(i, j), make_masked_opcode("DS", i, j)])
    run_tests("TEST: DS (masked): args range", testdata)


def test_DS_unmasked_simple():
    c = DecimalSubtract
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2021]]
    run_tests("TEST: DS (unmasked): simple", testdata)


def test_DS_unmasked_invalid_args():
    c = DecimalSubtract
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: DS (unmasked): invalid args", testdata)


def test_DS_unmasked_args_range():
    c = DecimalSubtract
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("DS", i, j, k, l)])
    run_tests("TEST: DS (unmasked): args range", testdata)


# ######## WD ########

def test_WD_masked_simple():
    c = WordDifference
    testdata = [[c, MaskedTestData(0, 0), 0o75]]
    run_tests("TEST: WD (masked): simple", testdata)


def test_WD_masked_invalid_args():
    c = WordDifference
    testdata = [
        [c, MaskedTestData(0, 32), 0],
        [c, MaskedTestData(2, 0), 0]
    ]
    run_exception_tests("TEST: WD (masked): invalid args", testdata)


def test_WD_masked_args_range():
    c = WordDifference
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, MaskedTestData(i, j), make_masked_opcode("WD", i, j)])
    run_tests("TEST: WD (masked): args range", testdata)


def test_WD_unmasked_simple():
    c = WordDifference
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2035]]
    run_tests("TEST: WD (unmasked): simple", testdata)


def test_WD_unmasked_invalid_args():
    c = WordDifference
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: WD (unmasked): invalid args", testdata)


def test_WD_unmasked_args_range():
    c = WordDifference
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("WD", i, j, k, l)])
    run_tests("TEST: WD (unmasked): args range", testdata)


# ######## NA ########

def test_NA_masked_simple():
    c = NotEqualAlphabetic
    testdata = [[c, MaskedTestData(0, 0), 0o54]]
    run_tests("TEST: NA (masked): simple", testdata)


def test_NA_masked_invalid_args():
    c = NotEqualAlphabetic
    testdata = [
        [c, MaskedTestData(0, 32), 0],
        [c, MaskedTestData(2, 0), 0]
    ]
    run_exception_tests("TEST: NA (masked): invalid args", testdata)


def test_NA_masked_args_range():
    c = NotEqualAlphabetic
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, MaskedTestData(i, j), make_masked_opcode("NA", i, j)])
    run_tests("TEST: NA (masked): args range", testdata)


def test_NA_unmasked_simple():
    c = NotEqualAlphabetic
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2014]]
    run_tests("TEST: NA (unmasked): simple", testdata)


def test_NA_unmasked_invalid_args():
    c = NotEqualAlphabetic
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: NA (unmasked): invalid args", testdata)


def test_NA_unmasked_args_range():
    c = NotEqualAlphabetic
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("NA", i, j, k, l)])
    run_tests("TEST: NA (unmasked): args range", testdata)


# ######## NN ########

def test_NN_masked_simple():
    c = NotEqualNumeric
    testdata = [[c, MaskedTestData(0, 0), 0o50]]
    run_tests("TEST: NN (masked): simple", testdata)


def test_NN_masked_invalid_args():
    c = NotEqualNumeric
    testdata = [
        [c, MaskedTestData(0, 32), 0],
        [c, MaskedTestData(2, 0), 0]
    ]
    run_exception_tests("TEST: NN (masked): invalid args", testdata)


def test_NN_masked_args_range():
    c = NotEqualNumeric
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, MaskedTestData(i, j), make_masked_opcode("NN", i, j)])
    run_tests("TEST: NN (masked): args range", testdata)


def test_NN_unmasked_simple():
    c = NotEqualNumeric
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2010]]
    run_tests("TEST: NN (unmasked): simple", testdata)


def test_NN_unmasked_invalid_args():
    c = NotEqualNumeric
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: NN (unmasked): invalid args", testdata)


def test_NN_unmasked_args_range():
    c = NotEqualNumeric
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("NN", i, j, k, l)])
    run_tests("TEST: NN (unmasked): args range", testdata)


# ######## LA ########

def test_LA_masked_simple():
    c = LessThanOrEqualAlphabetic
    testdata = [[c, MaskedTestData(0, 0), 0o74]]
    run_tests("TEST: LA (masked): simple", testdata)


def test_LA_masked_invalid_args():
    c = LessThanOrEqualAlphabetic
    testdata = [
        [c, MaskedTestData(0, 32), 0],
        [c, MaskedTestData(2, 0), 0]
    ]
    run_exception_tests("TEST: LA (masked): invalid args", testdata)


def test_LA_masked_args_range():
    c = LessThanOrEqualAlphabetic
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, MaskedTestData(i, j), make_masked_opcode("LA", i, j)])
    run_tests("TEST: LA (masked): args range", testdata)


def test_LA_unmasked_simple():
    c = LessThanOrEqualAlphabetic
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2034]]
    run_tests("TEST: LA (unmasked): simple", testdata)


def test_LA_unmasked_invalid_args():
    c = LessThanOrEqualAlphabetic
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: LA (unmasked): invalid args", testdata)


def test_LA_unmasked_args_range():
    c = LessThanOrEqualAlphabetic
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("LA", i, j, k, l)])
    run_tests("TEST: LA (unmasked): args range", testdata)


# ######## LN ########

def test_LN_masked_simple():
    c = LessThanOrEqualNumeric
    testdata = [[c, MaskedTestData(0, 0), 0o70]]
    run_tests("TEST: LN (masked): simple", testdata)


def test_LN_masked_invalid_args():
    c = LessThanOrEqualNumeric
    testdata = [
        [c, MaskedTestData(0, 32), 0],
        [c, MaskedTestData(2, 0), 0]
    ]
    run_exception_tests("TEST: LN (masked): invalid args", testdata)


def test_LN_masked_args_range():
    c = LessThanOrEqualNumeric
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, MaskedTestData(i, j), make_masked_opcode("LN", i, j)])
    run_tests("TEST: LN (masked): args range", testdata)


def test_LN_unmasked_simple():
    c = LessThanOrEqualNumeric
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2030]]
    run_tests("TEST: LN (unmasked): simple", testdata)


def test_LN_unmasked_invalid_args():
    c = LessThanOrEqualNumeric
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: LN (unmasked): invalid args", testdata)


def test_LN_unmasked_args_range():
    c = LessThanOrEqualNumeric
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("LN", i, j, k, l)])
    run_tests("TEST: LN (unmasked): args range", testdata)


# ######## TX ########

def test_TX_masked_simple():
    c = Transfer
    testdata = [[c, MaskedTestData(0, 0), 0o60]]
    run_tests("TEST: TX (masked): simple", testdata)


def test_TX_masked_invalid_args():
    c = Transfer
    testdata = [
        [c, MaskedTestData(0, 32), 0],
        [c, MaskedTestData(2, 0), 0]
    ]
    run_exception_tests("TEST: TX (masked): invalid args", testdata)


def test_TX_masked_args_range():
    c = Transfer
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, MaskedTestData(i, j), make_masked_opcode("TX", i, j)])
    run_tests("TEST: TX (masked): args range", testdata)


def test_TX_unmasked_simple():
    c = Transfer
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2020]]
    run_tests("TEST: TX (unmasked): simple", testdata)


def test_TX_unmasked_invalid_args():
    c = Transfer
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: TX (unmasked): invalid args", testdata)


def test_TX_unmasked_args_range():
    c = Transfer
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("TX", i, j, k, l)])
    run_tests("TEST: TX (unmasked): args range", testdata)


# ######## TS ########

def test_TS_masked_simple():
    c = TransferChangeSequence
    testdata = [[c, MaskedTestData(0, 0), 0o44]]
    run_tests("TEST: TS (masked): simple", testdata)


def test_TS_masked_invalid_args():
    c = TransferChangeSequence
    testdata = [
        [c, MaskedTestData(0, 32), 0],
        [c, MaskedTestData(2, 0), 0]
    ]
    run_exception_tests("TEST: TS (masked): invalid args", testdata)


def test_TS_masked_args_range():
    c = TransferChangeSequence
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, MaskedTestData(i, j), make_masked_opcode("TS", i, j)])
    run_tests("TEST: TS (masked): args range", testdata)


def test_TS_unmasked_simple():
    c = TransferChangeSequence
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2004]]
    run_tests("TEST: TS (unmasked): simple", testdata)


def test_TS_unmasked_invalid_args():
    c = TransferChangeSequence
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: TS (unmasked): invalid args", testdata)


def test_TS_unmasked_args_range():
    c = TransferChangeSequence
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("TS", i, j, k, l)])
    run_tests("TEST: TS (unmasked): args range", testdata)


# ######## HA ########

def test_HA_masked_simple():
    c = HalfAdd
    testdata = [[c, MaskedTestData(0, 0), 0o65]]
    run_tests("TEST: HA (masked): simple", testdata)


def test_HA_masked_invalid_args():
    c = HalfAdd
    testdata = [
        [c, MaskedTestData(0, 32), 0],
        [c, MaskedTestData(2, 0), 0]
    ]
    run_exception_tests("TEST: HA (masked): invalid args", testdata)


def test_HA_masked_args_range():
    c = HalfAdd
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, MaskedTestData(i, j), make_masked_opcode("HA", i, j)])
    run_tests("TEST: HA (masked): args range", testdata)


def test_HA_unmasked_simple():
    c = HalfAdd
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2025]]
    run_tests("TEST: HA (unmasked): simple", testdata)


def test_HA_unmasked_invalid_args():
    c = HalfAdd
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: HA (unmasked): invalid args", testdata)


def test_HA_unmasked_args_range():
    c = HalfAdd
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("HA", i, j, k, l)])
    run_tests("TEST: HA (unmasked): args range", testdata)


# ######## SM ########

def test_SM_masked_simple():
    c = Superimpose
    testdata = [[c, MaskedTestData(0, 0), 0o45]]
    run_tests("TEST: SM (masked): simple", testdata)


def test_SM_masked_invalid_args():
    c = Superimpose
    testdata = [
        [c, MaskedTestData(0, 32), 0],
        [c, MaskedTestData(2, 0), 0]
    ]
    run_exception_tests("TEST: SM (masked): invalid args", testdata)


def test_SM_masked_args_range():
    c = Superimpose
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, MaskedTestData(i, j), make_masked_opcode("SM", i, j)])
    run_tests("TEST: SM (masked): args range", testdata)


def test_SM_unmasked_simple():
    c = Superimpose
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2005]]
    run_tests("TEST: SM (unmasked): simple", testdata)


def test_SM_unmasked_invalid_args():
    c = Superimpose
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: SM (unmasked): invalid args", testdata)


def test_SM_unmasked_args_range():
    c = Superimpose
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("SM", i, j, k, l)])
    run_tests("TEST: SM (unmasked): args range", testdata)


# ######## CP ########

def test_CP_masked_simple():
    c = CheckParity
    testdata = [[c, MaskedTestData(0, 0), 0o64]]
    run_tests("TEST: CP (masked): simple", testdata)


def test_CP_masked_invalid_args():
    c = CheckParity
    testdata = [
        [c, MaskedTestData(0, 32), 0],
        [c, MaskedTestData(2, 0), 0]
    ]
    run_exception_tests("TEST: CP (masked): invalid args", testdata)


def test_CP_masked_args_range():
    c = CheckParity
    testdata = []
    for i in range(2):
        for j in range(32):
            testdata.append([c, MaskedTestData(i, j), make_masked_opcode("CP", i, j)])
    run_tests("TEST: CP (masked): args range", testdata)


def test_CP_unmasked_simple():
    c = CheckParity
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2024]]
    run_tests("TEST: CP (unmasked): simple", testdata)


def test_CP_unmasked_invalid_args():
    c = CheckParity
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: CP (unmasked): invalid args", testdata)


def test_CP_unmasked_args_range():
    c = CheckParity
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("CP", i, j, k, l)])
    run_tests("TEST: CP (unmasked): args range", testdata)


# ######## BM ########

def test_BM_simple():
    c = BinaryMultiply
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o13]]
    run_tests("TEST: BM simple", testdata)


def test_BM_invalid_args():
    c = BinaryMultiply
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: BM invalid args", testdata)


def test_BM_args_range():
    c = BinaryMultiply
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("BM", i, j, k, l)])
    run_tests("TEST: BM args range", testdata)


# ######## DM ########

def test_DM_simple():
    c = DecimalMultiply
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o03]]
    run_tests("TEST: DM simple", testdata)


def test_DM_invalid_args():
    c = DecimalMultiply
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: DM invalid args", testdata)


def test_DM_args_range():
    c = DecimalMultiply
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("DM", i, j, k, l)])
    run_tests("TEST: DM args range", testdata)


# ######## BT ########

def test_BT_simple():
    c = BinaryAccumulate
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2013]]
    run_tests("TEST: BT simple", testdata)


def test_BT_invalid_args():
    c = BinaryAccumulate
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: BT invalid args", testdata)


def test_BT_args_range():
    c = BinaryAccumulate
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("BT", i, j, k, l)])
    run_tests("TEST: BT args range", testdata)


# ######## DT ########

def test_DT_simple():
    c = DecimalAccumulate
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2003]]
    run_tests("TEST: DT simple", testdata)


def test_DT_invalid_args():
    c = DecimalAccumulate
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: DT invalid args", testdata)


def test_DT_args_range():
    c = DecimalAccumulate
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("DT", i, j, k, l)])
    run_tests("TEST: DT args range", testdata)


# ######## MT ########

def test_MT_simple():
    c = MultipleTransfer
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o0020]]
    run_tests("TEST: MT simple", testdata)


def test_MT_invalid_args():
    c = MultipleTransfer
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: MT invalid args", testdata)


def test_MT_args_range():
    c = MultipleTransfer
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("MT", i, j, k, l)])
    run_tests("TEST: MT args range", testdata)


# ######## TN ########

def test_TN_simple():
    c = TransferNWords
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o1020]]
    run_tests("TEST: TN simple", testdata)


def test_TN_invalid_args():
    c = TransferNWords
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: TN invalid args", testdata)


def test_TN_args_range():
    c = TransferNWords
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("TN", i, j, k, l)])
    run_tests("TEST: TN args range", testdata)


# ######## CC ########

def test_CC_simple():
    c = ComputeOrthocount
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o1010]]
    run_tests("TEST: CC simple", testdata)


def test_CC_invalid_args():
    c = ComputeOrthocount
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: CC invalid args", testdata)


def test_CC_args_range():
    c = ComputeOrthocount
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("CC", i, j, k, l)])
    run_tests("TEST: CC args range", testdata)


# ######## IT ########

def test_IT_simple():
    c = ItemTransfer
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o1030]]
    run_tests("TEST: IT simple", testdata)


def test_IT_invalid_args():
    c = ItemTransfer
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: IT invalid args", testdata)


def test_IT_args_range():
    c = ItemTransfer
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("IT", i, j, k, l)])
    run_tests("TEST: IT args range", testdata)


# ######## EBA ########

def test_EBA_simple():
    c = ExtendedBinaryAdd
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o3013]]
    run_tests("TEST: EBA simple", testdata)


def test_EBA_invalid_args():
    c = ExtendedBinaryAdd
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: EBA invalid args", testdata)


def test_EBA_args_range():
    c = ExtendedBinaryAdd
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("EBA", i, j, k, l)])
    run_tests("TEST: EBA args range", testdata)


# ######## EBS ########

def test_EBS_simple():
    c = ExtendedBinarySubtract
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o3033]]
    run_tests("TEST: EBS simple", testdata)


def test_EBS_invalid_args():
    c = ExtendedBinarySubtract
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: EBS invalid args", testdata)


def test_EBS_args_range():
    c = ExtendedBinarySubtract
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("EBS", i, j, k, l)])
    run_tests("TEST: EBS args range", testdata)


# ######## RT ########

def test_RT_simple():
    c = RecordTransfer
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o3030]]
    run_tests("TEST: RT simple", testdata)


def test_RT_invalid_args():
    c = RecordTransfer
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: RT invalid args", testdata)


def test_RT_args_range():
    c = RecordTransfer
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("RT", i, j, k, l)])
    run_tests("TEST: RT args range", testdata)


# ######## MPC ########

def test_MPC_simple():
    c = ControlProgram
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2000]]
    run_tests("TEST: MPC simple", testdata)


def test_MPC_invalid_args():
    c = ControlProgram
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: MPC invalid args", testdata)


def test_MPC_args_range():
    c = ControlProgram
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("MPC", i, j, k, l)])
    run_tests("TEST: MPC args range", testdata)


# ######## PR ########

def test_PR_simple():
    c = Proceed
    testdata = [[c, None, 0o0000]]
    run_tests("TEST: PR simple", testdata)


# ######## SWS ########

def test_SWS_simple():
    c = ShiftWordAndSubstitute
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2006]]
    run_tests("TEST: SWS simple", testdata)


def test_SWS_invalid_args():
    c = ShiftWordAndSubstitute
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: SWS invalid args", testdata)


def test_SWS_args_range():
    c = ShiftWordAndSubstitute
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("SWS", i, j, k, l)])
    run_tests("TEST: SWS args range", testdata)


# ######## SPS ########

def test_SPS_simple():
    c = ShiftPreservingSignAndSubstitute
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2002]]
    run_tests("TEST: SPS simple", testdata)


def test_SPS_invalid_args():
    c = ShiftPreservingSignAndSubstitute
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: SPS invalid args", testdata)


def test_SPS_args_range():
    c = ShiftPreservingSignAndSubstitute
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("SPS", i, j, k, l)])
    run_tests("TEST: SPS args range", testdata)


# ######## SWE ########

def test_SWE_simple():
    c = ShiftWordAndExtract
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2016]]
    run_tests("TEST: SWE simple", testdata)


def test_SWE_invalid_args():
    c = ShiftWordAndExtract
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: SWE invalid args", testdata)


def test_SWE_args_range():
    c = ShiftWordAndExtract
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("SWE", i, j, k, l)])
    run_tests("TEST: SWE args range", testdata)


# ######## SPE ########

def test_SPE_simple():
    c = ShiftPreservingSignAndExtract
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2012]]
    run_tests("TEST: SPE simple", testdata)


def test_SPE_invalid_args():
    c = ShiftPreservingSignAndExtract
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: SPE invalid args", testdata)


def test_SPE_args_range():
    c = ShiftPreservingSignAndExtract
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("SPE", i, j, k, l)])
    run_tests("TEST: SPE args range", testdata)


# ######## SSL ########

def test_SSL_simple():
    c = ShiftAndSelect
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2026]]
    run_tests("TEST: SSL simple", testdata)


def test_SSL_invalid_args():
    c = ShiftAndSelect
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: SSL invalid args", testdata)


def test_SSL_args_range():
    c = ShiftAndSelect
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("SSL", i, j, k, l)])
    run_tests("TEST: SSL args range", testdata)


# ######## SS ########

def test_SS_simple():
    c = Substitute
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o0006]]
    run_tests("TEST: SS simple", testdata)


def test_SS_invalid_args():
    c = Substitute
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: SS invalid args", testdata)


def test_SS_args_range():
    c = Substitute
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("SS", i, j, k, l)])
    run_tests("TEST: SS args range", testdata)


# ######## EX ########

def test_EX_simple():
    c = Extract
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o0016]]
    run_tests("TEST: EX simple", testdata)


def test_EX_invalid_args():
    c = Extract
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: EX invalid args", testdata)


def test_EX_args_range():
    c = Extract
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("EX", i, j, k, l)])
    run_tests("TEST: EX args range", testdata)


# ######## RF ########

def test_RF_simple():
    c = ReadForward
    testdata = [[c, PeripheralTestData(0), 0o0072]]
    run_tests("TEST: RF simple", testdata)


def test_RF_invalid_args():
    c = ReadForward
    testdata = [
        [c, PeripheralTestData(-1), 0],
        [c, PeripheralTestData(64), 0]
    ]
    run_exception_tests("TEST: RF invalid args", testdata)


def test_RF_args_range():
    c = ReadForward
    testdata = []
    for p in range(64):
        testdata.append([c, PeripheralTestData(p), make_peripheral_opcode("RF", p)])
    run_tests("TEST: RF args range", testdata)


# ######## RB ########

def test_RB_simple():
    c = ReadBackward
    testdata = [[c, PeripheralTestData(0), 0o0052]]
    run_tests("TEST: RB simple", testdata)


def test_RB_invalid_args():
    c = ReadBackward
    testdata = [
        [c, PeripheralTestData(-1), 0],
        [c, PeripheralTestData(64), 0]
    ]
    run_exception_tests("TEST: RB invalid args", testdata)


def test_RB_args_range():
    c = ReadBackward
    testdata = []
    for p in range(64):
        testdata.append([c, PeripheralTestData(p), make_peripheral_opcode("RB", p)])
    run_tests("TEST: RB args range", testdata)


# ######## WF ########

def test_WF_simple():
    c = WriteForward
    testdata = [[c, PeripheralTestData(0), 0o0056]]
    run_tests("TEST: WF simple", testdata)


def test_WF_invalid_args():
    c = WriteForward
    testdata = [
        [c, PeripheralTestData(-1), 0],
        [c, PeripheralTestData(64), 0]
    ]
    run_exception_tests("TEST: WF invalid args", testdata)


def test_WF_args_range():
    c = WriteForward
    testdata = []
    for p in range(64):
        testdata.append([c, PeripheralTestData(p), make_peripheral_opcode("WF", p)])
    run_tests("TEST: WF args range", testdata)


# ######## RW ########

def test_RW_simple():
    c = Rewind
    testdata = [[c, PeripheralTestData(0), 0o0042]]
    run_tests("TEST: RW simple", testdata)


def test_RW_invalid_args():
    c = Rewind
    testdata = [
        [c, PeripheralTestData(-1), 0],
        [c, PeripheralTestData(64), 0]
    ]
    run_exception_tests("TEST: RW invalid args", testdata)


def test_RW_args_range():
    c = Rewind
    testdata = []
    for p in range(64):
        testdata.append([c, PeripheralTestData(p), make_peripheral_opcode("RW", p)])
    run_tests("TEST: RW args range", testdata)


# ######## PRA ########

def test_PRA_simple():
    c = PrintAlphabetic
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o0046]]
    run_tests("TEST: PRA simple", testdata)


def test_PRA_invalid_args():
    c = PrintAlphabetic
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: PRA invalid args", testdata)


def test_PRA_args_range():
    c = PrintAlphabetic
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_print_opcode("PRA", i, j, k, l)])
    run_tests("TEST: PRA args range", testdata)


# ######## PRD ########

def test_PRD_simple():
    c = PrintDecimal
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o0046]]
    run_tests("TEST: PRD simple", testdata)


def test_PRD_invalid_args():
    c = PrintDecimal
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: PRD invalid args", testdata)


def test_PRD_args_range():
    c = PrintDecimal
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_print_opcode("PRD", i, j, k, l)])
    run_tests("TEST: PRD args range", testdata)


# ######## PRO ########

def test_PRO_simple():
    c = PrintOctal
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o0046]]
    run_tests("TEST: PRO simple", testdata)


def test_PRO_invalid_args():
    c = PrintOctal
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: PRO invalid args", testdata)


def test_PRO_args_range():
    c = PrintOctal
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_print_opcode("PRO", i, j, k, l)])
    run_tests("TEST: PRO args range", testdata)


# ######## S ########

def test_S_simple():
    c = Simulator
    testdata = [[c, SimulatorTestData(0), 0o0007]]
    run_tests("TEST: S simple", testdata)


def test_S_invalid_args():
    c = Simulator
    testdata = [
        [c, SimulatorTestData(2), 0]
    ]
    run_exception_tests("TEST: S invalid args", testdata)


def test_S_args_range():
    c = Simulator
    testdata = [
        [c, SimulatorTestData(0), 0o0007],
        [c, SimulatorTestData(1), 0o4007]
    ]
    run_tests("TEST: S args range", testdata)


# ######## FBA ########

def test_FBA_simple():
    c = FloatingBinaryAdd
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o1001]]
    run_tests("TEST: FBA simple", testdata)


def test_FBA_invalid_args():
    c = FloatingBinaryAdd
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: FBA invalid args", testdata)


def test_FBA_args_range():
    c = FloatingBinaryAdd
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("FBA", i, j, k, l)])
    run_tests("TEST: FBA args range", testdata)


# ######## FDA ########

def test_FDA_simple():
    c = FloatingDecimalAdd
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o1021]]
    run_tests("TEST: FDA simple", testdata)


def test_FDA_invalid_args():
    c = FloatingDecimalAdd
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: FDA invalid args", testdata)


def test_FDA_args_range():
    c = FloatingDecimalAdd
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("FDA", i, j, k, l)])
    run_tests("TEST: FDA args range", testdata)


# ######## FBS ########

def test_FBS_simple():
    c = FloatingBinarySubtract
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o1011]]
    run_tests("TEST: FBS simple", testdata)


def test_FBS_invalid_args():
    c = FloatingBinarySubtract
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: FBS invalid args", testdata)


def test_FBS_args_range():
    c = FloatingBinarySubtract
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("FBS", i, j, k, l)])
    run_tests("TEST: FBS args range", testdata)


# ######## FDS ########

def test_FDS_simple():
    c = FloatingDecimalSubtract
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o1031]]
    run_tests("TEST: FDS simple", testdata)


def test_FDS_invalid_args():
    c = FloatingDecimalSubtract
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: FDS invalid args", testdata)


def test_FDS_args_range():
    c = FloatingDecimalSubtract
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("FDS", i, j, k, l)])
    run_tests("TEST: FDS args range", testdata)


# ######## FBD ########

def test_FBD_simple():
    c = FloatingBinaryDivide
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o1005]]
    run_tests("TEST: FBD simple", testdata)


def test_FBD_invalid_args():
    c = FloatingBinaryDivide
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: FBD invalid args", testdata)


def test_FBD_args_range():
    c = FloatingBinaryDivide
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("FBD", i, j, k, l)])
    run_tests("TEST: FBD args range", testdata)


# ######## FDD ########

def test_FDD_simple():
    c = FloatingDecimalDivide
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o1025]]
    run_tests("TEST: FDD simple", testdata)


def test_FDD_invalid_args():
    c = FloatingDecimalDivide
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: FDD invalid args", testdata)


def test_FDD_args_range():
    c = FloatingDecimalDivide
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("FDD", i, j, k, l)])
    run_tests("TEST: FDD args range", testdata)


# ######## FBAU ########

def test_FBAU_simple():
    c = FloatingBinaryAddUnnormalized
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o3001]]
    run_tests("TEST: FBAU simple", testdata)


def test_FBAU_invalid_args():
    c = FloatingBinaryAddUnnormalized
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: FBAU invalid args", testdata)


def test_FBAU_args_range():
    c = FloatingBinaryAddUnnormalized
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("FBAU", i, j, k, l)])
    run_tests("TEST: FBAU args range", testdata)


# ######## FDAU ########

def test_FDAU_simple():
    c = FloatingDecimalAddUnnormalized
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o3021]]
    run_tests("TEST: FDAU simple", testdata)


def test_FDAU_invalid_args():
    c = FloatingDecimalAddUnnormalized
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: FDAU invalid args", testdata)


def test_FDAU_args_range():
    c = FloatingDecimalAddUnnormalized
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("FDAU", i, j, k, l)])
    run_tests("TEST: FDAU args range", testdata)


# ######## FBSU ########

def test_FBSU_simple():
    c = FloatingBinarySubtractUnnormalized
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o3011]]
    run_tests("TEST: FBSU simple", testdata)


def test_FBSU_invalid_args():
    c = FloatingBinarySubtractUnnormalized
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: FBSU invalid args", testdata)


def test_FBSU_args_range():
    c = FloatingBinarySubtractUnnormalized
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("FBSU", i, j, k, l)])
    run_tests("TEST: FBSU args range", testdata)


# ######## FDSU ########

def test_FDSU_simple():
    c = FloatingDecimalSubtractUnnormalized
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o3031]]
    run_tests("TEST: FDSU simple", testdata)


def test_FDSU_invalid_args():
    c = FloatingDecimalSubtractUnnormalized
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: FDSU invalid args", testdata)


def test_FDSU_args_range():
    c = FloatingDecimalSubtractUnnormalized
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("FDSU", i, j, k, l)])
    run_tests("TEST: FDSU args range", testdata)


# ######## FBM ########

def test_FBM_simple():
    c = FloatingBinaryMultiply
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o3005]]
    run_tests("TEST: FBM simple", testdata)


def test_FBM_invalid_args():
    c = FloatingBinaryMultiply
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: FBM invalid args", testdata)


def test_FBM_args_range():
    c = FloatingBinaryMultiply
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("FBM", i, j, k, l)])
    run_tests("TEST: FBM args range", testdata)


# ######## FDM ########

def test_FDM_simple():
    c = FloatingDecimalMultiply
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o3025]]
    run_tests("TEST: FDM simple", testdata)


def test_FDM_invalid_args():
    c = FloatingDecimalMultiply
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: FDM invalid args", testdata)


def test_FDM_args_range():
    c = FloatingDecimalMultiply
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("FDM", i, j, k, l)])
    run_tests("TEST: FDM args range", testdata)


# ######## ULD ########

def test_ULD_simple():
    c = MultipleUnload
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o3015]]
    run_tests("TEST: ULD simple", testdata)


def test_ULD_invalid_args():
    c = MultipleUnload
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: ULD invalid args", testdata)


def test_ULD_args_range():
    c = MultipleUnload
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("ULD", i, j, k, l)])
    run_tests("TEST: ULD args range", testdata)


# ######## FBAE ########

def test_FBAE_simple():
    c = FloatingBinaryAddExtendedPrecision
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o0001]]
    run_tests("TEST: FBAE simple", testdata)


def test_FBAE_invalid_args():
    c = FloatingBinaryAddExtendedPrecision
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: FBAE invalid args", testdata)


def test_FBAE_args_range():
    c = FloatingBinaryAddExtendedPrecision
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("FBAE", i, j, k, l)])
    run_tests("TEST: FBAE args range", testdata)


# ######## FBSE ########

def test_FBSE_simple():
    c = FloatingBinarySubtractExtendedPrecision
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o0011]]
    run_tests("TEST: FBSE simple", testdata)


def test_FBSE_invalid_args():
    c = FloatingBinarySubtractExtendedPrecision
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: FBSE invalid args", testdata)


def test_FBSE_args_range():
    c = FloatingBinarySubtractExtendedPrecision
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("FBSE", i, j, k, l)])
    run_tests("TEST: FBSE args range", testdata)


# ######## BD ########

def test_BD_simple():
    c = FixedBinaryDivide
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o0005]]
    run_tests("TEST: BD simple", testdata)


def test_BD_invalid_args():
    c = FixedBinaryDivide
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: BD invalid args", testdata)


def test_BD_args_range():
    c = FixedBinaryDivide
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("BD", i, j, k, l)])
    run_tests("TEST: BD args range", testdata)


# ######## DD ########

def test_DD_simple():
    c = FixedDecimalDivide
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o0025]]
    run_tests("TEST: DD simple", testdata)


def test_DD_invalid_args():
    c = FixedDecimalDivide
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: DD invalid args", testdata)


def test_DD_args_range():
    c = FixedDecimalDivide
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("DD", i, j, k, l)])
    run_tests("TEST: DD args range", testdata)


# ######## FFN ########

def test_FFN_simple():
    c = FixedToFloatingNormalize
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o0015]]
    run_tests("TEST: FFN simple", testdata)


def test_FFN_invalid_args():
    c = FixedToFloatingNormalize
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: FFN invalid args", testdata)


def test_FFN_args_range():
    c = FixedToFloatingNormalize
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("FFN", i, j, k, l)])
    run_tests("TEST: FFN args range", testdata)


# ######## FCON ########

def test_FCON_simple():
    c = Conversion
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o0035]]
    run_tests("TEST: FCON simple", testdata)


def test_FCON_invalid_args():
    c = Conversion
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: FCON invalid args", testdata)


def test_FCON_args_range():
    c = Conversion
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("FCON", i, j, k, l)])
    run_tests("TEST: FCON args range", testdata)


# ######## FLN ########

def test_FLN_simple():
    c = FloatingLessThanNormalized
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o0030]]
    run_tests("TEST: FLN simple", testdata)


def test_FLN_invalid_args():
    c = FloatingLessThanNormalized
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: FLN invalid args", testdata)


def test_FLN_args_range():
    c = FloatingLessThanNormalized
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("FLN", i, j, k, l)])
    run_tests("TEST: FLN args range", testdata)


# ######## FNN ########

def test_FNN_simple():
    c = FloatingNotEqualNormalized
    testdata = [[c, UnmaskedTestData(0, 0, 0, 0), 0o2014]]
    run_tests("TEST: FNN simple", testdata)


def test_FNN_invalid_args():
    c = FloatingNotEqualNormalized
    testdata = [
        [c, UnmaskedTestData(2, 0, 0, 0), 0],
        [c, UnmaskedTestData(0, 2, 0, 0), 0],
        [c, UnmaskedTestData(0, 1, 2, 3), 0]
    ]
    run_exception_tests("TEST: FNN invalid args", testdata)


def test_FNN_args_range():
    c = FloatingNotEqualNormalized
    testdata = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    testdata.append([c, UnmaskedTestData(i, j, k, l), make_unmasked_opcode("FNN", i, j, k, l)])
    run_tests("TEST: FNN args range", testdata)


# ######## ALF ########

def test_ALF_simple():
    c = AlphanumericConstant
    testdata = [[c, ConstantTestData(0), 0o0]]
    run_tests("TEST: ALF simple", testdata)


def test_ALF_invalid_args():
    c = AlphanumericConstant
    testdata = [
        [c, ConstantTestData(-1), 0],
        [c, ConstantTestData(2 ** 48), 0]
    ]
    run_exception_tests("TEST: ALF invalid args", testdata)


def test_ALF_args_range():
    c = AlphanumericConstant
    testdata = [
        [c, ConstantTestData(0), 0],
        [c, ConstantTestData(1), 1],
        [c, ConstantTestData(4095), 4095],
        [c, ConstantTestData(4096), 4096],
        [c, ConstantTestData(2 ** 48 - 1), 2 ** 48 - 1],
    ]
    run_tests("TEST: ALF args range", testdata)


# ######## DEC ########

def test_DEC_simple():
    c = DecimalConstant
    testdata = [[c, ConstantTestData(0), 0o0]]
    run_tests("TEST: DEC simple", testdata)


def test_DEC_invalid_args():
    c = DecimalConstant
    testdata = [
        [c, ConstantTestData(-1), 0],
        [c, ConstantTestData(2 ** 48), 0]
    ]
    run_exception_tests("TEST: DEC invalid args", testdata)


def test_DEC_args_range():
    c = DecimalConstant
    testdata = [
        [c, ConstantTestData(0), 0],
        [c, ConstantTestData(1), 1],
        [c, ConstantTestData(4095), 4095],
        [c, ConstantTestData(4096), 4096],
        [c, ConstantTestData(2 ** 48 - 1), 2 ** 48 - 1],
    ]
    run_tests("TEST: DEC args range", testdata)


# ######## EBC ########

def test_EBC_simple():
    c = ExtendedBinaryConstant
    testdata = [[c, ConstantTestData(0), 0o0]]
    run_tests("TEST: EBC simple", testdata)


def test_EBC_invalid_args():
    c = ExtendedBinaryConstant
    testdata = [
        [c, ConstantTestData(-1), 0],
        [c, ConstantTestData(2 ** 48), 0]
    ]
    run_exception_tests("TEST: EBC invalid args", testdata)


def test_EBC_args_range():
    c = ExtendedBinaryConstant
    testdata = [
        [c, ConstantTestData(0), 0],
        [c, ConstantTestData(1), 1],
        [c, ConstantTestData(4095), 4095],
        [c, ConstantTestData(4096), 4096],
        [c, ConstantTestData(2 ** 48 - 1), 2 ** 48 - 1],
    ]
    run_tests("TEST: EBC args range", testdata)


# ######## FLBIN ########

def test_FLBIN_simple():
    c = FloatingBinaryConstant
    testdata = [[c, ConstantTestData(0), 0o0]]
    run_tests("TEST: FLBIN simple", testdata)


def test_FLBIN_invalid_args():
    c = FloatingBinaryConstant
    testdata = [
        [c, ConstantTestData(-1), 0],
        [c, ConstantTestData(2 ** 48), 0]
    ]
    run_exception_tests("TEST: FLBIN invalid args", testdata)


def test_FLBIN_args_range():
    c = FloatingBinaryConstant
    testdata = [
        [c, ConstantTestData(0), 0],
        [c, ConstantTestData(1), 1],
        [c, ConstantTestData(4095), 4095],
        [c, ConstantTestData(4096), 4096],
        [c, ConstantTestData(2 ** 48 - 1), 2 ** 48 - 1],
    ]
    run_tests("TEST: FLBIN args range", testdata)


# ######## FLDEC ########

def test_FLDEC_simple():
    c = FloatingDecimalConstant
    testdata = [[c, ConstantTestData(0), 0o0]]
    run_tests("TEST: FLDEC simple", testdata)


def test_FLDEC_invalid_args():
    c = FloatingDecimalConstant
    testdata = [
        [c, ConstantTestData(-1), 0],
        [c, ConstantTestData(2 ** 48), 0]
    ]
    run_exception_tests("TEST: FLDEC invalid args", testdata)


def test_FLDEC_args_range():
    c = FloatingDecimalConstant
    testdata = [
        [c, ConstantTestData(0), 0],
        [c, ConstantTestData(1), 1],
        [c, ConstantTestData(4095), 4095],
        [c, ConstantTestData(4096), 4096],
        [c, ConstantTestData(2 ** 48 - 1), 2 ** 48 - 1],
    ]
    run_tests("TEST: FLDEC args range", testdata)


# ######## FXBIN ########

def test_FXBIN_simple():
    c = FixedBinaryConstant
    testdata = [[c, ConstantTestData(0), 0o0]]
    run_tests("TEST: FXBIN simple", testdata)


def test_FXBIN_invalid_args():
    c = FixedBinaryConstant
    testdata = [
        [c, ConstantTestData(-1), 0],
        [c, ConstantTestData(2 ** 48), 0]
    ]
    run_exception_tests("TEST: FXBIN invalid args", testdata)


def test_FXBIN_args_range():
    c = FixedBinaryConstant
    testdata = [
        [c, ConstantTestData(0), 0],
        [c, ConstantTestData(1), 1],
        [c, ConstantTestData(4095), 4095],
        [c, ConstantTestData(4096), 4096],
        [c, ConstantTestData(2 ** 48 - 1), 2 ** 48 - 1],
    ]
    run_tests("TEST: FXBIN args range", testdata)


# ######## OCT ########

def test_OCT_simple():
    c = OctalConstant
    testdata = [[c, ConstantTestData(0), 0o0]]
    run_tests("TEST: OCT simple", testdata)


def test_OCT_invalid_args():
    c = OctalConstant
    testdata = [
        [c, ConstantTestData(-1), 0],
        [c, ConstantTestData(2 ** 48), 0]
    ]
    run_exception_tests("TEST: OCT invalid args", testdata)


def test_OCT_args_range():
    c = OctalConstant
    testdata = [
        [c, ConstantTestData(0), 0],
        [c, ConstantTestData(1), 1],
        [c, ConstantTestData(4095), 4095],
        [c, ConstantTestData(4096), 4096],
        [c, ConstantTestData(2 ** 48 - 1), 2 ** 48 - 1],
    ]
    run_tests("TEST: OCT args range", testdata)


def test_machine_instructions():
    print "TEST: check for duplicate machine instructions"
    # Generate all possible instruction codes and look for duplicates.
    opcodes = []
    for mnemonic in OPCODES:
        o = OPCODES[mnemonic]
        if o.type == "maskable":
            for i in range(2):
                for j in range(32):
                    opcode = make_masked_opcode(mnemonic, i, j)
                    assert opcode not in opcodes
                    opcodes.append(opcode)
        elif o.type == "unmasked":
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        for l in range(2):
                            opcode = make_unmasked_opcode(mnemonic, i, j, k, l)
                            assert opcode not in opcodes
                            opcodes.append(opcode)
        elif o.type == "peripheral":
            for i in range(64):
                opcode = make_peripheral_opcode(mnemonic, i)
                assert opcode not in opcodes
                opcodes.append(opcode)
        elif o.type == "print":
            # Note: PRA, PRD and PRO all generate the same range of opcodes.
            # Only count once.
            if mnemonic == "PRD":
                for i in range(2):
                    for j in range(2):
                        for k in range(2):
                            for l in range(2):
                                opcode = make_print_opcode(mnemonic, i, j, k, l)
                                assert opcode not in opcodes
                                opcodes.append(opcode)
        elif o.type == "simulator":
            opcode = 0o0007
            assert opcode not in opcodes
            opcodes.append(opcode)
            opcode = 0o4007
            assert opcode not in opcodes
            opcodes.append(opcode)
        else:
            assert False, "Invalid instruction type!"
