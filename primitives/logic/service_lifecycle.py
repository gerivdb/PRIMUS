#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : service_lifecycle
Catégorie : logic
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Valide un manifeste de services et retourne un résumé typed.

Contrat :
  - Input  : services: list[dict]
  - Output : ServiceLifecycleResult
  - Side effects: none
  - Dépendances: stdlib only
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ServiceLifecycleResult:
    valid: bool = True
    error_count: int = 0
    errors: list[str] = field(default_factory=list)


def service_lifecycle(services: list[dict[str, Any]]) -> ServiceLifecycleResult:
    """Valide une liste de services et retourne un résumé."""
    errors: list[str] = []
    for index, service in enumerate(services):
        name = service.get("name") or service.get("id")
        if not name:
            errors.append(f"Service #{index} missing name/id")
            continue
        if "port" not in service:
            errors.append(f"Service {name} missing port")
        if "startup_order" not in service:
            errors.append(f"Service {name} missing startup_order")

    return ServiceLifecycleResult(
        valid=len(errors) == 0,
        error_count=len(errors),
        errors=errors,
    )


if __name__ == "__main__":
    import json
    import sys

    raw = sys.stdin.read() if sys.stdin.isatty() is False else "[]"
    services = json.loads(raw)
    if not isinstance(services, list):
        print(json.dumps({"error": "input must be a list of services"}))
        sys.exit(1)

    result = service_lifecycle(services)
    print(json.dumps({
        "valid": result.valid,
        "error_count": result.error_count,
        "errors": result.errors,
    }, indent=2))
    sys.exit(1 if not result.valid else 0)
