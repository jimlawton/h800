#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
list-symbols.py

Generate a listing of symbols found in one or more ARGUS assembly source files.

The symbol table structure (from h800.symbol_table.buildSymbolTable) looks like:
    symtab[symbol][segment][subsegment][symtype] = {
        "file": <filename>,
        "line": <line number>,
        "lognum": <log number or None>,
        "tagtype": <tag prefix letter or ' '>,
        "card": <Card object with .line etc.>
    }

Output (text mode) groups each symbol with its segment / subsegment / assignment
types (simple/complex) and shows a condensed view of the source card line.

Features added in this rewrite:
  - Argparse-based CLI (Python 3+ only).
  - Optional filtering for specific symbols (exact names).
  - Optional JSON output for downstream tooling.
  - Verbose reporting of per-file symbol table build errors.
  - Clean exit codes:
        0 - Success
        1 - Invalid arguments / usage error
        2 - No symbols found after filtering
        3 - Errors encountered while building symbol table

Examples:
    list-symbols.py file1.argus
    list-symbols.py -v file1.argus file2.argus
    list-symbols.py --symbols FOO,BAR file1.argus
    list-symbols.py --json file1.argus

"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, Iterable, List, Sequence, Tuple

from h800.symbol_table import buildSymbolTable


def build_combined_symbol_table(
    filenames: Sequence[str], verbose: bool
) -> Tuple[Dict[str, Any], int]:
    """
    Build a combined symbol table from all input filenames.

    Returns (symtab, total_errors).
    """
    symtab: Dict[str, Any] = {}
    total_errors = 0
    for filename in filenames:
        symtab, file_errors = buildSymbolTable(filename, symtab, verbose=verbose)
        total_errors += file_errors
        if verbose:
            print(
                f"{filename}: {file_errors} errors encountered building symbol table.",
                file=sys.stderr,
            )
    if verbose and total_errors:
        print(f"Total symbol table build errors: {total_errors}", file=sys.stderr)
    return symtab, total_errors


def filter_symbols(symtab: Dict[str, Any], names: Iterable[str]) -> Dict[str, Any]:
    """
    Return a new symbol table containing only the symbols named in 'names'.
    Symbols not present are ignored (warned to stderr).
    """
    wanted = set(n for n in names if n)
    if not wanted:
        return symtab
    filtered: Dict[str, Any] = {}
    for name in wanted:
        if name in symtab:
            filtered[name] = symtab[name]
        else:
            print(f"Warning: requested symbol '{name}' not found.", file=sys.stderr)
    return filtered


def symbol_table_to_json(symtab: Dict[str, Any]) -> str:
    """
    Convert the symbol table to a JSON string. The Card objects are reduced to line text.
    """
    json_ready: Dict[str, Any] = {}
    for sym, segs in symtab.items():
        json_ready[sym] = {}
        for seg, subseg_map in segs.items():
            json_ready[sym][seg] = {}
            for subseg, type_map in subseg_map.items():
                json_ready[sym][seg][subseg] = {}
                for symtype, entry in type_map.items():
                    json_ready[sym][seg][subseg][symtype] = {
                        key: (
                            entry[key].line.strip()
                            if key == "card" and hasattr(entry[key], "line")
                            else entry[key]
                        )
                        for key in entry.keys()
                        if key != "card" or hasattr(entry[key], "line")
                    }
    return json.dumps(json_ready, indent=2, sort_keys=True)


def format_symbol_entry(sym: str, entry: Dict[str, Any]) -> str:
    """
    Produce human-readable text for one symbol's definitions.
    """
    lines: List[str] = [sym]
    for seg in sorted(entry.keys()):
        lines.append(f"  Segment: {seg}")
        for subseg in sorted(entry[seg].keys()):
            lines.append(f"    Subsegment: {subseg}")
            for symtype in sorted(entry[seg][subseg].keys()):
                symdata = entry[seg][subseg][symtype]
                file_base = symdata["file"].split(".")[0]
                line_no = symdata["line"]
                tagtype = symdata.get("tagtype", " ")
                card_obj = symdata.get("card")
                card_line = ""
                if card_obj and hasattr(card_obj, "line"):
                    card_line = card_obj.line.strip()
                lines.append(
                    f"      <{symtype:7s}> {tagtype or ' '} {file_base}:{line_no:<5d}  {card_line}"
                )
    return "\n".join(lines)


def output_text(symtab: Dict[str, Any]) -> None:
    """
    Print the symbol table in text form.
    """
    for sym in sorted(symtab.keys()):
        print(format_symbol_entry(sym, symtab[sym]))
        print()  # Blank line between symbols


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="list-symbols",
        description="List symbols (and their definitions) from ARGUS assembly source files.",
    )
    parser.add_argument(
        "filenames",
        metavar="filename",
        nargs="+",
        help="ARGUS assembly source file(s) to process.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output (shows per-file build errors).",
    )
    parser.add_argument(
        "-s",
        "--symbols",
        metavar="SYMLIST",
        help="Comma-separated list of symbol names to display (exact matches).",
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="Output symbol table as JSON instead of text.",
    )
    return parser.parse_args(list(argv))


def main(argv: Sequence[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    args = parse_args(argv)

    symtab, total_errors = build_combined_symbol_table(
        args.filenames, verbose=args.verbose
    )

    if args.symbols:
        requested = [s.strip() for s in args.symbols.split(",")]
        symtab = filter_symbols(symtab, requested)

    if not symtab:
        print("No symbols found.", file=sys.stderr)
        return 2

    if args.json:
        print(symbol_table_to_json(symtab))
    else:
        output_text(symtab)

    # If there were build errors, return non-zero (but still produced output).
    if total_errors:
        return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
