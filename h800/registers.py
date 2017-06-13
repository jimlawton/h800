#!/usr/bin/env python

# H-800/H-1800 Registers
# ======================

from bitfield import BitField


REGISTERS = {
    'AU1':   0,     # AU-CU Counter No. 1
    'AU2':   1,     # AU-CU Counter No. 2
    'SC':    2,     # Sequence Counter
    'CSC':   3,     # Cosequence Counter
    'SH':    4,     # Sequence History Register
    'CSH':   5,     # Cosequence History Register
    'UTR':   6,     # Unprogrammed Transfer Register
    'MXR':   7,     # Mask Index Register
    'X0':    8,     # Index Register 0
    'X1':    9,     # Index Register 1
    'X2':   10,     # Index Register 2
    'X3':   11,     # Index Register 3
    'X4':   12,     # Index Register 4
    'X5':   13,     # Index Register 5
    'X6':   14,     # Index Register 6
    'X7':   15,     # Index Register 7
    'R0':   16,     # General Purpose Register
    'R1':   17,     # General Purpose Register
    'R2':   18,     # General Purpose Register
    'R3':   19,     # General Purpose Register
    'R4':   20,     # General Purpose Register
    'R5':   21,     # General Purpose Register
    'R6':   22,     # General Purpose Register
    'R7':   23,     # General Purpose Register
    'S0':   24,     # General Purpose Register
    'S1':   25,     # General Purpose Register
    'S2':   26,     # General Purpose Register
    'S3':   27,     # General Purpose Register
    'S4':   28,     # General Purpose Register
    'S5':   29,     # General Purpose Register
    'S6':   30,     # General Purpose Register
    'S7':   31,     # General Purpose Register
    'RAC':  28,     # Read Address Counter
    'DRAC': 29,     # Distributed Read Address Counter
    'WAC':  30,     # Write Address Counter
    'DWAC': 31      # Distributed Write Address Counter
}


def registerName(number):
    "Return the register name for the specified number."
    for name in REGISTERS:
        if REGISTERS[name] == number:
            return name
    raise ValueError("Invalid register number %d!" % number)


def registerNumber(name):
    "Return the register number for the specified name."
    if name in REGISTERS:
        return REGISTERS[name]
    raise ValueError("Invalid register name %s!" % name)


class Register(object):
    """H-x800 register class."""

    def __init__(self, data=0, name=None, width=16):
        self._data = BitField(0, width=width,
                             numbering=BitField.BIT_SCHEME_MSB_1,
                             order=BitField.BIT_ORDER_MSB_LEFT)
        self._data[1:16] = data
        self._name = name
        self._width = width

    @property
    def value(self):
        return int(self._data)

    @value.setter
    def value(self, value):
        self._data.value = value

