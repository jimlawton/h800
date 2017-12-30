# H-800/H-1800 Registers
# ======================

from h800.bitfield import BitField


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
    'S7':   31      # General Purpose Register
}

ALIASES = {
    'RAC':  28,     # Read Address Counter
    'DRAC': 29,     # Distributed Read Address Counter
    'WAC':  30,     # Write Address Counter
    'DWAC': 31      # Distributed Write Address Counter
}

REGISTER_NAMES = list(REGISTERS.keys()) + list(ALIASES.keys())


def registerName(number):
    "Return the register name for the specified number."
    for name in REGISTERS:
        if REGISTERS[name] == number:
            return name
    raise ValueError("Invalid register number %d!" % number)


def registerAlias(number):
    "Return the register alias for the specified number."
    for name in ALIASES:
        if ALIASES[name] == number:
            return name
    for name in REGISTERS:
        if REGISTERS[name] == number:
            return name
    raise ValueError("Invalid register number %d!" % number)


def registerNumber(name):
    "Return the register number for the specified name."
    if name in REGISTERS:
        return REGISTERS[name]
    if name in ALIASES:
        return ALIASES[name]
    raise ValueError("Invalid register name %s!" % name)


class Register(object):
    """H-x800 register class."""

    def __init__(self, data=0, name=None, width=16):
        if data < 0 or data > (2 ** width - 1):
            raise ValueError("Invalid value for %d-bit register!" % width)
        if name and name not in REGISTER_NAMES:
            raise ValueError("Invalid register name %s!" % name)
        if width != 16 and width != 24:
            raise ValueError("Invalid register width %d, must be 16 or 24!" %
                             width)
        self._data = BitField(0, width=width,
                              numbering=BitField.BIT_SCHEME_MSB_1,
                              order=BitField.BIT_ORDER_MSB_LEFT)
        self._data[1:width] = data
        self._name = name
        self._width = width

    @property
    def value(self):
        return int(self._data)

    @value.setter
    def value(self, value):
        if value < 0 or value > (2 ** self._width - 1):
            raise ValueError("Invalid value for %d-bit register!" %
                             self._width)
        self._data[1:self._width] = value

    @property
    def name(self):
        return self._name

    @property
    def width(self):
        return int(self._width)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self._data[key.start:key.stop]
        else:
            return self._data[key]

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            self._data[key.start:key.stop] = value
        else:
            self._data[key] = value

    def __len__(self):
        return self.width

    def __repr__(self):
        return "0o%06o" % self.value

    def clear(self):
        self._data.clear()


class RegisterGroup(object):
    """H-x800 register group class."""

    def __init__(self, width=16):
        self._width = width
        self._registers = {}
        for regname in REGISTERS:
            self._registers[REGISTERS[regname]] = \
                Register(name=regname, width=width)
        self._current = 0

    @property
    def width(self):
        return int(self._width)

    def __getitem__(self, key):
        if isinstance(key, slice):
            raise ValueError("Slices not supported!")
        if isinstance(key, str):
            if key not in REGISTERS:
                raise ValueError("Invalid register name %s!" % key)
            return self._registers[REGISTERS[key]]
        else:
            if key < 0 or key >= len(REGISTERS):
                raise ValueError("Invalid register number %d!" % key)
            return self._registers[key]

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            raise ValueError("Slices not supported!")
        if isinstance(key, str):
            self._registers[key] = value
        else:
            self._registers[REGISTERS[key]] = value

    def __len__(self):
        return len(self._registers)

    def __iter__(self):
        return self

    def __next__(self):
        if self._current >= len(REGISTERS):
            raise StopIteration
        else:
            self._current += 1
            return self._registers[self._current - 1]

    def __repr__(self):
        text = ""
        for r in self._registers:
            text += "%s " % self._registers[r]
        return text

    def clear(self):
        for register in self:
            register.clear()


class Registers(object):
    """H-x800 registers class."""

    _NUM_GROUPS = 8

    def __init__(self, width=16):
        self._width = width
        self._registers = {}
        for group in range(self._NUM_GROUPS):
            self._registers[group] = RegisterGroup(width=width)
        self._current = 0

    @property
    def width(self):
        return int(self._width)

    def __getitem__(self, key):
        if isinstance(key, slice):
            raise ValueError("Slices not supported!")
        if not isinstance(key, int):
            raise ValueError("Invalid register group number %s!" % key)
        else:
            if key < 0 or key >= self._NUM_GROUPS:
                raise ValueError("Invalid register group number %d!" % key)
            return self._registers[key]

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            raise ValueError("Slices not supported!")
        if not isinstance(key, int):
            raise ValueError("Invalid register group number %s!" % key)
        else:
            self._registers[key] = value

    def __len__(self):
        return len(self._registers)

    def __iter__(self):
        return self

    def __next__(self):
        if self._current >= self._NUM_GROUPS:
            raise StopIteration
        else:
            self._current += 1
            return self._registers[self._current - 1]

    def __repr__(self):
        text = ""
        for group in self._registers:
            text += "[%d] %s\n" % (group, self._registers[group])
        return text

    def clear(self):
        for group in self:
            group.clear()
