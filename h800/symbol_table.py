import sys

from rapidfuzz import process

from h800.arguscard import Deck

TAG_PREFIXES = ("B", "F", "L", "S", "X", "Z")


class SymbolTableEntry:
    def __init__(
        self,
        name,
        value=None,
        symtype=None,
        file=None,
        line=0,
        segment=None,
        subsegment=None,
    ):
        self._name = name  # Symbol name
        self._absoluteValue = self._complexValue = None
        self._symtype = symtype  # Type of record
        if symtype == "absolute":
            self._absoluteValue = value  # Absolute value
        else:
            self._complexValue = value  # Complex value
        self._file = file
        self._line = line
        self._segment = segment
        self._subsegment = subsegment
        self._references = []

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def references(self):
        return self._references

    @property
    def segment(self):
        return self._segment

    @property
    def subsegment(self):
        return self._subsegment

    @property
    def file(self):
        return self._file

    @property
    def line(self):
        return self._line

    def is_valid(self):
        return self._absoluteValue is not None or self._complexValue is not None

    def is_absolute(self):
        return self._absoluteValue is not None

    def is_complex(self):
        return self._complexValue is not None

    def is_multiple(self):
        return self.isAbsolute() and self.isComplex()

    def add_reference(self, ref):
        self._references.append(ref)


class SymbolTable:
    def __init__(self):
        self._symbols = {}
        self._undefs = []

    @property
    def symbols(self):
        return self._symbols

    @property
    def undefines(self):
        return self._undefs

    def add(
        self,
        name,
        srcfile,
        linenum,
        value=None,
        symtype=None,
        segment=None,
        subsegment=None,
    ):
        if name:
            if name in self._symbols:
                print(f'ERROR: Symbol "{name}" already defined!')
            else:
                self._symbols[name] = SymbolTableEntry(
                    name, value, symtype, srcfile, linenum, segment, subsegment
                )
                if value is None:
                    self._undefs.append(name)

    def update(self, name, value=None, symtype=None):
        if name:
            if name not in list(self._symbols.keys()):
                self.context.error(f'symbol "{name}" not defined!')
            else:
                entry = self._symbols[name]
                entry.value = value
                entry.type = symtype
                self._symbols[name] = entry

    def resolve(self, max_passes=10):
        n_prev_undefs = n_undefs = len(self._undefs)
        for i in range(max_passes):
            print(f"Symbol pass {i}: {n_undefs} undefined symbols")
            if n_undefs == 0:
                print("All symbols resolved!")
                break
            for symbol in self._undefs:
                print(f'Attempting to resolve symbol "{symbol}"')
                # TODO
            self.pruneUndefines()
            n_undefs = len(self._undefs)
            if n_undefs == n_prev_undefs:
                print(f"ERROR: No progress resolving symbols, {n_undefs} undefined symbols")
                break
            n_prev_undefs = n_undefs

    def prune_undefines(self):
        # Prune the undefs list.
        num_undefs = len(self._undefs)
        print(f"Pruning undefined symbols list ({num_undefs} undefs)")
        for i, symbol in enumerate(self._undefs):
            entry = self._symbols[symbol]
            if entry.isValid():
                print(f"Removing {symbol} from undefined symbols list")
                del self._undefs[i]
        print(f"Removed {num_undefs - len(self._undefs)} symbols from undef list")

    def get_num_symbols(self):
        return len(list(self._symbols.keys()))

    def get_num_undefs(self):
        return len(self._undefs)

    def lookup(self, name):
        entry = None
        if name in self._symbols:
            entry = self._symbols[name]
        return entry

    def print_table(self, outfile=None):
        if outfile is None:
            out = sys.stdout
        else:
            out = outfile
        symbols = list(self._symbols.keys())
        symbols.sort()
        print("\nDefined symbols:\n", file=out)
        for symbol in symbols:
            print(self._symbols[symbol], file=out)

        if len(self._undefs) > 0:
            print("\nUndefined symbols:\n", file=out)
            for symbol in self._undefs:
                print(self._symbols[symbol], file=out)

    def print_undefs(self, outfile=None):
        if outfile is None:
            out = sys.stdout
        else:
            out = outfile
        print(f"\nUndefined symbols: {len(self._undefs)}\n", file=out)
        for symbol in self._undefs:
            print(self._symbols[symbol], file=out)


def build_symbol_table(filename, symtab, verbose=False):
    """Build the symbol table."""
    seg = filename.split(".")[0]  # Default: name of the first file.
    subsegs = []  # List of subsegments.
    subseg = "1"  # Current subsegment, default is 1 (no starting SETLOC)
    d = Deck(file=filename, verbose=verbose)
    errcount = 0
    for card in d.cards:
        if card.column8 == "*":
            continue
        command = card.operation
        if command and command.startswith("SETLOC"):
            if "," in command:
                subseg = command.split(",")[1].strip()
            else:
                subseg = "0"
            subsegs.append(subseg)
            # print("Subsegment: %s" % subseg)
        if card.label:
            symtab_entry = {
                "file": card.filename,
                "line": card.linenum,
                "lognum": card.lognum,
                "tagtype": None,
                "card": card,
            }
            str_label = card.label.strip().replace(" ", "")
            if str_label.upper() != str_label:
                print(
                    f"*** ERROR: Symbol {str_label} is ill-formed (case)!",
                    file=sys.stderr,
                )
                print(f"Current definition: {symtab_entry}", file=sys.stderr)
                errcount += 1
                continue
            tag_name = str_label
            symtab_entry["tagtype"] = " "
            if "," in str_label:
                if str_label.count(",") > 1:
                    print(
                        f"*** ERROR: Symbol {str_label} is illegal, too many commas!",
                        file=sys.stderr,
                    )
                    print(f"Current definition: {symtab_entry}", file=sys.stderr)
                    errcount += 1
                    continue
                tag_prefix = str_label.split(",")[0]
                tag_name = str_label.split(",")[1]
                if tag_prefix not in TAG_PREFIXES:
                    print(
                        f"*** ERROR: Symbol {str_label} is ill-formed (tag prefix)!",
                        file=sys.stderr,
                    )
                    print(f"Current definition: {symtab_entry}", file=sys.stderr)
                    errcount += 1
                    continue
                if tag_prefix in ("L", "X"):
                    print(
                        f"*** ERROR: Symbol {str_label} has unsupported tag prefix!",
                        file=sys.stderr,
                    )
                    print(f"Current definition: {symtab_entry}", file=sys.stderr)
                    errcount += 1
                    continue
                symtab_entry["tagtype"] = tag_prefix
                if tag_prefix == "B":
                    # Mask tag for BOTH field and shift instructions.
                    pass
                elif tag_prefix == "F":
                    # Mask tag for field instructions only.
                    pass
                elif tag_prefix == "S":
                    # Mask tag for shift instructions only.
                    pass
                elif tag_prefix == "Z":
                    # Special register tag.
                    # TODO: check register tag symbolic name is valid, or
                    # absolute value is valid.
                    pass

            # Check the command code field. Depending on the command code
            # field operation, multiple declarations might be allowed,
            # e.g. RESERVE, EQUALS, ALF, SPEC, CAC, etc., all reserve
            # storage, but ASSIGN doesn't.
            if command is None:
                print(f"*** ERROR: Symbol {str_label} has no operation!", file=sys.stderr)
                print(f"Current definition: {symtab_entry}", file=sys.stderr)
                errcount += 1
                continue
            if command == "ASSIGN":
                symtype = "complex"
            else:
                symtype = "simple"
            if tag_name not in list(symtab.keys()):
                symtab[tag_name] = {}
                symtab[tag_name][seg] = {}
                symtab[tag_name][seg][subseg] = {}
                symtab[tag_name][seg][subseg][symtype] = symtab_entry
            elif seg not in symtab[tag_name].keys():
                symtab[tag_name][seg] = {}
                symtab[tag_name][seg][subseg] = {}
                symtab[tag_name][seg][subseg][symtype] = symtab_entry
            elif subseg not in symtab[tag_name][seg].keys():
                symtab[tag_name][seg][subseg] = {}
                symtab[tag_name][seg][subseg][symtype] = symtab_entry
            else:
                prevdef = symtab[tag_name]
                if symtype not in prevdef.keys():
                    symtab[tag_name][seg][subseg][symtype] = symtab_entry
                else:
                    if command == "EQUALS":
                        prevcard = prevdef[symtype]["card"]
                        if prevcard.operation == "EQUALS":
                            if (
                                card.addressa == prevcard.addressa
                                and card.addressb == prevcard.addressb
                                and card.addressc == prevcard.addressc
                            ):
                                # Equivalent assignment, ignore.
                                continue
                    print(
                        f"*** ERROR: Symbol {tag_name} is multiply-defined!",
                        file=sys.stderr,
                    )
                    print(
                        f"Previous definitions: {symtab[tag_name][seg][subseg]}",
                        file=sys.stderr,
                    )
                    print(f"Current definition: {symtab_entry}", file=sys.stderr)
                    print(f"command: {command}", file=sys.stderr)
                    errcount += 1
    return symtab, errcount


def check_symbol_table(symtab, verbose=False, complex_only_error=False):
    """Check the symbol table."""
    err_syms = []
    for symbol in sorted(symtab.keys()):
        found_simple = found_complex = False
        for seg in sorted(symtab[symbol].keys()):
            for subseg in sorted(symtab[symbol][seg].keys()):
                if "simple" in symtab[symbol][seg][subseg].keys():
                    found_simple = True
                if "complex" in symtab[symbol][seg][subseg].keys():
                    found_complex = True
        if not found_simple and (complex_only_error and found_complex):
            err_syms.append(symbol)
    for symbol in err_syms:
        print(
            f'ERROR: symbol "{symbol}" has a complex assignment, but no simple assignment!',
            file=sys.stderr,
        )
    return sorted(err_syms)


def get_absolute_symbols(symtab):
    """Return a list of the symbols that have absolute definitions."""
    syms = []
    found = False
    for symbol in sorted(symtab.keys()):
        for seg in sorted(symtab[symbol].keys()):
            for subseg in sorted(symtab[symbol][seg].keys()):
                if "simple" in symtab[symbol][seg][subseg].keys():
                    syms.append(symbol)
                    found = True
                    break
            if found:
                break
    return syms


def find_symbol_def(symtab, name, symtype=None, begin=False, end=False, fuzzy=False, verbose=False):
    """Find the definition location(s) of the specified symbol."""
    exact = not begin and not end and not fuzzy
    sym_names = sorted(symtab.keys())
    if exact:
        if name in sym_names:
            if symtype is None:
                return symtab[name]
            else:
                for seg in sorted(symtab[name].keys()):
                    for subseg in sorted(symtab[name][seg].keys()):
                        if symtype in symtab[name][seg][subseg].keys():
                            return symtab[name]
        print(f'ERROR: Undefined symbol "{name}"!', file=sys.stderr)
    else:
        matches = []
        if begin or end:
            for sym in sym_names:
                if begin and sym.startswith(name):
                    matches.append(sym)
                if end and sym.endswith(name):
                    matches.append(sym)
            return matches
        if fuzzy:
            # Try fuzzy finder.
            abs_syms = get_absolute_symbols(symtab)
            matches = process.extract(name, abs_syms, limit=10)
            if len(matches) > 0:
                match_list = []
                for match in matches:
                    match_list.append(match[0])
                return match_list
            else:
                return []
    return None


__all__ = [
    "TAG_PREFIXES",
    "SymbolTable",
    "SymbolTableEntry",
    "build_symbol_table",
    "check_symbol_table",
    "find_symbol_def",
]
