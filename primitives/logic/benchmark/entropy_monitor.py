#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : entropy_monitor
Catégorie : logic/benchmark
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Calcule l'entropie d'une distribution de probabilites.

Contrat :
  - Input  : probabilities: list[float]
  - Output : EntropyResult  {entropy, normalized_entropy, max_entropy}
  - Side effects: none
  - Dépendances: stdlib uniquement
"""
import math
from dataclasses import dataclass


@dataclass
class EntropyResult:
    entropy: float = 0.0
    normalized_entropy: float = 0.0
    max_entropy: float = 0.0


def entropy_monitor(probabilities: list[float]) -> EntropyResult:
    if not probabilities:
        return EntropyResult()

    entropy = 0.0
    for p in probabilities:
        if p > 0:
            entropy -= p * math.log(p)

    n = len(probabilities)
    max_entropy = math.log(n) if n > 1 else 1.0
    normalized = entropy / max_entropy if max_entropy > 0 else 0.0

    return EntropyResult(
        entropy=entropy,
        normalized_entropy=normalized,
        max_entropy=max_entropy,
    )


if __name__ == "__main__":
    import json
    import sys

    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    probabilities = data.get("probabilities", [])
    result = entropy_monitor(probabilities)
    print(json.dumps({
        "entropy": result.entropy,
        "normalized_entropy": result.normalized_entropy,
        "max_entropy": result.max_entropy,
    }, indent=2))
    sys.exit(0)
