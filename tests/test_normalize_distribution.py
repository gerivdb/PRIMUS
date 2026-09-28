"""Tests pour primitives/logic/normalize_distribution.py."""

from __future__ import annotations

import math

import pytest

from primitives.logic.normalize_distribution import normalize_distribution


def test_normalizes_to_unit_sum():
    result = normalize_distribution([1.0, 2.0, 3.0])
    assert math.isclose(sum(result), 1.0, abs_tol=1e-9)
    assert math.isclose(result[0], 1 / 6, abs_tol=1e-9)
    assert math.isclose(result[1], 2 / 6, abs_tol=1e-9)
    assert math.isclose(result[2], 3 / 6, abs_tol=1e-9)


def test_rejects_zero_sum():
    with pytest.raises(ValueError):
        normalize_distribution([0.0, 0.0])
