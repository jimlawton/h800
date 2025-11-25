"""
H-1800 Instruction Decoder Module
===================================

This module implements the instruction decoder for the H-1800 simulator.

The decoder is responsible for:
- Decoding 12-bit instruction words into their component fields
- Identifying instruction types (maskable, unmasked, peripheral, print, simulator)
- Extracting operand information
- Resolving addressing modes
- Preparing decoded instruction data for the executor

Instruction Format (12-bit word, MSB=1 to LSB=12):

Maskable Instructions:
    Bit 1:      Sequence bit (0 or 1)
    Bits 2-6:   Mask field (5 bits, 0-31)
    Bit 7:      1 (indicates masked form)
    Bits 8-12:  Opcode (5 bits)

Unmasked Instructions:
    Bit 1:      Sequence bit (0 or 1)
    Bits 2-3:   Variant bits (2 bits)
    Bit 4:      Operand A flag
    Bit 5:      Operand B flag
    Bit 6:      Operand C flag
    Bit 7:      0 (indicates unmasked form)
    Bits 8-12:  Opcode (5 bits)

Peripheral Instructions:
    Bits 1-6:   Peripheral address (6 bits, 0-63)
    Bit 7:      1 (indicates peripheral)
    Bits 8-12:  Opcode (5 bits)

Print Instructions:
    Bit 1:      Sequence bit
    Bits 2-3:   Variant bits
    Bit 4:      Operand A flag
    Bit 5:      Operand B flag
    Bit 6:      Operand C flag
    Bit 7:      1 (indicates print)
    Bits 8-12:  Opcode (5 bits, typically 0o06)

Simulator Instructions:
    Bits 1-9:   Not used/variant
    Bits 10-12: Simulator operation code

Key Components:
    DecodedInstruction  - Dataclass holding decoded instruction fields
    Decoder             - Main decoder class
"""

from dataclasses import dataclass

from h800.bitfield import BitField
from h800.opcodes import OPCODES


@dataclass
class DecodedInstruction:
    """
    Represents a decoded instruction with all extracted fields.

    Attributes:
        word: Original 12-bit instruction word
        mnemonic: Instruction mnemonic (e.g., "BA", "TX", "RF")
        opcode: Base opcode value (bits 8-12)
        instruction_type: Type of instruction ("maskable", "unmasked", "peripheral", "print", "simulator")
        sequence: Sequence bit (0 or 1), None for peripheral
        mask: Mask field (0-31) for maskable instructions, None otherwise
        variant: Variant bits (bits 2-3) for unmasked, None otherwise
        operand_a: Operand A flag for unmasked, None otherwise
        operand_b: Operand B flag for unmasked, None otherwise
        operand_c: Operand C flag for unmasked, None otherwise
        paddr: Peripheral address (0-63) for peripheral instructions, None otherwise
        bit7: Value of bit 7 (masked/unmasked indicator)
    """

    word: int
    mnemonic: str | None = None
    opcode: int | None = None
    instruction_type: str | None = None
    sequence: int | None = None
    mask: int | None = None
    variant: int | None = None
    operand_a: int | None = None
    operand_b: int | None = None
    operand_c: int | None = None
    paddr: int | None = None
    bit7: int | None = None

    def __repr__(self):
        parts = [f"word=0o{self.word:04o}"]
        if self.mnemonic:
            parts.append(f"mnemonic={self.mnemonic}")
        if self.instruction_type:
            parts.append(f"type={self.instruction_type}")
        if self.sequence is not None:
            parts.append(f"seq={self.sequence}")
        if self.mask is not None:
            parts.append(f"mask=0o{self.mask:02o}")
        if self.paddr is not None:
            parts.append(f"paddr=0o{self.paddr:02o}")
        return f"DecodedInstruction({', '.join(parts)})"


class DecoderError(Exception):
    """Exception raised for decoding errors."""

    pass


class Decoder:
    """
    H-1800 Instruction Decoder.

    Decodes 12-bit instruction words into their component fields and
    identifies the instruction mnemonic and type.

    Attributes:
        opcodes: Opcode metadata dictionary (from h800.opcodes)
    """

    def __init__(self, opcodes=None):
        """
        Initialize the decoder.

        Args:
            opcodes: Opcode metadata dictionary (default: OPCODES from h800.opcodes)
        """
        self.opcodes = opcodes if opcodes is not None else OPCODES

    def decode(self, word):
        """
        Decode a 12-bit instruction word.

        Args:
            word: 12-bit instruction word (0 to 0o7777)

        Returns:
            DecodedInstruction instance with all extracted fields

        Raises:
            DecoderError: If word is invalid or cannot be decoded
        """
        if not isinstance(word, int):
            raise DecoderError(f"Instruction word must be integer, got {type(word).__name__}")
        if word < 0 or word > 0o7777:
            raise DecoderError(f"Instruction word out of range: 0o{word:04o}")

        # Create BitField for easier bit extraction
        bits = BitField(
            word, width=12, numbering=BitField.BIT_SCHEME_MSB_1, order=BitField.BIT_ORDER_MSB_LEFT
        )

        # Extract common fields
        bit7 = bits[7]
        opcode = bits[8:12]

        # Initialize decoded instruction
        decoded = DecodedInstruction(word=word, bit7=bit7, opcode=opcode)

        # Decode based on bit 7 and opcode
        if bit7 == 1:
            # Either maskable (with mask), peripheral, or print
            # Check if bits 1-6 could be a peripheral address or mask
            bits_1_6 = bits[1:6]

            # Try to match against peripheral opcodes first
            if self._is_peripheral_opcode(opcode):
                decoded.instruction_type = "peripheral"
                decoded.paddr = bits_1_6
                decoded.mnemonic = self._find_mnemonic(opcode, "peripheral")
            elif self._is_print_opcode(opcode):
                # Print instruction (similar to unmasked but bit7=1)
                decoded.instruction_type = "print"
                decoded.sequence = bits[1]
                decoded.variant = bits[2:3]
                decoded.operand_a = bits[4]
                decoded.operand_b = bits[5]
                decoded.operand_c = bits[6]
                decoded.mnemonic = self._find_mnemonic(opcode, "print")
            else:
                # Maskable instruction
                decoded.instruction_type = "maskable"
                decoded.sequence = bits[1]
                decoded.mask = bits[2:6]
                decoded.mnemonic = self._find_mnemonic(opcode, "maskable", variant=0b10)
        else:
            # Unmasked instruction (bit7=0)
            decoded.instruction_type = "unmasked"
            decoded.sequence = bits[1]
            decoded.variant = bits[2:3]
            decoded.operand_a = bits[4]
            decoded.operand_b = bits[5]
            decoded.operand_c = bits[6]
            decoded.mnemonic = self._find_mnemonic(opcode, "unmasked", variant=decoded.variant)

        return decoded

    def _is_peripheral_opcode(self, opcode):
        """Check if opcode corresponds to a peripheral instruction."""
        for meta in self.opcodes.values():
            if hasattr(meta, "type") and meta.type == "peripheral" and meta.op == opcode:
                return True
        return False

    def _is_print_opcode(self, opcode):
        """Check if opcode corresponds to a print instruction."""
        for meta in self.opcodes.values():
            if hasattr(meta, "type") and meta.type == "print" and meta.op == opcode:
                return True
        return False

    def _find_mnemonic(self, opcode, instr_type, variant=None):
        """
        Find the mnemonic for a given opcode and instruction type.

        Args:
            opcode: Opcode value (bits 8-12)
            instr_type: Instruction type
            variant: Variant bits (for unmasked instructions)

        Returns:
            Mnemonic string or None if not found
        """
        for mnemonic, meta in self.opcodes.items():
            if meta.op != opcode:
                continue

            meta_type = getattr(meta, "type", "unmasked")
            if meta_type != instr_type:
                continue

            # For unmasked instructions, also check variant (bits 2-3)
            if instr_type == "unmasked" and variant is not None:
                meta_variant = getattr(meta, "b23", None)
                if meta_variant is not None and meta_variant != variant:
                    continue

            # For maskable instructions, check b23 = 0b10
            if instr_type == "maskable":
                meta_variant = getattr(meta, "b23", None)
                if meta_variant != 0b10:
                    continue

            return mnemonic

        return None

    def decode_operands(self, decoded, memory=None, registers=None):
        """
        Decode and resolve operand addresses.

        This is a placeholder for future implementation that will:
        - Resolve complex addresses using index registers
        - Apply masks and compute effective addresses
        - Handle indirect addressing modes

        Args:
            decoded: DecodedInstruction instance
            memory: Memory subsystem (optional, for reading constants)
            registers: Register file (optional, for index register values)

        Returns:
            Dictionary of resolved operand addresses
        """
        # TODO: Implement operand address resolution
        # This will be complex and involve:
        # - Reading address constants from memory
        # - Applying index registers
        # - Computing effective addresses based on operand flags
        # - Handling different addressing modes
        operands = {}

        if decoded.operand_a:
            operands["a"] = None  # Placeholder

        if decoded.operand_b:
            operands["b"] = None  # Placeholder

        if decoded.operand_c:
            operands["c"] = None  # Placeholder

        return operands

    def disassemble(self, word):
        """
        Disassemble an instruction word into human-readable format.

        Args:
            word: 12-bit instruction word

        Returns:
            Formatted disassembly string
        """
        decoded = self.decode(word)

        parts = [f"0o{word:04o}:"]

        if decoded.mnemonic:
            parts.append(decoded.mnemonic)
        else:
            parts.append("???")

        if decoded.sequence is not None:
            parts.append(f"seq={decoded.sequence}")

        if decoded.mask is not None:
            parts.append(f"mask=0o{decoded.mask:02o}")

        if decoded.paddr is not None:
            parts.append(f"paddr=0o{decoded.paddr:02o}")

        if decoded.operand_a or decoded.operand_b or decoded.operand_c:
            flags = []
            if decoded.operand_a:
                flags.append("A")
            if decoded.operand_b:
                flags.append("B")
            if decoded.operand_c:
                flags.append("C")
            parts.append(f"[{','.join(flags)}]")

        return " ".join(parts)

    def __repr__(self):
        return f"Decoder(opcodes={len(self.opcodes)} mnemonics)"
