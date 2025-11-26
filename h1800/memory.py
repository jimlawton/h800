"""
H-1800 Memory Module
====================

This module implements the memory subsystem for the H-1800 simulator.

The H-1800 uses magnetic core memory organized in words. This module simulates:
- Core memory storage (24-bit and 48-bit words)
- Memory read/write operations with masking
- Memory protection
- Memory-mapped I/O regions
- Memory bounds checking
- Memory initialization and clearing

Key Components:
    Memory          - Main memory class with storage array
    MemoryWord      - Individual memory word with masking support
    MemoryProtection - Memory protection control
    MemoryError     - Memory access error exceptions
"""

from h800.bitfield import BitField


class MemoryError(Exception):
    """Exception raised for memory access errors."""

    pass


class MemoryProtection:
    """Memory protection control."""

    def __init__(self):
        self.enabled = False
        self.protected_regions = []  # List of (start, end) tuples

    def add_protected_region(self, start, end):
        """Add a protected memory region."""
        self.protected_regions.append((start, end))

    def is_protected(self, address):
        """Check if address is in a protected region."""
        if not self.enabled:
            return False
        for start, end in self.protected_regions:
            if start <= address <= end:
                return True
        return False

    def check_read(self, address):
        """Check if read access is allowed."""
        # For now, reads are always allowed even in protected regions
        return True

    def check_write(self, address):
        """Check if write access is allowed."""
        if self.is_protected(address):
            return False
        return True


class MemoryWord:
    """
    Individual memory word with masking support.

    Supports both 24-bit and 48-bit words with mask-based read/write.

    Attributes:
        width: Word width in bits (24 or 48)
        value: Current word value
        mask: Optional mask for partial word operations
    """

    def __init__(self, width=24, value=0):
        """
        Initialize a memory word.

        Args:
            width: Word width in bits (24 or 48)
            value: Initial value (default: 0)
        """
        if width not in (24, 48):
            raise ValueError(f"Invalid word width: {width} (must be 24 or 48)")

        self.width = width
        self._max_value = (2**width) - 1
        self._data = BitField(
            value,
            width=width,
            numbering=BitField.BIT_SCHEME_MSB_1,
            order=BitField.BIT_ORDER_MSB_LEFT,
        )

    @property
    def value(self):
        """Get word value."""
        return int(self._data)

    @value.setter
    def value(self, val):
        """Set word value."""
        if val < 0 or val > self._max_value:
            raise ValueError(f"Value 0o{val:o} out of range for {self.width}-bit word")
        self._data.value = val

    def read(self, mask=None):
        """
        Read word with optional masking.

        Args:
            mask: Optional 48-bit mask (bits set to 1 are read)

        Returns:
            Masked word value
        """
        if mask is None:
            return self.value

        # Apply mask (extract only bits where mask is 1)
        return self.value & mask

    def write(self, value, mask=None):
        """
        Write word with optional masking.

        Args:
            value: Value to write
            mask: Optional 48-bit mask (bits set to 1 are written)

        If mask is provided, only bits where mask=1 are modified.
        Other bits retain their current value.
        """
        if mask is None:
            self.value = value
        else:
            # Keep existing bits where mask=0, write new bits where mask=1
            current = self.value
            new_value = (current & ~mask) | (value & mask)
            self.value = new_value

    def __int__(self):
        """Convert to integer."""
        return self.value

    def __repr__(self):
        if self.width == 24:
            return f"0o{self.value:08o}"
        else:
            return f"0o{self.value:016o}"


class Memory:
    """
    H-1800 Memory Subsystem.

    The memory is organized as an array of words.
    Each word can be 24-bit or 48-bit (for constants and double-precision).

    The H-1800 memory model:
    - 24-bit words for instructions and single-precision data
    - 48-bit words for constants and double-precision data
    - Mask-based partial word access

    Attributes:
        size        - Total memory size in words
        word_width  - Default bits per word (24 for H-1800)
        storage     - Internal storage array
        protection  - Memory protection control
    """

    WORD_WIDTH_24 = 24
    WORD_WIDTH_48 = 48
    DEFAULT_SIZE = 32768  # 32K words
    MAX_WORD_VALUE_24 = (2**24) - 1  # 0o77777777 (octal)
    MAX_WORD_VALUE_48 = (2**48) - 1  # 0o7777777777777777 (octal)

    def __init__(self, size=DEFAULT_SIZE, word_width=WORD_WIDTH_24):
        """
        Initialize memory subsystem.

        Args:
            size: Memory size in words (default: 32K)
            word_width: Default bits per word (default: 24)
        """
        if size <= 0:
            raise ValueError(f"Invalid memory size: {size}")
        if word_width not in (24, 48):
            raise ValueError(f"Invalid word width: {word_width} (must be 24 or 48)")

        self.size = size
        self.word_width = word_width
        self.max_value = (2**word_width) - 1
        self.storage = [MemoryWord(width=word_width) for _ in range(size)]
        self.protection = MemoryProtection()

        # Statistics
        self.read_count = 0
        self.write_count = 0

        # Track which addresses have 48-bit words
        self._wide_words = set()

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

    def _validate_value(self, value, width=None):
        """
        Validate a memory word value.

        Args:
            value: Word value to validate
            width: Word width (default: self.word_width)

        Raises:
            MemoryError: If value exceeds word width
        """
        if width is None:
            width = self.word_width

        if not isinstance(value, int):
            raise MemoryError(f"Value must be integer, got {type(value).__name__}")

        max_val = (2**width) - 1
        if value < 0 or value > max_val:
            raise MemoryError(f"Value 0o{value:o} out of range for {width}-bit word")

    def read(self, address, mask=None):
        """
        Read a word from memory.

        Args:
            address: Memory address to read from
            mask: Optional 48-bit mask for partial word read

        Returns:
            The word value at the specified address (masked if mask provided)

        Raises:
            MemoryError: If address is invalid or access is denied
        """
        self._validate_address(address)

        if not self.protection.check_read(address):
            raise MemoryError(f"Read access denied at address 0o{address:06o}")

        value = self.storage[address].read(mask)
        self.read_count += 1
        return value

    def write(self, address, value, mask=None):
        """
        Write a word to memory.

        Args:
            address: Memory address to write to
            value: Word value to write
            mask: Optional 48-bit mask for partial word write

        Raises:
            MemoryError: If address/value is invalid or access is denied
        """
        self._validate_address(address)

        if not self.protection.check_write(address):
            raise MemoryError(f"Write access denied at address 0o{address:06o}")

        # Get current word width at this address
        word_width = self.storage[address].width
        self._validate_value(value, word_width)

        self.storage[address].write(value, mask)
        self.write_count += 1

    def read_48(self, address, mask=None):
        """
        Read a 48-bit word from memory.

        For 48-bit constants, the word occupies two consecutive 24-bit locations,
        or a single 48-bit location if the memory was configured for 48-bit words.

        Args:
            address: Memory address to read from
            mask: Optional 48-bit mask

        Returns:
            48-bit value
        """
        if self.storage[address].width == 48:
            # Direct 48-bit read
            return self.read(address, mask)
        else:
            # Read two consecutive 24-bit words
            high = self.read(address)
            low = self.read(address + 1)
            value = (high << 24) | low

            if mask is not None:
                value &= mask

            return value

    def write_48(self, address, value, mask=None):
        """
        Write a 48-bit word to memory.

        Args:
            address: Memory address to write to
            value: 48-bit value to write
            mask: Optional 48-bit mask

        If the location is configured for 24-bit words, the value is split
        across two consecutive locations.
        """
        self._validate_value(value, 48)

        if self.storage[address].width == 48:
            # Direct 48-bit write
            self.write(address, value, mask)
            self._wide_words.add(address)
        else:
            # Split into two 24-bit words
            high = (value >> 24) & 0xFFFFFF
            low = value & 0xFFFFFF

            if mask is not None:
                # Split mask as well
                high_mask = (mask >> 24) & 0xFFFFFF
                low_mask = mask & 0xFFFFFF
                self.write(address, high, high_mask)
                self.write(address + 1, low, low_mask)
            else:
                self.write(address, high)
                self.write(address + 1, low)

    def set_word_width(self, address, width):
        """
        Set word width for a specific address.

        Args:
            address: Memory address
            width: Word width (24 or 48)
        """
        self._validate_address(address)
        if width not in (24, 48):
            raise ValueError(f"Invalid word width: {width}")

        # Preserve current value if possible
        current_value = self.storage[address].value
        self.storage[address] = MemoryWord(width=width, value=min(current_value, (2**width) - 1))

        if width == 48:
            self._wide_words.add(address)
        else:
            self._wide_words.discard(address)

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
        for i in range(self.size):
            self.storage[i].value = value

    def dump(self, start_address=0, count=16, format_octal=True, show_48bit=False):
        """
        Dump memory contents for debugging.

        Args:
            start_address: Starting address
            count: Number of words to dump
            format_octal: Format output in octal (default: True)
            show_48bit: Show 48-bit values if available

        Returns:
            Formatted string representation of memory contents
        """
        lines = []
        words_per_line = 8 if not show_48bit else 4

        for i in range(0, count, words_per_line):
            addr = start_address + i
            if addr >= self.size:
                break

            if format_octal:
                addr_str = f"0o{addr:06o}:"
                words = []
                for j in range(words_per_line):
                    if addr + j < self.size:
                        word = self.storage[addr + j]
                        if show_48bit and word.width == 48:
                            words.append(f"{word.value:016o}")
                        else:
                            words.append(f"{word.value:08o}")
                    else:
                        words.append("        ")
                lines.append(f"{addr_str} {' '.join(words)}")
            else:
                addr_str = f"0x{addr:04x}:"
                words = []
                for j in range(words_per_line):
                    if addr + j < self.size:
                        word = self.storage[addr + j]
                        if show_48bit and word.width == 48:
                            words.append(f"{word.value:012x}")
                        else:
                            words.append(f"{word.value:06x}")
                    else:
                        words.append("      ")
                lines.append(f"{addr_str} {' '.join(words)}")

        return "\n".join(lines)

    def load_image(self, data, start_address=0, word_width=None):
        """
        Load a memory image from a list of values.

        Args:
            data: List of word values to load
            start_address: Starting address to load at (default: 0)
            word_width: Word width for loaded data (default: self.word_width)
        """
        if word_width is not None and word_width not in (24, 48):
            raise ValueError(f"Invalid word width: {word_width}")

        for i, value in enumerate(data):
            addr = start_address + i
            if word_width == 48:
                self.set_word_width(addr, 48)
            self.write(addr, value)

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
