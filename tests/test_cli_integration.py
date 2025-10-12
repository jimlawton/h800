"""
Integration tests for the h800 CLI utilities.

These tests exercise the public CLI entry points (decode, enumerate, list, collisions)
and the opcode markdown generator to ensure end-to-end behavior without relying on
facade instruction classes.

All tests call the underlying Python functions directly (not spawning subprocesses)
to keep them fast and deterministic. Output is captured via pytest's `capsys`.
"""

from __future__ import annotations

import io
import re

from h800.cli import main as cli_main
from h800.gen_opcodes_md import main as gen_opcodes_main


def run_cli(args: list[str]) -> int:
    """
    Helper to invoke the CLI main with an argument list and return the exit code.
    """
    return cli_main(args)


# -----------------------------------------------------------------------------
# Decode command tests
# -----------------------------------------------------------------------------


def test_cli_decode_masked_ba(capsys):
    # BA masked, sequence=1, mask=5
    # Encoding formula (masked): (0o4000 * s) + (0o100 * mask) + (0o40 * b7) + op
    # BA: b7=1, op=0o11 -> 0o4000 + 0o500 + 0o40 + 0o11 = 0o4551
    code = "0o4551"
    rc = run_cli(["decode", code])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Word: 0o4551" in out
    assert "BA" in out  # Candidate mnemonic present
    # Ensure fields include sequence and mask
    assert re.search(r"Fields: .*sequence=1.*mask=5", out) is not None


def test_cli_decode_unmasked_ba(capsys):
    # BA unmasked example: sequence=0, a=1,b=0,c=1
    # Unmasked: (0o4000*s)+(0o1000*b23)+(0o400*a)+(0o200*b)+(0o100*c)+op
    # BA b23=0b10=2 -> 0o4000*0 + 0o1000*2 + 0o400*1 + 0o200*0 + 0o100*1 + 0o11
    # 0o2000 + 0o400 + 0o100 + 0o11 = 0o2511
    rc = run_cli(["decode", "0o2511"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "BA" in out
    assert "mask" not in out  # Unmasked form should show operand flags instead
    assert re.search(r"Fields: .*sequence=0.*a=1.*c=1", out) is not None


def test_cli_decode_peripheral_rf(capsys):
    # RF peripheral word paddr=0: (0o100 * paddr) + (0o40 * b7) + op
    # RF b7=1 op=0o32 -> 0o0 + 0o40 + 0o32 = 0o72
    rc = run_cli(["decode", "0o72"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "RF" in out
    assert re.search(r"Fields: .*paddr=0", out) is not None


def test_cli_decode_print_collision(capsys):
    # PRA sequence=1 a=1 b=0 c=1 -> 0o4000 + 0o400 + 0o100 + 0o40 + 0o06 = 0o4546
    rc = run_cli(["decode", "0o4546"])
    assert rc == 0
    out = capsys.readouterr().out
    # All three print mnemonics should appear
    assert "PRA" in out and "PRD" in out and "PRO" in out
    assert re.search(r"Fields: .*sequence=1.*a=1.*c=1", out) is not None


def test_cli_decode_simulator(capsys):
    # Simulator sequence=0 word = 0o0007
    rc = run_cli(["decode", "0o7"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "S" in out
    assert re.search(r"Fields: .*sequence=0", out) is not None


def test_cli_decode_invalid_word(capsys):
    # Outside 12-bit range -> error
    rc = run_cli(["decode", "0o10000"])
    assert rc == 1
    err_out = capsys.readouterr().out + capsys.readouterr().err
    assert "ERROR" in err_out


# -----------------------------------------------------------------------------
# Enumerate command tests
# -----------------------------------------------------------------------------


def test_cli_enumerate_maskable_sample_limit(capsys):
    rc = run_cli(["enumerate", "BA", "--sample", "3"])
    assert rc == 0
    out = capsys.readouterr().out
    # Header
    assert "Enumerated" in out
    # Should list exactly 3 variants after header
    variant_lines = [line for line in out.splitlines() if re.match(r"\s*0o[0-7]{4}\s", line)]
    assert len(variant_lines) == 3


def test_cli_enumerate_print_all(capsys):
    rc = run_cli(["enumerate", "PRA", "--print-all", "--sample", "4"])
    assert rc == 0
    out = capsys.readouterr().out
    # Ensure multiple mnemonics appear in sample (since print-all replicates)
    assert any("PRD" in line or "PRO" in line for line in out.splitlines())


def test_cli_enumerate_simulator(capsys):
    rc = run_cli(["enumerate", "S"])
    assert rc == 0
    out = capsys.readouterr().out
    variant_lines = [line for line in out.splitlines() if re.match(r"\s*0o[0-7]{4}\s", line)]
    assert len(variant_lines) == 2  # Only two sequence variants


def test_cli_enumerate_unknown(capsys):
    rc = run_cli(["enumerate", "ZZ"])
    assert rc == 1
    out = capsys.readouterr().out + capsys.readouterr().err
    assert "Unknown mnemonic" in out


# -----------------------------------------------------------------------------
# List command tests
# -----------------------------------------------------------------------------


def test_cli_list_contains_known_mnemonics(capsys):
    rc = run_cli(["list"])
    assert rc == 0
    out = capsys.readouterr().out
    # Check presence of at least one mnemonic per key category
    assert "MASKABLE" in out  # Maskable group header
    assert "BA" in out
    assert "UNMASKED" in out
    assert "BM" in out
    assert "PERIPHERAL" in out
    assert "RF" in out
    assert "PRINT" in out
    assert "PRA" in out
    assert "SIMULATOR" in out
    assert "S" in out


# -----------------------------------------------------------------------------
# Collisions command tests
# -----------------------------------------------------------------------------


def test_cli_collisions_print_space(capsys):
    # PRA sample that collides (see earlier print example)
    rc = run_cli(["collisions", "0o4546"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Print collision space" in out
    assert all(m in out for m in ("PRA", "PRD", "PRO"))


def test_cli_collisions_no_collision(capsys):
    # BA masked word (0o4551) should not be in print collision space
    rc = run_cli(["collisions", "0o4551"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "No print collision" in out


# -----------------------------------------------------------------------------
# Opcode markdown generator tests
# -----------------------------------------------------------------------------


def test_gen_opcodes_md_default_output(tmp_path, capsys, monkeypatch):
    # Redirect output path to temporary directory
    out_file = tmp_path / "opcodes.md"
    monkeypatch.chdir(tmp_path)
    rc = gen_opcodes_main(["--output", str(out_file)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Wrote opcode summary" in out
    contents = out_file.read_text(encoding="utf-8")
    # Basic structural checks
    assert contents.startswith("# Honeywell H-800/H-1800 Opcode Summary")
    assert "| Mnemonic | Type" in contents
    assert "PRA, PRD, PRO share identical numeric opcode encodings" in contents
    # Sample section present by default
    assert "## Sample Encodings" in contents


def test_gen_opcodes_md_no_samples(tmp_path, capsys):
    out_file = tmp_path / "opcodes_no_samples.md"
    rc = gen_opcodes_main(
        ["--output", str(out_file), "--no-samples"]
    )  # No need for monkeypatch chdir; explicit path
    assert rc == 0
    contents = out_file.read_text(encoding="utf-8")
    assert "## Sample Encodings" not in contents
    assert "| Mnemonic | Type" in contents


def test_cli_disassemble_stream(monkeypatch, capsys):
    # Mixed set: masked BA, unmasked BA, peripheral RF, print collision, simulator S
    data = "0o4551\n0o2511\n0o72\n0o4546\n0o7\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(data))
    rc = run_cli(["disassemble", "--show-binary"])
    assert rc == 0
    out = capsys.readouterr().out
    # Header present
    assert "OCTAL" in out and "BINARY" in out
    # Check each word line emitted with expected mnemonics
    assert "0o4551" in out and "BA" in out
    assert "0o2511" in out and "BA" in out  # unmasked variant
    assert (
        "0o0072" not in out
    )  # formatting: expected 0o0072 becomes 0o0072 or 0o72 depending; ensure numeric is present
    assert "0o72" in out and "RF" in out
    # Print collision lists PRA/PRD/PRO
    assert "0o4546" in out and "PRA" in out and "PRD" in out and "PRO" in out
    # Simulator
    assert "0o0007" in out or "0o7" in out
    assert "S" in out


# -----------------------------------------------------------------------------
# End
# -----------------------------------------------------------------------------
