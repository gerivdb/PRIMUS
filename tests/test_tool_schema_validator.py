#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from primitives.validation import tool_schema_validator, ToolSchemaValidationResult


def test_valid_tools():
    tools = [
        {"id": "tool-1", "status": "STABLE", "path": "src/tools/a.py"},
        {"id": "tool-2", "status": "DRAFT", "path": "src/tools/b.py"},
    ]
    result = tool_schema_validator(tools)
    assert result.valid is True
    assert result.valid_count == 2
    assert result.invalid_count == 0


def test_missing_fields():
    tools = [
        {"id": "tool-1", "status": "STABLE"},  # path missing
        {"path": "src/tools/b.py"},  # id and status missing
    ]
    result = tool_schema_validator(tools)
    assert result.valid is False
    assert result.invalid_count == 2
    assert result.error_count == 2


def test_non_dict_tool():
    tools = ["not-a-dict", {"id": "tool-1", "status": "STABLE", "path": "src/tools/a.py"}]
    result = tool_schema_validator(tools)
    assert result.valid is False
    assert result.invalid_count == 1
    assert result.valid_count == 1


def test_empty_list():
    result = tool_schema_validator([])
    assert result.valid is True
    assert result.valid_count == 0
    assert result.invalid_count == 0


if __name__ == "__main__":
    test_valid_tools()
    test_missing_fields()
    test_non_dict_tool()
    test_empty_list()
    print("OK: All tool_schema_validator tests passed")
