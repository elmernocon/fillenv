# Copyright (c) 2025 Elmer Nocon
# SPDX-License-Identifier: MIT

.PHONY: setup test lint format check

setup:
	uv sync --extra dev --extra test

format:
	uv run ruff format .

lint:
	uv run ruff check .

test:
	uv run pytest -q

build:
	uv build

publish:
	uv run twine upload --non-interactive dist/*
