"""Tests pour primitives/logic/decode_answers.py."""

from __future__ import annotations

import pytest

from primitives.logic.decode_answers import DecodedAnswer, decode_answers


def test_decode_noul_answer():
    questions = [
        {"internal_id": "q1", "key": "question1", "kind": "noul", "choices": []},
    ]
    raw = {"q1": 0.92}
    result = decode_answers(raw, questions)
    assert result["question1"].type == "noul"
    assert result["question1"].value == 0.92
    assert result["question1"].confidence == 0.92


def test_decode_choice_answer():
    questions = [
        {"internal_id": "q1", "key": "question1", "kind": "choice", "choices": [("a", "A"), ("b", "B")]},
    ]
    raw = {"q1": [0.8, 0.2]}
    result = decode_answers(raw, questions)
    assert result["question1"].type == "choice"
    assert result["question1"].value == [0.8, 0.2]
    assert result["question1"].confidence == 0.8
