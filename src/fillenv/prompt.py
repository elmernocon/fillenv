# Copyright (c) 2025 Elmer Nocon
# SPDX-License-Identifier: MIT

from getpass import getpass
from typing import Iterable, List, Tuple

from .constants import SENSITIVE_HINTS


def should_mask(key: str) -> bool:
    """Return True if the key appears sensitive based on configured hints."""

    upper = key.upper()
    return any(hint in upper for hint in SENSITIVE_HINTS)


def prompt_for_values(entries: Iterable[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Prompt the user for values, showing defaults and masking when needed."""

    results: List[Tuple[str, str]] = []
    try:
        for key, default in entries:
            prompt = f"{key}"
            if default is not None and default != "":
                prompt += f" [{default}]"
            prompt += ": "
            if should_mask(key):
                user_input = getpass(prompt)
            else:
                try:
                    user_input = input(prompt)
                except EOFError:
                    user_input = ""
            value = default if user_input == "" else user_input
            results.append((key, value))
    except KeyboardInterrupt:
        return results
    return results
