"""
H-1800 Simulator Command-Line Interface
=========================================

This module implements the command-line interface for the H-1800 simulator.

The CLI provides:
- Interactive REPL for simulator control
- Batch execution mode
- Program loading and execution
- Memory inspection and modification
- Register examination
- Breakpoint management
- Single-step debugging
- Trace control
- Device management
- State save/restore

Commands:
    load <file>         - Load program from file
    run [cycles]        - Run program (optional cycle limit)
    step [count]        - Execute N instructions (default: 1)
    continue            - Continue from breakpoint
    halt                - Halt execution
    reset               - Reset simulator

    break <addr>        - Set breakpoint at address
    unbreak <addr>      - Remove breakpoint
    breaks              - List all breakpoints

    memory <addr>       - Display memory at address
    dump <start> <end>  - Dump memory range
    set <addr> <value>  - Set memory location

    registers [group]   - Display registers (optional: specific group)
    setreg <name> <val> - Set register value

    trace on|off        - Enable/disable instruction trace
    status              - Display simulator status
    devices             - List attached devices

    help [command]      - Show help
    quit                - Exit simulator

Key Components:
    CLI             - Main CLI class
    CommandError    - CLI command error exception
    cli_main        - Main entry point
"""

import cmd
import sys

from .sim import Simulator, SimulatorState


class CommandError(Exception):
    """Exception raised for CLI command errors."""

    pass


class CLI(cmd.Cmd):
    """
    H-1800 Simulator Interactive Command-Line Interface.

    Provides an interactive shell for controlling the simulator.

    Attributes:
        intro: Welcome message
        prompt: Command prompt
        simulator: Simulator instance
    """

    intro = """
H-1800 Simulator
================
Type 'help' or '?' for a list of commands.
Type 'help <command>' for detailed help on a command.
"""
    prompt = "h1800> "

    def __init__(self, config=None):
        """
        Initialize the CLI.

        Args:
            config: SimulatorConfig instance (optional)
        """
        super().__init__()
        self.simulator = Simulator(config=config)
        self.running = True

    # -------------------------------------------------------------------------
    # Program Control Commands
    # -------------------------------------------------------------------------

    def do_load(self, arg):
        """
        Load a program from a file.

        Usage: load <filename> [address]

        Loads program data from the specified file into memory.
        Optional address specifies starting address (default: 0).
        """
        args = arg.split()
        if not args:
            print("ERROR: Filename required")
            return

        filename = args[0]
        start_address = 0
        if len(args) > 1:
            try:
                start_address = int(args[1], 0)
            except ValueError:
                print(f"ERROR: Invalid address: {args[1]}")
                return

        try:
            # TODO: Implement actual program loader
            # This will need to parse object files, binary images, etc.
            print(f"Loading {filename} at address 0o{start_address:06o}...")
            print("(Program loading not yet implemented)")
        except Exception as e:
            print(f"ERROR: Failed to load program: {e}")

    def do_run(self, arg):
        """
        Run the simulator.

        Usage: run [max_cycles] [max_instructions]

        Runs the simulator until halted or limits reached.
        """
        args = arg.split()
        max_cycles = None
        max_instructions = None

        if len(args) > 0:
            try:
                max_cycles = int(args[0], 0)
            except ValueError:
                print(f"ERROR: Invalid cycle count: {args[0]}")
                return

        if len(args) > 1:
            try:
                max_instructions = int(args[1], 0)
            except ValueError:
                print(f"ERROR: Invalid instruction count: {args[1]}")
                return

        try:
            print("Running simulator...")
            result = self.simulator.run(max_cycles=max_cycles, max_instructions=max_instructions)
            print(f"Execution stopped: {result['state']}")
            print(f"  Cycles: {result['cycles']}")
            print(f"  Instructions: {result['instructions']}")
            print(f"  Final PC: 0o{result['final_pc']:06o}")
        except Exception as e:
            print(f"ERROR: Execution failed: {e}")

    def do_step(self, arg):
        """
        Execute one or more instructions.

        Usage: step [count]

        Execute N instructions (default: 1).
        """
        count = 1
        if arg:
            try:
                count = int(arg, 0)
            except ValueError:
                print(f"ERROR: Invalid count: {arg}")
                return

        try:
            for i in range(count):
                if not self.simulator.step():
                    print(f"Execution stopped after {i + 1} instructions")
                    break
            else:
                print(f"Executed {count} instruction(s)")
                print(f"PC: 0o{self.simulator.cpu.pc:06o}")
        except Exception as e:
            print(f"ERROR: Step failed: {e}")

    def do_continue(self, arg):
        """
        Continue execution from breakpoint.

        Usage: continue
        """
        if self.simulator.state == SimulatorState.BREAKPOINT:
            self.simulator.resume()
            try:
                result = self.simulator.run()
                print(f"Execution stopped: {result['state']}")
            except Exception as e:
                print(f"ERROR: Execution failed: {e}")
        else:
            print("Not at a breakpoint")

    def do_halt(self, arg):
        """
        Halt execution.

        Usage: halt
        """
        self.simulator.halt()
        print("Simulator halted")

    def do_reset(self, arg):
        """
        Reset the simulator.

        Usage: reset

        Resets CPU, memory, and all devices to initial state.
        """
        self.simulator.reset()
        print("Simulator reset")

    # -------------------------------------------------------------------------
    # Breakpoint Commands
    # -------------------------------------------------------------------------

    def do_break(self, arg):
        """
        Set a breakpoint.

        Usage: break <address>

        Sets a breakpoint at the specified address.
        Address can be in octal (0o prefix) or decimal.
        """
        if not arg:
            print("ERROR: Address required")
            return

        try:
            address = int(arg, 0)
            bp = self.simulator.add_breakpoint(address)
            print(f"Breakpoint set at 0o{address:06o}")
        except ValueError:
            print(f"ERROR: Invalid address: {arg}")

    def do_unbreak(self, arg):
        """
        Remove a breakpoint.

        Usage: unbreak <address>

        Removes the breakpoint at the specified address.
        """
        if not arg:
            print("ERROR: Address required")
            return

        try:
            address = int(arg, 0)
            bp = self.simulator.remove_breakpoint(address)
            if bp:
                print(f"Breakpoint removed at 0o{address:06o}")
            else:
                print(f"No breakpoint at 0o{address:06o}")
        except ValueError:
            print(f"ERROR: Invalid address: {arg}")

    def do_breaks(self, arg):
        """
        List all breakpoints.

        Usage: breaks

        Displays all currently set breakpoints.
        """
        if not self.simulator.breakpoints:
            print("No breakpoints set")
            return

        print("Breakpoints:")
        for address in sorted(self.simulator.breakpoints.keys()):
            bp = self.simulator.breakpoints[address]
            status = "enabled" if bp.enabled else "disabled"
            print(f"  0o{address:06o}: {status} (hits: {bp.hit_count})")

    # -------------------------------------------------------------------------
    # Memory Commands
    # -------------------------------------------------------------------------

    def do_memory(self, arg):
        """
        Display memory contents.

        Usage: memory <address> [count]

        Displays memory starting at address.
        Count defaults to 16 words.
        """
        args = arg.split()
        if not args:
            print("ERROR: Address required")
            return

        try:
            address = int(args[0], 0)
            count = 16
            if len(args) > 1:
                count = int(args[1], 0)

            print(self.simulator.dump_memory(address, count))
        except ValueError as e:
            print(f"ERROR: Invalid argument: {e}")
        except Exception as e:
            print(f"ERROR: {e}")

    def do_dump(self, arg):
        """
        Dump a range of memory.

        Usage: dump <start> <end>

        Dumps memory from start to end address (inclusive).
        """
        args = arg.split()
        if len(args) < 2:
            print("ERROR: Start and end addresses required")
            return

        try:
            start = int(args[0], 0)
            end = int(args[1], 0)
            count = end - start + 1
            print(self.simulator.dump_memory(start, count))
        except ValueError as e:
            print(f"ERROR: Invalid argument: {e}")
        except Exception as e:
            print(f"ERROR: {e}")

    def do_set(self, arg):
        """
        Set a memory location.

        Usage: set <address> <value>

        Sets the memory location to the specified value.
        """
        args = arg.split()
        if len(args) < 2:
            print("ERROR: Address and value required")
            return

        try:
            address = int(args[0], 0)
            value = int(args[1], 0)
            self.simulator.memory.write(address, value)
            print(f"Memory[0o{address:06o}] = 0o{value:08o}")
        except ValueError as e:
            print(f"ERROR: Invalid argument: {e}")
        except Exception as e:
            print(f"ERROR: {e}")

    # -------------------------------------------------------------------------
    # Register Commands
    # -------------------------------------------------------------------------

    def do_registers(self, arg):
        """
        Display register contents.

        Usage: registers [group]

        Displays all registers, or registers in specified group (0-7).
        """
        if arg:
            try:
                group = int(arg, 0)
                if group < 0 or group >= 8:
                    print("ERROR: Group must be 0-7")
                    return

                print(f"Register Group {group}:")
                reg_group = self.simulator.registers[group]
                # TODO: Format register display nicely
                print("  (Register display not yet implemented)")
            except ValueError:
                print(f"ERROR: Invalid group number: {arg}")
        else:
            print("All Registers:")
            # TODO: Format all register display
            print("  (Register display not yet implemented)")

    def do_setreg(self, arg):
        """
        Set a register value.

        Usage: setreg <group> <register> <value>

        Sets the specified register to the given value.
        """
        args = arg.split()
        if len(args) < 3:
            print("ERROR: Group, register, and value required")
            return

        try:
            group = int(args[0], 0)
            register = args[1]  # Can be name or number
            value = int(args[2], 0)

            # Try as number first, then as name
            try:
                reg_num = int(register, 0)
                self.simulator.registers.set_register(group, reg_num, value)
                print(f"Register[{group}][{reg_num}] = 0o{value:08o}")
            except ValueError:
                self.simulator.registers.set_register(group, register, value)
                print(f"Register[{group}][{register}] = 0o{value:08o}")
        except Exception as e:
            print(f"ERROR: {e}")

    # -------------------------------------------------------------------------
    # Trace and Debug Commands
    # -------------------------------------------------------------------------

    def do_trace(self, arg):
        """
        Control instruction tracing.

        Usage: trace on|off

        Enables or disables instruction trace output.
        """
        if arg.lower() == "on":
            self.simulator.enable_trace()
            print("Trace enabled")
        elif arg.lower() == "off":
            self.simulator.disable_trace()
            print("Trace disabled")
        else:
            print("ERROR: Use 'trace on' or 'trace off'")

    def do_status(self, arg):
        """
        Display simulator status.

        Usage: status

        Shows current simulator state, PC, cycle count, etc.
        """
        state = self.simulator.dump_state()
        print("Simulator Status:")
        print(f"  State: {state['simulator_state']}")
        print(f"  CPU State: {state['cpu']['state']}")
        print(f"  PC: 0o{state['cpu']['pc']:06o}")
        print(f"  Sequence: {state['cpu']['sequence']}")
        print(f"  Cosequence: {state['cpu']['cosequence']}")
        print(f"  Cycles: {state['statistics']['total_cycles']}")
        print(f"  Instructions: {state['statistics']['total_instructions']}")
        print(f"  Memory: {state['memory']['size']} words")
        print(f"  Memory Reads: {state['memory']['reads']}")
        print(f"  Memory Writes: {state['memory']['writes']}")

    def do_devices(self, arg):
        """
        List attached devices.

        Usage: devices

        Shows all currently attached peripheral devices.
        """
        devices = self.simulator.devices.list_devices()
        if not devices:
            print("No devices attached")
            return

        print("Attached Devices:")
        for addr, device in devices:
            print(f"  0o{addr:02o}: {device}")

    # -------------------------------------------------------------------------
    # Utility Commands
    # -------------------------------------------------------------------------

    def do_quit(self, arg):
        """
        Exit the simulator.

        Usage: quit

        Exits the H-1800 simulator.
        """
        print("Goodbye!")
        return True

    def do_exit(self, arg):
        """Alias for quit."""
        return self.do_quit(arg)

    def do_EOF(self, arg):
        """Handle EOF (Ctrl-D)."""
        print()
        return self.do_quit(arg)

    # -------------------------------------------------------------------------
    # Help Override
    # -------------------------------------------------------------------------

    def emptyline(self):
        """Don't repeat last command on empty line."""
        pass

    def default(self, line):
        """Handle unknown commands."""
        print(f"Unknown command: {line}")
        print("Type 'help' for a list of commands")


def cli_main(argv=None):
    """
    Main entry point for the CLI.

    Args:
        argv: Command-line arguments (default: sys.argv)

    Returns:
        Exit code (0 = success, non-zero = error)
    """
    if argv is None:
        argv = sys.argv

    # Parse command-line arguments
    # TODO: Add argparse support for batch mode, script files, etc.

    # Create and run CLI
    try:
        cli = CLI()
        cli.cmdloop()
        return 0
    except KeyboardInterrupt:
        print("\nInterrupted")
        return 130
    except Exception as e:
        print(f"FATAL ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(cli_main())
