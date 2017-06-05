#!/usr/bin/env python

from word import *


def test_simple_defaults():
    print "TEST: simple default cases."
    w = Word()
    assert w.value == 0, "Word is %d, should be 0" % w.value
    w = Word(0, 4095, 0, 4095)
    assert w.value == 68702703615, "Word is %d, should be 68702703615" % w.value
    w = Word(4095, 0, 4095, 0)
    assert w.value == 281406274007040, "Word is %d, should be 281406274007040" % w.value
    w = Word(4095, 4095, 4095, 4095)
    assert w.value == 2 ** 48 - 1, "Word is %d, should be %d" % (w.value, w.data.maxval)


def test_field_set_get():
    print "TEST: test field set/get."
    w = Word()
    assert w.value == 0, "Word is %d, should be 0" % w.value

    w.command = 4095
    assert w.command == 4095, "Field is %d, should be 4095" % w.command
    assert w.a == 0, "Field is %d, should be 0" % w.a
    assert w.b == 0, "Field is %d, should be 0" % w.b
    assert w.c == 0, "Field is %d, should be 0" % w.c
    assert w.value == 281406257233920, "Word is %d, should be 281406257233920" % w.value
    w.value = 0
    assert w.value == 0, "Word is %d, should be 0" % w.value

    w.a = 4095
    assert w.command == 0, "Field is %d, should be 0" % w.command
    assert w.a == 4095, "Field is %d, should be 4095" % w.a
    assert w.b == 0, "Field is %d, should be 0" % w.b
    assert w.c == 0, "Field is %d, should be 0" % w.c
    assert w.value == 68702699520, "Word is %d, should be 68702699520" % w.value
    w.value = 0
    assert w.value == 0, "Word is %d, should be 0" % w.value

    w.b = 4095
    assert w.command == 0, "Field is %d, should be 0" % w.command
    assert w.a == 0, "Field is %d, should be 0" % w.a
    assert w.b == 4095, "Field is %d, should be 4095" % w.b
    assert w.c == 0, "Field is %d, should be 0" % w.c
    assert w.value == 16773120, "Word is %d, should be 16773120" % w.value
    w.value = 0
    assert w.value == 0, "Word is %d, should be 0" % w.value

    w.c = 4095
    assert w.command == 0, "Field is %d, should be 0" % w.command
    assert w.a == 0, "Field is %d, should be 0" % w.a
    assert w.b == 0, "Field is %d, should be 0" % w.b
    assert w.c == 4095, "Field is %d, should be 4095" % w.c
    assert w.value == 4095, "Word is %d, should be 4095" % w.value
    w.value = 0
    assert w.value == 0, "Word is %d, should be 0" % w.value

