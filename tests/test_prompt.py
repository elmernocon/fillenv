# Copyright (c) 2025 Elmer Nocon
# SPDX-License-Identifier: MIT

import builtins

from fillenv.prompt import prompt_for_values, should_mask


def test_should_mask_from_hints():
    assert should_mask("api_key") is True
    assert should_mask("PASSWORD") is True
    assert should_mask("user_secret_id") is True
    assert should_mask("access_token") is True
    assert should_mask("username") is False


def test_prompt_for_values_uses_defaults_and_user_input(monkeypatch):
    # First prompt returns empty -> uses default; second returns custom
    inputs = iter(["", "custom"])

    def fake_input(prompt: str) -> str:
        return next(inputs)

    monkeypatch.setattr(builtins, "input", fake_input)
    entries = [("NAME", "default"), ("CITY", "")]  # CITY empty default
    result = prompt_for_values(entries)
    assert result == [("NAME", "default"), ("CITY", "custom")]


def test_prompt_for_values_masks_sensitive(monkeypatch):
    from getpass import getpass as real_getpass

    def fake_getpass(prompt: str) -> str:
        return "maskedval"

    monkeypatch.setattr("fillenv.prompt.getpass", fake_getpass)
    entries = [("DB_PASSWORD", "")]
    out = prompt_for_values(entries)
    assert out == [("DB_PASSWORD", "maskedval")]

    # Restore (pytest will undo via monkeypatch anyway) to avoid linter complaints
    _ = real_getpass


def test_prompt_for_values_eoferror_treated_as_empty(monkeypatch):
    def raising_input(prompt: str) -> str:
        raise EOFError

    monkeypatch.setattr(builtins, "input", raising_input)
    entries = [("CITY", "default")]
    assert prompt_for_values(entries) == [("CITY", "default")]


def test_prompt_for_values_keyboard_interrupt_returns_partial(monkeypatch):
    calls = {"count": 0}

    def maybe_interrupt(prompt: str) -> str:
        calls["count"] += 1
        if calls["count"] == 2:
            raise KeyboardInterrupt
        return "first"

    monkeypatch.setattr(builtins, "input", maybe_interrupt)
    entries = [("NAME", ""), ("CITY", ""), ("COUNTRY", "")]
    out = prompt_for_values(entries)
    # Should contain only the first answered value
    assert out == [("NAME", "first")]
