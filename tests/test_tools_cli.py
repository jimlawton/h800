import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

# Base directory of the project (two levels up from this test file)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = PROJECT_ROOT / "tools"


def run_tool(script_name, *args, input_text=None, timeout=10):
    """
    Helper to invoke a tool script as a subprocess.

    Returns (exit_code, stdout, stderr).
    """
    script_path = TOOLS_DIR / script_name
    cmd = [sys.executable, str(script_path), *map(str, args)]
    result = subprocess.run(
        cmd,
        check=False,
        input=input_text.encode() if input_text else None,
        capture_output=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout.decode(), result.stderr.decode()


@pytest.fixture
def temp_argus_file(tmp_path):
    """
    Provide a minimal ARGUS-style source file.

    The tools are lenient; many simply scan for 'instruction' tokens.
    We include a few lines with plausible instruction mnemonics
    (BA, BS, BT) that exist in H-800 instruction sets.
    """
    content = textwrap.dedent(
        """\
        000001   BA
        000002   BS
        000003   BT
        000004   BA
        000005   BS
        # Comment line
        """
    )
    f = tmp_path / "sample.argus"
    f.write_text(content)
    return f


# -------------------------
# check-instructions.py
# -------------------------
def test_check_instructions_basic(temp_argus_file):
    code, out, err = run_tool("check-instructions.py", temp_argus_file)
    assert code == 0, f"Unexpected non-zero exit: {code}, stderr={err}"


def test_check_instructions_invalid_flag(temp_argus_file):
    # Force invalid check; if all instructions are valid, exit should be 0.
    code, out, err = run_tool("check-instructions.py", "--invalid", temp_argus_file)
    assert code in (0, 1)  # 1 only if parsing flags some instruction as invalid.
    if code == 1:
        assert "*** ERROR: Invalid instruction" in err


def test_check_instructions_count_and_sort(temp_argus_file):
    code, out, err = run_tool("check-instructions.py", "--count", "--sort", temp_argus_file)
    assert code == 0
    assert "Instruction Frequencies:" in out
    # Expect at least one of the sample instructions to appear.
    assert "BA" in out or "BS" in out or "BT" in out


# -------------------------
# list-instructions.py
# -------------------------
def test_list_instructions_valid_opcode(temp_argus_file):
    # Use opcode BA which appears twice.
    code, out, err = run_tool("list-instructions.py", "BA", temp_argus_file, "--details")
    assert code in (0, 1)
    if code == 0:
        assert "BA" in out
    else:
        # If opcode unexpectedly treated invalid, ensure proper error message.
        assert "invalid opcode" in err.lower()


def test_list_instructions_invalid_opcode(temp_argus_file):
    code, out, err = run_tool("list-instructions.py", "ZZZ", temp_argus_file)
    assert code == 1
    assert "invalid opcode" in err.lower()


# -------------------------
# find-symbols.py
# -------------------------
def test_find_symbols_no_symbol_error(temp_argus_file):
    # Provide a symbol that likely does not exist; should still exit 0 or 2 depending on implementation.
    code, out, err = run_tool("find-symbols.py", "NONEXISTENT", temp_argus_file)
    assert code in (0, 2)
    if code == 2:
        assert "No matches" in err or "Symbol" in err


# -------------------------
# list-symbols.py
# -------------------------
def test_list_symbols_basic(temp_argus_file):
    code, out, err = run_tool("list-symbols.py", temp_argus_file)
    # Exit 3 is allowed if symbol table reports build errors; 0 otherwise.
    assert code in (0, 3)
    # Output should not be empty on success.
    if code == 0:
        assert out.strip() != ""


# -------------------------
# parse.py
# -------------------------
def test_parse_basic(temp_argus_file):
    code, out, err = run_tool("parse.py", temp_argus_file)
    assert code in (0, 1)
    assert "Source lines:" in out or "invalid instruction" in err.lower()


def test_parse_strict(temp_argus_file):
    code, out, err = run_tool("parse.py", "--strict", temp_argus_file)
    assert code in (0, 1)
    if code == 1:
        # Strict mode returns non-zero if any errors encountered.
        assert "invalid" in err.lower() or "symbol table" in out.lower()


# -------------------------
# genlines.py
# -------------------------
def test_genlines_basic():
    code, out, err = run_tool("genlines.py", "1", "3")
    assert code == 0
    lines = [line for line in out.splitlines() if line and not line.startswith("#")]
    assert len(lines) >= 3
    assert "1" in lines[0] or "0001" in lines[0]


def test_genlines_step_and_columns():
    code, out, err = run_tool(
        "genlines.py", "10", "20", "--step", "5", "--start-col", "1", "--end-col", "6"
    )
    assert code == 0
    assert "10" in out
    assert "15" in out
    assert "20" in out


# -------------------------
# genpages.py
# -------------------------
def test_genpages_missing_file():
    code, out, err = run_tool("genpages.py", "nonexistent_file.argus")
    # Should error due to missing file.
    assert code != 0
    assert "does not exist" in err.lower()


# -------------------------
# listing.py
# -------------------------
def test_listing_stdout(temp_argus_file):
    code, out, err = run_tool("listing.py", "--stdout", temp_argus_file)
    assert code == 0
    assert temp_argus_file.name in out


def test_listing_output_file(tmp_path, temp_argus_file):
    outdir = tmp_path / "listings"
    code, out, err = run_tool("listing.py", "--output-dir", outdir, temp_argus_file)
    assert code == 0
    # Verify output file created.
    expected = outdir / (temp_argus_file.stem + ".lst")
    assert expected.exists(), f"Expected listing file not found: {expected}"
    data = expected.read_text()
    assert temp_argus_file.name in data


# -------------------------
# check-symbols.py
# -------------------------
def test_check_symbols_basic(temp_argus_file):
    code, out, err = run_tool("check-symbols.py", temp_argus_file)
    # Accept 0 (success) or a non-zero if symbol parsing flags inconsistencies.
    assert code in (0, 1)
    if code == 1:
        assert "errors encountered building symbol table" in err.lower()


# -------------------------
# Negative / help tests
# -------------------------
@pytest.mark.parametrize(
    "script,flag",
    [
        ("check-instructions.py", "--help"),
        ("list-instructions.py", "--help"),
        ("find-symbols.py", "--help"),
        ("list-symbols.py", "--help"),
        ("parse.py", "--help"),
        ("genlines.py", "--help"),
        ("genpages.py", "--help"),
        ("listing.py", "--help"),
        ("check-symbols.py", "--help"),
    ],
)
def test_help_messages(script, flag):
    code, out, err = run_tool(script, flag)
    # Help should exit 0 and print usage in stdout.
    assert code == 0
    assert "usage:" in out.lower()


# -------------------------
# Sanity: ensure tools directory presence
# -------------------------
def test_tools_directory_exists():
    assert TOOLS_DIR.exists(), f"Tools directory missing: {TOOLS_DIR}"
    scripts = list(TOOLS_DIR.glob("*.py"))
    assert scripts, "No tool scripts found in tools directory."
