#!/usr/bin/env python

from registers import *


def my_assert(value, good):
    assert value == good, "Value is 0o%06o, should be 0o%06o" % (value, good)


def test_register_16bit_simple_defaults():
    print "TEST: register 16-bit simple default cases."
    r = Register()
    my_assert(r.value, 0)
    r = Register(4095)
    my_assert(r.value, 4095)
    r = Register(65535)
    my_assert(r.value, 65535)
    r = Register(2 ** 16 - 1)
    my_assert(r.value, 2 ** 16 - 1)


def test_register_16bit_invalid_args():
    print "TEST: register 16-bit invalid args."
    gotexc = False
    try:
        r = Register(-1)
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"

    gotexc = False
    try:
        r = Register(2 ** 16)
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"


def test_register_16bit_args_range():
    print "TEST: register 16-bit args range."
    r = Register()
    for i in range(2 ** 16, 16):
        r.value = i
        my_assert(r.value, i)


def test_register_16bit_slices():
    print "TEST: register 16-bit slices."
    r = Register(width=16)
    my_assert(r.value, 0)
    r = Register(0o777)
    my_assert(r.value, 0o777)
    r[1] = 1
    my_assert(r.value, 0o100777)
    r[1] = 0
    my_assert(r.value, 0o0777)
    r[1:16] = 0
    my_assert(r[1:16], 0)
    for i in range(r.width):
        r[i+1] = 1
        my_assert(r[i+1], 1)
        my_assert(r.value, 2 ** (16 - i - 1))
        r[i+1] = 0
        my_assert(r[i+1], 0)
        my_assert(r.value, 0)


def test_register_24bit_simple_defaults():
    print "TEST: register 24-bit simple default cases."
    r = Register(width=24)
    my_assert(r.value, 0)
    r = Register(4095, width=24)
    my_assert(r.value, 4095)
    r = Register(65535, width=24)
    my_assert(r.value, 65535)
    r = Register(2 ** 16 - 1, width=24)
    my_assert(r.value, 2 ** 16 - 1)
    r = Register(2 ** 24 - 1, width=24)
    my_assert(r.value, 2 ** 24 - 1)


def test_register_24bit_invalid_args():
    print "TEST: register 24-bit invalid args."
    gotexc = False
    try:
        r = Register(-1, width=24)
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"

    gotexc = False
    try:
        r = Register(2 ** 24, width=24)
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"


def test_register_24bit_args_range():
    print "TEST: register 24-bit args range."
    r = Register(width=24)
    for i in range(2 ** 24, 16):
        r.value = i
        my_assert(r.value, i)


def test_register_24bit_slices():
    print "TEST: register 24-bit slices."
    r = Register(width=24)
    my_assert(r.value, 0)
    r = Register(0o777, width=24)
    my_assert(r.value, 0o777)
    r[1] = 1
    my_assert(r.value, 2 ** 23 + 0o0777)
    r[1] = 0
    my_assert(r.value, 0o0777)
    r[1:r.width] = 0
    my_assert(r[1:r.width], 0)
    for i in range(r.width):
        r[i+1] = 1
        my_assert(r[i+1], 1)
        my_assert(r.value, 2 ** (r.width - i - 1))
        r[i+1] = 0
        my_assert(r[i+1], 0)
        my_assert(r.value, 0)


def test_registergroup_invalid_args():
    print "TEST: register group 16-bit invalid args."
    gotexc = False
    try:
        r = RegisterGroup(17)
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"

    gotexc = False
    try:
        r = RegisterGroup(25)
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"


def test_registergroup_16bit_simple_defaults():
    print "TEST: register group 16-bit simple default cases."
    r = RegisterGroup()
    for i in range(len(REGISTERS)):
        my_assert(r[i].value, 0)
    for i in range(len(REGISTERS)):
        r[i].value = 65535
        my_assert(r[i].value, 65535)


def test_registergroup_16bit_invalid_args():
    print "TEST: register group 16-bit invalid args."
    r = RegisterGroup()
    gotexc = False
    try:
        for i in range(len(REGISTERS)+1):
            r[i].value = 0
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"

    gotexc = False
    try:
        for i in range(len(REGISTERS)):
            r[i].value = -1
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"

    gotexc = False
    try:
        for i in range(len(REGISTERS)):
            r[i].value = 2 ** 16
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"


def test_registergroup_16bit_args_range():
    print "TEST: register group 16-bit args range."
    r = RegisterGroup()
    for i in range(len(REGISTERS)):
        for j in range(2 ** 16, 16):
            r[i].value = j
            my_assert(r[i].value, j)


def test_registergroup_24bit_simple_defaults():
    print "TEST: register group 16-bit simple default cases."
    r = RegisterGroup(24)
    for i in range(len(REGISTERS)):
        my_assert(r[i].value, 0)
    for i in range(len(REGISTERS)):
        r[i].value = 2** 24 - 1
        my_assert(r[i].value, 2 ** 24 - 1)


def test_registergroup_24bit_invalid_args():
    print "TEST: register group 24-bit invalid args."
    r = RegisterGroup(24)
    gotexc = False
    try:
        for i in range(len(REGISTERS)+1):
            r[i].value = 0
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"

    gotexc = False
    try:
        for i in range(len(REGISTERS)):
            r[i].value = -1
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"

    gotexc = False
    try:
        for i in range(len(REGISTERS)):
            r[i].value = 2 ** 24
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"


def test_registergroup_24bit_args_range():
    print "TEST: register group 24-bit args range."
    r = RegisterGroup(24)
    for i in range(len(REGISTERS)):
        for j in range(2 ** 24, 16):
            r[i].value = j
            my_assert(r[i].value, j)

