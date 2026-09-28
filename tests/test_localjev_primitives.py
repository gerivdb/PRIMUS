#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from primitives.logic.localjev.confidence import confidence
from primitives.logic.localjev.normalize_distribution import normalize_distribution
from primitives.logic.localjev.extract_json import extract_json
from primitives.logic.localjev.prepare_questions import prepare_questions, PreparedQuestion
from primitives.logic.localjev.build_output_schema import build_output_schema
from primitives.logic.localjev.decode_answers import decode_answers


def test_confidence_uniform():
    result = confidence([0.5, 0.5])
    assert result == 0.0


def test_confidence_certain():
    result = confidence([1.0, 0.0])
    assert result == 1.0


def test_confidence_uncertain():
    result = confidence([0.25, 0.25, 0.25, 0.25])
    assert result == 0.0


def test_normalize_distribution():
    result = normalize_distribution([1.0, 2.0, 3.0])
    assert len(result) == 3
    assert abs(sum(result) - 1.0) < 1e-9


def test_normalize_invalid():
    try:
        normalize_distribution([0.0, 0.0])
        assert False, "Should raise ValueError"
    except ValueError:
        pass


def test_extract_json_simple():
    result = extract_json('{"key": "value"}')
    assert result == {"key": "value"}


def test_extract_json_markdown():
    result = extract_json('```json\n{"key": "value"}\n```')
    assert result == {"key": "value"}


def test_prepare_questions_noul():
    questions = {
        "q1": {
            "type": "noul",
            "instructions": "Test?",
            "criteria": {"true": "yes text", "false": "no text"},
        }
    }
    prepared = prepare_questions(questions)
    assert len(prepared) == 1
    assert prepared[0].kind == "noul"
    assert prepared[0].choices[0][0] == "yes"


def test_build_output_schema():
    questions = [
        PreparedQuestion(key="q1", internal_id="q1", kind="noul", instructions="", choices=[("yes", ""), ("no", "")]),
        PreparedQuestion(key="q2", internal_id="q2", kind="choice", instructions="", choices=[("a", ""), ("b", "")]),
    ]
    schema = build_output_schema(questions)
    assert "answers" in schema["properties"]
    assert "q1" in schema["properties"]["answers"]["properties"]


def test_decode_answers_choice():
    questions = [
        PreparedQuestion(key="q1", internal_id="q1", kind="choice", instructions="", choices=[("a", ""), ("b", "")]),
    ]
    raw = {"answers": {"q1": [0.8, 0.2]}}
    result = decode_answers(raw, questions)
    assert result["q1"]["type"] == "choice"
    assert result["q1"]["choice"] == "a"
    assert abs(result["q1"]["probabilities"]["a"] - 0.8) < 1e-9


if __name__ == "__main__":
    test_confidence_uniform()
    test_confidence_certain()
    test_confidence_uncertain()
    test_normalize_distribution()
    test_normalize_invalid()
    test_extract_json_simple()
    test_extract_json_markdown()
    test_prepare_questions_noul()
    test_build_output_schema()
    test_decode_answers_choice()
    print("OK: All localjev primitive tests passed")
