#!/usr/bin/env python

from .memory import MemoryBank, MemoryModule, ExpansionMemoryModule


def my_assert(value, good):
    assert value == good, "Value is 0o%016o, should be 0o%016o" % (value, good)


def test_memorybank_simple_defaults():
    print("TEST: memory bank simple default cases.")
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
    print("TEST: memory bank invalid args.")
    pass


def test_memorymodule_simple_defaults():
    print("TEST: memory module simple default cases.")
    m = MemoryModule()
    my_assert(m.size(), 8192)
    for i in range(len(m)):
        for j in range(len(m[i])):
            my_assert(m[i][j], 0)
    for i in range(len(m)):
        for j in range(len(m[i])):
            m[i][j] = 2 ** 48 - 1
            my_assert(m[i][j], 2 ** 48 - 1)
    for i in range(len(m)):
        m[i].clear()
    for i in range(len(m)):
        for j in range(len(m[i])):
            my_assert(m[i][j], 0)


def test_expansionmemorymodule_simple_defaults():
    print("TEST: expansion memory module simple default cases.")
    m = ExpansionMemoryModule()
    my_assert(m.size(), 16384)
    for i in range(len(m)):
        for j in range(len(m[i])):
            my_assert(m[i][j], 0)
    for i in range(len(m)):
        for j in range(len(m[i])):
            m[i][j] = 2 ** 48 - 1
            my_assert(m[i][j], 2 ** 48 - 1)
    for i in range(len(m)):
        m[i].clear()
    for i in range(len(m)):
        for j in range(len(m[i])):
            my_assert(m[i][j], 0)
