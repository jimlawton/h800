"""
H-1800 Registers Module
========================

This module implements the register file for the H-1800 simulator.

The H-1800 has a hierarchical register organization:
- 8 register groups (0-7)
- 32 registers per group
- 24-bit word width (can be extended to 48-bit for double precision)
- Mask-based partial register access

Register Types:
    - AU1, AU2: AU-CU Counters
    - SC, CSC: Sequence/Cosequence Counters
    - SH, CSH: Sequence/Cosequence History
    - UTR: Unprogrammed Transfer Register
    - MXR: Mask Index Register
    - X0-X7: Index Registers
    - R0-R7: General Purpose Registers
    - S0-S7: General Purpose Registers

Special Aliases:
    - RAC (S4): Read Address Counter
    - DRAC (S5): Distributed Read Address Counter
    - WAC (S6): Write Address Counter
    - DWAC (S7): Distributed Write Address Counter

Key Components:
    Register        - Single register implementation with masking
    RegisterGroup   - Group of 32 registers
    RegisterFile    - Complete register file with 8 groups of 32 registers
"""

from h800.bitfield import BitField

# Register definitions (register number within a group)
REGISTERS = {
    "AU1": 0,  # AU-CU Counter No. 1
    "AU2": 1,  # AU-CU Counter No. 2
    "SC": 2,  # Sequence Counter
    "CSC": 3,  # Cosequence Counter
    "SH": 4,  # Sequence History Register
    "CSH": 5,  # Cosequence History Register
    "UTR": 6,  # Unprogrammed Transfer Register
    "MXR": 7,  # Mask Index Register
    "X0": 8,  # Index Register 0
    "X1": 9,  # Index Register 1
    "X2": 10,  # Index Register 2
    "X3": 11,  # Index Register 3
    "X4": 12,  # Index Register 4
    "X5": 13,  # Index Register 5
    "X6": 14,  # Index Register 6
    "X7": 15,  # Index Register 7
    "R0": 16,  # General Purpose Register
    "R1": 17,  # General Purpose Register
    "R2": 18,  # General Purpose Register
    "R3": 19,  # General Purpose Register
    "R4": 20,  # General Purpose Register
    "R5": 21,  # General Purpose Register
    "R6": 22,  # General Purpose Register
    "R7": 23,  # General Purpose Register
    "S0": 24,  # General Purpose Register
    "S1": 25,  # General Purpose Register
    "S2": 26,  # General Purpose Register
    "S3": 27,  # General Purpose Register
    "S4": 28,  # General Purpose Register (RAC alias)
    "S5": 29,  # General Purpose Register (DRAC alias)
    "S6": 30,  # General Purpose Register (WAC alias)
    "S7": 31,  # General Purpose Register (DWAC alias)
}

# Register aliases for address counters
ALIASES = {
    "RAC": 28,  # Read Address Counter (S4)
    "DRAC": 29,  # Distributed Read Address Counter (S5)
    "WAC": 30,  # Write Address Counter (S6)
    "DWAC": 31,  # Distributed Write Address Counter (S7)
}

# Combined register names
REGISTER_NAMES = list(REGISTERS.keys()) + list(ALIASES.keys())


class RegisterError(Exception):
    """Exception raised for register access errors."""

    pass


class Register:
    """
    Single register implementation with masking support.

    Represents a register with bit-level access and mask-based read/write.
    Supports both 24-bit and 48-bit (double-precision) registers.

    Attributes:
        name: Register name (optional)
        value: Current register value (0 to 2^width-1)
        width: Register width in bits (24 or 48)
    """

    def __init__(self, name=None, value=0, width=24):
        """
        Initialize a register.

        Args:
            name: Register name (optional)
            value: Initial value (default: 0)
            width: Register width in bits (default: 24)
        """
        if width not in (24, 48):
            raise ValueError(f"Invalid register width: {width} (must be 24 or 48)")

        if value < 0 or value > (2**width - 1):
            raise ValueError(f"Invalid value for {width}-bit register: {value}")

        self.name = name
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
        """Get register value."""
        return int(self._data)

    @value.setter
    def value(self, val):
        """Set register value."""
        if val < 0 or val > self._max_value:
            raise ValueError(f"Invalid value for {self.width}-bit register: {val}")
        self._data.value = val

    def read(self, mask=None):
        """
        Read register with optional masking.

        Args:
            mask: Optional mask (bits set to 1 are read)

        Returns:
            Masked register value
        """
        if mask is None:
            return self.value

        # Apply mask (extract only bits where mask is 1)
        return self.value & mask

    def write(self, value, mask=None):
        """
        Write register with optional masking.

        Args:
            value: Value to write
            mask: Optional mask (bits set to 1 are written)

        If mask is provided, only bits where mask=1 are modified.
        Other bits retain their current value.
        """
        if value < 0 or value > self._max_value:
            raise ValueError(f"Invalid value for {self.width}-bit register: {value}")

        if mask is None:
            self.value = value
        else:
            # Keep existing bits where mask=0, write new bits where mask=1
            current = self.value
            new_value = (current & ~mask) | (value & mask)
            self.value = new_value

    def get_bit(self, bit):
        """
        Get a specific bit (1-indexed, MSB=1).

        Args:
            bit: Bit position (1 to width)

        Returns:
            Bit value (0 or 1)
        """
        if bit < 1 or bit > self.width:
            raise RegisterError(f"Bit {bit} out of range (1-{self.width})")
        return self._data[bit]

    def set_bit(self, bit, value):
        """
        Set a specific bit (1-indexed, MSB=1).

        Args:
            bit: Bit position (1 to width)
            value: Bit value (0 or 1)
        """
        if bit < 1 or bit > self.width:
            raise RegisterError(f"Bit {bit} out of range (1-{self.width})")
        self._data[bit] = 1 if value else 0

    def get_bits(self, start, end):
        """
        Get a range of bits (1-indexed, inclusive).

        Args:
            start: Starting bit position
            end: Ending bit position

        Returns:
            Value of bit range
        """
        if start < 1 or start > self.width or end < 1 or end > self.width:
            raise RegisterError(f"Bit range [{start}:{end}] out of range (1-{self.width})")
        return self._data[start:end]

    def set_bits(self, start, end, value):
        """
        Set a range of bits (1-indexed, inclusive).

        Args:
            start: Starting bit position
            end: Ending bit position
            value: Value to set
        """
        if start < 1 or start > self.width or end < 1 or end > self.width:
            raise RegisterError(f"Bit range [{start}:{end}] out of range (1-{self.width})")
        self._data[start:end] = value

    def clear(self):
        """Clear register to zero."""
        self._data.clear()

    def increment(self):
        """Increment register value (with wraparound)."""
        self.value = (self.value + 1) & self._max_value

    def decrement(self):
        """Decrement register value (with wraparound)."""
        self.value = (self.value - 1) & self._max_value

    def __int__(self):
        """Convert to integer."""
        return self.value

    def __repr__(self):
        if self.name:
            if self.width == 24:
                return f"Register({self.name}=0o{self.value:08o})"
            else:
                return f"Register({self.name}=0o{self.value:016o})"
        elif self.width == 24:
            return f"Register(0o{self.value:08o})"
        else:
            return f"Register(0o{self.value:016o})"


class RegisterGroup:
    """
    A group of 32 registers.

    The H-1800 has 8 register groups, each containing 32 registers.

    Attributes:
        group_number: Group number (0-7)
        width: Register width in bits
    """

    def __init__(self, group_number=0, width=24):
        """
        Initialize a register group.

        Args:
            group_number: Group number (0-7)
            width: Register width in bits (default: 24)
        """
        self.group_number = group_number
        self.width = width
        self._registers = {}

        # Initialize all 32 registers
        for reg_num in range(32):
            # Find name if this is a named register
            name = None
            for reg_name, num in REGISTERS.items():
                if num == reg_num:
                    name = reg_name
                    break
            self._registers[reg_num] = Register(name=name, width=width)

    def get(self, key):
        """
        Get a register by number or name.

        Args:
            key: Register number (0-31) or name (e.g., "X0", "RAC")

        Returns:
            Register instance
        """
        if isinstance(key, str):
            if key in REGISTERS:
                return self._registers[REGISTERS[key]]
            elif key in ALIASES:
                return self._registers[ALIASES[key]]
            else:
                raise KeyError(f"Unknown register name: {key}")
        else:
            if key < 0 or key >= 32:
                raise IndexError(f"Register number out of range: {key}")
            return self._registers[key]

    def set(self, key, value, mask=None):
        """
        Set a register value by number or name.

        Args:
            key: Register number (0-31) or name
            value: Value to set
            mask: Optional mask for partial write
        """
        register = self.get(key)
        register.write(value, mask)

    def read(self, key, mask=None):
        """
        Read a register value by number or name.

        Args:
            key: Register number (0-31) or name
            mask: Optional mask for partial read

        Returns:
            Register value (masked if mask provided)
        """
        register = self.get(key)
        return register.read(mask)

    def clear_all(self):
        """Clear all registers in this group."""
        for reg in self._registers.values():
            reg.clear()

    def dump(self):
        """
        Dump all registers in this group.

        Returns:
            Dictionary mapping register numbers to values
        """
        return {num: reg.value for num, reg in self._registers.items()}

    def __getitem__(self, key):
        """Array-style access: reg = group[0] or group["X0"]"""
        return self.get(key)

    def __setitem__(self, key, value):
        """Array-style write: group[0] = value or group["X0"] = value"""
        self.set(key, value)

    def __repr__(self):
        return f"RegisterGroup(group={self.group_number}, width={self.width})"


class RegisterFile:
    """
    Complete H-1800 register file.

    Contains 8 register groups, each with 32 registers.
    Total: 256 registers organized as 8 groups × 32 registers.

    Attributes:
        width: Register width in bits (24 for H-1800)
        num_groups: Number of register groups (8)
    """

    NUM_GROUPS = 8
    REGISTERS_PER_GROUP = 32

    def __init__(self, width=24):
        """
        Initialize the register file.

        Args:
            width: Register width in bits (default: 24)
        """
        self.width = width
        self.num_groups = self.NUM_GROUPS
        self._groups = {}

        # Initialize all 8 register groups
        for group_num in range(self.NUM_GROUPS):
            self._groups[group_num] = RegisterGroup(group_number=group_num, width=width)

        # Current active group (for instructions that don't specify group)
        self.active_group = 0

    def get_group(self, group_number):
        """
        Get a register group.

        Args:
            group_number: Group number (0-7)

        Returns:
            RegisterGroup instance
        """
        if group_number < 0 or group_number >= self.NUM_GROUPS:
            raise IndexError(f"Group number out of range: {group_number}")
        return self._groups[group_number]

    def get_register(self, group_number, register_key):
        """
        Get a specific register.

        Args:
            group_number: Group number (0-7)
            register_key: Register number (0-31) or name

        Returns:
            Register instance
        """
        group = self.get_group(group_number)
        return group.get(register_key)

    def set_register(self, group_number, register_key, value, mask=None):
        """
        Set a specific register value.

        Args:
            group_number: Group number (0-7)
            register_key: Register number (0-31) or name
            value: Value to set
            mask: Optional mask for partial write
        """
        group = self.get_group(group_number)
        group.set(register_key, value, mask)

    def read_register(self, group_number, register_key, mask=None):
        """
        Read a specific register value.

        Args:
            group_number: Group number (0-7)
            register_key: Register number (0-31) or name
            mask: Optional mask for partial read

        Returns:
            Register value (masked if mask provided)
        """
        group = self.get_group(group_number)
        return group.read(register_key, mask)

    def clear_all(self):
        """Clear all registers in all groups."""
        for group in self._groups.values():
            group.clear_all()

    def dump(self):
        """
        Dump all registers in all groups.

        Returns:
            Dictionary mapping (group, register) to values
        """
        dump_data = {}
        for group_num, group in self._groups.items():
            dump_data[group_num] = group.dump()
        return dump_data

    def dump_formatted(self, group=None):
        """
        Dump registers in formatted output.

        Args:
            group: Optional group number to dump (None = all groups)

        Returns:
            Formatted string representation
        """
        lines = []

        if group is not None:
            # Dump specific group
            groups = [group]
        else:
            # Dump all groups
            groups = range(self.NUM_GROUPS)

        for group_num in groups:
            lines.append(f"Group {group_num}:")
            reg_group = self._groups[group_num]

            # Dump named registers
            for name, num in sorted(REGISTERS.items(), key=lambda x: x[1]):
                if num < 32:
                    reg = reg_group.get(num)
                    lines.append(f"  {name:4s} [{num:2d}]: 0o{reg.value:08o}")

            lines.append("")

        return "\n".join(lines)

    def __getitem__(self, key):
        """Array-style access: reg = registers[group_num]"""
        return self.get_group(key)

    def __repr__(self):
        return f"RegisterFile(groups={self.NUM_GROUPS}, width={self.width})"
