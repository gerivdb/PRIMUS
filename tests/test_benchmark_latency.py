"""Tests pour primitives/logic/benchmark_latency.py."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from primitives.logic.benchmark_latency import BenchmarkLatencyResult, benchmark_latency


def test_benchmark_returns_typed_result():
    result = benchmark_latency("http://localhost:8080/v1/systemone", runs=1, timeout=0.1)
    assert isinstance(result, BenchmarkLatencyResult)
    assert result.url == "http://localhost:8080/v1/systemone"
    assert isinstance(result.runs, int)
    assert isinstance(result.successful, int)
    assert isinstance(result.errors, int)
    assert isinstance(result.avg_ms, float)
    assert isinstance(result.median_ms, float)
    assert isinstance(result.min_ms, float)
    assert isinstance(result.max_ms, float)


def test_benchmark_no_successful_measurement():
    result = benchmark_latency("http://localhost:1/v1/systemone", runs=1, timeout=0.1)
    assert isinstance(result, BenchmarkLatencyResult)
    assert result.successful == 0
    assert result.error is not None
