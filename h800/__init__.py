"""
Top-level public API for the h800 package.

The instruction and opcode system has been modernized to use unified factories and a reverse
decoder instead of facade classes.

Key entry points:
    - get_instruction(mnemonic, **kwargs): Build any 12-bit instruction.
    - build_constant(mnemonic, value): Create a 48-bit constant wrapper.
    - decode_instruction(word, OPCODES): Reverse-decode a 12-bit word to candidate mnemonics.
    - enumerate_encodings(mnemonic): Enumerate all legal encodings for a mnemonic.
    - cli.main(): Command-line interface entry point (python -m h800.cli ...).

Validation rules:
    - mask is mutually exclusive with operand flags (a, b, c).
    - paddr (peripheral address) is mutually exclusive with sequence, mask, and operand flags.

Print instruction collision:
    PRA, PRD, PRO share identical opcode space; decoding a print word yields all three.
"""

from __future__ import annotations

# CLI utilities (exposed for programmatic use)
from .cli import (
    EncodedVariant,
    build_parser,
    enumerate_encodings,
    fmt_binary,
    fmt_hex,
    fmt_octal,
    main as cli_main,
    parse_int,
)

# Core instruction & factories
from .instruction import (
    Constant,
    Instruction,
    OpcodeDict,
    OpcodeMeta,
    build_masked,
    build_peripheral,
    build_print,
    build_simulator,
    build_unmasked,
    decode_instruction,
    get_instruction,
)

# Opcode metadata & numeric helpers
from .instructions import (
    ARGUS_INSTRUCTIONS,
    CONTROL_CONSTANTS,
    CONTROL_INSTRUCTIONS,
    DATA_CONSTANTS,
    EXTENDED_INSTRUCTIONS,
    INSTRUCTIONS,
    MISC_INSTRUCTIONS,
    OPCODES,
    build_constant,
    make_masked_opcode,
    make_peripheral_opcode,
    make_print_opcode,
    make_unmasked_opcode,
    print_instructions,
)

__version__ = "0.9"

__all__ = [
    # Version
    "__version__",
    # Instruction core
    "Instruction",
    "Constant",
    "OpcodeMeta",
    "OpcodeDict",
    # Factories
    "get_instruction",
    "build_masked",
    "build_unmasked",
    "build_peripheral",
    "build_print",
    "build_simulator",
    "build_constant",
    # Reverse / enumeration
    "decode_instruction",
    "enumerate_encodings",
    "EncodedVariant",
    # Opcode metadata tables
    "OPCODES",
    "INSTRUCTIONS",
    "CONTROL_INSTRUCTIONS",
    "DATA_CONSTANTS",
    "CONTROL_CONSTANTS",
    "EXTENDED_INSTRUCTIONS",
    "MISC_INSTRUCTIONS",
    "ARGUS_INSTRUCTIONS",
    # Numeric helpers
    "make_masked_opcode",
    "make_unmasked_opcode",
    "make_peripheral_opcode",
    "make_print_opcode",
    "print_instructions",
    # CLI helpers
    "cli_main",
    "build_parser",
    "parse_int",
    "fmt_octal",
    "fmt_binary",
    "fmt_hex",
]
