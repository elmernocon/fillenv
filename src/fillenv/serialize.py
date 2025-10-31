# Copyright (c) 2025 Elmer Nocon
# SPDX-License-Identifier: MIT


def needs_quotes(value: str) -> bool:
    """Return True if the value should be double-quoted when serialized."""

    if value == "":
        return False
    if value != value.strip():
        return True
    for ch in (" ", "#", ";"):
        if ch in value:
            return True
    return False


def serialize_value(value: str) -> str:
    """Serialize a value, escaping when double quotes are required."""

    if needs_quotes(value):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return value
