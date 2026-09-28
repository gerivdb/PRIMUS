#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : generate_validation_report
Catégorie : logic/reporting
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Génère un rapport de validation à partir d'une liste de résultats.

Contrat :
  - Input  : results: list[dict]
  - Output : dict  {summary, details}
  - Side effects: none
  - Dépendances: stdlib uniquement
"""
from dataclasses import dataclass, field


@dataclass
class ValidationReport:
    total: int = 0
    passed: int = 0
    failed: int = 0
    details: list[dict] = field(default_factory=list)

    @property
    def summary(self) -> dict:
        return {
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "pass_rate": self.passed / self.total if self.total > 0 else 0.0,
        }


def generate_validation_report(results: list[dict]) -> ValidationReport:
    report = ValidationReport(total=len(results))

    for result in results:
        passed = result.get("passed", False)
        if passed:
            report.passed += 1
        else:
            report.failed += 1
        report.details.append(result)

    return report


if __name__ == "__main__":
    import json
    import sys

    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    results = data.get("results", [])
    report = generate_validation_report(results)
    print(json.dumps({
        "summary": report.summary,
        "details": report.details,
    }, indent=2))
    sys.exit(0)
