"""
H-1800 Memory Module
====================

This module implements the memory subsystem for the H-1800 simulator.

The H-1800 uses magnetic core memory organized in words. This module simulates:
- Core memory storage (24-bit words)
- Memory read/write operations
- Memory protection (if applicable)
- Memory-mapped I/O regions
- Memory bounds checking
- Memory initialization and clearing

Key Components:
    Memory          - Main memory class with storage array
    MemoryProtection - Memory protection control
    MemoryError     - Memory access error exceptions
"""


class MemoryError(Exception):
    """Exception raised for memory access errors."""

    pass


class MemoryProtection:
    """Memory protection control (for future implementation)."""

    def __init__(self):
        self.enabled = False
        self.protected_regions = []

    def check_read(self, address):
        """Check if read access is allowed."""
        # TODO: Implement protection checking
        return True

    def check_write(self, address):
        """Check if write access is allowed."""
        # TODO: Implement protection checking
        return True


class Memory:
    """
    H-1800 Memory Subsystem.

    The memory is organized as an array of 24-bit words.
    The default configuration provides 32K words (32768 words).

    Attributes:
        size        - Total memory size in words
        word_width  - Bits per word (24 for H-1800)
        storage     - Internal storage array
        protection  - Memory protection control
    """

    WORD_WIDTH = 24
    DEFAULT_SIZE = 32768  # 32K words
    MAX_WORD_VALUE = (2**WORD_WIDTH) - 1  # 0o77777777 (octal)

    def __init__(self, size=DEFAULT_SIZE, word_width=WORD_WIDTH):
        """
        Initialize memory subsystem.

        Args:
            size: Memory size in words (default: 32K)
            word_width: Bits per word (default: 24)
        """
        if size <= 0:
            raise ValueError(f"Invalid memory size: {size}")
        if word_width not in (16, 24):
            raise ValueError(f"Invalid word width: {word_width} (must be 16 or 24)")

        self.size = size
        self.word_width = word_width
        self.max_value = (2**word_width) - 1
        self.storage = [0] * size
        self.protection = MemoryProtection()

        # Statistics
        self.read_count = 0
        self.write_count = 0

    def _validate_address(self, address):
        """
        Validate a memory address.

        Args:
            address: Memory address to validate

        Raises:
            MemoryError: If address is out of bounds
        """
        if not isinstance(address, int):
            raise MemoryError(f"Address must be integer, got {type(address).__name__}")
        if address < 0 or address >= self.size:
            raise MemoryError(f"Address 0o{address:06o} out of bounds (0 - 0o{self.size - 1:06o})")

    def _validate_value(self, value):
        """
        Validate a memory word value.

        Args:
            value: Word value to validate

        Raises:
            MemoryError: If value exceeds word width
        """
        if not isinstance(value, int):
            raise MemoryError(f"Value must be integer, got {type(value).__name__}")
        if value < 0 or value > self.max_value:
            raise MemoryError(f"Value 0o{value:08o} out of range (0 - 0o{self.max_value:08o})")

    def read(self, address):
        """
        Read a word from memory.

        Args:
            address: Memory address to read from

        Returns:
            The word value at the specified address

        Raises:
            MemoryError: If address is invalid or access is denied
        """
        self._validate_address(address)

        if not self.protection.check_read(address):
            raise MemoryError(f"Read access denied at address 0o{address:06o}")

        value = self.storage[address]
        self.read_count += 1
        return value

    def write(self, address, value):
        """
        Write a word to memory.

        Args:
            address: Memory address to write to
            value: Word value to write

        Raises:
            MemoryError: If address/value is invalid or access is denied
        """
        self._validate_address(address)
        self._validate_value(value)

        if not self.protection.check_write(address):
            raise MemoryError(f"Write access denied at address 0o{address:06o}")

        self.storage[address] = value
        self.write_count += 1

    def read_block(self, start_address, count):
        """
        Read multiple consecutive words from memory.

        Args:
            start_address: Starting address
            count: Number of words to read

        Returns:
            List of word values
        """
        return [self.read(start_address + i) for i in range(count)]

    def write_block(self, start_address, values):
        """
        Write multiple consecutive words to memory.

        Args:
            start_address: Starting address
            values: List of word values to write
        """
        for i, value in enumerate(values):
            self.write(start_address + i, value)

    def clear(self, value=0):
        """
        Clear all memory to a specified value.

        Args:
            value: Value to fill memory with (default: 0)
        """
        self._validate_value(value)
        self.storage = [value] * self.size

    def dump(self, start_address=0, count=16, format_octal=True):
        """
        Dump memory contents for debugging.

        Args:
            start_address: Starting address
            count: Number of words to dump
            format_octal: Format output in octal (default: True)

        Returns:
            Formatted string representation of memory contents
        """
        lines = []
        for i in range(0, count, 8):
            addr = start_address + i
            if addr >= self.size:
                break

            if format_octal:
                addr_str = f"0o{addr:06o}:"
                words = []
                for j in range(8):
                    if addr + j < self.size:
                        word = self.storage[addr + j]
                        words.append(f"{word:08o}")
                    else:
                        words.append("        ")
                lines.append(f"{addr_str} {' '.join(words)}")
            else:
                addr_str = f"0x{addr:04x}:"
                words = []
                for j in range(8):
                    if addr + j < self.size:
                        word = self.storage[addr + j]
                        words.append(f"{word:06x}")
                    else:
                        words.append("      ")
                lines.append(f"{addr_str} {' '.join(words)}")

        return "\n".join(lines)

    def load_image(self, data, start_address=0):
        """
        Load a memory image from a list of values.

        Args:
            data: List of word values to load
            start_address: Starting address to load at (default: 0)
        """
        self.write_block(start_address, data)

    def save_image(self, start_address=0, count=None):
        """
        Save a memory image to a list of values.

        Args:
            start_address: Starting address (default: 0)
            count: Number of words to save (default: all remaining)

        Returns:
            List of word values
        """
        if count is None:
            count = self.size - start_address
        return self.read_block(start_address, count)

    def reset_statistics(self):
        """Reset memory access statistics."""
        self.read_count = 0
        self.write_count = 0

    def __len__(self):
        """Return memory size in words."""
        return self.size

    def __getitem__(self, address):
        """Allow array-style read access: value = memory[addr]"""
        return self.read(address)

    def __setitem__(self, address, value):
        """Allow array-style write access: memory[addr] = value"""
        self.write(address, value)

    def __repr__(self):
        return (
            f"Memory(size={self.size} words, width={self.word_width} bits, "
            f"reads={self.read_count}, writes={self.write_count})"
        )
