"""Tests pour primitives/logic/validate_system_one_request.py."""

from __future__ import annotations

import pytest

from primitives.logic.validate_system_one_request import ValidationResult, validate_system_one_request


def test_valid_request():
    request = {
        "questions": {"q1": {"type": "noul", "instructions": "x", "criteria": {}}},
        "state": {"text": "doc"},
    }
    result = validate_system_one_request(request)
    assert isinstance(result, ValidationResult)
    assert result.valid is True
    assert result.error_count == 0


def test_missing_fields():
    request = {"state": {"text": "doc"}}
    result = validate_system_one_request(request)
    assert result.valid is False
    assert result.error_count == 2
    assert "missing questions" in result.errors
