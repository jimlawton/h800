"""
CLI utilities for Honeywell H-800/H-1800 instruction disassembly and opcode enumeration.

Features:
    - Decode (disassemble) a 12-bit instruction word into candidate mnemonics/fields.
    - Enumerate all valid encoded 12-bit opcodes for a given mnemonic.
    - List all defined instruction mnemonics grouped by category.
    - Show collisions (e.g., PRA/PRD/PRO print opcode space).
    - Utility formatting helpers (binary, octal, hex).

Usage examples:
    python -m h800.cli decode 0o4065
    python -m h800.cli decode 0x835    # Hex
    python -m h800.cli decode 2133     # Decimal
    python -m h800.cli enumerate BA --masked --sample 3
    python -m h800.cli enumerate PRA --print-all
    python -m h800.cli list
    python -m h800.cli collisions 0o1046

All decoding relies on `decode_instruction` from `h800.instruction`.

Note:
    Print instructions PRA, PRD, PRO share an identical opcode space; decoding a print
    word will list all three mnemonics.

Exit codes:
    0: Success
    1: Invalid arguments / decoding error.

"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from dataclasses import dataclass

from .instruction import decode_instruction
from .instructions import OPCODES

# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------


def fmt_octal(word: int) -> str:
    return f"0o{word:04o}"  # 12-bit width up to 0o7777


def fmt_binary(word: int) -> str:
    return f"{word:012b}"  # 12 bits


def fmt_hex(word: int) -> str:
    return f"0x{word:03X}"  # Up to 0xFFF


def parse_int(token: str) -> int:
    """
    Parse an integer token supporting:
        - 0o (octal), 0x (hex), 0b (binary) prefixes
        - raw octal (digits 0-7) if token starts with 'o' or all digits (fallback decimal otherwise)
    """
    token = token.strip()
    if token.startswith(("0o", "0O")):
        return int(token, 8)
    if token.startswith(("0x", "0X")):
        return int(token, 16)
    if token.startswith(("0b", "0B")):
        return int(token, 2)
    # Raw octal heuristic: all digits in 0-7 and length <= 4
    if all(c in "01234567" for c in token) and len(token) <= 4:
        try:
            return int(token, 8)
        except ValueError:
            pass
    # Fallback decimal
    return int(token, 10)


# ---------------------------------------------------------------------------
# Enumeration utilities
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EncodedVariant:
    mnemonic: str
    word: int
    detail: str  # Human-readable detail of the parameterization.


def enumerate_encodings(
    mnemonic: str,
    *,
    include_all_print: bool = False,
    sample_limit: int | None = None,
) -> list[EncodedVariant]:
    """
    Enumerate all valid encodings for a mnemonic.
    For PRA/PRD/PRO (print collision) produce one unified set (mnemonic shown as provided)
    unless include_all_print=True (then each operand pattern is replicated for all three mnemonics).

    sample_limit:
        For very large sets (maskable instructions: 2*32 variants = 64,
        unmasked: 2*8=16, print: 2*8=16, etc.) you can cap enumeration.
    """
    if mnemonic not in OPCODES:
        raise KeyError(f"Unknown mnemonic: {mnemonic}")
    meta = OPCODES[mnemonic]
    mtype = getattr(meta, "type", "unmasked")
    variants: list[EncodedVariant] = []

    def add(m: str, w: int, detail: str) -> None:
        variants.append(EncodedVariant(mnemonic=m, word=w, detail=detail))

    if mtype == "maskable":
        # Mask form (bit7=1, mask 0..31, sequence 0/1)
        for sequence in (0, 1):
            for mask in range(32):
                word = (0o4000 * sequence) + (0o100 * mask) + (0o40 * meta.b7) + meta.op
                add(mnemonic, word, f"sequence={sequence} mask={mask}")
                if sample_limit and len(variants) >= sample_limit:
                    return variants
        # Unmasked form (bit7=0)
        for sequence in (0, 1):
            for a in (0, 1):
                for b in (0, 1):
                    for c in (0, 1):
                        word = (
                            0o4000 * sequence
                            + 0o1000 * meta.b23
                            + 0o400 * a
                            + 0o200 * b
                            + 0o100 * c
                            + meta.op
                        )
                        add(mnemonic, word, f"sequence={sequence} a={a} b={b} c={c}")
                        if sample_limit and len(variants) >= sample_limit:
                            return variants

    elif mtype == "unmasked":
        for sequence in (0, 1):
            for a in (0, 1):
                for b in (0, 1):
                    for c in (0, 1):
                        word = (
                            0o4000 * sequence
                            + 0o1000 * meta.b23
                            + 0o400 * a
                            + 0o200 * b
                            + 0o100 * c
                            + meta.op
                        )
                        add(mnemonic, word, f"sequence={sequence} a={a} b={b} c={c}")
                        if sample_limit and len(variants) >= sample_limit:
                            return variants

    elif mtype == "peripheral":
        for paddr in range(64):
            word = (0o100 * paddr) + (0o40 * meta.b7) + meta.op
            add(mnemonic, word, f"paddr={paddr}")
            if sample_limit and len(variants) >= sample_limit:
                return variants

    elif mtype == "print":
        # PRA enumeration only; code space identical for PRD, PRO.
        targets = ["PRA", "PRD", "PRO"] if include_all_print else [mnemonic]
        for sequence in (0, 1):
            for a in (0, 1):
                for b in (0, 1):
                    for c in (0, 1):
                        word = (
                            0o4000 * sequence
                            + 0o400 * a
                            + 0o200 * b
                            + 0o100 * c
                            + 0o40 * meta.b7
                            + meta.op
                        )
                        for t in targets:
                            add(t, word, f"sequence={sequence} a={a} b={b} c={c}")
                            if sample_limit and len(variants) >= sample_limit:
                                return variants

    elif mtype == "simulator":
        # Two sequence variants; value determined by sequence bit.
        for sequence in (0, 1):
            word = 0o4000 * sequence + meta.op
            add(mnemonic, word, f"sequence={sequence}")

    else:
        # Pseudo or unknown types produce no encodings.
        pass

    return variants


# ---------------------------------------------------------------------------
# CLI command implementations
# ---------------------------------------------------------------------------


def cmd_decode(args: argparse.Namespace) -> int:
    try:
        value = parse_int(args.word)
    except Exception as exc:
        print(f"ERROR: Cannot parse word '{args.word}': {exc}", file=sys.stderr)
        return 1

    try:
        info = decode_instruction(value, OPCODES)
    except Exception as exc:
        print(f"ERROR: Decode failed: {exc}", file=sys.stderr)
        return 1

    print(f"Word: {fmt_octal(value)}  bin={fmt_binary(value)}  hex={fmt_hex(value)}")
    print(f"Candidate mnemonics: {', '.join(info['mnemonics']) or '(none)'}")
    if info["fields"]:
        field_str = ", ".join(f"{k}={v}" for k, v in info["fields"].items())
        print(f"Fields: {field_str}")
    if info["types"]:
        print(f"Types: {', '.join(info['types'])}")
    return 0


def cmd_enumerate(args: argparse.Namespace) -> int:
    mnemonic = args.mnemonic
    if mnemonic not in OPCODES:
        print(f"ERROR: Unknown mnemonic '{mnemonic}'", file=sys.stderr)
        return 1

    try:
        variants = enumerate_encodings(
            mnemonic,
            include_all_print=args.print_all,
            sample_limit=args.sample,
        )
    except Exception as exc:
        print(f"ERROR: Enumeration failed: {exc}", file=sys.stderr)
        return 1

    if not variants:
        print(f"No encodings generated for mnemonic '{mnemonic}'. (Pseudo or unsupported.)")
        return 0

    print(f"Enumerated {len(variants)} encoding(s) for {mnemonic}:")
    for ev in variants:
        print(f"  {fmt_octal(ev.word)}  {fmt_binary(ev.word)}  {ev.mnemonic}  ({ev.detail})")
    if not args.sample:
        # Show uniqueness summary (optional)
        codes = [ev.word for ev in variants]
        if len(codes) != len(set(codes)):
            print("WARNING: Duplicate opcode values detected (expected only for print collisions).")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    # Group mnemonics by type
    buckets: dict[str, list[str]] = {
        "maskable": [],
        "unmasked": [],
        "peripheral": [],
        "print": [],
        "simulator": [],
        "pseudo": [],
    }
    for m, meta in OPCODES.items():
        t = getattr(meta, "type", "unmasked")
        if t not in buckets:
            buckets["pseudo"].append(m)
        else:
            buckets[t].append(m)

    for t in buckets:
        buckets[t].sort()

    for t, mm in buckets.items():
        if not mm:
            continue
        print(f"{t.upper():<11}: {' '.join(mm)}")
    return 0


def cmd_collisions(args: argparse.Namespace) -> int:
    try:
        value = parse_int(args.word)
    except Exception as exc:
        print(f"ERROR: Cannot parse word '{args.word}': {exc}", file=sys.stderr)
        return 1

    try:
        info = decode_instruction(value, OPCODES)
    except Exception as exc:
        print(f"ERROR: Decode failed: {exc}", file=sys.stderr)
        return 1

    mnemonics = info["mnemonics"]
    if set(mnemonics) & {"PRA", "PRD", "PRO"}:
        print(
            f"Print collision space: {fmt_octal(value)} -> {', '.join(sorted(set(mnemonics) & {'PRA', 'PRD', 'PRO'}))}"
        )
    else:
        print(
            f"No print collision for {fmt_octal(value)} (mnemonics: {', '.join(mnemonics) or '(none)'})"
        )
    return 0


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="h800.cli",
        description="Honeywell H-800/H-1800 instruction disassembler and opcode utilities.",
    )
    sub = p.add_subparsers(dest="command", required=True)

    # decode
    sp_decode = sub.add_parser("decode", help="Decode a 12-bit instruction word.")
    sp_decode.add_argument(
        "word", help="Word (supports 0o / 0x / 0b prefixes or raw octal/decimal)."
    )
    sp_decode.set_defaults(func=cmd_decode)

    # enumerate
    sp_enum = sub.add_parser("enumerate", help="Enumerate valid encodings for a mnemonic.")
    sp_enum.add_argument("mnemonic", help="Instruction mnemonic (e.g., BA, PRA, RF).")
    sp_enum.add_argument(
        "--print-all",
        action="store_true",
        help="For print mnemonics, enumerate PRA/PRD/PRO variants instead of just provided mnemonic.",
    )
    sp_enum.add_argument(
        "--sample",
        type=int,
        default=None,
        help="Only show the first N encodings (useful for large sets).",
    )
    sp_enum.set_defaults(func=cmd_enumerate)

    # list
    sp_list = sub.add_parser("list", help="List all known instruction mnemonics grouped by type.")
    sp_list.set_defaults(func=cmd_list)

    # collisions
    sp_coll = sub.add_parser(
        "collisions",
        help="Show print mnemonic collisions for a given word (PRA/PRD/PRO shared space).",
    )
    sp_coll.add_argument("word", help="Word to check (same parsing rules as decode).")
    sp_coll.set_defaults(func=cmd_collisions)

    # disassemble (stream)
    sp_dis = sub.add_parser(
        "disassemble",
        help="Disassemble a stream of 12-bit words from stdin (one per line; supports 0o/0x/0b prefixes).",
    )
    sp_dis.add_argument(
        "--max",
        type=int,
        default=None,
        help="Maximum number of words to read from stdin (default: unlimited until EOF).",
    )
    sp_dis.add_argument(
        "--skip-invalid",
        action="store_true",
        help="Skip invalid lines instead of stopping with an error.",
    )
    sp_dis.add_argument(
        "--show-binary",
        action="store_true",
        help="Include 12-bit binary column in output.",
    )
    sp_dis.set_defaults(func=cmd_disassemble)

    return p


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def disassemble_stream(
    lines: Sequence[str],
    *,
    skip_invalid: bool = False,
) -> list[tuple[int, dict]]:
    """
    Disassemble a sequence of textual word representations into decoded info objects.

    Each line may be:
        - Octal with 0o prefix or raw octal (up to 4 digits)
        - Hex with 0x prefix
        - Binary with 0b prefix
        - Decimal (fallback)

    Returns list of tuples: (word_int, decode_info_dict).
    """
    results: list[tuple[int, dict]] = []
    for raw in lines:
        text = raw.strip()
        if not text:
            continue
        try:
            value = parse_int(text)
            info = decode_instruction(value, OPCODES)
            results.append((value, info))
        except Exception:
            if skip_invalid:
                continue
            raise
    return results


def cmd_disassemble(args: argparse.Namespace) -> int:
    # Read from stdin
    data_lines = []
    count = 0
    for line in sys.stdin:
        if args.max is not None and count >= args.max:
            break
        data_lines.append(line)
        count += 1

    try:
        decoded = disassemble_stream(
            data_lines,
            skip_invalid=args.skip_invalid,
        )
    except Exception as exc:
        print(f"ERROR: Disassembly aborted: {exc}", file=sys.stderr)
        return 1

    if not decoded:
        print("No words decoded.")
        return 0

    # Header
    hdr_cols = ["OCTAL", "MNEMONICS", "FIELDS"]
    if args.show_binary:
        hdr_cols.insert(1, "BINARY")
    print(" | ".join(hdr_cols))
    print("-" * (sum(len(c) for c in hdr_cols) + 3 * (len(hdr_cols) - 1)))

    for word, info in decoded:
        octal = fmt_octal(word)
        mns = ",".join(info["mnemonics"]) or "-"
        fields_str = ",".join(f"{k}={v}" for k, v in info["fields"].items()) or "-"
        if args.show_binary:
            binary = fmt_binary(word)
            print(f"{octal} | {binary} | {mns} | {fields_str}")
        else:
            print(f"{octal} | {mns} | {fields_str}")

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "EncodedVariant",
    "build_parser",
    "decode_instruction",
    "disassemble_stream",
    "enumerate_encodings",
    "fmt_binary",
    "fmt_hex",
    "fmt_octal",
    "main",
    "parse_int",
]
