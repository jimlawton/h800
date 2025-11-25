"""
H-1800 Peripheral Devices Module
==================================

This module implements peripheral device interfaces for the H-1800 simulator.

The H-1800 supports various peripheral devices:
- Magnetic tape drives
- Card readers and punches
- Line printers
- Paper tape readers and punches
- Disk drives
- Console typewriter

Each peripheral device has:
- A unique peripheral address (0-63)
- Device-specific operations (read, write, rewind, etc.)
- Status and control registers
- Buffer management
- Timing characteristics

Key Components:
    Device              - Abstract base class for all devices
    TapeDrive           - Magnetic tape drive
    CardReader          - Card reader
    CardPunch           - Card punch
    LinePrinter         - Line printer
    PaperTapeReader     - Paper tape reader
    PaperTapePunch      - Paper tape punch
    DiskDrive           - Disk drive
    Console             - Console typewriter
    DeviceManager       - Device manager and dispatcher
"""

from abc import ABC, abstractmethod
from enum import Enum, auto


class DeviceStatus(Enum):
    """Device status states."""

    IDLE = auto()
    BUSY = auto()
    READY = auto()
    ERROR = auto()
    NOT_READY = auto()
    END_OF_FILE = auto()
    END_OF_TAPE = auto()


class DeviceError(Exception):
    """Exception raised for device errors."""

    pass


class Device(ABC):
    """
    Abstract base class for all peripheral devices.

    All peripheral devices must implement this interface.

    Attributes:
        address: Peripheral address (0-63)
        name: Device name
        status: Current device status
    """

    def __init__(self, address, name="Device"):
        """
        Initialize a device.

        Args:
            address: Peripheral address (0-63)
            name: Device name
        """
        if address < 0 or address > 63:
            raise ValueError(f"Invalid peripheral address: {address}")

        self.address = address
        self.name = name
        self.status = DeviceStatus.IDLE

    @abstractmethod
    def read(self, count=1):
        """
        Read data from the device.

        Args:
            count: Number of words to read

        Returns:
            List of words read from device
        """
        pass

    @abstractmethod
    def write(self, data):
        """
        Write data to the device.

        Args:
            data: List of words to write
        """
        pass

    @abstractmethod
    def reset(self):
        """Reset the device to initial state."""
        pass

    def is_ready(self):
        """Check if device is ready for operations."""
        return self.status in (DeviceStatus.IDLE, DeviceStatus.READY)

    def is_busy(self):
        """Check if device is busy."""
        return self.status == DeviceStatus.BUSY

    def __repr__(self):
        return f"{self.__class__.__name__}(addr=0o{self.address:02o}, status={self.status.name})"


class TapeDrive(Device):
    """
    Magnetic tape drive.

    Supports forward/backward read, write, and rewind operations.

    Attributes:
        tape: Tape image data (list of records)
        position: Current position on tape
        density: Tape density (bpi)
    """

    def __init__(self, address, name="TapeDrive"):
        """Initialize tape drive."""
        super().__init__(address, name)
        self.tape = []  # List of records
        self.position = 0
        self.density = 556  # Default density: 556 bpi
        self.at_load_point = True

    def read(self, count=1):
        """
        Read forward from tape.

        Args:
            count: Number of records to read

        Returns:
            List of records read
        """
        if not self.is_ready():
            raise DeviceError(f"Tape drive {self.address} not ready")

        records = []
        for _ in range(count):
            if self.position >= len(self.tape):
                self.status = DeviceStatus.END_OF_TAPE
                break
            records.append(self.tape[self.position])
            self.position += 1

        self.at_load_point = False
        return records

    def read_backward(self, count=1):
        """
        Read backward from tape.

        Args:
            count: Number of records to read

        Returns:
            List of records read (in reverse order)
        """
        if not self.is_ready():
            raise DeviceError(f"Tape drive {self.address} not ready")

        records = []
        for _ in range(count):
            if self.position <= 0:
                self.at_load_point = True
                break
            self.position -= 1
            records.append(self.tape[self.position])

        return records

    def write(self, data):
        """
        Write records to tape.

        Args:
            data: List of records to write
        """
        if not self.is_ready():
            raise DeviceError(f"Tape drive {self.address} not ready")

        for record in data:
            if self.position >= len(self.tape):
                self.tape.append(record)
            else:
                self.tape[self.position] = record
            self.position += 1

        self.at_load_point = False

    def rewind(self):
        """Rewind tape to load point."""
        self.position = 0
        self.at_load_point = True
        self.status = DeviceStatus.READY

    def load_tape(self, tape_data):
        """
        Load a tape image.

        Args:
            tape_data: List of records to load onto tape
        """
        self.tape = list(tape_data)
        self.position = 0
        self.at_load_point = True
        self.status = DeviceStatus.READY

    def reset(self):
        """Reset tape drive."""
        self.rewind()
        self.status = DeviceStatus.IDLE


class CardReader(Device):
    """
    Card reader.

    Reads 80-column punched cards.

    Attributes:
        hopper: Card hopper (queue of cards)
        cards_read: Number of cards read
    """

    def __init__(self, address, name="CardReader"):
        """Initialize card reader."""
        super().__init__(address, name)
        self.hopper = []
        self.cards_read = 0

    def read(self, count=1):
        """
        Read cards from hopper.

        Args:
            count: Number of cards to read

        Returns:
            List of card images
        """
        if not self.is_ready():
            raise DeviceError(f"Card reader {self.address} not ready")

        cards = []
        for _ in range(count):
            if not self.hopper:
                self.status = DeviceStatus.END_OF_FILE
                break
            card = self.hopper.pop(0)
            cards.append(card)
            self.cards_read += 1

        return cards

    def write(self, data):
        """Card reader does not support write."""
        raise DeviceError("Card reader does not support write operation")

    def load_deck(self, deck):
        """
        Load a deck of cards into the hopper.

        Args:
            deck: List of card images
        """
        self.hopper.extend(deck)
        self.status = DeviceStatus.READY

    def reset(self):
        """Reset card reader."""
        self.hopper = []
        self.cards_read = 0
        self.status = DeviceStatus.IDLE


class CardPunch(Device):
    """
    Card punch.

    Punches 80-column cards.

    Attributes:
        stacker: Output stacker (cards punched)
        cards_punched: Number of cards punched
    """

    def __init__(self, address, name="CardPunch"):
        """Initialize card punch."""
        super().__init__(address, name)
        self.stacker = []
        self.cards_punched = 0

    def read(self, count=1):
        """Card punch does not support read."""
        raise DeviceError("Card punch does not support read operation")

    def write(self, data):
        """
        Punch cards.

        Args:
            data: List of card images to punch
        """
        if not self.is_ready():
            raise DeviceError(f"Card punch {self.address} not ready")

        for card in data:
            self.stacker.append(card)
            self.cards_punched += 1

    def get_output(self):
        """
        Get punched cards from stacker.

        Returns:
            List of punched card images
        """
        output = list(self.stacker)
        self.stacker = []
        return output

    def reset(self):
        """Reset card punch."""
        self.stacker = []
        self.cards_punched = 0
        self.status = DeviceStatus.IDLE


class LinePrinter(Device):
    """
    Line printer.

    Prints formatted output lines.

    Attributes:
        buffer: Output buffer
        lines_printed: Number of lines printed
        columns: Printer width (default: 120)
    """

    def __init__(self, address, name="LinePrinter", columns=120):
        """Initialize line printer."""
        super().__init__(address, name)
        self.buffer = []
        self.lines_printed = 0
        self.columns = columns

    def read(self, count=1):
        """Line printer does not support read."""
        raise DeviceError("Line printer does not support read operation")

    def write(self, data):
        """
        Print lines.

        Args:
            data: List of lines to print (as strings or word lists)
        """
        if not self.is_ready():
            raise DeviceError(f"Line printer {self.address} not ready")

        for line in data:
            self.buffer.append(line)
            self.lines_printed += 1

    def get_output(self):
        """
        Get printed output.

        Returns:
            List of printed lines
        """
        output = list(self.buffer)
        return output

    def clear_buffer(self):
        """Clear the output buffer."""
        self.buffer = []

    def reset(self):
        """Reset line printer."""
        self.buffer = []
        self.lines_printed = 0
        self.status = DeviceStatus.IDLE


class PaperTapeReader(Device):
    """
    Paper tape reader.

    Reads paper tape.

    Attributes:
        tape: Paper tape data
        position: Current position on tape
    """

    def __init__(self, address, name="PaperTapeReader"):
        """Initialize paper tape reader."""
        super().__init__(address, name)
        self.tape = []
        self.position = 0

    def read(self, count=1):
        """
        Read from paper tape.

        Args:
            count: Number of frames to read

        Returns:
            List of frames read
        """
        if not self.is_ready():
            raise DeviceError(f"Paper tape reader {self.address} not ready")

        frames = []
        for _ in range(count):
            if self.position >= len(self.tape):
                self.status = DeviceStatus.END_OF_FILE
                break
            frames.append(self.tape[self.position])
            self.position += 1

        return frames

    def write(self, data):
        """Paper tape reader does not support write."""
        raise DeviceError("Paper tape reader does not support write operation")

    def load_tape(self, tape_data):
        """
        Load paper tape.

        Args:
            tape_data: List of frames
        """
        self.tape = list(tape_data)
        self.position = 0
        self.status = DeviceStatus.READY

    def reset(self):
        """Reset paper tape reader."""
        self.position = 0
        self.status = DeviceStatus.IDLE


class PaperTapePunch(Device):
    """
    Paper tape punch.

    Punches paper tape.

    Attributes:
        tape: Output tape data
    """

    def __init__(self, address, name="PaperTapePunch"):
        """Initialize paper tape punch."""
        super().__init__(address, name)
        self.tape = []

    def read(self, count=1):
        """Paper tape punch does not support read."""
        raise DeviceError("Paper tape punch does not support read operation")

    def write(self, data):
        """
        Punch paper tape.

        Args:
            data: List of frames to punch
        """
        if not self.is_ready():
            raise DeviceError(f"Paper tape punch {self.address} not ready")

        self.tape.extend(data)

    def get_output(self):
        """
        Get punched tape.

        Returns:
            List of punched frames
        """
        return list(self.tape)

    def reset(self):
        """Reset paper tape punch."""
        self.tape = []
        self.status = DeviceStatus.IDLE


class DiskDrive(Device):
    """
    Disk drive (placeholder for future implementation).

    Attributes:
        tracks: Disk storage organized by tracks
        current_track: Current head position
    """

    def __init__(self, address, name="DiskDrive"):
        """Initialize disk drive."""
        super().__init__(address, name)
        self.tracks = {}
        self.current_track = 0

    def read(self, count=1):
        """Read from disk."""
        # TODO: Implement disk read
        raise NotImplementedError("Disk drive read not yet implemented")

    def write(self, data):
        """Write to disk."""
        # TODO: Implement disk write
        raise NotImplementedError("Disk drive write not yet implemented")

    def seek(self, track):
        """Seek to track."""
        self.current_track = track

    def reset(self):
        """Reset disk drive."""
        self.current_track = 0
        self.status = DeviceStatus.IDLE


class Console(Device):
    """
    Console typewriter.

    Interactive console for operator communication.

    Attributes:
        input_buffer: Input buffer
        output_buffer: Output buffer
    """

    def __init__(self, address, name="Console"):
        """Initialize console."""
        super().__init__(address, name)
        self.input_buffer = []
        self.output_buffer = []

    def read(self, count=1):
        """
        Read from console input.

        Args:
            count: Number of characters to read

        Returns:
            List of characters
        """
        chars = []
        for _ in range(count):
            if not self.input_buffer:
                break
            chars.append(self.input_buffer.pop(0))
        return chars

    def write(self, data):
        """
        Write to console output.

        Args:
            data: List of characters or strings to write
        """
        self.output_buffer.extend(data)

    def type_input(self, text):
        """
        Simulate operator typing input.

        Args:
            text: Text to type
        """
        self.input_buffer.extend(list(text))

    def get_output(self):
        """
        Get console output.

        Returns:
            Output text
        """
        output = "".join(str(c) for c in self.output_buffer)
        return output

    def reset(self):
        """Reset console."""
        self.input_buffer = []
        self.output_buffer = []
        self.status = DeviceStatus.IDLE


class DeviceManager:
    """
    Device manager and dispatcher.

    Manages all peripheral devices and routes I/O operations.

    Attributes:
        devices: Dictionary mapping peripheral addresses to devices
    """

    def __init__(self):
        """Initialize device manager."""
        self.devices = {}

    def attach_device(self, device):
        """
        Attach a device to the system.

        Args:
            device: Device instance to attach

        Raises:
            ValueError: If address is already in use
        """
        if device.address in self.devices:
            raise ValueError(f"Device already attached at address {device.address}")
        self.devices[device.address] = device

    def detach_device(self, address):
        """
        Detach a device from the system.

        Args:
            address: Peripheral address to detach

        Returns:
            Detached device instance
        """
        if address not in self.devices:
            raise KeyError(f"No device at address {address}")
        return self.devices.pop(address)

    def get_device(self, address):
        """
        Get device at specified address.

        Args:
            address: Peripheral address

        Returns:
            Device instance

        Raises:
            KeyError: If no device at address
        """
        if address not in self.devices:
            raise KeyError(f"No device at address 0o{address:02o}")
        return self.devices[address]

    def read(self, address, count=1):
        """
        Read from device at address.

        Args:
            address: Peripheral address
            count: Number of words to read

        Returns:
            Data read from device
        """
        device = self.get_device(address)
        return device.read(count)

    def write(self, address, data):
        """
        Write to device at address.

        Args:
            address: Peripheral address
            data: Data to write
        """
        device = self.get_device(address)
        device.write(data)

    def reset_all(self):
        """Reset all attached devices."""
        for device in self.devices.values():
            device.reset()

    def list_devices(self):
        """
        List all attached devices.

        Returns:
            List of (address, device) tuples
        """
        return sorted(self.devices.items())

    def __repr__(self):
        return f"DeviceManager({len(self.devices)} devices)"
