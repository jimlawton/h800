# H-1800 Memory and Register Implementation

This document describes the memory and register implementations for the H-1800 simulator, including 48-bit word support and masking operations.

## Overview

The H-1800 memory and register subsystems support:
- 24-bit and 48-bit word operations
- Mask-based partial word access (critical for H-1800 instruction execution)
- Memory protection
- Register groups and aliases
- Bit-level access to registers and memory

## Memory Architecture

### MemoryWord Class

Individual memory words with configurable width and masking support.

```python
class MemoryWord:
    """
    Individual memory word with masking support.
    
    Attributes:
        width: Word width in bits (24 or 48)
        value: Current word value
    """
```

**Key Features:**
- Supports 24-bit and 48-bit words
- Mask-based read/write for partial updates
- Uses BitField for bit-level operations

**Examples:**

```python
# Create 24-bit word
word = MemoryWord(width=24, value=0o12345670)

# Read without mask
value = word.read()  # Returns: 0o12345670

# Read with mask (extract lower 12 bits)
mask = 0o000007777
value = word.read(mask)  # Returns: 0o005670

# Write with mask (preserve upper bits, update lower bits)
word.write(0o00001234, mask=0o000007777)
# Result: 0o12341234 (upper 12 bits preserved)
```

### Memory Class

Main memory subsystem with array of MemoryWord instances.

```python
class Memory:
    """
    H-1800 Memory Subsystem.
    
    Attributes:
        size: Total memory size in words (default: 32K)
        word_width: Default bits per word (24 or 48)
        storage: Array of MemoryWord instances
        protection: Memory protection control
    """
```

**Configuration:**
- Default: 32K words × 24 bits
- Configurable size (1 to MAX_SIZE words)
- Configurable word width (24 or 48 bits)
- Per-address word width (can mix 24-bit and 48-bit words)

**Basic Operations:**

```python
# Create memory
mem = Memory(size=32768, word_width=24)

# Read/write 24-bit words
mem.write(address=100, value=0o12345670)
value = mem.read(address=100)

# Read/write with masking
mask = 0o000007777
mem.write(address=100, value=0o00001234, mask=mask)
value = mem.read(address=100, mask=mask)

# Block operations
data = [0o111, 0o222, 0o333, 0o444]
mem.write_block(start_address=0, values=data)
result = mem.read_block(start_address=0, count=4)

# Clear memory
mem.clear(value=0)
```

**48-Bit Operations:**

The H-1800 uses 48-bit words for constants and double-precision data.

```python
# Set a location to 48-bit width
mem.set_word_width(address=0, width=48)

# Write 48-bit value
mem.write_48(address=0, value=0o123456701234567)

# Read 48-bit value
value = mem.read_48(address=0)

# With masking
mask = 0o000000007777777  # Lower 24 bits
mem.write_48(address=0, value=0o123456701234567, mask=mask)
```

**48-Bit on 24-Bit Memory:**

When a 48-bit value is written to 24-bit memory, it spans two consecutive locations:

```python
mem = Memory(size=1024, word_width=24)

# Write 48-bit value (spans addresses 100-101)
value_48 = 0o123456701234567
mem.write_48(address=100, value=value_48)

# Read back
result = mem.read_48(address=100)

# Internally stored as:
#   mem[100] = 0o12345670  (upper 24 bits)
#   mem[101] = 0o01234567  (lower 24 bits)
```

**Memory Protection:**

```python
# Enable protection
mem.protection.enabled = True

# Add protected region
mem.protection.add_protected_region(start=100, end=200)

# Reads are allowed
value = mem.read(150)  # OK

# Writes to protected region fail
mem.write(150, value)  # Raises MemoryError
```

**Memory Dump:**

```python
# Dump memory contents (octal format)
dump = mem.dump(start_address=0, count=16, format_octal=True)
print(dump)
# Output:
# 0o000000: 12345670 76543210 00000000 00000000 ...
# 0o000010: ...

# Show 48-bit words
dump = mem.dump(start_address=0, count=8, show_48bit=True)
```

**Statistics:**

```python
# Memory tracks access counts
print(f"Reads: {mem.read_count}")
print(f"Writes: {mem.write_count}")

# Reset statistics
mem.reset_statistics()
```

## Register Architecture

### Register Class

Individual register with masking and bit-level access.

```python
class Register:
    """
    Single register with masking support.
    
    Attributes:
        name: Register name (optional)
        value: Current register value
        width: Register width in bits (24 or 48)
    """
```

**Basic Operations:**

```python
# Create register
reg = Register(name="X0", value=0o12345670, width=24)

# Read/write
reg.write(0o76543210)
value = reg.read()

# Masked read/write
mask = 0o000007777
reg.write(0o00001234, mask=mask)
value = reg.read(mask=mask)
```

**Bit-Level Access:**

```python
# Individual bit access (1-indexed, MSB=1)
reg.set_bit(1, 1)      # Set MSB
bit = reg.get_bit(1)   # Get MSB

reg.set_bit(24, 1)     # Set LSB
bit = reg.get_bit(24)  # Get LSB

# Bit range access
reg.set_bits(start=1, end=12, value=0o1234)  # Set upper 12 bits
upper = reg.get_bits(start=1, end=12)        # Get upper 12 bits
```

**Arithmetic Operations:**

```python
reg.value = 0o100
reg.increment()  # Now 0o101
reg.decrement()  # Back to 0o100

# Wraparound
reg.value = 0o77777777  # Max 24-bit value
reg.increment()         # Wraps to 0
reg.decrement()         # Wraps to 0o77777777
```

### Register Names and Numbers

The H-1800 has 32 registers per group, organized as:

| Registers | Numbers | Purpose |
|-----------|---------|---------|
| AU1, AU2 | 0-1 | AU-CU Counters |
| SC, CSC | 2-3 | Sequence/Cosequence Counters |
| SH, CSH | 4-5 | Sequence/Cosequence History |
| UTR | 6 | Unprogrammed Transfer Register |
| MXR | 7 | Mask Index Register |
| X0-X7 | 8-15 | Index Registers |
| R0-R7 | 16-23 | General Purpose Registers |
| S0-S7 | 24-31 | General Purpose Registers |

**Register Aliases:**

| Alias | Register | Number | Purpose |
|-------|----------|--------|---------|
| RAC | S4 | 28 | Read Address Counter |
| DRAC | S5 | 29 | Distributed Read Address Counter |
| WAC | S6 | 30 | Write Address Counter |
| DWAC | S7 | 31 | Distributed Write Address Counter |

### RegisterGroup Class

A group of 32 registers.

```python
class RegisterGroup:
    """
    A group of 32 registers.
    
    Attributes:
        group_number: Group number (0-7)
        width: Register width in bits
    """
```

**Operations:**

```python
# Create group
group = RegisterGroup(group_number=0, width=24)

# Access by number
reg = group.get(0)  # Get AU1
group.set(0, 0o12345670)

# Access by name
reg = group.get("X0")  # Get X0
group.set("X0", 0o12345670)

# Access by alias
reg = group.get("RAC")  # Get S4 (via alias)
group.set("RAC", 0o11111111)

# Read with mask
value = group.read("X0", mask=0o000007777)

# Write with mask
group.set("X0", 0o00001234, mask=0o000007777)

# Clear all registers in group
group.clear_all()

# Dump group state
dump = group.dump()  # Returns dict: {reg_num: value}
```

### RegisterFile Class

Complete register file with 8 groups.

```python
class RegisterFile:
    """
    Complete H-1800 register file.
    
    Contains 8 register groups, each with 32 registers.
    Total: 256 registers (8 groups × 32 registers).
    
    Attributes:
        width: Register width in bits (24 or 48)
        num_groups: Number of register groups (8)
    """
```

**Operations:**

```python
# Create register file
rf = RegisterFile(width=24)

# Access group
group = rf.get_group(0)  # Get group 0

# Access specific register
reg = rf.get_register(group_number=0, register_key="X0")

# Read register
value = rf.read_register(group_number=0, register_key="X0")

# Read with mask
value = rf.read_register(group_number=0, register_key="X0", 
                        mask=0o000007777)

# Write register
rf.set_register(group_number=0, register_key="X0", value=0o12345670)

# Write with mask
rf.set_register(group_number=0, register_key="X0", 
               value=0o00001234, mask=0o000007777)

# Clear all registers
rf.clear_all()

# Dump all registers
dump = rf.dump()  # Returns nested dict: {group: {reg: value}}

# Formatted dump
formatted = rf.dump_formatted(group=0)  # Dump specific group
print(formatted)
# Output:
# Group 0:
#   AU1  [ 0]: 0o00000000
#   AU2  [ 1]: 0o00000000
#   ...
```

**Array-Style Access:**

```python
# Access group
group = rf[0]

# Access register via group
reg = group["X0"]
group["X0"] = 0o12345670
```

## Masking Operations

Masking is critical for H-1800 operations, allowing selective bit updates.

### Mask Format (24-bit)

```
Bit Position:  1  2  3  4  5  6 ... 22 23 24
Mask Value:    |  |  |  |  |  |     |  |  |
               MSB                       LSB
```

### Common Masks

```python
# Full word (no masking)
MASK_FULL = 0o77777777  # All 24 bits

# Upper 12 bits
MASK_UPPER_12 = 0o77770000

# Lower 12 bits
MASK_LOWER_12 = 0o000007777

# Upper 6 bits
MASK_UPPER_6 = 0o77000000

# Lower 6 bits
MASK_LOWER_6 = 0o000000077

# Byte 0 (bits 1-6)
MASK_BYTE_0 = 0o77000000

# Byte 1 (bits 7-12)
MASK_BYTE_1 = 0o00770000

# Byte 2 (bits 13-18)
MASK_BYTE_2 = 0o00007700

# Byte 3 (bits 19-24)
MASK_BYTE_3 = 0o00000077
```

### Mask Examples

**Example 1: Update Lower 12 Bits**

```python
# Initial value
reg.value = 0o77770000

# Write only lower 12 bits
mask = 0o000007777
reg.write(0o00001234, mask=mask)

# Result: 0o77771234
# Upper 12 bits (0o7777) preserved
# Lower 12 bits (0o0000) replaced with 0o1234
```

**Example 2: Extract Specific Field**

```python
# Value with multiple fields
mem.write(100, 0o12345670)

# Extract middle 12 bits (bits 7-18)
mask = 0o00777700
masked_value = mem.read(100, mask=mask)

# Result: 0o00345600
# Only bits 7-18 are extracted
```

**Example 3: Selective Bit Update**

```python
# Set specific bits using mask
value = 0o77777777

# Create mask for bits 1, 5, 10, 15, 20 (custom pattern)
mask = 0o40201004  # Binary: 100000010000001000000100

# Write with mask
mem.write(50, 0o00000000, mask=mask)

# Result: Only bits specified in mask are cleared
```

## Integration with Instruction Execution

### Typical Instruction Pattern

```python
# Fetch instruction
instruction = cpu.fetch()

# Decode to get operand addresses
decoded = decoder.decode(instruction)

# Get mask (if maskable instruction)
mask = decoded.mask  # 5-bit mask value (0-31)

# Convert 5-bit mask to 24-bit mask pattern
# (Implementation-specific based on mask group)
full_mask = expand_mask(mask)

# Read operand A with mask
addr_a = resolve_address(decoded.operand_a)
value_a = memory.read(addr_a, mask=full_mask)

# Perform operation
result = operate(value_a)

# Write result with mask
addr_c = resolve_address(decoded.operand_c)
memory.write(addr_c, result, mask=full_mask)
```

### Example: Masked Binary Add

```python
def execute_ba_masked(ctx, mask):
    """Execute Binary Add with mask."""
    # Read operands with mask
    a = ctx.memory.read(addr_a, mask=mask)
    b = ctx.memory.read(addr_b, mask=mask)
    
    # Add (only masked bits participate)
    result = (a + b) & mask
    
    # Write result with mask (preserve unmasked bits)
    ctx.memory.write(addr_c, result, mask=mask)
```

### Example: Unmasked Transfer

```python
def execute_tx_unmasked(ctx, operands):
    """Execute Transfer without mask."""
    # Read from address A (full word)
    value = ctx.memory.read(addr_a)
    
    # Write to address C (full word)
    ctx.memory.write(addr_c, value)
```

## Performance Considerations

### Memory Access

- Each `read()` or `write()` increments access counters
- Masking operations are performed in-place (efficient)
- BitField operations use bit manipulation (fast)

### Register Access

- Registers use BitField internally (bit-level accuracy)
- Masking is implemented via bitwise operations
- No performance penalty for masked vs. unmasked access

### Best Practices

```python
# GOOD: Single masked write
mem.write(addr, value, mask=mask)

# AVOID: Read-modify-write when mask available
old_value = mem.read(addr)
new_value = (old_value & ~mask) | (value & mask)
mem.write(addr, new_value)
```

## Error Handling

### MemoryError

Raised for memory access violations:
- Invalid address (out of bounds)
- Invalid value (exceeds word width)
- Write to protected region

```python
try:
    mem.write(address, value)
except MemoryError as e:
    print(f"Memory error: {e}")
```

### RegisterError

Raised for register access violations:
- Invalid bit position
- Invalid bit range

```python
try:
    reg.set_bit(100, 1)  # Bit 100 doesn't exist
except RegisterError as e:
    print(f"Register error: {e}")
```

## Testing

Comprehensive tests are available in `test_memory_registers.py`:
- MemoryWord tests (24-bit and 48-bit)
- Memory tests (read/write, masking, protection, 48-bit)
- Register tests (masking, bit access, arithmetic)
- RegisterGroup tests
- RegisterFile tests
- Integration tests (memory ↔ register transfers)

Run tests:
```bash
python -m pytest h1800/test_memory_registers.py -v
```

## Summary

The H-1800 memory and register implementation provides:

✅ **24-bit and 48-bit word support**
✅ **Mask-based partial word access** (critical for H-1800)
✅ **Memory protection** (read/write control)
✅ **Bit-level access** (via BitField)
✅ **Register groups and aliases** (8 groups × 32 registers)
✅ **Integration-ready** (designed for instruction execution)
✅ **Well-tested** (comprehensive test suite)
✅ **Statistics tracking** (read/write counts)

The implementation accurately models H-1800 memory and register behavior, enabling correct instruction simulation with full masking support.