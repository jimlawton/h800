#!/usr/bin/env python

from registers import *


def my_assert(value, good):
    assert value == good, "Value is 0o%06o, should be 0o%06o" % (value, good)


def test_registers_simple_defaults():
    print "TEST: registers simple default cases."
    r = Register()
    my_assert(r.value, 0)
    r = Register(4095)
    my_assert(r.value, 4095)
    r = Register(65535)
    my_assert(r.value, 65535)
    r = Register(2 ** 16 - 1)
    my_assert(r.value, 2 ** 16 - 1)

