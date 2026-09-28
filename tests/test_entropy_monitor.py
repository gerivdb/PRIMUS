#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from primitives.logic.benchmark.entropy_monitor import entropy_monitor, EntropyResult


def test_entropy_certain():
    result = entropy_monitor([1.0, 0.0])
    assert isinstance(result, EntropyResult)
    assert result.entropy == 0.0


def test_entropy_uniform():
    result = entropy_monitor([0.5, 0.5])
    assert result.entropy > 0
    assert result.normalized_entropy == 1.0


def test_entropy_empty():
    result = entropy_monitor([])
    assert result.entropy == 0.0


if __name__ == "__main__":
    test_entropy_certain()
    test_entropy_uniform()
    test_entropy_empty()
    print("OK: All entropy_monitor tests passed")
