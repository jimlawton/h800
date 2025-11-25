# H-1800 Opcode Metadata

This document describes the opcode metadata structure used by the H-1800 simulator.

## Overview

The opcode metadata has been ported from `h800.opcodes` into a neutral structure (`h1800/opcodes.py`) that can be reused by both the decoder and executor modules.

## Metadata Structure

Each opcode is represented by an `OpcodeMetadata` dataclass with the following fields:

```python
@dataclass
class OpcodeMetadata:
    mnemonic: str           # Instruction mnemonic (e.g., "BA", "TX")
    name: str               # Full instruction name (e.g., "Binary Add")
    opcode: int             # Base opcode value (bits 8-12, 0-31)
    type: str               # Instruction type (see below)
    variant: int | None     # Variant bits (bits 2-3) for unmasked
    bit7: int | None        # Expected value of bit 7
    category: str           # Instruction category for executor dispatch
    cycles: int             # Typical execution cycles
    description: str        # Brief operation description
```

### Instruction Types

- **`maskable`**: Can be used in masked or unmasked form
- **`unmasked`**: Only unmasked form (bit7=0)
- **`peripheral`**: Peripheral I/O instruction (bit7=1)
- **`print`**: Print instruction (bit7=1)
- **`simulator`**: Simulator control instruction

### Instruction Categories

Categories are used by the executor for dispatching to handler methods:

- **`arithmetic`**: BA, BS, DA, DS, WA, WD, BM, DM, HA, etc.
- **`comparison`**: NA, NN, LA, LN
- **`transfer`**: TX, TS, MT, TN, IT, RT
- **`shift`**: SWS, SPS, SWE, SPE, SSL, SS, EX
- **`logical`**: SM, CP
- **`control`**: MPC, PR
- **`peripheral`**: RF, RB, WF, RW
- **`print`**: PRA, PRD, PRO
- **`scientific`**: FBA, FBS, FBM, FBD, FDA, FDS, FDM, FDD, etc.
- **`simulator`**: S

## Data Structures

### OPCODES Dictionary

Maps mnemonic strings to `OpcodeMetadata` instances:

```python
OPCODES = {
    "BA": OpcodeMetadata(
        mnemonic="BA",
        name="Binary Add",
        opcode=0o11,
        type="maskable",
        variant=0b10,
        bit7=1,
        category="arithmetic",
        cycles=1,
        description="Binary addition with optional masking",
    ),
    # ... 64 total opcodes
}
```

### OPCODES_BY_CODE Reverse Lookup

Maps `(opcode, bit7, variant)` tuples to lists of `OpcodeMetadata` instances:

```python
OPCODES_BY_CODE = {
    (0o11, 1, None): [OPCODES["BA"]],      # BA masked form
    (0o11, 0, 0b10): [OPCODES["BA"]],      # BA unmasked form
    (0o32, 1, None): [OPCODES["RF"]],      # RF peripheral
    (0o06, 1, None): [                      # Print collision
        OPCODES["PRA"],
        OPCODES["PRD"],
        OPCODES["PRO"]
    ],
    # ...
}
```

## Lookup Functions

### get_opcode(mnemonic)

Retrieve metadata by mnemonic:

```python
ba = get_opcode("BA")
# Returns: OpcodeMetadata(mnemonic="BA", name="Binary Add", ...)
```

### lookup_opcode(opcode, bit7, variant)

Reverse lookup by instruction fields (used by decoder):

```python
# Lookup masked BA: opcode=0o11, bit7=1
results = lookup_opcode(0o11, 1, None)
# Returns: [OpcodeMetadata for BA]

# Lookup print instructions: opcode=0o06, bit7=1
results = lookup_opcode(0o06, 1, None)
# Returns: [OpcodeMetadata for PRA, PRD, PRO]
```

### list_opcodes_by_category(category)

List all opcodes in a category:

```python
arithmetic = list_opcodes_by_category("arithmetic")
# Returns: [BA, BS, DA, DS, WA, WD, HA, BM, DM, ...]
```

### get_categories()

Get all instruction categories:

```python
categories = get_categories()
# Returns: ['arithmetic', 'comparison', 'control', ...]
```

## Usage Examples

### Decoder Usage

```python
from h1800.decoder import Decoder
from h1800.opcodes import lookup_opcode

decoder = Decoder()
decoded = decoder.decode(0o4551)  # BA instruction

# Decoder uses lookup_opcode internally
results = lookup_opcode(decoded.opcode, decoded.bit7, decoded.variant)
```

### Executor Usage

```python
from h1800.executor import Executor
from h1800.opcodes import get_opcode

executor = Executor(...)
decoded = decoder.decode(word)

# Get metadata for cycle count and category
meta = get_opcode(decoded.mnemonic)
cycles = meta.cycles
category = meta.category

# Dispatch based on category
handler = getattr(executor, f"_execute_{category}")
handler(execution_context)
```

## Instruction Summary

### Maskable Instructions (15 total)

Can be used in both masked (bit7=1, mask in bits 2-6) and unmasked (bit7=0, variant=0b10, operands in bits 4-6) forms:

| Mnemonic | Opcode | Name | Category | Cycles |
|----------|--------|------|----------|--------|
| BA | 0o11 | Binary Add | arithmetic | 1 |
| DA | 0o01 | Decimal Add | arithmetic | 1 |
| WA | 0o15 | Word Add | arithmetic | 1 |
| BS | 0o31 | Binary Subtract | arithmetic | 1 |
| DS | 0o21 | Decimal Subtract | arithmetic | 1 |
| WD | 0o35 | Word Difference | arithmetic | 1 |
| NA | 0o14 | Not Equal Alphabetic | comparison | 1 |
| NN | 0o10 | Not Equal Numeric | comparison | 1 |
| LA | 0o34 | Less Than or Equal Alphabetic | comparison | 1 |
| LN | 0o30 | Less Than or Equal Numeric | comparison | 1 |
| TX | 0o20 | Transfer | transfer | 1 |
| TS | 0o04 | Transfer and Change Sequence | transfer | 1 |
| HA | 0o25 | Half Add | arithmetic | 1 |
| SM | 0o05 | Superimpose | logical | 1 |
| CP | 0o24 | Check Parity | logical | 1 |

### Unmasked Instructions (32 total)

Always unmasked (bit7=0), with variant bits specifying sub-types:

| Mnemonic | Opcode | Variant | Name | Category | Cycles |
|----------|--------|---------|------|----------|--------|
| BM | 0o13 | 0b00 | Binary Multiply | arithmetic | 2 |
| DM | 0o03 | 0b00 | Decimal Multiply | arithmetic | 2 |
| BT | 0o13 | 0b10 | Binary Accumulate | arithmetic | 2 |
| DT | 0o03 | 0b10 | Decimal Accumulate | arithmetic | 2 |
| MT | 0o20 | 0b00 | Multiple Transfer | transfer | 2 |
| TN | 0o20 | 0b01 | Transfer N Words | transfer | 2 |
| CC | 0o10 | 0b01 | Compute Orthocount | arithmetic | 2 |
| IT | 0o30 | 0b01 | Item Transfer | transfer | 1 |
| EBA | 0o13 | 0b11 | Extended Binary Add | arithmetic | 2 |
| EBS | 0o33 | 0b11 | Extended Binary Subtract | arithmetic | 2 |
| RT | 0o30 | 0b11 | Record Transfer | transfer | 2 |
| MPC | 0o00 | 0b10 | Control Program | control | 1 |
| PR | 0o00 | 0b00 | Proceed | control | 1 |

### Shift Instructions (7 total)

Shift and mask operations (unmasked, bit7=0):

| Mnemonic | Opcode | Variant | Name | Cycles |
|----------|--------|---------|------|--------|
| SWS | 0o06 | 0b10 | Shift Word and Substitute | 1 |
| SPS | 0o02 | 0b10 | Shift Preserving Sign and Substitute | 1 |
| SWE | 0o16 | 0b10 | Shift Word and Extract | 1 |
| SPE | 0o12 | 0b10 | Shift Preserving Sign and Extract | 1 |
| SSL | 0o26 | 0b10 | Shift and Select | 1 |
| SS | 0o06 | 0b00 | Substitute | 1 |
| EX | 0o16 | 0b00 | Extract | 1 |

### Peripheral Instructions (4 total)

I/O operations (bit7=1, peripheral address in bits 1-6):

| Mnemonic | Opcode | Name | Cycles |
|----------|--------|------|--------|
| RF | 0o32 | Read Forward | 10 |
| RB | 0o12 | Read Backward | 10 |
| WF | 0o16 | Write Forward | 10 |
| RW | 0o02 | Rewind | 100 |

### Print Instructions (3 total)

All share opcode 0o06 with bit7=1 (collision handled by context):

| Mnemonic | Name | Cycles |
|----------|------|--------|
| PRA | Print Alphabetic | 10 |
| PRD | Print Decimal | 10 |
| PRO | Print Octal | 10 |

### Scientific Instructions (17 total)

Floating-point operations:

| Mnemonic | Opcode | Variant | Name | Cycles |
|----------|--------|---------|------|--------|
| FBA | 0o01 | 0b01 | Floating Binary Add | 3 |
| FDA | 0o21 | 0b01 | Floating Decimal Add | 3 |
| FBS | 0o11 | 0b01 | Floating Binary Subtract | 3 |
| FDS | 0o31 | 0b01 | Floating Decimal Subtract | 3 |
| FBD | 0o05 | 0b01 | Floating Binary Divide | 8 |
| FDD | 0o25 | 0b01 | Floating Decimal Divide | 8 |
| FBAU | 0o01 | 0b11 | Floating Binary Add Unnormalized | 3 |
| FDAU | 0o21 | 0b11 | Floating Decimal Add Unnormalized | 3 |
| FBSU | 0o11 | 0b11 | Floating Binary Subtract Unnormalized | 3 |
| FDSU | 0o31 | 0b11 | Floating Decimal Subtract Unnormalized | 3 |
| FBM | 0o05 | 0b11 | Floating Binary Multiply | 5 |
| FDM | 0o25 | 0b11 | Floating Decimal Multiply | 5 |
| ULD | 0o15 | 0b11 | Multiple Unload | 2 |
| FBAE | 0o01 | 0b00 | Floating Binary Add Extended | 4 |
| FBSE | 0o11 | 0b00 | Floating Binary Subtract Extended | 4 |
| BD | 0o05 | 0b00 | Fixed Binary Divide | 4 |
| DD | 0o25 | 0b00 | Fixed Decimal Divide | 4 |
| FFN | 0o15 | 0b00 | Fixed to Floating Normalize | 2 |
| FCON | 0o35 | 0b00 | Conversion | 2 |
| FLN | 0o30 | 0b00 | Floating Less Than Normalized | 2 |
| FNN | 0o14 | 0b10 | Floating Not Equal Normalized | 2 |

### Simulator Instruction (1 total)

| Mnemonic | Opcode | Name | Cycles |
|----------|--------|------|--------|
| S | 0o07 | Simulator | 1 |

## Total: 64 Opcodes

- Maskable: 15
- Unmasked (non-shift): 13
- Shift: 7
- Peripheral: 4
- Print: 3 (collision)
- Scientific: 21
- Simulator: 1

## Migration from h800.opcodes

The metadata was ported from the `h800.opcodes` module with the following changes:

1. **Renamed fields**: `m` → `mnemonic`, `op` → `opcode`, `b23` → `variant`, `b7` → `bit7`
2. **Added fields**: `category`, `cycles`, `description`
3. **Removed fields**: `c` (class name, not needed for simulation)
4. **Changed structure**: From namedtuple to dataclass
5. **Added methods**: `OpcodeMetadata.matches()` for field matching
6. **Added functions**: `lookup_opcode()`, `get_categories()`, `list_opcodes_by_category()`
7. **Built reverse lookup**: `OPCODES_BY_CODE` for efficient decoder operation

This neutral structure allows both the decoder and executor to use the same metadata without coupling to the assembly/encoding logic in `h800.opcodes`.