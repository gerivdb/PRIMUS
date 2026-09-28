"""Tests pour primitives/logic/integration_score.py."""

from __future__ import annotations

import pytest

from primitives.logic.integration_score import IntegrationScoreResult, integration_score


def test_symbiotic_score():
    result = integration_score(0.95, 0.9, 0.85)
    assert isinstance(result, IntegrationScoreResult)
    assert result.status == "SYMBIOTIC"
    assert 0.0 <= result.overall <= 1.0


def test_near_symbiotic_score():
    result = integration_score(0.75, 0.7, 0.65)
    assert result.status == "NEAR-SYMBIOTIC"


def test_partially_integrated_score():
    result = integration_score(0.5, 0.4, 0.3)
    assert result.status == "PARTIALLY INTEGRATED"


def test_exact_thresholds():
    result = integration_score(0.85, 0.85, 0.85)
    assert result.status == "SYMBIOTIC"
    assert result.overall >= 0.85

    result = integration_score(0.7, 0.7, 0.7)
    assert result.status == "NEAR-SYMBIOTIC"
    assert result.overall >= 0.7

    result = integration_score(0.69, 0.69, 0.69)
    assert result.status == "PARTIALLY INTEGRATED"
    assert result.overall < 0.7
