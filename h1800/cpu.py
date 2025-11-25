"""
H-1800 CPU Module
=================

This module implements the central processing unit (CPU) for the H-1800 simulator.

The CPU manages:
- Program execution control
- Instruction fetch cycle
- Sequence/cosequence counters
- Program counter management
- CPU state and status flags
- Interrupt handling
- Timing and cycle management

Key Components:
    CPU         - Main CPU class with execution state
    CPUState    - CPU state enumeration (running, halted, error, etc.)
    CPUFlags    - Status flags and condition indicators
"""

from enum import Enum, auto


class CPUState(Enum):
    """CPU execution states."""

    RESET = auto()
    RUNNING = auto()
    HALTED = auto()
    WAITING = auto()
    ERROR = auto()
    BREAKPOINT = auto()


class CPUFlags:
    """CPU status flags and condition indicators."""

    def __init__(self):
        self.overflow = False
        self.zero = False
        self.negative = False
        self.carry = False
        self.parity = False
        self.interrupt_enabled = False

    def clear(self):
        """Clear all flags."""
        self.overflow = False
        self.zero = False
        self.negative = False
        self.carry = False
        self.parity = False

    def __repr__(self):
        flags = []
        if self.overflow:
            flags.append("O")
        if self.zero:
            flags.append("Z")
        if self.negative:
            flags.append("N")
        if self.carry:
            flags.append("C")
        if self.parity:
            flags.append("P")
        if self.interrupt_enabled:
            flags.append("I")
        return f"CPUFlags({' '.join(flags) if flags else 'none'})"


class CPU:
    """
    H-1800 Central Processing Unit.

    The CPU coordinates instruction execution, maintains program state,
    and manages the fetch-decode-execute cycle.

    Attributes:
        state       - Current CPU state (running, halted, etc.)
        flags       - CPU status flags
        pc          - Program counter (current instruction address)
        sequence    - Sequence bit (0 or 1)
        cosequence  - Cosequence bit (0 or 1)
        cycle_count - Total instruction cycles executed
    """

    def __init__(self, registers=None, memory=None):
        """
        Initialize the CPU.

        Args:
            registers: Register file instance (optional, can be set later)
            memory: Memory subsystem instance (optional, can be set later)
        """
        self.registers = registers
        self.memory = memory
        self.state = CPUState.RESET
        self.flags = CPUFlags()

        # Program counter and sequence control
        self.pc = 0
        self.sequence = 0
        self.cosequence = 0

        # Execution statistics
        self.cycle_count = 0
        self.instruction_count = 0

        # Current instruction being executed
        self.current_instruction = None

    def reset(self):
        """Reset the CPU to initial state."""
        self.state = CPUState.RESET
        self.flags.clear()
        self.pc = 0
        self.sequence = 0
        self.cosequence = 0
        self.cycle_count = 0
        self.instruction_count = 0
        self.current_instruction = None

    def fetch(self):
        """
        Fetch the next instruction from memory.

        Returns:
            The instruction word at the current PC.

        Raises:
            RuntimeError: If memory is not attached or PC is invalid.
        """
        if self.memory is None:
            raise RuntimeError("Memory subsystem not attached to CPU")

        instruction = self.memory.read(self.pc)
        self.current_instruction = instruction
        return instruction

    def step(self):
        """
        Execute a single instruction step.

        This performs the fetch-decode-execute cycle for one instruction.

        Returns:
            True if execution should continue, False if halted.
        """
        if self.state not in (CPUState.RUNNING, CPUState.RESET):
            return False

        if self.state == CPUState.RESET:
            self.state = CPUState.RUNNING

        try:
            # Fetch instruction
            instruction = self.fetch()

            # Decode and execute (placeholder for now)
            # TODO: Implement actual decode/execute logic
            self._execute_instruction(instruction)

            # Increment counters
            self.pc += 1
            self.instruction_count += 1
            self.cycle_count += 1  # Simplified; actual cycles vary by instruction

            return True

        except Exception as e:
            self.state = CPUState.ERROR
            raise RuntimeError(f"CPU execution error at PC={self.pc:06o}: {e}") from e

    def _execute_instruction(self, instruction):
        """
        Execute a decoded instruction (placeholder).

        Args:
            instruction: The instruction word to execute.
        """
        # TODO: Implement actual instruction execution
        # This will delegate to the executor module
        pass

    def run(self, max_cycles=None):
        """
        Run the CPU until halted or max_cycles reached.

        Args:
            max_cycles: Maximum number of cycles to execute (None = unlimited)

        Returns:
            The number of cycles executed.
        """
        cycles = 0
        while self.state == CPUState.RUNNING:
            if max_cycles is not None and cycles >= max_cycles:
                break

            if not self.step():
                break

            cycles += 1

        return cycles

    def halt(self):
        """Halt CPU execution."""
        self.state = CPUState.HALTED

    def is_halted(self):
        """Check if CPU is halted."""
        return self.state == CPUState.HALTED

    def is_running(self):
        """Check if CPU is running."""
        return self.state == CPUState.RUNNING

    def __repr__(self):
        return (
            f"CPU(state={self.state.name}, pc=0o{self.pc:06o}, "
            f"seq={self.sequence}, coseq={self.cosequence}, "
            f"cycles={self.cycle_count}, instructions={self.instruction_count})"
        )
