"""Tests pour primitives/logic/extract_json.py."""

from __future__ import annotations

import pytest

from primitives.logic.extract_json import extract_json


def test_extracts_plain_json():
    assert extract_json('{"a": 1}') == {"a": 1}


def test_extracts_json_from_markdown_block():
    text = "```json\n{\"a\": 1}\n```"
    assert extract_json(text) == {"a": 1}


def test_raises_on_missing_object():
    with pytest.raises(SyntaxError):
        extract_json("no json here")
