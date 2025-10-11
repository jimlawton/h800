# Honeywell H-800/H-1800 instruction core.
# Provides the Instruction base class (encoding 12-bit opcodes) and Constant
# for 48-bit constant values used by various assembler directives.

from __future__ import annotations

from .bitfield import BitField

# Validation constants
MASK_MAX = 31  # 5-bit mask (0..31)
PADDR_MAX = 63  # 6-bit peripheral address (0..63)
BITS23_MAX = 3  # Bits 2-3 when present (00..11)
OPCODE_MAX = 31  # Bits 8-12 base opcode (00000..11111)
WORD_48_MAX = 2**48 - 1  # Maximum 48-bit constant value


class Instruction:
    """
    Base opcode class.

    Encodes a 12-bit instruction word in a BitField. The opcode object passed
    in (constructed in instructions.py) supplies structural metadata:

        m      : mnemonic string
        b23    : bits 2-3 (unmasked forms) or None
        b7     : bit 7 (masked/unmasked indicator or None)
        op     : bits 8-12 base opcode (0..31)
        type   : one of: "unmasked", "maskable", "peripheral", "print", "simulator"

    Parameters (only some valid per type):
        sequence : 0/1 (boolean) for sequence/cosequence bit at position 1
        mask     : 0..31 mask (maskable instructions only)
        a,b,c    : operand presence flags (0/1) for unmasked, print instructions
        paddr    : 0..63 peripheral address (peripheral instructions only)
        pseudo   : if True no binary will be generated (placeholder feature)
    """

    def __init__(
        self,
        opcode,
        sequence=None,
        mask=None,
        a=None,
        b=None,
        c=None,
        paddr=None,
        pseudo: bool = False,
    ):
        # Store metadata from opcode definition.
        self._opcode_obj = opcode
        self._mnemonic = opcode.m
        self._bits23 = opcode.b23
        self._bit7 = opcode.b7
        self._op = opcode.op
        self._type = opcode.type

        # Store user-supplied fields.
        self._sequence = sequence
        self._mask = mask
        self._a = a
        self._b = b
        self._c = c
        self._paddr = paddr
        self._pseudo = pseudo

        # 12-bit instruction storage (MSB-1 numbering, MSB-left order).
        self.data = BitField(
            0,
            width=12,
            numbering=BitField.BIT_SCHEME_MSB_1,
            order=BitField.BIT_ORDER_MSB_LEFT,
        )

        # Validate combinations before encoding.
        self._check()

        # Field placement follows original encoding layout:
        #   Bit 1        : sequence/cosequence (if present)
        #   Bits 2..6    : mask (maskable) OR bits 2..3 (unmasked) + A/B/C flags
        #   Bit 7        : masked/unmasked indicator (if provided in opcode)
        #   Bits 8..12   : base opcode
        #
        # Masked instructions: bits 2..6 contain full mask; A/B/C unused.
        # Unmasked & print instructions: bits 2..3 may contain opcode variant,
        #   bits 4,5,6 hold A,B,C flags if supplied.
        # Peripheral instructions: bits 1..6 hold peripheral address; bit 7 may
        #   reflect opcode bit7; A/B/C and mask unused.

        # Sequence bit
        if self._sequence is not None:
            self.data[1] = 1 if bool(self._sequence) else 0

        # Masked / peripheral / print set bit7 if defined
        if self._type in ("maskable", "peripheral", "print"):
            if (self._type == "maskable" and self._mask is not None) or self._type != "maskable":
                if self._bit7 is not None:
                    self.data[7] = self._bit7

        # Mask vs bits 2-3
        if self._mask is not None:
            # Full 5-bit mask occupies bits 2..6
            self.data[2:6] = self._mask
        elif self._bits23 is not None:
            # Partial bits 2..3 (2 bits)
            self.data[2:3] = self._bits23

        # Operand presence flags (unmasked / print)
        if self._a is not None:
            self.data[4] = 1 if bool(self._a) else 0
        if self._b is not None:
            self.data[5] = 1 if bool(self._b) else 0
        if self._c is not None:
            self.data[6] = 1 if bool(self._c) else 0

        # Peripheral address overrides bits 1..6
        if self._paddr is not None:
            self.data[1:6] = self._paddr

        # Base opcode bits 8..12
        self.data[8:12] = self._op

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    def _check(self):
        """Validate instruction field combinations and ranges."""
        # Mutual exclusion: sequence vs peripheral address.
        if self._sequence is not None and self._paddr is not None:
            raise ValueError("Cannot specify sequence and peripheral address together.")
        if self._sequence is not None and self._sequence not in (0, 1, True, False):
            raise ValueError("Sequence must be boolean (0/1).")

        # Mask validation.
        if self._mask is not None:
            if self._type != "maskable":
                raise ValueError("Mask supplied to a non-maskable instruction.")
            if any(x is not None for x in (self._a, self._b, self._c, self._paddr)):
                raise ValueError("Cannot specify A/B/C or peripheral address with a mask.")
            if not (0 <= self._mask <= MASK_MAX):
                raise ValueError(f"Mask must be in range 0..{MASK_MAX}.")

        # Operand flags.
        for name, flag in (("A", self._a), ("B", self._b), ("C", self._c)):
            if flag is not None and flag not in (0, 1, True, False):
                raise ValueError(f"{name} flag must be boolean (0/1).")

        # Peripheral address.
        if self._paddr is not None:
            if any(x is not None for x in (self._sequence, self._mask, self._a, self._b, self._c)):
                raise ValueError("Cannot specify sequence/mask/A/B/C with peripheral address.")
            if not (0 <= self._paddr <= PADDR_MAX):
                raise ValueError(f"Peripheral address must be in range 0..{PADDR_MAX}.")

        # bit7 (masked indicator) if present in opcode metadata.
        if self._bit7 is not None and self._bit7 not in (0, 1):
            raise ValueError("Bit 7 must be 0 or 1.")

        # bits23 (variant) range.
        if self._bits23 is not None and not (0 <= self._bits23 <= BITS23_MAX):
            raise ValueError(f"Bits 2-3 must be in range 0..{BITS23_MAX}.")

        # base opcode range sanity.
        if not (0 <= self._op <= OPCODE_MAX):
            raise ValueError(f"Opcode must be in range 0..{OPCODE_MAX}.")

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    @property
    def mnemonic(self) -> str:
        return self._mnemonic

    @property
    def value(self) -> int:
        """Return encoded 12-bit instruction integer."""
        return int(self.data)

    def __int__(self) -> int:  # Convenience
        return self.value

    def __repr__(self) -> str:
        return (
            f"Instruction(mnemonic={self._mnemonic!r}, value=0o{self.value:04o}, "
            f"type={self._type}, sequence={self._sequence}, mask={self._mask}, "
            f"a={self._a}, b={self._b}, c={self._c}, paddr={self._paddr})"
        )


class Constant:
    """
    48-bit constant value wrapper.

    Used by various directive-like pseudo instructions (e.g., DecimalConstant,
    AlphanumericConstant, etc.) to carry raw data values into the assembled
    output space.

    Range enforced: 0 .. (2**48 - 1).
    """

    def __init__(self, mnemonic: str, data: int):
        self._mnemonic = mnemonic
        if not isinstance(data, int):
            raise TypeError("Constant data must be int.")
        if not (0 <= data <= WORD_48_MAX):
            raise ValueError(f"Constant {mnemonic} out of range 0..{WORD_48_MAX}.")
        self._data = data

    @property
    def mnemonic(self) -> str:
        return self._mnemonic

    @property
    def value(self) -> int:
        return self._data

    def __int__(self) -> int:
        return self._data

    def __repr__(self) -> str:
        return f"Constant(mnemonic={self._mnemonic!r}, value={self._data})"
