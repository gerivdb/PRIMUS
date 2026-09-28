#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : integration_score
Catégorie : logic
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Calcule un score d'intégration global à partir de sous-scores.

Contrat :
  - Input  : contract_score: float, matrix_score: float, crosslink_score: float
  - Output : IntegrationScoreResult
  - Side effects: none
  - Dépendances: stdlib only
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class IntegrationScoreResult:
    overall: float = 0.0
    status: str = ""


def integration_score(
    contract_score: float,
    matrix_score: float,
    crosslink_score: float,
) -> IntegrationScoreResult:
    """Calcule le score global et déduit le statut."""
    overall = round((contract_score + matrix_score + crosslink_score) / 3, 10)
    if overall >= 0.85:
        status = "SYMBIOTIC"
    elif overall >= 0.7:
        status = "NEAR-SYMBIOTIC"
    else:
        status = "PARTIALLY INTEGRATED"
    return IntegrationScoreResult(overall=overall, status=status)


if __name__ == "__main__":
    import json
    import sys

    raw = sys.stdin.read() if sys.stdin.isatty() is False else "{}"
    payload = json.loads(raw)
    result = integration_score(
        float(payload.get("contract_score", 0)),
        float(payload.get("matrix_score", 0)),
        float(payload.get("crosslink_score", 0)),
    )
    print(json.dumps({"overall": result.overall, "status": result.status}, indent=2))
