"""
H-1800 Simulator Package
========================

A simulator for the Honeywell H-1800 computer system.

This package provides:
- CPU emulation with full instruction execution
- Memory subsystem (core memory simulation)
- Register file management
- Instruction decoder
- Instruction executor
- Peripheral device interfaces
- Simulation control and runtime
- Command-line interface

Modules:
    cpu         - CPU state and control logic
    memory      - Memory subsystem implementation
    registers   - Register file and register operations
    decoder     - Instruction decoding logic
    executor    - Instruction execution engine
    devices     - Peripheral device implementations
    sim         - Simulation runtime and control
    cli         - Command-line interface

Usage:
    from h1800 import Simulator

    sim = Simulator()
    sim.load_program(program_data)
    sim.run()
"""

__version__ = "0.1.0"

# Import main components
from .cpu import CPU, CPUFlags, CPUState
from .decoder import DecodedInstruction, Decoder
from .devices import (
    CardPunch,
    CardReader,
    Console,
    Device,
    DeviceManager,
    DiskDrive,
    LinePrinter,
    PaperTapePunch,
    PaperTapeReader,
    TapeDrive,
)
from .executor import ExecutionContext, Executor
from .memory import Memory, MemoryError, MemoryProtection, MemoryWord
from .opcodes import OPCODES, OpcodeMetadata, get_categories, get_opcode, list_opcodes_by_category
from .registers import Register, RegisterError, RegisterFile, RegisterGroup
from .sim import Breakpoint, Simulator, SimulatorConfig, SimulatorState, TraceOptions

__all__ = [
    # Core components
    "Simulator",
    "SimulatorConfig",
    "SimulatorState",
    "CPU",
    "CPUState",
    "CPUFlags",
    "Memory",
    "MemoryWord",
    "MemoryError",
    "MemoryProtection",
    "Register",
    "RegisterFile",
    "RegisterGroup",
    "RegisterError",
    "Decoder",
    "DecodedInstruction",
    "Executor",
    "ExecutionContext",
    # Opcodes
    "OPCODES",
    "OpcodeMetadata",
    "get_opcode",
    "get_categories",
    "list_opcodes_by_category",
    # Devices
    "Device",
    "DeviceManager",
    "TapeDrive",
    "CardReader",
    "CardPunch",
    "LinePrinter",
    "PaperTapeReader",
    "PaperTapePunch",
    "DiskDrive",
    "Console",
    # Debugging
    "Breakpoint",
    "TraceOptions",
    # Version
    "__version__",
]
