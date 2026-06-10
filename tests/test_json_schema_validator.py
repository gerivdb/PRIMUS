#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from primitives.validation.json_schema_validator import json_schema_validator, ValidationResult


_TOOL_SCHEMA = {
    "type": "object",
    "required": ["id", "status", "path"],
    "properties": {
        "id": {"type": "string", "minLength": 1},
        "status": {"type": "string", "enum": ["SPIKE", "DRAFT", "STABLE", "DEPRECATED"]},
        "path": {"type": "string"},
        "primitives": {"type": "array", "items": {"type": "string"}},
    }
}


def test_valid_object():
    data = {"id": "dag-navigator", "status": "SPIKE", "path": "src/frontend/"}
    result = json_schema_validator(data, _TOOL_SCHEMA)
    assert result.valid is True
    assert result.error_count == 0
    assert bool(result) is True


def test_missing_required_field():
    data = {"id": "dag-navigator", "status": "SPIKE"}  # path manquant
    result = json_schema_validator(data, _TOOL_SCHEMA)
    assert result.valid is False
    assert result.error_count >= 1


def test_invalid_enum():
    data = {"id": "x", "status": "UNKNOWN", "path": "src/"}
    result = json_schema_validator(data, _TOOL_SCHEMA)
    assert result.valid is False
    assert any("enum" in e.message.lower() or "unknown" in e.message.lower() for e in result.errors)


def test_invalid_type():
    data = {"id": 42, "status": "DRAFT", "path": "src/"}  # id devrait être str
    result = json_schema_validator(data, _TOOL_SCHEMA)
    assert result.valid is False


def test_array_items_validation():
    schema = {"type": "array", "items": {"type": "string"}}
    assert json_schema_validator(["a", "b", "c"], schema).valid
    assert not json_schema_validator(["a", 2, "c"], schema).valid


def test_first_error():
    data = {"status": "DRAFT"}  # id et path manquants
    result = json_schema_validator(data, _TOOL_SCHEMA)
    assert result.first_error() is not None
    assert result.first_error().path.startswith("$")


def test_empty_schema_accepts_anything():
    result = json_schema_validator({"anything": True}, {})
    assert result.valid is True


if __name__ == "__main__":
    test_valid_object()
    test_missing_required_field()
    test_invalid_enum()
    test_invalid_type()
    test_array_items_validation()
    test_first_error()
    test_empty_schema_accepts_anything()
    print("✅ All json_schema_validator tests passed")
