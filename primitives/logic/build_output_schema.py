#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : build_output_schema
Catégorie : logic
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Construit le schéma de sortie JSON depuis une liste de questions préparées.
"""
from __future__ import annotations

from typing import Any


def build_output_schema(questions: list[dict[str, Any]]) -> dict[str, Any]:
    """Construit le schéma de réponse attendu."""
    properties: dict[str, Any] = {}
    for question in questions:
        internal_id = question["internal_id"]
        kind = question["kind"]
        if kind == "noul":
            properties[internal_id] = {
                "type": "number",
                "minimum": 0,
                "maximum": 1,
            }
        else:
            properties[internal_id] = {
                "type": "array",
                "items": {"type": "number", "minimum": 0, "maximum": 1},
                "minItems": len(question["choices"]),
                "maxItems": len(question["choices"]),
            }
    return {
        "type": "object",
        "properties": {
            "answers": {
                "type": "object",
                "properties": properties,
                "required": list(properties.keys()),
                "additionalProperties": False,
            }
        },
        "required": ["answers"],
        "additionalProperties": False,
    }
