# Copyright (c) 2025 Elmer Nocon
# SPDX-License-Identifier: MIT

from fillenv.parser import (
    is_comment_or_blank,
    parse_template_lines,
    split_key_value,
    strip_inline_comment_outside_quotes,
    strip_leading_export,
    unquote,
)


def test_is_comment_or_blank():
    assert is_comment_or_blank("") is True
    assert is_comment_or_blank("   ") is True
    assert is_comment_or_blank("# comment") is True
    assert is_comment_or_blank("   ; also comment") is True
    assert is_comment_or_blank("KEY=VAL") is False


def test_strip_leading_export():
    assert strip_leading_export("export KEY=VAL") == "KEY=VAL"
    assert strip_leading_export("  export KEY=VAL") == "  KEY=VAL"
    assert strip_leading_export("notexport KEY=VAL") == "notexport KEY=VAL"


def test_strip_inline_comment_outside_quotes():
    assert strip_inline_comment_outside_quotes("KEY=VAL # comment") == "KEY=VAL"
    assert strip_inline_comment_outside_quotes("KEY=VAL ; comment") == "KEY=VAL"
    # Inside double quotes should keep the hash
    assert (
        strip_inline_comment_outside_quotes('KEY="va l#ue" # tail') == 'KEY="va l#ue"'
    )
    # Inside single quotes should keep the semicolon
    assert strip_inline_comment_outside_quotes("KEY='va;lue' ; tail") == "KEY='va;lue'"
    # Escapes should be respected
    assert (
        strip_inline_comment_outside_quotes('KEY="say \\"#hi\\"" # tail')
        == 'KEY="say \\"#hi\\""'
    )


def test_split_key_value():
    assert split_key_value("KEY=VAL") == ("KEY", "VAL")
    assert split_key_value("KEY:VAL") == ("KEY", "VAL")
    # First unquoted '=' used
    assert split_key_value('KEY="A=B"=X') == ("KEY", '"A=B"=X')
    # Unquoted '=' inside quotes ignored
    assert split_key_value('KEY="A=B"') == ("KEY", '"A=B"')
    # No separator
    assert split_key_value("NOVAL") == (None, None)


def test_unquote_and_escapes():
    assert unquote('"value"') == "value"
    assert unquote("'value'") == "value"
    # Escapes inside double quotes
    assert unquote('"he said \\"hi\\""') == 'he said "hi"'
    # No surrounding quotes
    assert unquote("plain") == "plain"


def test_parse_template_lines_end_to_end():
    lines = [
        "# comment\n",
        "; also comment\n",
        "export KEY1=value1 # trailing\n",
        'KEY2="va l#ue" # trailing\n',
        "KEY3: 'abc'\n",
        "INVALID LINE WITHOUT SEP\n",
        "BAD KEY = value\n",  # whitespace in key -> ignored
        "   \n",
    ]
    entries = parse_template_lines(lines)
    assert entries == [
        ("KEY1", "value1"),
        ("KEY2", "va l#ue"),
        ("KEY3", "abc"),
    ]
