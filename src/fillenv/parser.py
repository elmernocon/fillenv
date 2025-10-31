# Copyright (c) 2025 Elmer Nocon
# SPDX-License-Identifier: MIT

from typing import Iterable, List, Tuple


def is_comment_or_blank(line: str) -> bool:
    """Return True if the line is blank or a comment.

    A comment starts with ``#`` or ``;`` after stripping leading whitespace.
    """

    stripped = line.strip()
    if not stripped:
        return True
    if stripped.startswith("#") or stripped.startswith(";"):
        return True
    return False


def strip_leading_export(s: str) -> str:
    """Remove an optional leading ``export `` token (as in shell env files)."""

    if s.lstrip().startswith("export "):
        leading_ws_len = len(s) - len(s.lstrip())
        return s[:leading_ws_len] + s.lstrip()[len("export ") :]
    return s


def strip_inline_comment_outside_quotes(s: str) -> str:
    """Strip trailing ``#`` or ``;`` comments when they occur outside quotes."""

    in_single = False
    in_double = False
    escaped = False
    for idx, ch in enumerate(s):
        if escaped:
            escaped = False
            continue
        if ch == "\\":
            escaped = True
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            continue
        if not in_single and not in_double and (ch == "#" or ch == ";"):
            return s[:idx].rstrip()
    return s.rstrip()


def split_key_value(s: str) -> tuple[str | None, str | None]:
    """Split a line into ``(key, value)`` on the first unquoted ``=`` or ``:``.

    Returns ``(None, None)`` when no separator is found.
    """

    in_single = False
    in_double = False
    escaped = False
    for idx, ch in enumerate(s):
        if escaped:
            escaped = False
            continue
        if ch == "\\":
            escaped = True
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            continue
        if not in_single and not in_double and (ch == "=" or ch == ":"):
            key = s[:idx].strip()
            val = s[idx + 1 :].strip()
            return key, val
    return None, None


def unquote(value: str) -> str:
    """Remove surrounding single or double quotes and unescape inside doubles."""

    if len(value) >= 2 and (
        (value[0] == '"' and value[-1] == '"') or (value[0] == "'" and value[-1] == "'")
    ):
        quote = value[0]
        inner = value[1:-1]
        if quote == '"':
            inner = inner.replace('\\"', '"').replace('\\\\', "\\")
        return inner
    return value


def parse_template_lines(lines: Iterable[str]) -> List[Tuple[str, str]]:
    """Parse template lines into a list of ``(key, default)`` pairs.

    Skips comments and blank lines, supports optional ``export `` prefix, and
    recognizes inline comments outside of quotes.
    """

    entries: List[Tuple[str, str]] = []
    for ln, raw in enumerate(lines, start=1):
        if is_comment_or_blank(raw):
            continue
        line = strip_leading_export(raw.rstrip("\n"))
        line = strip_inline_comment_outside_quotes(line)
        if not line.strip():
            continue
        key, val = split_key_value(line)
        if not key:
            continue
        if any(ch.isspace() for ch in key) or key == "":
            continue
        default = unquote(val if val is not None else "")
        entries.append((key, default))
    return entries
