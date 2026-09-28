"""Tests pour primitives/logic/prepare_questions.py."""

from __future__ import annotations

import pytest

from primitives.logic.prepare_questions import PreparedQuestion, prepare_questions


def test_prepare_noul_question():
    questions = {
        "q1": {
            "type": "noul",
            "instructions": "Is 2+2=4?",
            "criteria": {"true": "Yes", "false": "No"},
        }
    }
    result = prepare_questions(questions)
    assert len(result) == 1
    assert result[0].key == "q1"
    assert result[0].kind == "noul"
    assert result[0].choices == [("yes", "Yes"), ("no", "No")]


def test_prepare_choice_question():
    questions = {
        "q1": {
            "type": "choice",
            "instructions": "Pick one",
            "criteria": {"a": "A", "b": "B"},
        }
    }
    result = prepare_questions(questions)
    assert result[0].choices == [("a", "A"), ("b", "B")]


def test_prepare_score_question():
    questions = {
        "q1": {
            "type": "score",
            "instructions": "Rate",
            "criteria": ["bad", "good"],
        }
    }
    result = prepare_questions(questions)
    assert result[0].legend == ["bad", "good"]
    assert result[0].choices == [("0", "bad"), ("1", "good")]
