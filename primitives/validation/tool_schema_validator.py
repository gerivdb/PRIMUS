#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : tool_schema_validator
Catégorie : validation
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Valide un dictionnaire d'outils MCP contre un schéma minimal.
  Vérifie la présence des champs requis : id, status, path.

Contrat :
  - Input  : tools: list[dict], schema: dict (optionnel)
  - Output : ToolSchemaValidationResult  {valid, errors, error_count, valid_tools, invalid_tools}
  - Side effects: none
  - Dépendances: stdlib uniquement
"""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolSchemaValidationError:
    index: int
    tool_id: str | None
    message: str
    value: Any = None


@dataclass
class ToolSchemaValidationResult:
    valid: bool
    errors: list[ToolSchemaValidationError] = field(default_factory=list)
    valid_tools: list[dict[str, Any]] = field(default_factory=list)
    invalid_tools: list[dict[str, Any]] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return len(self.errors)

    @property
    def valid_count(self) -> int:
        return len(self.valid_tools)

    @property
    def invalid_count(self) -> int:
        return len(self.invalid_tools)


REQUIRED_TOOL_FIELDS = ["id", "status", "path"]


def _validate_tool(tool: Any, index: int) -> ToolSchemaValidationError | None:
    if not isinstance(tool, dict):
        return ToolSchemaValidationError(
            index=index,
            tool_id=None,
            message="Tool must be a dict",
            value=tool,
        )

    missing = [field for field in REQUIRED_TOOL_FIELDS if field not in tool]
    if missing:
        return ToolSchemaValidationError(
            index=index,
            tool_id=tool.get("id"),
            message=f"Missing required fields: {', '.join(missing)}",
            value=tool,
        )

    return None


def tool_schema_validator(tools: list[dict[str, Any]], schema: dict[str, Any] | None = None) -> ToolSchemaValidationResult:
    """Validate a list of MCP tool definitions against a minimal schema."""
    errors: list[ToolSchemaValidationError] = []
    valid_tools: list[dict[str, Any]] = []
    invalid_tools: list[dict[str, Any]] = []

    for index, tool in enumerate(tools):
        error = _validate_tool(tool, index)
        if error is None:
            valid_tools.append(tool)
        else:
            errors.append(error)
            invalid_tools.append(tool)

    return ToolSchemaValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        valid_tools=valid_tools,
        invalid_tools=invalid_tools,
    )


if __name__ == "__main__":
    import json
    import sys

    payload = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    tools = payload.get("tools", [])
    result = tool_schema_validator(tools)
    print(json.dumps({
        "valid": result.valid,
        "valid_count": result.valid_count,
        "invalid_count": result.invalid_count,
        "errors": [
            {
                "index": e.index,
                "tool_id": e.tool_id,
                "message": e.message,
                "value": str(e.value),
            }
            for e in result.errors
        ],
    }, indent=2))
    sys.exit(1 if not result.valid else 0)
