# h800
Tools for the Honeywell H-800 and H-1800 mainframe family of computers. Initially I am working on a cross-assembler, but eventually I hope to build a simulator also.

The Honeywell H-800 (https://en.wikipedia.org/wiki/Honeywell_800) was a transistorized mainframe computer developed at the end of the 1950s. It was later followed by other more-powerful versions, the H-1800 and H-1800-II. 

The reason for my interest in the H-x800 family is that these were the machines that the original Apollo Guidance Computer (https://github.com/virtualagc/virtualagc) software was developed on at the MIT Instrumentation Lab (now Draper Labs). You can see the source code for the original "YUL" AGC cross-assembler, developed by Hugh Blair-Smith (https://www.amazon.com/Left-Brains-Right-Stuff-Computers-ebook/dp/B0192KEGUS/ref=la_B018FDP8MI_1_1?s=books&ie=UTF8&qid=1487895605&sr=1-1) at MIT/IL here: https://github.com/virtualagc/virtualagc/tree/master/YUL.

The H-x800s were 48-bit word-size machines (with an addiitonal 8 parity bits per word), and had a 3-address instruction format, and banked memory (2048 words per bank). They had 8 separate identical register banks, so that 8 programs could be run simultaneously (sort of: the ALU was multiplexed among the 8 banks). Each bank included a pair of program counters, and assembler syntax allowed instructions to specify which PC should be used for the next instruction. This is also the only architecture I've ever heard of that allowed PCs to count down as well as up.

The _H-1800 Programmers' Reference Manual_ has been transcribed to Markdown here:
https://github.com/jimlawton/h800/blob/master/docs/prm/Honeywell-1800-PRM.md

The _ARGUS Manual of Assembly Language_ has been transcribed to Markdown here:
https://github.com/jimlawton/h800/blob/master/docs/argus/ARGUS_Manual_of_Assembly_Language.md
(there are 2 pages missing in the original document scan)

## Caveats
 - No support for segments, only subsegments. YUL does not use segments. All
   code is assumed to be in the same segment.

## Installation and Development (uv)

This project now uses a modern `pyproject.toml` with the [uv](https://github.com/astral-sh/uv) Python package manager / resolver instead of Pipenv.

### 1. Install uv
On macOS/Linux:
curl -Ls https://astral.sh/uv/install.sh | sh

(See uv docs for other platforms.)

### 2. Create and activate a virtual environment
uv venv
source .venv/bin/activate

(uv will default to a Python it finds; specify one with `uv venv --python 3.11` if desired.)

### 3. Install dependencies
uv sync
This reads `pyproject.toml` and `uv.lock` (if present) and installs everything reproducibly.

### 4. Editable development
The package is included automatically (via setuptools). If you need explicit editable mode:
uv pip install -e .

### 5. Run tests
uv run pytest

### 6. Add or upgrade dependencies
Add a new runtime dependency:
uv add <package>

Add a dev-only dependency:
uv add --group dev <package>

Upgrade existing dependencies (respecting version constraints):
uv lock --upgrade
uv sync

### 7. Build a distribution
uv build
Artifacts will appear under `dist/`.

### 8. Run the assembler (example)
uv run python -c "import h800; print('h800 imported')"

Or if/when an entry point script is added you can:
uv run h800 ...

### Notes
- Dependency management migrated from Pipenv / requirements.txt to uv.
- To regenerate the lock file after changes: `uv lock` then `uv sync`.

## Modernization (Python 3.13 Upgrade)

The project has been bumped to require Python 3.13. The following cleanup / enhancement tasks align the codebase with modern Python best practices:

- Remove any lingering Python 2 compatibility imports (`from __future__ import print_function`) and legacy patterns.
- Replace use of `optparse` in tools with `argparse` (richer API, maintained).
- Audit encoding headers (e.g. `# -*- coding: iso-8859-15 -*-`); convert source to UTF-8 unless non-ASCII content requires otherwise.
- Add type hints progressively (start with public functions/classes) to improve maintainability.
- Consider introducing `ruff` (lint/format) and `mypy` (type checking) in the `dev` dependency group.
- Evaluate replacing `fuzzywuzzy` with `python-Levenshtein` or `rapidfuzz` directly for performance (if fuzzy matching is performance-critical).
- Ensure tests cover edge cases (banked registers, symbol resolution) and add property-based tests where appropriate.
- Add a CLI entry point via `[project.scripts]` in `pyproject.toml` (e.g. `h800-asm = h800.__main__:main`) if a command-line interface is desired.
- Consider adopting `dataclasses` for structured records (e.g. parser records, instruction representations) to reduce boilerplate.
- Replace any deprecated APIs and confirm all dependencies are at their latest compatible versions.
- Add continuous integration (GitHub Actions) using `uv sync --frozen` to enforce lockfile reproducibility.
- Optional: Introduce `pyproject.toml` tool sections (`[tool.coverage]`, `[tool.ruff]`, etc.) for centralized configuration.

These items can be tackled incrementally; none (except removing obsolete compatibility code) are strictly required for Python 3.13 functionality but will modernize the project overall.
- Runtime and development dependencies now declared under `[project]` and `[project.optional-dependencies]` in `pyproject.toml`.
- `uv.lock` provides a deterministic, reproducible lock; regenerate with `uv lock`.
- Common commands:
  - `uv venv` / `source .venv/bin/activate` to create & activate the environment.
  - `uv sync` to install according to the lock file.
  - `uv add <package>` or `uv add --group dev <package>` to add dependencies.
  - `uv lock --upgrade` followed by `uv sync` to update installed versions within constraints.
  - `uv run pytest` to execute tests.
