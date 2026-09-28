"""Tests pour primitives/validation/tool_schema_validator.py."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from primitives.validation.tool_schema_validator import (
    ToolSchemaValidationResult,
    tool_schema_validator,
)


def test_valid_tool_list():
    tools = [
        {"name": "edit", "parameters": {"filePath": "x", "oldString": "a", "newString": "b"}},
        {"name": "write", "parameters": {"filePath": "y", "content": "z"}},
    ]
    result = tool_schema_validator(tools)
    assert isinstance(result, ToolSchemaValidationResult)
    assert result.valid is True
    assert result.valid_count == 2
    assert result.invalid_count == 0
    assert result.errors == []


def test_schema_enforcement_catches_missing_required():
    tools = [
        {"name": "edit", "parameters": {"filePath": "x"}},
    ]
    schema = {
        "required": ["filePath", "oldString", "newString"],
        "properties": {
            "filePath": {"type": "string"},
            "oldString": {"type": "string"},
            "newString": {"type": "string"},
        },
    }
    result = tool_schema_validator(tools, schema)
    assert result.valid is False
    assert result.invalid_count == 1
    assert any("missing required parameter" in err for err in result.errors)


def test_type_mismatch_detection():
    tools = [
        {"name": "write", "parameters": {"filePath": 123, "content": "z"}},
    ]
    schema = {
        "required": ["filePath", "content"],
        "properties": {
            "filePath": {"type": "string"},
            "content": {"type": "string"},
        },
    }
    result = tool_schema_validator(tools, schema)
    assert result.invalid_count == 1
    assert any("expected string, got int" in err for err in result.errors)
