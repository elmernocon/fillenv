# fillenv

Minimal Python project managed with `uv`.

## Setup

```bash
# Create and sync environment (uses uv.lock/pyproject.toml)
uv sync

# Run a Python REPL using the environment
uv run python -V
```

## Make commands

```bash
# Create and sync environment with dev/test extras
make setup

# Format code (ruff formatter)
make format

# Lint code (ruff lint)
make lint

# Run tests (pytest)
make test
```

## Usage

Fill variables from a template and write KEY=value lines to a file:

```bash
# Install from PyPI
pip install fillenv

# Use the installed CLI (writes to .env or .env1, .env2, ...)
fillenv .env.template
# Or rely on default template path (".env.template" in CWD)
fillenv

# Alternatively via python -m
uv run python -m fillenv .env.template
# Or rely on default template path (".env.template" in CWD)
uv run python -m fillenv

# Uses same write behavior (.env, or .env1, .env2, ...)
uv run python -m fillenv
```

You can also import and call `fillenv.cli.run(argv)` from Python code.

## Project layout

```
.
├── pyproject.toml
├── README.md
├── Makefile              # common tasks: setup, format, lint, test
├── src/
│   └── fillenv/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py        # entrypoint and command handling
│       ├── constants.py  # shared constants
│       ├── parser.py     # parse template into variables and prompts
│       ├── prompt.py     # interactive prompting utilities
│       └── serialize.py  # serialize variables to KEY=value lines
└── tests/...
```

## Releasing

Update the version in `pyproject.toml`.

Create a build and upload to PyPI:

```bash
# Build (requires uv)
uv build

# Upload (requires twine and a configured token)
twine upload dist/*
```

Issues and releases:

- Issues: https://github.com/elmernocon/fillenv/issues
- Releases/Changelog: https://github.com/elmernocon/fillenv/releases
