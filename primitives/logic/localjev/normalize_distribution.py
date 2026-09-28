#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : normalize_distribution
Catégorie : logic/localjev
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Normalise une distribution de probabilites pour que la somme vaille 1.

Contrat :
  - Input  : probabilities: list[float]
  - Output : list[float]
  - Side effects: none
  - Dépendances: stdlib uniquement
"""
import math


def normalize_distribution(probabilities: list[float]) -> list[float]:
    """Normalize a probability distribution to sum to 1."""
    if not probabilities:
        return []

    total = sum(probabilities)
    if total <= 0:
        raise ValueError("Probabilities must have a positive sum")

    return [p / total for p in probabilities]


if __name__ == "__main__":
    import json
    import sys

    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    probabilities = data.get("probabilities", [])
    try:
        result = normalize_distribution(probabilities)
        print(json.dumps({"normalized": result}, indent=2))
        sys.exit(0)
    except ValueError as e:
        print(json.dumps({"error": str(e)}, indent=2))
        sys.exit(1)
