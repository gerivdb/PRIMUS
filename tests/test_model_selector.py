#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from primitives.logic.selection.model_selector import model_selector, ModelSelectionResult


def test_best_model_selected():
    models = [
        {"name": "big", "size": 5000 * 1024 * 1024},
        {"name": "small", "size": 500 * 1024 * 1024},
    ]
    result = model_selector(models)
    assert isinstance(result, ModelSelectionResult)
    assert result.best_model == "small"


def test_min_size_filter():
    models = [
        {"name": "big", "size": 5000 * 1024 * 1024},
        {"name": "small", "size": 500 * 1024 * 1024},
    ]
    result = model_selector(models, min_size_mb=1000)
    assert result.best_model == "big"


def test_no_candidates():
    result = model_selector([])
    assert result.best_model is None


if __name__ == "__main__":
    test_best_model_selected()
    test_min_size_filter()
    test_no_candidates()
    print("OK: All model_selector tests passed")
