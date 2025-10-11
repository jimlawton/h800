# H-800/H-1800 Memory
# ===================

from h800.word import Word


class MemoryBank:
    """H-x800 memory bank class."""

    MEMORY_WIDTH = 48  # 48 data, 6 parity.
    BANK_SIZE = 2048

    def __init__(self):
        self._data = {}
        for addr in range(self.BANK_SIZE):
            self._data[addr] = Word(0)
        self._width = self.MEMORY_WIDTH
        self._current = 0

    def _check_value(self, value: int) -> None:
        if value < 0 or value > (1 << self._width) - 1:
            raise ValueError(f"Invalid value for {self._width}-bit word!")

    def _check_address(self, address: int) -> None:
        if address < 0 or address >= self.BANK_SIZE:
            raise ValueError("Invalid value for address!")

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self._data[i].value for i in range(key.start, key.stop)]
        return self._data[key].value

    @property
    def width(self) -> int:
        return self._width

    def read(self, address: int, parity: bool = False) -> int:
        # TODO: add parity handling
        self._check_address(address)
        return int(self._data[address])

    def write(self, address: int, value: int, parity: bool = False) -> None:
        # TODO: add parity handling
        self._check_address(address)
        self._check_value(value)
        self._data[address][1 : self._width] = value

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            for i in range(key.start, key.stop):
                self._data[i].value = value
        else:
            self._data[key].value = value

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return self

    def __next__(self):
        if self._current >= len(self._data):
            raise StopIteration
        else:
            self._current += 1
            return self._data[self._current - 1]

    def __repr__(self):
        text = ""
        for addr in self._data:
            text += f"0o{self._data[addr].value:016o} "
        return text

    def clear(self):
        for addr in self._data:
            self._data[addr].value = 0


class MemoryModule:
    """H-x800 memory module class."""

    NUM_BANKS = 4

    def __init__(self):
        self._data = {}
        for b in range(self.NUM_BANKS):
            self._data[b] = MemoryBank()
        self._current = 0

    def __getitem__(self, key):
        if isinstance(key, slice):
            banks = []
            for i in range(key.start, key.stop):
                banks.append(self._data[i])
            return banks
        else:
            return self._data[key]

    def __len__(self):
        return len(self._data)

    def size(self):
        return self.NUM_BANKS * len(self._data[0])


class ExpansionMemoryModule:
    """H-1800 expansion memory module class."""

    NUM_BANKS = 8

    def __init__(self):
        self._data = {}
        for b in range(self.NUM_BANKS):
            self._data[b] = MemoryBank()
        self._current = 0

    def __getitem__(self, key):
        if isinstance(key, slice):
            banks = []
            for i in range(key.start, key.stop):
                banks.append(self._data[i])
            return banks
        else:
            return self._data[key]

    def __len__(self):
        return len(self._data)

    def size(self):
        return self.NUM_BANKS * len(self._data[0])
