"""
H-1800 Simulation Runtime Module
==================================

This module implements the simulation runtime and control for the H-1800 simulator.

The simulation runtime coordinates all subsystems:
- CPU execution control
- Memory management
- Register file access
- Device I/O operations
- Breakpoint management
- Trace and debugging support
- Performance monitoring
- State save/restore

Key Components:
    Simulator       - Main simulator class coordinating all subsystems
    SimulatorConfig - Configuration settings
    SimulatorState  - Simulator state enumeration
    Breakpoint      - Breakpoint management
    TraceOptions    - Trace/debug configuration
"""

from dataclasses import dataclass
from enum import Enum, auto

from .cpu import CPU, CPUState
from .decoder import Decoder
from .devices import DeviceManager
from .executor import Executor
from .memory import Memory
from .registers import RegisterFile


class SimulatorState(Enum):
    """Simulator execution states."""

    INITIALIZED = auto()
    RUNNING = auto()
    PAUSED = auto()
    HALTED = auto()
    ERROR = auto()
    BREAKPOINT = auto()


@dataclass
class SimulatorConfig:
    """
    Simulator configuration settings.

    Attributes:
        memory_size: Memory size in words (default: 32K)
        word_width: Word width in bits (default: 24)
        enable_trace: Enable instruction trace
        enable_timing: Enable cycle-accurate timing
        breakpoints_enabled: Enable breakpoint checking
    """

    memory_size: int = 32768  # 32K words
    word_width: int = 24
    enable_trace: bool = False
    enable_timing: bool = True
    breakpoints_enabled: bool = True


@dataclass
class TraceOptions:
    """
    Trace and debug configuration.

    Attributes:
        trace_instructions: Trace each instruction execution
        trace_memory: Trace memory reads/writes
        trace_registers: Trace register changes
        trace_devices: Trace device I/O
        trace_output: Output stream for trace (None = stdout)
    """

    trace_instructions: bool = False
    trace_memory: bool = False
    trace_registers: bool = False
    trace_devices: bool = False
    trace_output: object = None


class Breakpoint:
    """
    Execution breakpoint.

    Attributes:
        address: Memory address to break at
        enabled: Whether breakpoint is active
        condition: Optional condition function
        hit_count: Number of times breakpoint has been hit
    """

    def __init__(self, address, enabled=True, condition=None):
        """
        Initialize a breakpoint.

        Args:
            address: Memory address
            enabled: Whether breakpoint is active
            condition: Optional condition function (ctx -> bool)
        """
        self.address = address
        self.enabled = enabled
        self.condition = condition
        self.hit_count = 0

    def should_break(self, ctx=None):
        """
        Check if execution should break.

        Args:
            ctx: Execution context (for condition evaluation)

        Returns:
            True if should break, False otherwise
        """
        if not self.enabled:
            return False

        if self.condition is not None and ctx is not None:
            return self.condition(ctx)

        return True

    def hit(self):
        """Record a breakpoint hit."""
        self.hit_count += 1

    def __repr__(self):
        status = "enabled" if self.enabled else "disabled"
        return f"Breakpoint(0o{self.address:06o}, {status}, hits={self.hit_count})"


class Simulator:
    """
    H-1800 Simulator.

    Main simulator class that coordinates all subsystems and provides
    the primary interface for running H-1800 programs.

    Attributes:
        config: Simulator configuration
        state: Current simulator state
        cpu: CPU instance
        memory: Memory subsystem
        registers: Register file
        decoder: Instruction decoder
        executor: Instruction executor
        devices: Device manager
        trace: Trace options
        breakpoints: Breakpoint dictionary
    """

    def __init__(self, config=None):
        """
        Initialize the simulator.

        Args:
            config: SimulatorConfig instance (default: use defaults)
        """
        self.config = config if config is not None else SimulatorConfig()
        self.state = SimulatorState.INITIALIZED

        # Initialize subsystems
        self.memory = Memory(size=self.config.memory_size, word_width=self.config.word_width)
        self.registers = RegisterFile(width=self.config.word_width)
        self.decoder = Decoder()
        self.devices = DeviceManager()

        # Initialize CPU (links to other subsystems)
        self.cpu = CPU(registers=self.registers, memory=self.memory)

        # Initialize executor (links to all subsystems)
        self.executor = Executor(
            cpu=self.cpu, memory=self.memory, registers=self.registers, decoder=self.decoder
        )

        # Trace and debugging
        self.trace = TraceOptions()
        self.breakpoints = {}

        # Statistics
        self.total_cycles = 0
        self.total_instructions = 0

    def reset(self):
        """Reset the simulator to initial state."""
        self.cpu.reset()
        self.memory.clear()
        self.registers.clear_all()
        self.devices.reset_all()
        self.state = SimulatorState.INITIALIZED
        self.total_cycles = 0
        self.total_instructions = 0

    def load_program(self, program_data, start_address=0):
        """
        Load a program into memory.

        Args:
            program_data: List of words to load
            start_address: Starting address (default: 0)
        """
        self.memory.load_image(program_data, start_address)
        self.cpu.pc = start_address

    def step(self):
        """
        Execute a single instruction step.

        Returns:
            True if execution should continue, False if halted/paused

        Raises:
            RuntimeError: If execution error occurs
        """
        if self.state not in (SimulatorState.RUNNING, SimulatorState.INITIALIZED):
            return False

        if self.state == SimulatorState.INITIALIZED:
            self.state = SimulatorState.RUNNING

        # Check for breakpoint
        if self.config.breakpoints_enabled and self.cpu.pc in self.breakpoints:
            bp = self.breakpoints[self.cpu.pc]
            if bp.should_break():
                bp.hit()
                self.state = SimulatorState.BREAKPOINT
                return False

        # Fetch instruction
        try:
            instruction_word = self.cpu.fetch()

            # Decode instruction
            decoded = self.decoder.decode(instruction_word)

            # Trace instruction if enabled
            if self.trace.trace_instructions:
                self._trace_instruction(decoded)

            # Execute instruction
            cycles = self.executor.execute(decoded)

            # Update statistics
            self.total_cycles += cycles
            self.total_instructions += 1
            self.cpu.cycle_count += cycles
            self.cpu.instruction_count += 1

            # Increment PC (TODO: some instructions modify PC directly)
            self.cpu.pc += 1

            # Check CPU state
            if self.cpu.state == CPUState.HALTED:
                self.state = SimulatorState.HALTED
                return False

            return True

        except Exception as e:
            self.state = SimulatorState.ERROR
            raise RuntimeError(f"Execution error at PC=0o{self.cpu.pc:06o}: {e}") from e

    def run(self, max_cycles=None, max_instructions=None):
        """
        Run the simulator until halted or limits reached.

        Args:
            max_cycles: Maximum cycles to execute (None = unlimited)
            max_instructions: Maximum instructions to execute (None = unlimited)

        Returns:
            Dictionary with execution statistics
        """
        self.state = SimulatorState.RUNNING

        cycles_executed = 0
        instructions_executed = 0

        while self.state == SimulatorState.RUNNING:
            # Check limits
            if max_cycles is not None and cycles_executed >= max_cycles:
                self.pause()
                break

            if max_instructions is not None and instructions_executed >= max_instructions:
                self.pause()
                break

            # Execute one step
            if not self.step():
                break

            cycles_executed = self.cpu.cycle_count
            instructions_executed = self.cpu.instruction_count

        return {
            "cycles": cycles_executed,
            "instructions": instructions_executed,
            "state": self.state.name,
            "final_pc": self.cpu.pc,
        }

    def pause(self):
        """Pause execution."""
        if self.state == SimulatorState.RUNNING:
            self.state = SimulatorState.PAUSED

    def resume(self):
        """Resume execution from paused state."""
        if self.state == SimulatorState.PAUSED:
            self.state = SimulatorState.RUNNING

    def halt(self):
        """Halt execution."""
        self.cpu.halt()
        self.state = SimulatorState.HALTED

    def is_running(self):
        """Check if simulator is running."""
        return self.state == SimulatorState.RUNNING

    def is_halted(self):
        """Check if simulator is halted."""
        return self.state == SimulatorState.HALTED

    def add_breakpoint(self, address, condition=None):
        """
        Add a breakpoint at the specified address.

        Args:
            address: Memory address
            condition: Optional condition function

        Returns:
            Breakpoint instance
        """
        bp = Breakpoint(address, condition=condition)
        self.breakpoints[address] = bp
        return bp

    def remove_breakpoint(self, address):
        """
        Remove a breakpoint.

        Args:
            address: Memory address

        Returns:
            Removed breakpoint or None
        """
        return self.breakpoints.pop(address, None)

    def enable_breakpoint(self, address):
        """Enable a breakpoint."""
        if address in self.breakpoints:
            self.breakpoints[address].enabled = True

    def disable_breakpoint(self, address):
        """Disable a breakpoint."""
        if address in self.breakpoints:
            self.breakpoints[address].enabled = False

    def clear_breakpoints(self):
        """Clear all breakpoints."""
        self.breakpoints.clear()

    def enable_trace(self, instructions=True, memory=False, registers=False, devices=False):
        """
        Enable tracing.

        Args:
            instructions: Trace instructions
            memory: Trace memory operations
            registers: Trace register changes
            devices: Trace device I/O
        """
        self.trace.trace_instructions = instructions
        self.trace.trace_memory = memory
        self.trace.trace_registers = registers
        self.trace.trace_devices = devices

    def disable_trace(self):
        """Disable all tracing."""
        self.trace.trace_instructions = False
        self.trace.trace_memory = False
        self.trace.trace_registers = False
        self.trace.trace_devices = False

    def _trace_instruction(self, decoded):
        """
        Output instruction trace.

        Args:
            decoded: DecodedInstruction instance
        """
        output = self.trace.trace_output
        trace_line = self.decoder.disassemble(decoded.word)
        if output is not None:
            output.write(f"[{self.cpu.pc:06o}] {trace_line}\n")
        else:
            print(f"[{self.cpu.pc:06o}] {trace_line}")

    def dump_state(self):
        """
        Dump current simulator state.

        Returns:
            Dictionary with complete simulator state
        """
        return {
            "simulator_state": self.state.name,
            "cpu": {
                "pc": self.cpu.pc,
                "sequence": self.cpu.sequence,
                "cosequence": self.cpu.cosequence,
                "state": self.cpu.state.name,
                "cycles": self.cpu.cycle_count,
                "instructions": self.cpu.instruction_count,
            },
            "memory": {
                "size": len(self.memory),
                "reads": self.memory.read_count,
                "writes": self.memory.write_count,
            },
            "statistics": {
                "total_cycles": self.total_cycles,
                "total_instructions": self.total_instructions,
            },
            "breakpoints": {addr: str(bp) for addr, bp in self.breakpoints.items()},
        }

    def dump_memory(self, start=0, count=64):
        """
        Dump memory contents.

        Args:
            start: Starting address
            count: Number of words to dump

        Returns:
            Formatted memory dump string
        """
        return self.memory.dump(start, count)

    def __repr__(self):
        return (
            f"Simulator(state={self.state.name}, pc=0o{self.cpu.pc:06o}, "
            f"cycles={self.total_cycles}, instructions={self.total_instructions})"
        )
