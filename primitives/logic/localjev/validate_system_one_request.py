#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : validate_system_one_request
Catégorie : logic/localjev
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Valide qu'une requête SystemOne contient les champs requis.

Contrat :
  - Input  : request: dict
  - Output : ValidationResult  {valid, errors}
  - Side effects: none
  - Dépendances: stdlib uniquement
"""
from dataclasses import dataclass, field


@dataclass
class ValidationError:
    path: str
    message: str


@dataclass
class ValidationResult:
    valid: bool = True
    errors: list[ValidationError] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return len(self.errors)


def validate_system_one_request(request: dict) -> ValidationResult:
    result = ValidationResult()
    if not isinstance(request, dict):
        result.valid = False
        result.errors.append(ValidationError(path="$", message="Request must be a dict"))
        return result

    required = ["questions", "state"]
    for field_name in required:
        if field_name not in request:
            result.valid = False
            result.errors.append(ValidationError(path=f"$.{field_name}", message=f"Missing required field: {field_name}"))

    questions = request.get("questions")
    if questions is not None and not isinstance(questions, dict):
        result.valid = False
        result.errors.append(ValidationError(path="$.questions", message="questions must be a dict"))

    return result


if __name__ == "__main__":
    import json
    import sys

    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    result = validate_system_one_request(data.get("request", {}))
    print(json.dumps({
        "valid": result.valid,
        "error_count": result.error_count,
        "errors": [{"path": e.path, "message": e.message} for e in result.errors],
    }, indent=2))
    sys.exit(1 if not result.valid else 0)
