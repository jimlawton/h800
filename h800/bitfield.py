# Copyright 2010 Jim Lawton <jim dot lawton at gmail dot com>
#
# Modernized 2025: helper names converted to snake_case with backward-compatible
# wrappers; string formatting migrated to f-strings; added type hints.
#
# This file is part of h800 (GPL-2.0-only).

from __future__ import annotations


class BitField:
    """Generic bit-field utility supporting multiple numbering and ordering schemes.

    Numbering schemes:
        LSB_0:   Bit 0 is least significant
        LSB_1:   Bit 1 is least significant (shifts all virtual indices by +1)
        MSB_0:   Bit 0 is most significant
        MSB_1:   Bit 1 is most significant (shifts all virtual indices by +1)

    Ordering:
        BIT_ORDER_MSB_LEFT  (value rendered left→right, MSB appears left)
        BIT_ORDER_MSB_RIGHT (alias: BIT_ORDER_LSB_LEFT) (LSB appears left)

    Public API (legacy camelCase preserved via wrappers):
        width, maxval, numbering, order, value
        set(), clear()
        isBit(), isBitSet(), isBitClr(), isRange(), isRangeSet(), isRangeClr()

    New preferred snake_case API mirrors the above:
        is_bit(), is_bit_set(), is_bit_clr(), is_range(), is_range_set(), is_range_clr()
    """

    DEFAULT_WIDTH = 8
    MAX_WIDTH = 64  # Internal safety cap (adjust as needed).

    # Numbering schemes.
    BIT_SCHEME_LSB_0 = 0
    BIT_SCHEME_LSB_1 = 1
    BIT_SCHEME_MSB_0 = 2
    BIT_SCHEME_MSB_1 = 3

    # Ordering.
    BIT_ORDER_MSB_LEFT = BIT_ORDER_LSB_RIGHT = 0  # MSB ... LSB visually left→right
    BIT_ORDER_LSB_LEFT = BIT_ORDER_MSB_RIGHT = 1  # LSB ... MSB visually left→right

    def __init__(
        self,
        value: int = 0,
        width: int = DEFAULT_WIDTH,
        numbering: int = BIT_SCHEME_LSB_0,
        order: int = BIT_ORDER_MSB_RIGHT,
    ) -> None:
        self._width = width
        if width > self.MAX_WIDTH or width <= 0:
            raise ValueError("Width is greater than maximum allowed or non-positive!")
        self._maxval = (1 << width) - 1
        self._value = int(value)
        if self._value > self._maxval or self._value < 0:
            raise ValueError("Value is outside the allowable range for this bit-field width!")
        self._numbering = numbering
        if numbering not in (
            self.BIT_SCHEME_LSB_0,
            self.BIT_SCHEME_LSB_1,
            self.BIT_SCHEME_MSB_0,
            self.BIT_SCHEME_MSB_1,
        ):
            raise ValueError("Invalid bit numbering scheme!")
        self._order = order
        if order not in (self.BIT_ORDER_MSB_LEFT, self.BIT_ORDER_MSB_RIGHT):
            raise ValueError("Invalid bit order!")

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def width(self) -> int:
        return self._width

    @property
    def maxval(self) -> int:
        return self._maxval

    @property
    def numbering(self) -> int:
        return self._numbering

    @property
    def order(self) -> int:
        return self._order

    @property
    def value(self) -> int:
        return int(self._value)

    @value.setter
    def value(self, value: int) -> None:
        self._check_value(value)
        self._value = int(value)

    @property
    def indices(self) -> list[int]:
        return [self._vindex(i) for i in range(self._width)]

    @property
    def lsb(self) -> int:
        return self.indices[0] if self._order == self.BIT_ORDER_LSB_LEFT else self.indices[-1]

    @property
    def msb(self) -> int:
        return self.indices[0] if self._order == self.BIT_ORDER_MSB_LEFT else self.indices[-1]

    # -------------------------------------------------------------------------
    # Internal index conversions
    # -------------------------------------------------------------------------

    def _rindex(self, index: int, width: int | None = None) -> int:
        """Map virtual index to real (python) index."""
        if width is None:
            width = self._width
        if self._order == self.BIT_ORDER_MSB_LEFT:
            if self._numbering == self.BIT_SCHEME_LSB_0:
                return width - (index + 1)
            if self._numbering == self.BIT_SCHEME_LSB_1:
                return width - index
            if self._numbering == self.BIT_SCHEME_MSB_0:
                return index
            if self._numbering == self.BIT_SCHEME_MSB_1:
                return index - 1
        else:  # LSB-left ordering
            if self._numbering == self.BIT_SCHEME_LSB_0:
                return index
            if self._numbering == self.BIT_SCHEME_LSB_1:
                return index - 1
            if self._numbering == self.BIT_SCHEME_MSB_0:
                return width - (index + 1)
            if self._numbering == self.BIT_SCHEME_MSB_1:
                return width - index
        raise ValueError("Invalid numbering/order combination in _rindex")

    def _vindex(self, index: int, width: int | None = None) -> int:
        """Inverse mapping: real index → virtual index."""
        if width is None:
            width = self._width
        if self._order == self.BIT_ORDER_MSB_LEFT:
            if self._numbering == self.BIT_SCHEME_LSB_0:
                return width - (index + 1)
            if self._numbering == self.BIT_SCHEME_LSB_1:
                return width - index
            if self._numbering == self.BIT_SCHEME_MSB_0:
                return index
            if self._numbering == self.BIT_SCHEME_MSB_1:
                return index + 1
        else:  # LSB-left
            if self._numbering == self.BIT_SCHEME_LSB_0:
                return index
            if self._numbering == self.BIT_SCHEME_LSB_1:
                return index + 1
            if self._numbering == self.BIT_SCHEME_MSB_0:
                return width - (index + 1)
            if self._numbering == self.BIT_SCHEME_MSB_1:
                return width - index
        raise ValueError("Invalid numbering/order combination in _vindex")

    def _shift(self, index: int) -> int:
        """Return left-shift needed to align bit at 'index' to bit 0."""
        if self._order == self.BIT_ORDER_MSB_LEFT:
            return self._width - index - 1
        return index

    # -------------------------------------------------------------------------
    # Modern snake_case helpers + legacy wrappers
    # -------------------------------------------------------------------------

    def _lsb_index(self, start: int, end: int) -> int:
        return max(start, end) if self._order == self.BIT_ORDER_MSB_LEFT else min(start, end)

    def _msb_index(self, start: int, end: int) -> int:
        return min(start, end) if self._order == self.BIT_ORDER_MSB_LEFT else max(start, end)

    def _check_index(self, index: int) -> None:
        rindex = self._rindex(index)
        if rindex < 0 or rindex >= self._width:
            raise ValueError(f"Invalid index for {self._width}-bit bit-field!")

    def _check_range(self, start: int, end: int) -> None:
        self._check_index(start)
        self._check_index(end)
        if self._order == self.BIT_ORDER_MSB_LEFT:
            if self._numbering in (self.BIT_SCHEME_LSB_0, self.BIT_SCHEME_LSB_1):
                if start < end:
                    raise ValueError("Invalid bit range for MSB...LSB bit-field!")
            elif start > end:
                raise ValueError("Invalid bit range for MSB...LSB bit-field!")
        elif self._numbering in (self.BIT_SCHEME_LSB_0, self.BIT_SCHEME_LSB_1):
            if start > end:
                raise ValueError("Invalid bit range for MSB...LSB bit-field!")
        elif start < end:
            raise ValueError("Invalid bit range for MSB...LSB bit-field!")

    def _get_range(self, start: int, end: int) -> tuple[int, int]:
        self._check_range(start, end)
        return self._rindex(start), self._rindex(end)

    def _check_value(self, value: int, width: int | None = None) -> None:
        if width is None:
            width = self._width
        if width < 0 or width > self._width:
            raise ValueError(f"Illegal bit-field width {width}!")
        if value < 0 or value > (1 << width):
            raise ValueError(f"Value is greater than allowed for {width}-bit field!")

    def _bitmask(self, start: int, end: int) -> int:
        self._check_range(start, end)
        rstart, rend = self._get_range(start, end)
        slice_width = rend - rstart + 1
        shift = 0 if slice_width == self._width else self._shift(rend)
        return ((1 << slice_width) - 1) << shift

    def _get_bit_value(self, index: int, value: int, width: int) -> int:
        """Return value of a single bit at index within provided value."""
        self._check_value(value, width=width)
        return (value >> index) & 0x1

    # Legacy camelCase wrappers (to be deprecated)
    def _lsbIndex(self, start, end):  # noqa: N802
        return self._lsb_index(start, end)

    def _msbIndex(self, start, end):  # noqa: N802
        return self._msb_index(start, end)

    def _checkIndex(self, index):  # noqa: N802
        self._check_index(index)

    def _checkRange(self, start, end):  # noqa: N802
        self._check_range(start, end)

    def _getRange(self, start, end):  # noqa: N802
        return self._get_range(start, end)

    def _checkValue(self, value, width=None):  # noqa: N802
        self._check_value(value, width)

    def _getBitValue(self, index, value, width):  # noqa: N802
        return self._get_bit_value(index, value, width)

    # -------------------------------------------------------------------------
    # Element access
    # -------------------------------------------------------------------------

    def __getitem__(self, key) -> int:
        if isinstance(key, slice):
            start, end = key.start, key.stop
            self._check_range(start, end)
            rstart, rend = self._get_range(start, end)
            bitmask = self._bitmask(start, end)
            shift = self._shift(self._lsb_index(rstart, rend))
            return (self._value & bitmask) >> shift
        index = key
        self._check_index(index)
        rindex = self._rindex(index)
        shift = self._shift(rindex)
        return (self._value >> shift) & 1

    def __setitem__(self, key, value: int) -> None:
        if isinstance(key, slice):
            start, end = key.start, key.stop
            self._check_range(start, end)
            rstart, rend = self._get_range(start, end)
            slice_width = rend - rstart + 1
            self._check_value(value, width=slice_width)
            bitmask = self._bitmask(start, end)
            shift = self._shift(self._lsb_index(rstart, rend))
            newvalue = (self._value & (self._maxval - bitmask)) | (value << shift)
        else:
            index = key
            self._check_index(index)
            self._check_value(value, width=1)
            rindex = self._rindex(index)
            shift = self._shift(rindex)
            bitmask = 1 << shift
            if value == 1:
                newvalue = self._value | bitmask
            else:
                newvalue = self._value & (self._maxval ^ bitmask)
        self._value = newvalue

    def __len__(self) -> int:
        return self._width

    def __int__(self) -> int:
        return self._value

    def __index__(self) -> int:
        return self._value

    def __repr__(self) -> str:
        return f"{self._value:0{self._width}b}"

    # -------------------------------------------------------------------------
    # Bulk operations
    # -------------------------------------------------------------------------

    def set(self, index: int | None = None) -> None:
        """Set all bits (or a specific bit) to 1."""
        if index is not None:
            self._check_index(index)
            self[index] = 1
        else:
            self._value = self._maxval

    def clear(self, index: int | None = None) -> None:
        """Clear all bits (or a specific bit) to 0."""
        if index is not None:
            self._check_index(index)
            self[index] = 0
        else:
            self._value = 0

    # -------------------------------------------------------------------------
    # Predicate operations (snake_case + legacy)
    # -------------------------------------------------------------------------

    def is_bit(self, index: int, value: int) -> bool:
        self._check_index(index)
        if value not in (0, 1):
            raise ValueError("Bit value must be 0 or 1.")
        return self[index] == value

    def isBit(self, index, value):  # noqa: N802
        return self.is_bit(index, value)

    def is_bit_set(self, index: int) -> bool:
        return self.is_bit(index, 1)

    def isBitSet(self, index):  # noqa: N802
        return self.is_bit_set(index)

    def is_bit_clr(self, index: int) -> bool:
        return not self.is_bit_set(index)

    def isBitClr(self, index):  # noqa: N802
        return self.is_bit_clr(index)

    def is_range(self, start: int, end: int, value: int) -> bool:
        self._check_range(start, end)
        if value not in (0, 1):
            raise ValueError("Bit-field value must be 0 or 1!")
        subfield = self[slice(start, end)]
        bitmask = self._bitmask(start, end)
        if value == 0:
            return subfield == 0
        return subfield == bitmask

    def isRange(self, start, end, value):  # noqa: N802
        return self.is_range(start, end, value)

    def is_range_set(self, start: int, end: int) -> bool:
        return self.is_range(start, end, 1)

    def isRangeSet(self, start, end):  # noqa: N802
        return self.is_range_set(start, end)

    def is_range_clr(self, start: int, end: int) -> bool:
        return not self.is_range_set(start, end)

    def isRangeClr(self, start, end):  # noqa: N802
        return self.is_range_clr(start, end)
