"""Tests pour primitives/logic/entropy_monitor.py."""

from __future__ import annotations

import math

import pytest

from primitives.logic.entropy_monitor import EntropyResult, entropy_monitor


def test_uniform_distribution():
    result = entropy_monitor([0.25, 0.25, 0.25, 0.25])
    assert isinstance(result, EntropyResult)
    assert math.isclose(result.entropy, math.log(4), rel_tol=1e-9)
    assert math.isclose(result.normalized_entropy, 1.0, rel_tol=1e-9)
    assert math.isclose(result.max_entropy, math.log(4), rel_tol=1e-9)


def test_certain_distribution():
    result = entropy_monitor([1.0, 0.0, 0.0])
    assert math.isclose(result.entropy, 0.0, abs_tol=1e-9)
    assert math.isclose(result.normalized_entropy, 0.0, abs_tol=1e-9)
    assert math.isclose(result.max_entropy, math.log(3), rel_tol=1e-9)


def test_empty_input():
    result = entropy_monitor([])
    assert result.entropy == 0.0
    assert result.normalized_entropy == 0.0
    assert result.max_entropy == 0.0
