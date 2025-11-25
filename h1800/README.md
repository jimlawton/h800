# H-1800 Simulator

A cycle-accurate simulator for the Honeywell H-1800 computer system.

## Overview

This package provides a complete simulation environment for the H-1800, including:

- **CPU**: Full instruction execution engine with sequence control
- **Memory**: 24-bit word-oriented core memory (default: 32K words)
- **Registers**: 8 groups × 32 registers with specialized functions
- **Decoder**: Instruction decoder supporting all H-1800 instruction formats
- **Executor**: Instruction execution engine with all opcode implementations
- **Devices**: Peripheral device simulation (tape, cards, printer, etc.)
- **Simulator**: High-level simulation runtime with debugging support
- **CLI**: Interactive command-line interface

## Architecture

### Module Structure

```
h1800/
├── __init__.py      # Package exports and public API
├── cpu.py           # CPU state and control logic
├── memory.py        # Memory subsystem
├── registers.py     # Register file implementation
├── decoder.py       # Instruction decoder
├── executor.py      # Instruction executor
├── devices.py       # Peripheral device implementations
├── sim.py           # Simulation runtime
└── cli.py           # Command-line interface
```

### CPU Architecture

The H-1800 CPU implements:
- 12-bit instruction words
- 24-bit data words
- Program counter (PC)
- Sequence/cosequence bits for instruction modification
- Status flags (overflow, zero, negative, carry, parity)
- Fetch-decode-execute cycle

### Memory Organization

- Word-addressable memory (24-bit words)
- Configurable size (default: 32K words)
- Memory protection support (future)
- Memory-mapped I/O regions (future)

### Register File

The register file contains 8 groups of 32 registers each:

**Special Registers (0-7):**
- AU1, AU2: AU-CU Counters
- SC, CSC: Sequence/Cosequence Counters  
- SH, CSH: Sequence/Cosequence History
- UTR: Unprogrammed Transfer Register
- MXR: Mask Index Register

**Index Registers (8-15):**
- X0-X7: Index registers for address modification

**General Purpose Registers (16-31):**
- R0-R7: General purpose registers
- S0-S7: General purpose registers (with address counter aliases)
  - S4 (RAC): Read Address Counter
  - S5 (DRAC): Distributed Read Address Counter
  - S6 (WAC): Write Address Counter
  - S7 (DWAC): Distributed Write Address Counter

### Instruction Format

The H-1800 uses 12-bit instruction words with multiple formats:

**Maskable Instructions** (bit 7 = 1):
```
[1]     Sequence bit
[2-6]   Mask field (5 bits)
[7]     1 (masked indicator)
[8-12]  Opcode (5 bits)
```

**Unmasked Instructions** (bit 7 = 0):
```
[1]     Sequence bit
[2-3]   Variant bits
[4-6]   Operand flags (A, B, C)
[7]     0 (unmasked indicator)
[8-12]  Opcode (5 bits)
```

**Peripheral Instructions** (bit 7 = 1):
```
[1-6]   Peripheral address (6 bits)
[7]     1
[8-12]  Opcode (5 bits)
```

### Peripheral Devices

Supported device types:
- **Tape Drives**: Magnetic tape with forward/backward read, write, rewind
- **Card Reader**: 80-column card input
- **Card Punch**: 80-column card output
- **Line Printer**: Formatted line output (120 columns)
- **Paper Tape**: Reader and punch
- **Disk Drive**: Random access storage (placeholder)
- **Console**: Interactive typewriter

Each device has a peripheral address (0-63) and supports device-specific operations.

## Usage

### Basic Simulation

```python
from h1800 import Simulator

# Create simulator
sim = Simulator()

# Load a program
program = [0o4711, 0o0123, ...]  # Example program data
sim.load_program(program, start_address=0)

# Run the program
result = sim.run(max_cycles=10000)
print(f"Executed {result['instructions']} instructions in {result['cycles']} cycles")
```

### Interactive CLI

```python
from h1800.cli import cli_main

# Start interactive shell
cli_main()
```

Or from the command line:
```bash
python -m h1800.cli
```

### Debugging Support

```python
# Enable instruction tracing
sim.enable_trace(instructions=True)

# Set breakpoints
sim.add_breakpoint(0o1000)

# Single-step execution
sim.step()

# Inspect memory
print(sim.dump_memory(start=0, count=64))

# Dump state
state = sim.dump_state()
print(state)
```

### Device Attachment

```python
from h1800.devices import TapeDrive, LinePrinter

# Attach a tape drive
tape = TapeDrive(address=0o32)
tape.load_tape(tape_data)
sim.devices.attach_device(tape)

# Attach a printer
printer = LinePrinter(address=0o06)
sim.devices.attach_device(printer)
```

## CLI Commands

The interactive CLI provides the following commands:

**Program Control:**
- `load <file>` - Load program from file
- `run [cycles]` - Run program
- `step [count]` - Execute N instructions
- `continue` - Continue from breakpoint
- `halt` - Halt execution
- `reset` - Reset simulator

**Breakpoints:**
- `break <addr>` - Set breakpoint
- `unbreak <addr>` - Remove breakpoint
- `breaks` - List breakpoints

**Memory:**
- `memory <addr> [count]` - Display memory
- `dump <start> <end>` - Dump memory range
- `set <addr> <value>` - Set memory location

**Registers:**
- `registers [group]` - Display registers
- `setreg <group> <reg> <val>` - Set register

**Debug:**
- `trace on|off` - Enable/disable trace
- `status` - Display status
- `devices` - List devices

## Development Status

**Implemented:**
- ✅ Core simulator framework
- ✅ CPU state management
- ✅ Memory subsystem
- ✅ Register file
- ✅ Instruction decoder (structure)
- ✅ Device framework
- ✅ CLI framework

**In Progress:**
- 🚧 Instruction execution (stubs created)
- 🚧 Address resolution
- 🚧 Operand decoding
- 🚧 Device I/O operations

**Planned:**
- ⏳ Complete instruction set implementation
- ⏳ Floating-point operations
- ⏳ Program loader (binary/object file formats)
- ⏳ Comprehensive test suite
- ⏳ Performance optimization
- ⏳ State save/restore
- ⏳ Debugger enhancements

## See Also

- `../docs/h1800-spec.md` - Register and addressing bit definitions
- `../h800/` - H-800/H-1800 instruction encoding and assembly tools
- `../docs/` - Original documentation and programmer's reference manuals

## License

Same as parent project.