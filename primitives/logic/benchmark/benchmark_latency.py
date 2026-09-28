#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : benchmark_latency
Catégorie : logic/benchmark
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Mesure la latence moyenne d'un endpoint HTTP sur N appels.

Contrat :
  - Input  : url: str, runs: int = 10, timeout: float = 10.0
  - Output : BenchmarkResult  {avg_ms, median_ms, min_ms, max_ms, error}
  - Side effects: none
  - Dépendances: stdlib uniquement
"""
import json
import math
import statistics
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, field


@dataclass
class BenchmarkResult:
    avg_ms: float = 0.0
    median_ms: float = 0.0
    min_ms: float = 0.0
    max_ms: float = 0.0
    error: str | None = None

    @property
    def success(self) -> bool:
        return self.error is None


def _measure_once(url: str, payload: bytes, timeout: float = 10.0) -> float | None:
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
    except Exception:
        return None
    return (time.perf_counter() - start) * 1000.0


def benchmark_latency(url: str, runs: int = 10, payload: dict | None = None, timeout: float = 10.0) -> BenchmarkResult:
    if payload is None:
        payload = {"benchmark": True}
    data = json.dumps(payload).encode("utf-8")

    latencies: list[float] = []
    for _ in range(runs):
        latency = _measure_once(url, data, timeout)
        if latency is not None:
            latencies.append(latency)

    if not latencies:
        return BenchmarkResult(error="no successful measurements")

    return BenchmarkResult(
        avg_ms=round(statistics.mean(latencies), 2),
        median_ms=round(statistics.median(latencies), 2),
        min_ms=round(min(latencies), 2),
        max_ms=round(max(latencies), 2),
    )


if __name__ == "__main__":
    import sys

    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080/v1/systemone"
    runs = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    result = benchmark_latency(url, runs=runs)
    print(json.dumps({
        "avg_ms": result.avg_ms,
        "median_ms": result.median_ms,
        "min_ms": result.min_ms,
        "max_ms": result.max_ms,
        "error": result.error,
    }, indent=2))
    sys.exit(1 if result.error else 0)
