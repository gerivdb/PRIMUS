"""Tests pour primitives/logic/model_selector.py."""

from __future__ import annotations

import pytest

from primitives.logic.model_selector import ModelSelectorResult, model_selector


def test_selects_smallest_candidate():
    models = [
        {"name": "big-model", "size": 5 * 1024 * 1024 * 1024},
        {"name": "small-model", "size": 1 * 1024 * 1024 * 1024},
    ]
    result = model_selector(models)
    assert isinstance(result, ModelSelectorResult)
    assert result.best_model == "small-model"
    assert len(result.all_candidates) == 2


def test_min_size_filter():
    models = [
        {"name": "big-model", "size": 5 * 1024 * 1024 * 1024},
        {"name": "small-model", "size": 1 * 1024 * 1024 * 1024},
    ]
    result = model_selector(models, min_size_mb=1024)
    assert result.best_model == "small-model"
    assert len(result.all_candidates) == 2


def test_no_candidate():
    result = model_selector([], min_size_mb=10)
    assert result.best_model is None
    assert result.all_candidates == []
