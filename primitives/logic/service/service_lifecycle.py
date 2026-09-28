#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : service_lifecycle
Catégorie : logic/service
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Valide le cycle de vie d'un service (startup_order < shutdown_order).

Contrat :
  - Input  : services: list[dict]
  - Output : ServiceLifecycleResult  {valid, errors}
  - Side effects: none
  - Dépendances: stdlib uniquement
"""
from dataclasses import dataclass, field


@dataclass
class ServiceLifecycleError:
    service: str
    message: str


@dataclass
class ServiceLifecycleResult:
    valid: bool = True
    errors: list[ServiceLifecycleError] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return len(self.errors)


def service_lifecycle(services: list[dict]) -> ServiceLifecycleResult:
    result = ServiceLifecycleResult()
    for svc in services:
        name = svc.get("name", "unknown")
        startup = svc.get("startup_order")
        shutdown = svc.get("shutdown_order")
        if startup is None:
            result.valid = False
            result.errors.append(ServiceLifecycleError(service=name, message="missing startup_order"))
        if shutdown is None:
            result.valid = False
            result.errors.append(ServiceLifecycleError(service=name, message="missing shutdown_order"))
    return result


if __name__ == "__main__":
    import json
    import sys

    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    result = service_lifecycle(data.get("services", []))
    print(json.dumps({
        "valid": result.valid,
        "error_count": result.error_count,
        "errors": [{"service": e.service, "message": e.message} for e in result.errors],
    }, indent=2))
    sys.exit(1 if not result.valid else 0)
