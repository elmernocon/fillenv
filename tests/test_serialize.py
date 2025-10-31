# Copyright (c) 2025 Elmer Nocon
# SPDX-License-Identifier: MIT

from fillenv.serialize import needs_quotes, serialize_value


def test_needs_quotes_rules():
    assert needs_quotes("") is False
    assert needs_quotes("simple") is False
    assert needs_quotes("with space") is True
    assert needs_quotes(" leading") is True
    assert needs_quotes("trailing ") is True
    assert needs_quotes("hash#tag") is True
    assert needs_quotes("semi;colon") is True


def test_serialize_value_with_quotes_and_escapes():
    # No quotes needed
    assert serialize_value("simple") == "simple"
    # Quotes and escapes for double quotes
    assert serialize_value('say "hi"') == '"say \\"hi\\""'
    # Backslashes are escaped
    assert serialize_value('path \\network') == '"path \\\\network"'
