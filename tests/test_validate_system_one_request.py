#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from primitives.logic.localjev.validate_system_one_request import validate_system_one_request, ValidationResult


def test_valid_request():
    request = {"questions": {"q1": {}}, "state": {}}
    result = validate_system_one_request(request)
    assert isinstance(result, ValidationResult)
    assert result.valid is True
    assert result.error_count == 0


def test_missing_questions():
    request = {"state": {}}
    result = validate_system_one_request(request)
    assert result.valid is False
    assert result.error_count == 1


def test_invalid_type():
    result = validate_system_one_request("not-a-dict")
    assert result.valid is False
    assert result.error_count >= 1


if __name__ == "__main__":
    test_valid_request()
    test_missing_questions()
    test_invalid_type()
    print("OK: All validate_system_one_request tests passed")
