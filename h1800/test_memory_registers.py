"""
Test module for H-1800 memory and register classes.

Tests memory and register operations including 48-bit word support and masking.
"""

import pytest

from h1800.memory import Memory, MemoryError, MemoryProtection, MemoryWord
from h1800.registers import (
    ALIASES,
    REGISTERS,
    Register,
    RegisterFile,
    RegisterGroup,
)

# =============================================================================
# MemoryWord Tests
# =============================================================================


class TestMemoryWord:
    """Test MemoryWord class."""

    def test_create_24bit_word(self):
        """Test creating a 24-bit memory word."""
        word = MemoryWord(width=24, value=0o12345670)
        assert word.width == 24
        assert word.value == 0o12345670

    def test_create_48bit_word(self):
        """Test creating a 48-bit memory word."""
        word = MemoryWord(width=48, value=0o123456701234567)
        assert word.width == 48
        assert word.value == 0o123456701234567

    def test_invalid_width(self):
        """Test that invalid widths are rejected."""
        with pytest.raises(ValueError):
            MemoryWord(width=16)
        with pytest.raises(ValueError):
            MemoryWord(width=32)

    def test_value_overflow(self):
        """Test that values exceeding width are rejected."""
        word = MemoryWord(width=24)
        with pytest.raises(ValueError):
            word.value = 0o100000000  # Too large for 24 bits

    def test_read_without_mask(self):
        """Test reading word without mask."""
        word = MemoryWord(width=24, value=0o12345670)
        assert word.read() == 0o12345670

    def test_read_with_mask(self):
        """Test reading word with mask."""
        word = MemoryWord(width=24, value=0o77777777)
        # Mask to read only lower 12 bits
        mask = 0o000007777
        result = word.read(mask)
        assert result == 0o7777

    def test_write_without_mask(self):
        """Test writing word without mask."""
        word = MemoryWord(width=24, value=0)
        word.write(0o12345670)
        assert word.value == 0o12345670

    def test_write_with_mask(self):
        """Test writing word with mask (partial update)."""
        word = MemoryWord(width=24, value=0o77777777)
        # Write only lower 12 bits
        mask = 0o000007777
        word.write(0o00001234, mask)
        # Upper bits should be preserved, lower bits updated
        assert word.value == 0o77771234

    def test_repr(self):
        """Test string representation."""
        word24 = MemoryWord(width=24, value=0o12345670)
        assert "12345670" in repr(word24)

        word48 = MemoryWord(width=48, value=0o123456701234567)
        assert "123456701234567" in repr(word48)


# =============================================================================
# Memory Tests
# =============================================================================


class TestMemory:
    """Test Memory class."""

    def test_create_default_memory(self):
        """Test creating memory with default parameters."""
        mem = Memory()
        assert mem.size == 32768
        assert mem.word_width == 24
        assert len(mem.storage) == 32768

    def test_create_custom_size(self):
        """Test creating memory with custom size."""
        mem = Memory(size=1024)
        assert mem.size == 1024
        assert len(mem.storage) == 1024

    def test_invalid_size(self):
        """Test that invalid sizes are rejected."""
        with pytest.raises(ValueError):
            Memory(size=0)
        with pytest.raises(ValueError):
            Memory(size=-100)

    def test_read_write(self):
        """Test basic read and write operations."""
        mem = Memory(size=100)
        mem.write(0, 0o12345670)
        assert mem.read(0) == 0o12345670

    def test_read_write_with_mask(self):
        """Test masked read and write operations."""
        mem = Memory(size=100)

        # Write initial value
        mem.write(0, 0o77777777)

        # Write only lower 12 bits with mask
        mask = 0o000007777
        mem.write(0, 0o00001234, mask)

        # Verify partial update
        assert mem.read(0) == 0o77771234

        # Read only lower 12 bits
        assert mem.read(0, mask) == 0o1234

    def test_address_validation(self):
        """Test address bounds checking."""
        mem = Memory(size=100)

        # Valid addresses
        mem.write(0, 0o123)
        mem.write(99, 0o456)

        # Invalid addresses
        with pytest.raises(MemoryError):
            mem.read(-1)
        with pytest.raises(MemoryError):
            mem.read(100)
        with pytest.raises(MemoryError):
            mem.write(100, 0o123)

    def test_48bit_read_write(self):
        """Test 48-bit word operations."""
        mem = Memory(size=100)

        # Set address 0 to 48-bit width
        mem.set_word_width(0, 48)

        # Write 48-bit value
        value = 0o123456701234567
        mem.write_48(0, value)
        assert mem.read_48(0) == value

    def test_48bit_on_24bit_words(self):
        """Test 48-bit operations on 24-bit word memory."""
        mem = Memory(size=100, word_width=24)

        # Write 48-bit value to 24-bit memory (spans 2 words)
        value = 0o123456701234567
        mem.write_48(0, value)

        # Read it back
        result = mem.read_48(0)
        assert result == value

        # Verify it occupied two words
        high = (value >> 24) & 0xFFFFFF
        low = value & 0xFFFFFF
        assert mem.read(0) == high
        assert mem.read(1) == low

    def test_48bit_masking(self):
        """Test 48-bit operations with masking."""
        mem = Memory(size=100)
        mem.set_word_width(0, 48)

        # Write full 48-bit value
        mem.write_48(0, 0o777777777777777)

        # Write with mask (update only lower 24 bits)
        mask = 0o000000007777777
        mem.write_48(0, 0o123456701234567, mask)

        # Upper 24 bits should be preserved, lower 24 bits updated
        expected = 0o777777701234567
        assert mem.read_48(0) == expected

    def test_read_write_block(self):
        """Test block read and write operations."""
        mem = Memory(size=100)

        # Write block
        data = [0o111, 0o222, 0o333, 0o444, 0o555]
        mem.write_block(10, data)

        # Read block back
        result = mem.read_block(10, 5)
        assert result == data

    def test_clear(self):
        """Test clearing memory."""
        mem = Memory(size=100)

        # Write some data
        mem.write(0, 0o12345670)
        mem.write(10, 0o76543210)

        # Clear
        mem.clear()

        # Verify all zeros
        assert mem.read(0) == 0
        assert mem.read(10) == 0

    def test_load_save_image(self):
        """Test loading and saving memory images."""
        mem = Memory(size=100)

        # Load image
        data = [0o111, 0o222, 0o333, 0o444, 0o555]
        mem.load_image(data, start_address=10)

        # Save image
        result = mem.save_image(start_address=10, count=5)
        assert result == data

    def test_dump(self):
        """Test memory dump."""
        mem = Memory(size=100)
        mem.write(0, 0o12345670)
        mem.write(1, 0o76543210)

        dump = mem.dump(start_address=0, count=8)
        assert "12345670" in dump
        assert "76543210" in dump

    def test_statistics(self):
        """Test memory access statistics."""
        mem = Memory(size=100)

        assert mem.read_count == 0
        assert mem.write_count == 0

        mem.write(0, 0o123)
        assert mem.write_count == 1

        mem.read(0)
        assert mem.read_count == 1

        mem.read(0)
        assert mem.read_count == 2

    def test_array_access(self):
        """Test array-style memory access."""
        mem = Memory(size=100)

        # Array-style write
        mem[10] = 0o12345670
        assert mem[10] == 0o12345670

        # Array-style read
        assert mem[10] == 0o12345670


class TestMemoryProtection:
    """Test MemoryProtection class."""

    def test_create_protection(self):
        """Test creating memory protection."""
        prot = MemoryProtection()
        assert not prot.enabled
        assert len(prot.protected_regions) == 0

    def test_add_protected_region(self):
        """Test adding protected regions."""
        prot = MemoryProtection()
        prot.add_protected_region(100, 200)
        assert len(prot.protected_regions) == 1

    def test_is_protected(self):
        """Test checking if address is protected."""
        prot = MemoryProtection()
        prot.add_protected_region(100, 200)

        # Not enabled yet
        assert not prot.is_protected(150)

        # Enable protection
        prot.enabled = True
        assert prot.is_protected(150)
        assert prot.is_protected(100)
        assert prot.is_protected(200)
        assert not prot.is_protected(99)
        assert not prot.is_protected(201)

    def test_write_protection(self):
        """Test write protection enforcement."""
        mem = Memory(size=1000)
        mem.protection.enabled = True
        mem.protection.add_protected_region(100, 200)

        # Write to unprotected region
        mem.write(50, 0o123)
        assert mem.read(50) == 0o123

        # Write to protected region should fail
        with pytest.raises(MemoryError):
            mem.write(150, 0o456)


# =============================================================================
# Register Tests
# =============================================================================


class TestRegister:
    """Test Register class."""

    def test_create_register(self):
        """Test creating a register."""
        reg = Register(name="X0", value=0o12345670, width=24)
        assert reg.name == "X0"
        assert reg.value == 0o12345670
        assert reg.width == 24

    def test_create_48bit_register(self):
        """Test creating a 48-bit register."""
        reg = Register(width=48, value=0o123456701234567)
        assert reg.width == 48
        assert reg.value == 0o123456701234567

    def test_invalid_width(self):
        """Test that invalid widths are rejected."""
        with pytest.raises(ValueError):
            Register(width=16)

    def test_read_write(self):
        """Test basic read and write."""
        reg = Register(width=24)
        reg.write(0o12345670)
        assert reg.read() == 0o12345670

    def test_read_write_with_mask(self):
        """Test masked read and write."""
        reg = Register(width=24, value=0o77777777)

        # Write only lower 12 bits with mask
        mask = 0o000007777
        reg.write(0o00001234, mask)

        # Upper bits preserved, lower bits updated
        assert reg.value == 0o77771234

        # Read only lower 12 bits
        assert reg.read(mask) == 0o1234

    def test_bit_access(self):
        """Test individual bit access."""
        reg = Register(width=24, value=0)

        # Set bit
        reg.set_bit(1, 1)  # MSB
        assert reg.get_bit(1) == 1

        reg.set_bit(24, 1)  # LSB
        assert reg.get_bit(24) == 1

    def test_bit_range_access(self):
        """Test bit range access."""
        reg = Register(width=24, value=0o77777777)

        # Get lower 12 bits (bits 13-24)
        lower = reg.get_bits(13, 24)
        assert lower == 0o7777

        # Set upper 12 bits (bits 1-12)
        reg.set_bits(1, 12, 0o1234)
        upper = reg.get_bits(1, 12)
        assert upper == 0o1234

    def test_increment_decrement(self):
        """Test increment and decrement."""
        reg = Register(width=24, value=0o100)

        reg.increment()
        assert reg.value == 0o101

        reg.decrement()
        assert reg.value == 0o100

        # Test wraparound
        reg.value = 0o77777777
        reg.increment()
        assert reg.value == 0

        reg.decrement()
        assert reg.value == 0o77777777

    def test_clear(self):
        """Test clearing register."""
        reg = Register(width=24, value=0o12345670)
        reg.clear()
        assert reg.value == 0

    def test_repr(self):
        """Test string representation."""
        reg = Register(name="X0", width=24, value=0o12345670)
        rep = repr(reg)
        assert "X0" in rep
        assert "12345670" in rep


class TestRegisterGroup:
    """Test RegisterGroup class."""

    def test_create_group(self):
        """Test creating a register group."""
        group = RegisterGroup(group_number=0, width=24)
        assert group.group_number == 0
        assert group.width == 24

    def test_get_by_number(self):
        """Test getting register by number."""
        group = RegisterGroup()
        reg = group.get(0)
        assert reg is not None
        assert reg.name == "AU1"

    def test_get_by_name(self):
        """Test getting register by name."""
        group = RegisterGroup()
        reg = group.get("X0")
        assert reg is not None
        assert reg.name == "X0"

    def test_get_by_alias(self):
        """Test getting register by alias."""
        group = RegisterGroup()
        reg = group.get("RAC")  # Alias for S4
        assert reg is not None
        assert reg.name == "S4"

    def test_set_value(self):
        """Test setting register value."""
        group = RegisterGroup()
        group.set("X0", 0o12345670)
        assert group.get("X0").value == 0o12345670

    def test_set_with_mask(self):
        """Test setting register with mask."""
        group = RegisterGroup()
        group.set("X0", 0o77777777)
        mask = 0o000007777
        group.set("X0", 0o00001234, mask)
        assert group.get("X0").value == 0o77771234

    def test_read_with_mask(self):
        """Test reading register with mask."""
        group = RegisterGroup()
        group.set("X0", 0o77777777)
        mask = 0o000007777
        result = group.read("X0", mask)
        assert result == 0o7777

    def test_clear_all(self):
        """Test clearing all registers."""
        group = RegisterGroup()
        group.set("X0", 0o12345670)
        group.set("X1", 0o76543210)

        group.clear_all()

        assert group.get("X0").value == 0
        assert group.get("X1").value == 0

    def test_dump(self):
        """Test dumping register group."""
        group = RegisterGroup()
        group.set(0, 0o111)
        group.set(1, 0o222)

        dump = group.dump()
        assert dump[0] == 0o111
        assert dump[1] == 0o222

    def test_array_access(self):
        """Test array-style access."""
        group = RegisterGroup()
        group[0] = 0o12345670
        assert group[0].value == 0o12345670

        group["X0"] = 0o76543210
        assert group["X0"].value == 0o76543210


class TestRegisterFile:
    """Test RegisterFile class."""

    def test_create_register_file(self):
        """Test creating a register file."""
        rf = RegisterFile(width=24)
        assert rf.num_groups == 8
        assert rf.width == 24

    def test_get_group(self):
        """Test getting a register group."""
        rf = RegisterFile()
        group = rf.get_group(0)
        assert group is not None
        assert group.group_number == 0

    def test_get_register(self):
        """Test getting a specific register."""
        rf = RegisterFile()
        reg = rf.get_register(0, "X0")
        assert reg is not None
        assert reg.name == "X0"

    def test_set_register(self):
        """Test setting a register value."""
        rf = RegisterFile()
        rf.set_register(0, "X0", 0o12345670)
        reg = rf.get_register(0, "X0")
        assert reg.value == 0o12345670

    def test_set_register_with_mask(self):
        """Test setting register with mask."""
        rf = RegisterFile()
        rf.set_register(0, "X0", 0o77777777)
        mask = 0o000007777
        rf.set_register(0, "X0", 0o00001234, mask)
        reg = rf.get_register(0, "X0")
        assert reg.value == 0o77771234

    def test_read_register(self):
        """Test reading a register value."""
        rf = RegisterFile()
        rf.set_register(0, "X0", 0o12345670)
        value = rf.read_register(0, "X0")
        assert value == 0o12345670

    def test_read_register_with_mask(self):
        """Test reading register with mask."""
        rf = RegisterFile()
        rf.set_register(0, "X0", 0o77777777)
        mask = 0o000007777
        value = rf.read_register(0, "X0", mask)
        assert value == 0o7777

    def test_clear_all(self):
        """Test clearing all registers."""
        rf = RegisterFile()
        rf.set_register(0, "X0", 0o12345670)
        rf.set_register(1, "X1", 0o76543210)

        rf.clear_all()

        assert rf.read_register(0, "X0") == 0
        assert rf.read_register(1, "X1") == 0

    def test_dump(self):
        """Test dumping all registers."""
        rf = RegisterFile()
        rf.set_register(0, 0, 0o111)
        rf.set_register(0, 1, 0o222)

        dump = rf.dump()
        assert dump[0][0] == 0o111
        assert dump[0][1] == 0o222

    def test_dump_formatted(self):
        """Test formatted dump."""
        rf = RegisterFile()
        rf.set_register(0, "X0", 0o12345670)

        formatted = rf.dump_formatted(group=0)
        assert "X0" in formatted
        assert "12345670" in formatted

    def test_array_access(self):
        """Test array-style access."""
        rf = RegisterFile()
        group = rf[0]
        assert group is not None
        assert group.group_number == 0


class TestRegisterConstants:
    """Test register name constants."""

    def test_registers_dict(self):
        """Test REGISTERS dictionary."""
        assert "AU1" in REGISTERS
        assert "X0" in REGISTERS
        assert "R0" in REGISTERS
        assert "S7" in REGISTERS

        assert REGISTERS["AU1"] == 0
        assert REGISTERS["X0"] == 8
        assert REGISTERS["S7"] == 31

    def test_aliases_dict(self):
        """Test ALIASES dictionary."""
        assert "RAC" in ALIASES
        assert "DRAC" in ALIASES
        assert "WAC" in ALIASES
        assert "DWAC" in ALIASES

        assert ALIASES["RAC"] == 28
        assert ALIASES["DWAC"] == 31


# =============================================================================
# Integration Tests
# =============================================================================


class TestMemoryRegisterIntegration:
    """Test integration between memory and registers."""

    def test_load_from_memory_to_register(self):
        """Test loading value from memory to register."""
        mem = Memory(size=100)
        rf = RegisterFile()

        # Store value in memory
        mem.write(10, 0o12345670)

        # Load to register
        value = mem.read(10)
        rf.set_register(0, "X0", value)

        # Verify
        assert rf.read_register(0, "X0") == 0o12345670

    def test_store_from_register_to_memory(self):
        """Test storing value from register to memory."""
        mem = Memory(size=100)
        rf = RegisterFile()

        # Set register value
        rf.set_register(0, "X0", 0o76543210)

        # Store to memory
        value = rf.read_register(0, "X0")
        mem.write(20, value)

        # Verify
        assert mem.read(20) == 0o76543210

    def test_masked_transfer(self):
        """Test masked transfer between memory and register."""
        mem = Memory(size=100)
        rf = RegisterFile()

        # Initialize memory and register
        mem.write(10, 0o77777777)
        rf.set_register(0, "X0", 0o00000000)

        # Transfer with mask (only lower 12 bits)
        mask = 0o000007777
        value = mem.read(10, mask)
        rf.set_register(0, "X0", value, mask)

        # Verify partial transfer
        assert rf.read_register(0, "X0") == 0o7777

    def test_48bit_transfer(self):
        """Test 48-bit transfer between memory and register."""
        mem = Memory(size=100)
        mem.set_word_width(0, 48)

        # Create 48-bit register (simulated as double-precision)
        reg_high = Register(width=24)
        reg_low = Register(width=24)

        # Write 48-bit value to memory
        value_48 = 0o123456701234567
        mem.write_48(0, value_48)

        # Read to registers (split)
        read_value = mem.read_48(0)
        reg_high.value = (read_value >> 24) & 0xFFFFFF
        reg_low.value = read_value & 0xFFFFFF

        # Reconstruct
        reconstructed = (reg_high.value << 24) | reg_low.value
        assert reconstructed == value_48


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
