# H-1800 Memory and Register Implementation Summary

## Overview

This document summarizes the implementation of the H-1800 memory and register subsystems with full 48-bit word support and masking capabilities.

## What Was Implemented

### 1. MemoryWord Class (`memory.py`)

**Purpose:** Individual memory word with configurable width and masking support.

**Features:**
- Supports 24-bit and 48-bit words
- Mask-based read/write for partial updates
- Uses BitField for accurate bit-level operations
- Octal representation for debugging

**Key Methods:**
```python
word = MemoryWord(width=24, value=0o12345670)
value = word.read(mask=0o000007777)           # Read with mask
word.write(0o00001234, mask=0o000007777)      # Write with mask
```

### 2. Memory Class (`memory.py`)

**Purpose:** Main memory subsystem managing array of MemoryWord instances.

**Features:**
- Configurable size (default: 32K words)
- Configurable default word width (24 or 48 bits)
- Per-address word width (can mix 24-bit and 48-bit)
- Memory protection with protected regions
- 48-bit operations (spanning two 24-bit words if needed)
- Block read/write operations
- Memory dump for debugging
- Access statistics (read/write counts)

**Key Methods:**
```python
mem = Memory(size=32768, word_width=24)
mem.write(addr, value, mask=None)             # Write with optional mask
value = mem.read(addr, mask=None)              # Read with optional mask
mem.write_48(addr, value_48, mask=None)        # 48-bit write
value_48 = mem.read_48(addr, mask=None)        # 48-bit read
mem.set_word_width(addr, width)                # Configure word width
mem.write_block(start, values)                 # Block operations
mem.load_image(data, start, word_width)        # Load memory image
```

**Memory Protection:**
```python
mem.protection.enabled = True
mem.protection.add_protected_region(start=100, end=200)
# Writes to protected regions raise MemoryError
```

### 3. Register Class (`registers.py`)

**Purpose:** Individual register with masking and bit-level access.

**Features:**
- Supports 24-bit and 48-bit registers
- Mask-based read/write
- Bit-level access (1-indexed, MSB=1)
- Bit range access
- Increment/decrement with wraparound
- Named registers (optional)

**Key Methods:**
```python
reg = Register(name="X0", value=0o12345670, width=24)
value = reg.read(mask=None)                    # Read with optional mask
reg.write(value, mask=None)                    # Write with optional mask
bit = reg.get_bit(position)                    # Get single bit (1-24)
reg.set_bit(position, value)                   # Set single bit
bits = reg.get_bits(start, end)                # Get bit range
reg.set_bits(start, end, value)                # Set bit range
reg.increment()                                # Increment with wraparound
reg.decrement()                                # Decrement with wraparound
```

### 4. RegisterGroup Class (`registers.py`)

**Purpose:** Group of 32 registers.

**Features:**
- 32 registers (0-31) per group
- Access by number or name
- Support for register aliases (RAC, DRAC, WAC, DWAC)
- Group-level clear and dump operations
- Array-style access

**Key Methods:**
```python
group = RegisterGroup(group_number=0, width=24)
reg = group.get("X0")                          # Get by name
reg = group.get(8)                             # Get by number
group.set("X0", value, mask=None)              # Set with optional mask
value = group.read("X0", mask=None)            # Read with optional mask
group.clear_all()                              # Clear all registers
dump = group.dump()                            # Dump to dictionary
```

### 5. RegisterFile Class (`registers.py`)

**Purpose:** Complete register file with 8 groups × 32 registers.

**Features:**
- 8 register groups (0-7)
- Total: 256 registers
- Hierarchical access (group → register)
- File-level clear and dump operations
- Formatted dump for debugging

**Key Methods:**
```python
rf = RegisterFile(width=24)
group = rf.get_group(group_num)                # Get group
reg = rf.get_register(group_num, reg_key)      # Get specific register
value = rf.read_register(group, reg, mask)     # Read with optional mask
rf.set_register(group, reg, value, mask)       # Write with optional mask
rf.clear_all()                                 # Clear all registers
dump = rf.dump()                               # Dump all to nested dict
formatted = rf.dump_formatted(group=0)         # Formatted dump
```

## Register Organization

### Register Names and Numbers

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

### Register Aliases

| Alias | Register | Number | Purpose |
|-------|----------|--------|---------|
| RAC | S4 | 28 | Read Address Counter |
| DRAC | S5 | 29 | Distributed Read Address Counter |
| WAC | S6 | 30 | Write Address Counter |
| DWAC | S7 | 31 | Distributed Write Address Counter |

## Masking Operations

### How Masking Works

Masking allows selective bit updates, critical for H-1800 instruction execution:

```python
# Initial value
value = 0o77777777

# Mask (lower 12 bits)
mask = 0o000007777

# Write with mask
# Result = (current & ~mask) | (new_value & mask)
# Result = 0o77771234
#   Upper 12 bits: 0o7777 (preserved from current)
#   Lower 12 bits: 0o1234 (from new_value)
```

### Common Mask Patterns (24-bit)

```python
MASK_FULL        = 0o77777777  # All 24 bits
MASK_UPPER_12    = 0o77770000  # Bits 1-12
MASK_LOWER_12    = 0o000007777  # Bits 13-24
MASK_UPPER_6     = 0o77000000  # Bits 1-6
MASK_LOWER_6     = 0o000000077  # Bits 19-24
MASK_BYTE_0      = 0o77000000  # Bits 1-6
MASK_BYTE_1      = 0o00770000  # Bits 7-12
MASK_BYTE_2      = 0o00007700  # Bits 13-18
MASK_BYTE_3      = 0o00000077  # Bits 19-24
```

### 48-bit Masks

```python
MASK_FULL_48     = 0o7777777777777777  # All 48 bits
MASK_UPPER_24    = 0o7777777700000000  # Upper 24 bits
MASK_LOWER_24    = 0o0000000077777777  # Lower 24 bits
```

## 48-Bit Word Support

### Native 48-bit Storage

```python
# Configure location for 48-bit storage
mem.set_word_width(addr=0, width=48)

# Write 48-bit value directly
mem.write_48(0, 0o123456701234567)

# Read back
value = mem.read_48(0)  # Returns: 0o123456701234567
```

### 48-bit on 24-bit Memory

When 48-bit values are written to 24-bit memory, they span two consecutive locations:

```python
mem = Memory(size=1024, word_width=24)

# Write 48-bit value (uses addresses 100-101)
value_48 = 0o123456701234567
mem.write_48(100, value_48)

# Internally stored as:
#   mem[100] = 0o01234567  (upper 24 bits)
#   mem[101] = 0o01234567  (lower 24 bits)

# Read back combines both
result = mem.read_48(100)  # Returns: 0o0123456701234567
```

## Integration with Instruction Execution

### Typical Instruction Pattern

```python
# 1. Fetch instruction
instruction_word = cpu.fetch()

# 2. Decode
decoded = decoder.decode(instruction_word)

# 3. Get mask (if maskable instruction)
if decoded.mask is not None:
    # Convert 5-bit mask value to 24-bit mask pattern
    full_mask = expand_mask(decoded.mask)
else:
    full_mask = None

# 4. Read operands with mask
addr_a = resolve_address(decoded.operand_a)
value_a = memory.read(addr_a, mask=full_mask)

addr_b = resolve_address(decoded.operand_b)
value_b = memory.read(addr_b, mask=full_mask)

# 5. Perform operation
result = operate(value_a, value_b)

# 6. Write result with mask (preserves unmasked bits)
addr_c = resolve_address(decoded.operand_c)
memory.write(addr_c, result, mask=full_mask)
```

### Example: Masked Binary Add

```python
def execute_ba_masked(ctx, addr_a, addr_b, addr_c, mask):
    """Execute Binary Add with mask."""
    # Read operands (only masked bits)
    a = ctx.memory.read(addr_a, mask=mask)
    b = ctx.memory.read(addr_b, mask=mask)
    
    # Add
    result = (a + b) & mask
    
    # Write result (preserve unmasked bits at destination)
    ctx.memory.write(addr_c, result, mask=mask)
    
    # Update flags based on result
    ctx.cpu.flags.zero = (result == 0)
    ctx.cpu.flags.overflow = detect_overflow(a, b, result, mask)
```

## Error Handling

### MemoryError

Raised for:
- Invalid address (out of bounds)
- Invalid value (exceeds word width)
- Write to protected region
- Invalid parameters

### RegisterError

Raised for:
- Invalid bit position
- Invalid bit range
- Invalid register key

## Testing

Comprehensive test suite in `test_memory_registers.py`:

**Test Coverage:**
- MemoryWord: creation, read/write, masking, 24/48-bit
- Memory: basic operations, masking, protection, 48-bit, blocks
- Register: creation, read/write, masking, bits, arithmetic
- RegisterGroup: access methods, masking, aliases
- RegisterFile: multi-group operations, dump
- Integration: memory ↔ register transfers with masking

**Run Tests:**
```bash
python -m pytest h1800/test_memory_registers.py -v
```

## Files Created/Modified

### Created Files:
1. `h1800/memory.py` - Memory subsystem (overwritten with new implementation)
2. `h1800/registers.py` - Register subsystem (overwritten with new implementation)
3. `h1800/test_memory_registers.py` - Comprehensive test suite
4. `h1800/MEMORY_REGISTERS.md` - Detailed documentation
5. `h1800/IMPLEMENTATION_SUMMARY.md` - This file

### Modified Files:
1. `h1800/__init__.py` - Added exports for MemoryWord, MemoryError, MemoryProtection, RegisterError

## Key Design Decisions

### 1. BitField Foundation
Using the existing `h800.bitfield.BitField` class ensures:
- Correct bit numbering (MSB=1, LSB=24/48)
- Accurate bit-level operations
- Consistency with H-1800 conventions

### 2. Masking as First-Class Feature
Masking is built into the core read/write methods rather than being a separate layer:
- Simpler API
- More efficient
- Matches H-1800 instruction semantics

### 3. Mixed Word Widths
Allowing per-address word width configuration supports:
- 24-bit instructions
- 48-bit constants
- Future expansion to double-precision arithmetic

### 4. Memory Protection
Basic protection framework enables:
- Protected code regions
- Operating system simulation (future)
- Debugging aids

### 5. Statistics Tracking
Read/write counters support:
- Performance analysis
- Debugging
- Instruction profiling

## Performance Characteristics

**Memory Operations:**
- Read/write: O(1)
- Masking: O(1) bitwise operations
- Block operations: O(n)
- Protection check: O(m) where m = number of protected regions

**Register Operations:**
- Read/write: O(1)
- Bit access: O(1) via BitField
- Group/file access: O(1) dictionary lookup

**Memory Overhead:**
- MemoryWord: ~100 bytes per word (BitField overhead)
- For 32K words: ~3.2 MB (vs ~128KB for raw array)
- Trade-off: accuracy and features vs. memory

## Integration Status

✅ **Fully Integrated:**
- Memory subsystem with masking
- Register subsystem with masking
- 48-bit word support
- Memory protection framework
- Statistics tracking

✅ **Ready for Integration:**
- Instruction decoder (can use memory/registers)
- Instruction executor (can perform masked operations)
- CPU (can access memory/registers)

⏳ **Pending:**
- Mask expansion logic (5-bit mask → 24-bit pattern)
- Address resolution logic
- Complete instruction execution

## Usage Examples

### Example 1: Basic Memory Operations
```python
from h1800 import Memory

mem = Memory(size=1024)
mem.write(0, 0o12345670)
value = mem.read(0)  # Returns: 0o12345670
```

### Example 2: Masked Operations
```python
# Preserve upper bits, update lower bits
mem.write(100, 0o77770000)
mem.write(100, 0o00001234, mask=0o000007777)
# Result: 0o77771234
```

### Example 3: 48-bit Constants
```python
mem.set_word_width(200, 48)
mem.write_48(200, 0o123456701234567)
value = mem.read_48(200)
```

### Example 4: Register File
```python
from h1800 import RegisterFile

rf = RegisterFile(width=24)
rf.set_register(0, "X0", 0o12345670)
rf.set_register(0, "RAC", 0o55555555)  # Alias for S4

value = rf.read_register(0, "X0")
```

### Example 5: Memory ↔ Register Transfer
```python
# Load from memory to register (masked)
mask = 0o000007777
value = mem.read(100, mask=mask)
rf.set_register(0, "R0", value, mask=mask)

# Store from register to memory (masked)
value = rf.read_register(0, "R1", mask=mask)
mem.write(200, value, mask=mask)
```

## Conclusion

The H-1800 memory and register implementation provides:

✅ **Complete 24-bit and 48-bit word support**
✅ **Full masking capabilities** (critical for H-1800 instructions)
✅ **Memory protection** (basic framework)
✅ **Register organization** (8 groups, 32 registers, aliases)
✅ **Bit-level accuracy** (via BitField)
✅ **Well-tested** (comprehensive test suite)
✅ **Integration-ready** (designed for instruction execution)
✅ **Documented** (detailed documentation and examples)

The implementation accurately models H-1800 memory and register behavior, providing the foundation for correct instruction simulation. All masking operations work correctly, enabling proper execution of H-1800 instructions with selective bit updates.

**Status: Complete and tested. Ready for instruction execution integration.**