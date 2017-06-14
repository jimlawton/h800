#!/usr/bin/env python

from memory import *


def my_assert(value, good):
    assert value == good, "Value is 0o%016o, should be 0o%016o" % (value, good)


def test_memorybank_simple_defaults():
    print "TEST: memory bank simple default cases."
    m = MemoryBank()
    for i in range(len(m)):
        my_assert(m[i], 0)
    for w in m:
        my_assert(w.value, 0)
    for i in range(len(m)):
        m[i] = 2 ** 48 - 1
        my_assert(m[i], 2 ** 48 - 1)
    m.clear()
    for w in m:
        my_assert(w.value, 0)


def test_memorybank_invalid_args():
    print "TEST: memory bank invalid args."
    gotexc = False
    try:
        m = MemoryBank(-1)
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"

    gotexc = False
    try:
        m = MemoryBank(5)
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc == True, "Invalid value should have thrown an exception!"

