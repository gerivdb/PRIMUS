#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : entropy_monitor
Catégorie : logic
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Calcule l'entropie d'une distribution de probabilités.

Contrat :
  - Input  : probabilities: list[float]
  - Output : EntropyResult
  - Side effects: none
  - Dépendances: stdlib only
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class EntropyResult:
    entropy: float = 0.0
    normalized_entropy: float = 0.0
    max_entropy: float = 0.0


def entropy_monitor(probabilities: list[float]) -> EntropyResult:
    """Calcule l'entropie brute, normalisée et maximale."""
    if not probabilities:
        return EntropyResult()

    max_entropy = math.log(len(probabilities))
    entropy = 0.0
    for p in probabilities:
        if p > 0:
            entropy -= p * math.log(p)

    normalized = entropy / max_entropy if max_entropy > 0 else 0.0
    return EntropyResult(
        entropy=entropy,
        normalized_entropy=normalized,
        max_entropy=max_entropy,
    )


if __name__ == "__main__":
    import json
    import sys

    raw = sys.stdin.read() if sys.stdin.isatty() is False else "[]"
    probabilities = json.loads(raw)
    if not isinstance(probabilities, list):
        print(json.dumps({"error": "input must be a list of probabilities"}))
        sys.exit(1)

    result = entropy_monitor(probabilities)
    print(json.dumps({
        "entropy": result.entropy,
        "normalized_entropy": result.normalized_entropy,
        "max_entropy": result.max_entropy,
    }, indent=2))
