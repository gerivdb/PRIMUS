"""Tests pour primitives/logic/build_output_schema.py."""

from __future__ import annotations

import pytest

from primitives.logic.build_output_schema import build_output_schema


def test_build_schema_with_noul_and_choice():
    questions = [
        {"internal_id": "q1", "kind": "noul", "choices": [("yes", None), ("no", None)]},
        {"internal_id": "q2", "kind": "choice", "choices": [("a", "A"), ("b", "B")]},
    ]
    schema = build_output_schema(questions)
    assert schema["required"] == ["answers"]
    answers = schema["properties"]["answers"]
    assert answers["required"] == ["q1", "q2"]
    assert answers["properties"]["q1"]["type"] == "number"
    assert answers["properties"]["q2"]["type"] == "array"


def test_build_schema_empty():
    schema = build_output_schema([])
    assert schema["properties"]["answers"]["required"] == []
