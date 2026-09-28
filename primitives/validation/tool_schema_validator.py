#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : tool_schema_validator
Catégorie : validation
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Valide les paramètres d'appels outils contre un schema fourni.

Contrat :
  - Input  : tools: list[dict], schema: dict | None
  - Output : ToolSchemaValidationResult
  - Side effects: none
  - Dépendances: stdlib only
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolSchemaValidationResult:
    valid: bool = True
    valid_count: int = 0
    invalid_count: int = 0
    errors: list[str] = field(default_factory=list)


class ToolSchemaValidationError(Exception):
    """Erreur de validation de schema d'outil."""


def _type_name(value: Any) -> str:
    if isinstance(value, str):
        return "string"
    if isinstance(value, int):
        return "int"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def tool_schema_validator(
    tools: list[dict[str, Any]],
    schema: dict[str, Any] | None = None,
) -> ToolSchemaValidationResult:
    """Valide une liste d'outils contre un schema optionnel."""
    errors: list[str] = []
    valid_count = 0
    invalid_count = 0

    for tool in tools:
        name = tool.get("name") or tool.get("id") or "unknown"
        if not isinstance(name, str):
            errors.append(f"Tool name must be a string, got {_type_name(name)}")
            invalid_count += 1
            continue

        parameters = tool.get("parameters") or tool.get("input") or {}
        if not isinstance(parameters, dict):
            errors.append(f"Tool {name}: parameters must be an object")
            invalid_count += 1
            continue

        tool_errors: list[str] = []
        if schema:
            required = schema.get("required", [])
            for field_name in required:
                if field_name not in parameters:
                    tool_errors.append(f"missing required parameter {field_name}")
            properties = schema.get("properties", {})
            for field_name, value in parameters.items():
                expected = properties.get(field_name, {}).get("type")
                if expected and _type_name(value) != expected:
                    tool_errors.append(
                        f"{field_name}: expected {expected}, got {_type_name(value)}"
                    )

        if tool_errors:
            errors.append(f"Tool {name}: " + "; ".join(tool_errors))
            invalid_count += 1
        else:
            valid_count += 1

    return ToolSchemaValidationResult(
        valid=invalid_count == 0,
        valid_count=valid_count,
        invalid_count=invalid_count,
        errors=errors,
    )


if __name__ == "__main__":
    import json

    raw = sys.stdin.read() if sys.stdin.isatty() is False else "[]"
    payload = json.loads(raw)
    tools = payload.get("tools", [])
    schema = payload.get("schema")
    result = tool_schema_validator(tools, schema)
    print(
        json.dumps(
            {
                "valid": result.valid,
                "valid_count": result.valid_count,
                "invalid_count": result.invalid_count,
                "errors": result.errors,
            },
            indent=2,
        )
    )
    sys.exit(1 if not result.valid else 0)
