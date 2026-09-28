#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : confidence
Catégorie : logic/localjev
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Calcule le score de confiance d'une distribution de probabilites.

Formule :
  confidence = 1 - (entropy / log(n))

Contrat :
  - Input  : probabilities: list[float]
  - Output : float  (entre 0 et 1)
  - Side effects: none
  - Dépendances: stdlib uniquement
"""
import math


def confidence(probabilities: list[float]) -> float:
    """Compute confidence score from a probability distribution."""
    if not probabilities:
        return 0.0

    entropy = 0.0
    for p in probabilities:
        if p > 0:
            entropy -= p * math.log(p)

    n = len(probabilities)
    if n <= 1:
        return 1.0

    value = 1.0 - entropy / math.log(n)
    return max(0.0, min(1.0, value))


if __name__ == "__main__":
    import json
    import sys

    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    probabilities = data.get("probabilities", [])
    result = confidence(probabilities)
    print(json.dumps({"confidence": result}, indent=2))
    sys.exit(0)
