#!/usr/bin/env python

from .word import Word, InstructionWord


def my_assert(value, good):
    assert value == good, "Value is %d, should be %d" % (value, good)


def test_word_simple_defaults():
    print("TEST: word simple default cases.")
    w = Word()
    my_assert(w.value, 0)
    w = Word(4095)
    my_assert(w.value, 4095)
    w = Word(281406274007040)
    my_assert(w.value, 281406274007040)
    w = Word(2 ** 48 - 1)
    my_assert(w.value, 2 ** 48 - 1)


def test_word_invalid_args():
    gotexc = False
    try:
        print("TEST: test negative value")
        w = Word(-1)
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc is True, "Invalid value should have thrown an exception!"

    gotexc = False
    try:
        print("TEST: test too-large value")
        w = Word(2 ** 48)
        assert w is not None
    except ValueError:
        gotexc = True
    else:
        raise
    assert gotexc is True, "Invalid value should have thrown an exception!"


def test_inst_simple_defaults():
    print("TEST: inst simple default cases.")
    w = InstructionWord()
    my_assert(w.value, 0)
    w = InstructionWord(0, 4095, 0, 4095)
    my_assert(w.value, 68702703615)
    w = InstructionWord(4095, 0, 4095, 0)
    my_assert(w.value, 281406274007040)
    w = InstructionWord(4095, 4095, 4095, 4095)
    my_assert(w.value, 2 ** 48 - 1)


def test_inst_field_set_get():
    print("TEST: inst test field set/get.")
    w = InstructionWord()
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
