"""Tests pour primitives/logic/confidence.py."""

from __future__ import annotations

import math

import pytest

from primitives.logic.confidence import confidence


def test_certain_distribution():
    assert math.isclose(confidence([1.0, 0.0, 0.0]), 1.0, abs_tol=1e-9)


def test_uniform_distribution():
    result = confidence([0.25, 0.25, 0.25, 0.25])
    assert math.isclose(result, 0.0, abs_tol=1e-9)


def test_bounded_result():
    result = confidence([0.5, 0.5])
    assert 0.0 <= result <= 1.0
