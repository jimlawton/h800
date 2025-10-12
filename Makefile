# Top-level Makefile for the h800 project
#
# Provides unified developer workflow:
#   - Environment management (uv)
#   - Dependency locking / syncing
#   - Linting (ruff), formatting, type checking (mypy)
#   - Building distributions
#   - Running unit tests (core + tool CLI tests)
#   - Running tool scripts (generic entry point)
#   - Generating coverage reports
#
# Requirements:
#   - uv installed (https://github.com/astral-sh/uv)
#   - Python >= 3.13 (per pyproject.toml)
#
# Usage examples:
#   make            # default goal (help)
#   make sync       # install dependencies from uv.lock
#   make lock       # update uv.lock
#   make lint       # run ruff checks
#   make format     # apply ruff formatting
#   make typecheck  # run mypy
#   make test       # run all tests (unit + tool CLI)
#   make unit       # run only core unit tests (h800/h800/*_test.py)
#   make tool-tests # run CLI integration tests (tests/test_tools_cli.py)
#   make coverage   # run pytest with coverage
#   make build      # build wheel & sdist
#   make run-tool TOOL=parse.py ARGS="--strict examples/source.argus"
#
# Override variables:
#   make test PYTEST_ARGS="-k bitfield"
#   make run-tool TOOL=list-instructions.py ARGS="BA examples/source.argus"
#
# NOTE: All commands use 'uv run' to ensure the virtual environment context.

# --------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------
UV              ?= uv
PYTHON          ?= python
PROJECT_ROOT    := $(CURDIR)
TOOLS_DIR       := tools
UNIT_TEST_DIRS  := h800/h800 h800/tests
TOOL_TEST_FILE  := h800/tests/test_tools_cli.py
COVERAGE_PACKAGE := h800
PYTEST_ARGS     ?=

# Tool scripts (for validation / bulk operations)
TOOL_SCRIPTS := \
	check-instructions.py \
	check-symbols.py \
	find-symbols.py \
	list-symbols.py \
	list-instructions.py \
	parse.py \
	genlines.py \
	genpages.py \
	listing.py

# Default goal
.DEFAULT_GOAL := help

# Ensure make does not treat these names as files
.PHONY: help sync lock install develop build wheel sdist clean distclean \
        lint format typecheck test unit tool-tests coverage \
        run-tool tools-list tools-validate \
        upgrade deps list-instructions find-symbols parse \
        check-instructions check-symbols list-symbols \
        genlines genpages listing

# --------------------------------------------------------------------
# Help
# --------------------------------------------------------------------
help:
	@echo "h800 Make targets:"
	@echo "  build            - Build wheel+sdist (uv build)"
	@echo "  clean            - Remove build artifacts"
	@echo "  coverage         - Test with coverage report"
	@echo "  deps             - Alias for sync"
	@echo "  distclean        - Clean + remove .venv (CAUTION)"
	@echo "  format           - Ruff auto-format"
	@echo "  help             - Show this help message"
	@echo "  lint             - Ruff lint checks"
	@echo "  lock             - Resolve & update uv.lock (upgrade)"
	@echo "  run-tool         - Run a tool script (TOOL=<script> ARGS=\"...\")"
	@echo "  sync             - Install dependencies from uv.lock"
	@echo "  tools-list       - List available tool scripts"
	@echo "  tools-validate   - Basic help invocation for all tools"
	@echo "  typecheck        - Mypy static type checks"
	@echo "  test             - Run all tests (unit + tool CLI)"
	@echo "  upgrade          - lock + sync (full dependency update)"

# --------------------------------------------------------------------
# Dependency / environment management
# --------------------------------------------------------------------
sync deps:
	$(UV) sync

lock:
	$(UV) lock --upgrade

upgrade: lock sync

# Optional install target for editable install (not strictly needed with uv run)
install:
	$(UV) run pip install -e .

develop: install

# --------------------------------------------------------------------
# Linting / Formatting / Type Checking
# --------------------------------------------------------------------
lint:
	$(UV) run ruff check .

format:
	$(UV) run ruff format .

typecheck:
	$(UV) run mypy h800

# --------------------------------------------------------------------
# Testing
# --------------------------------------------------------------------
test:
	$(UV) run pytest $(PYTEST_ARGS)

coverage:
	$(UV) run pytest --cov=$(COVERAGE_PACKAGE) --cov-report=term-missing $(PYTEST_ARGS)

# --------------------------------------------------------------------
# Build artifacts
# --------------------------------------------------------------------
build: wheel sdist

wheel sdist:
	$(UV) build

# --------------------------------------------------------------------
# Tool script helpers
# --------------------------------------------------------------------
tools-list:
	@echo "Tool scripts:"
	@for s in $(TOOL_SCRIPTS); do echo "  $$s"; done

# Validate help for each tool (ensures argparse entry points don't crash)
tools-validate:
	@status=0; \
	for s in $(TOOL_SCRIPTS); do \
		echo "Validating $$s --help"; \
		$(UV) run $(PYTHON) $(TOOLS_DIR)/$$s --help >/dev/null 2>&1 || status=1; \
	done; \
	exit $$status

# Generic runner:
# Usage: make run-tool TOOL=parse.py ARGS="--strict samples/source.argus"
run-tool:
	@if [ -z "$(TOOL)" ]; then echo "ERROR: Specify TOOL=<script.py>"; exit 2; fi
	$(UV) run $(PYTHON) $(TOOLS_DIR)/$(TOOL) $(ARGS)

# Convenience aliases (invoke specific tools quickly)
check-instructions:
	$(UV) run $(PYTHON) $(TOOLS_DIR)/check-instructions.py $(ARGS)

check-symbols:
	$(UV) run $(PYTHON) $(TOOLS_DIR)/check-symbols.py $(ARGS)

find-symbols:
	$(UV) run $(PYTHON) $(TOOLS_DIR)/find-symbols.py $(ARGS)

list-symbols:
	$(UV) run $(PYTHON) $(TOOLS_DIR)/list-symbols.py $(ARGS)

list-instructions:
	$(UV) run $(PYTHON) $(TOOLS_DIR)/list-instructions.py $(ARGS)

parse:
	$(UV) run $(PYTHON) $(TOOLS_DIR)/parse.py $(ARGS)

genlines:
	$(UV) run $(PYTHON) $(TOOLS_DIR)/genlines.py $(ARGS)

genpages:
	$(UV) run $(PYTHON) $(TOOLS_DIR)/genpages.py $(ARGS)

listing:
	$(UV) run $(PYTHON) $(TOOLS_DIR)/listing.py $(ARGS)

# --------------------------------------------------------------------
# Cleaning
# --------------------------------------------------------------------
clean:
	@echo "Removing build artifacts..."
	rm -rf dist build *.egg-info

distclean: clean
	@echo "Removing virtual environment (CAUTION)..."
	rm -rf .venv

# --------------------------------------------------------------------
# Guard / sanity
# --------------------------------------------------------------------
# Ensure uv is available before running most targets
# (Skip for help to allow discovery)
ifeq ($(filter help,$(MAKECMDGOALS)),)
UV_CHECK := $(shell command -v $(UV) 2>/dev/null)
ifeq ($(UV_CHECK),)
$(error "uv not found in PATH. Install from https://astral.sh/uv/")
endif
endif

# End of Makefile
