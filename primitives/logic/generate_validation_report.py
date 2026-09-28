#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : generate_validation_report
Catégorie : logic
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Génère un rapport de validation à partir de résultats de tests.

Contrat :
  - Input  : results: list[dict]
  - Output : ValidationReportResult
  - Side effects: none
  - Dépendances: stdlib only
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ValidationReportResult:
    summary: dict[str, Any] = field(default_factory=dict)
    details: list[dict[str, Any]] = field(default_factory=list)


def generate_validation_report(results: list[dict[str, Any]]) -> ValidationReportResult:
    """Génère un rapport de validation depuis une liste de résultats."""
    timestamp = datetime.now(timezone.utc).isoformat()
    total = len(results)
    passed = sum(1 for r in results if r.get("status") == "PASS")
    failed = total - passed

    summary = {
        "timestamp": timestamp,
        "total": total,
        "passed": passed,
        "failed": failed,
        "result": "PASS" if failed == 0 else "FAIL",
    }

    details = [
        {
            "name": r.get("name", "unknown"),
            "status": r.get("status", "UNKNOWN"),
            "exit_code": r.get("exit_code", -1),
            "stdout": r.get("stdout", ""),
            "stderr": r.get("stderr", ""),
        }
        for r in results
    ]

    return ValidationReportResult(summary=summary, details=details)


if __name__ == "__main__":
    import sys

    raw = sys.stdin.read() if sys.stdin.isatty() is False else "[]"
    results = json.loads(raw)
    if not isinstance(results, list):
        print(json.dumps({"error": "input must be a list of results"}))
        sys.exit(1)

    report = generate_validation_report(results)
    print(json.dumps({
        "summary": report.summary,
        "details": report.details,
    }, indent=2))
