#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : benchmark_latency
Catégorie : logic
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Mesure la latence d'un endpoint HTTP sur N appels et retourne des métriques.

Contrat :
  - Input  : url: str, runs: int, timeout: float
  - Output : BenchmarkLatencyResult
  - Side effects: none
  - Dépendances: stdlib only
"""
from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass
from statistics import mean, median
from typing import List

try:
    import urllib.request
    import urllib.error
except ImportError:
    urllib = None  # type: ignore


@dataclass
class BenchmarkLatencyResult:
    url: str = ""
    runs: int = 0
    successful: int = 0
    errors: int = 0
    avg_ms: float = 0.0
    median_ms: float = 0.0
    min_ms: float = 0.0
    max_ms: float = 0.0
    error: str | None = None


def _measure_once(url: str, payload: bytes, timeout: float) -> float:
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            resp.read()
    except Exception as exc:
        raise RuntimeError(str(exc)) from exc
    return (time.perf_counter() - start) * 1000.0


def benchmark_latency(
    url: str,
    runs: int = 10,
    payload: dict | None = None,
    timeout: float = 10.0,
) -> BenchmarkLatencyResult:
    if urllib is None:
        return BenchmarkLatencyResult(error="urllib not available")

    data = json.dumps(payload or {}).encode("utf-8")
    latencies: List[float] = []
    errors = 0

    for _ in range(runs):
        try:
            latencies.append(_measure_once(url, data, timeout))
        except RuntimeError:
            errors += 1

    if not latencies:
        return BenchmarkLatencyResult(
            url=url, runs=runs, errors=errors, error="no successful measurements"
        )

    latencies_sorted = sorted(latencies)
    return BenchmarkLatencyResult(
        url=url,
        runs=runs,
        successful=len(latencies),
        errors=errors,
        avg_ms=round(mean(latencies), 2),
        median_ms=round(median(latencies), 2),
        min_ms=round(min(latencies), 2),
        max_ms=round(max(latencies), 2),
    )


if __name__ == "__main__":
    target_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080/v1/systemone"
    runs = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    result = benchmark_latency(target_url, runs=runs)
    print(json.dumps({
        "url": result.url,
        "runs": result.runs,
        "successful": result.successful,
        "errors": result.errors,
        "avg_ms": result.avg_ms,
        "median_ms": result.median_ms,
        "min_ms": result.min_ms,
        "max_ms": result.max_ms,
        "error": result.error,
    }, indent=2))
    sys.exit(1 if result.error else 0)
