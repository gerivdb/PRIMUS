#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from primitives.logic.reporting.integration_score import integration_score, IntegrationScoreResult


def test_symbiote():
    result = integration_score(0.9, 0.9, 0.9)
    assert isinstance(result, IntegrationScoreResult)
    assert result.status == "SYMBIOTIC"


def test_near_symbiote():
    result = integration_score(0.75, 0.75, 0.75)
    assert result.status == "NEAR-SYMBIOTIC"


def test_partial():
    result = integration_score(0.5, 0.5, 0.5)
    assert result.status == "PARTIALLY INTEGRATED"


if __name__ == "__main__":
    test_symbiote()
    test_near_symbiote()
    test_partial()
    print("OK: All integration_score tests passed")
