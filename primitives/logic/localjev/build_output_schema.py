#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : build_output_schema
Catégorie : logic/localjev
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Construit le schema JSON attendu en sortie du modele,
  a partir d'une liste de questions preparees.

Contrat :
  - Input  : questions: list[PreparedQuestion]
  - Output : dict
  - Side effects: none
  - Dépendances: stdlib uniquement
"""
from dataclasses import dataclass
from typing import Any


@dataclass
class PreparedQuestion:
    key: str
    internal_id: str
    kind: str
    instructions: Any
    choices: list[tuple[str, Any]]
    legend: list[Any] | None = None


def build_output_schema(questions: list[PreparedQuestion]) -> dict[str, Any]:
    """Build the expected output JSON schema."""
    properties: dict[str, Any] = {}

    for question in questions:
        if question.kind == "noul":
            properties[question.internal_id] = {
                "type": "number",
                "minimum": 0,
                "maximum": 1,
                "description": "Probability that the answer is yes or true.",
            }
        else:
            properties[question.internal_id] = {
                "type": "array",
                "items": {"type": "number", "minimum": 0, "maximum": 1},
                "minItems": len(question.choices),
                "maxItems": len(question.choices),
                "description": "Probabilities in the listed outcome order; must sum to 1.",
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


if __name__ == "__main__":
    import json
    import sys

    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    raw_questions = data.get("questions", [])
    questions = [
        PreparedQuestion(
            key=q.get("key", ""),
            internal_id=q.get("internal_id", ""),
            kind=q.get("kind", ""),
            instructions=q.get("instructions", ""),
            choices=[tuple(c) for c in q.get("choices", [])],
            legend=q.get("legend"),
        )
        for q in raw_questions
    ]
    schema = build_output_schema(questions)
    print(json.dumps(schema, indent=2))
    sys.exit(0)
