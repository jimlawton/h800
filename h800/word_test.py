#!/usr/bin/env python

from word import *


def my_assert(value, good):
    assert value == good, "Value is %d, should be %d" % (value, good)


def test_simple_defaults():
    print "TEST: simple default cases."
    w = Word()
    my_assert(w.value, 0)
    w = Word(0, 4095, 0, 4095)
    my_assert(w.value, 68702703615)
    w = Word(4095, 0, 4095, 0)
    my_assert(w.value, 281406274007040)
    w = Word(4095, 4095, 4095, 4095)
    my_assert(w.value, 2 ** 48 - 1)


def test_field_set_get():
    print "TEST: test field set/get."
    w = Word()
    my_assert(w.value, 0)

    w.command = 4095
    my_assert(w.command, 4095)
    my_assert(w.a, 0)
    my_assert(w.b, 0)
    my_assert(w.c, 0)
    my_assert(w.value, 281406257233920)
    w.value = 0
    my_assert(w.value, 0)

    w.a = 4095
    my_assert(w.command, 0)
    my_assert(w.a, 4095)
    my_assert(w.b, 0)
    my_assert(w.c, 0)
    my_assert(w.value, 68702699520)
    w.value = 0
    my_assert(w.value, 0)

    w.b = 4095
    my_assert(w.command, 0)
    my_assert(w.a, 0)
    my_assert(w.b, 4095)
    my_assert(w.c, 0)
    my_assert(w.value, 16773120)
    w.value = 0
    my_assert(w.value, 0)

    w.c = 4095
    my_assert(w.command, 0)
    my_assert(w.a, 0)
    my_assert(w.b, 0)
    my_assert(w.c, 4095)
    my_assert(w.value, 4095)
    w.value = 0
    my_assert(w.value, 0)

