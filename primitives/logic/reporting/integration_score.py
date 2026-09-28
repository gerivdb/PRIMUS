#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : integration_score
Catégorie : logic/reporting
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Calcule un score d'intégration à partir de métriques de contrat et de matrice.

Contrat :
  - Input  : contract_score: float, matrix_score: float, crosslink_score: float
  - Output : IntegrationScoreResult  {overall, status}
  - Side effects: none
  - Dépendances: stdlib uniquement
"""
from dataclasses import dataclass


@dataclass
class IntegrationScoreResult:
    overall: float = 0.0
    status: str = "PARTIALLY INTEGRATED"


def integration_score(contract_score: float, matrix_score: float, crosslink_score: float) -> IntegrationScoreResult:
    overall = (contract_score + matrix_score + crosslink_score) / 3.0

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

    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    result = integration_score(
        data.get("contract_score", 0.0),
        data.get("matrix_score", 0.0),
        data.get("crosslink_score", 0.0),
    )
    print(json.dumps({
        "overall": result.overall,
        "status": result.status,
    }, indent=2))
    sys.exit(0)
