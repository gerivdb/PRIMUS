#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : json_schema_validator
Catégorie : validation
Spec      : ONTOLOGY/primitives/ (voir schema ci-dessous)

Responsabilité unique :
  Valide un objet Python (dict/list) contre un JSON Schema (draft-07).
  Retourne un résultat structuré avec statut, erreurs et chemin.

Contrat :
  - Input  : data: Any, schema: Dict  (JSON Schema draft-07)
  - Output : ValidationResult  {valid, errors, error_count}
  - Stateless : oui
  - Effets de bord : aucun
  - Dépendances : stdlib uniquement (pas de jsonschema externe requis)
                  Si jsonschema est installé, il est utilisé automatiquement.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

@dataclass
class ValidationError:
    path: str        # JSONPath de l'erreur (ex: "$.tools[0].id")
    message: str     # Message d'erreur lisible
    value: Any = None  # Valeur incriminiée


@dataclass
class ValidationResult:
    valid: bool
    errors: List[ValidationError] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return len(self.errors)

    def first_error(self) -> Optional[ValidationError]:
        return self.errors[0] if self.errors else None

    def __bool__(self) -> bool:
        return self.valid


# ---------------------------------------------------------------------------
# Primitive
# ---------------------------------------------------------------------------

def json_schema_validator(
    data: Any,
    schema: Dict[str, Any],
) -> ValidationResult:
    """
    Valide `data` contre `schema` (JSON Schema draft-07).

    Stratégie :
    1. Si le package `jsonschema` est installé, l'utilise (validation complète).
    2. Sinon, fallback sur un validateur minimal stdlib
       couvrant : type, required, properties, enum, minimum, maximum,
       minLength, maxLength, const, items.

    Returns:
        ValidationResult(valid=True)  si valide
        ValidationResult(valid=False, errors=[...])  si invalide
    """
    try:
        return _validate_with_jsonschema(data, schema)
    except ImportError:
        return _validate_minimal(data, schema, path="$")


# ---------------------------------------------------------------------------
# Backend 1 : jsonschema (si disponible)
# ---------------------------------------------------------------------------

def _validate_with_jsonschema(data: Any, schema: Dict) -> ValidationResult:
    import jsonschema
    validator = jsonschema.Draft7Validator(schema)
    errors = list(validator.iter_errors(data))
    if not errors:
        return ValidationResult(valid=True)
    return ValidationResult(
        valid=False,
        errors=[
            ValidationError(
                path="$" + "".join(f"[{p!r}]" if isinstance(p, str) else f"[{p}]" for p in e.absolute_path),
                message=e.message,
                value=e.instance,
            )
            for e in errors
        ],
    )


# ---------------------------------------------------------------------------
# Backend 2 : validateur minimal stdlib (fallback)
# ---------------------------------------------------------------------------

_TYPE_MAP = {
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "array": list,
    "object": dict,
    "null": type(None),
}


def _validate_minimal(
    data: Any,
    schema: Dict,
    path: str = "$",
) -> ValidationResult:
    errors: List[ValidationError] = []
    _check(data, schema, path, errors)
    return ValidationResult(valid=len(errors) == 0, errors=errors)


def _check(data: Any, schema: Dict, path: str, errors: List[ValidationError]) -> None:
    # type
    if "type" in schema:
        expected = schema["type"]
        py_type = _TYPE_MAP.get(expected)
        if py_type and not isinstance(data, py_type):
            # bool est sous-classe de int — éviter faux positifs
            if not (expected == "integer" and isinstance(data, bool)):
                errors.append(ValidationError(
                    path=path,
                    message=f"Expected type '{expected}', got '{type(data).__name__}'",
                    value=data,
                ))
                return

    # const
    if "const" in schema and data != schema["const"]:
        errors.append(ValidationError(path=path, message=f"Expected const {schema['const']!r}, got {data!r}", value=data))

    # enum
    if "enum" in schema and data not in schema["enum"]:
        errors.append(ValidationError(path=path, message=f"Value {data!r} not in enum {schema['enum']}", value=data))

    # string constraints
    if isinstance(data, str):
        if "minLength" in schema and len(data) < schema["minLength"]:
            errors.append(ValidationError(path=path, message=f"String too short (min {schema['minLength']})", value=data))
        if "maxLength" in schema and len(data) > schema["maxLength"]:
            errors.append(ValidationError(path=path, message=f"String too long (max {schema['maxLength']})", value=data))

    # numeric constraints
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        if "minimum" in schema and data < schema["minimum"]:
            errors.append(ValidationError(path=path, message=f"Value {data} < minimum {schema['minimum']}", value=data))
        if "maximum" in schema and data > schema["maximum"]:
            errors.append(ValidationError(path=path, message=f"Value {data} > maximum {schema['maximum']}", value=data))

    # object: required + properties
    if isinstance(data, dict):
        for req in schema.get("required", []):
            if req not in data:
                errors.append(ValidationError(path=f"{path}.{req}", message=f"Required field '{req}' is missing", value=None))
        for key, subschema in schema.get("properties", {}).items():
            if key in data:
                _check(data[key], subschema, f"{path}.{key}", errors)

    # array: items
    if isinstance(data, list) and "items" in schema:
        for i, item in enumerate(data):
            _check(item, schema["items"], f"{path}[{i}]", errors)
