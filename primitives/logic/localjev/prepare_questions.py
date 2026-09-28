#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : prepare_questions
Catégorie : logic/localjev
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Transforme un dictionnaire de questions en liste de questions preparees
  pour le moteur LocalJev.

Contrat :
  - Input  : questions: dict[str, dict]
  - Output : list[PreparedQuestion]
  - Side effects: none
  - Dépendances: stdlib uniquement
"""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PreparedQuestion:
    key: str
    internal_id: str
    kind: str
    instructions: Any
    choices: list[tuple[str, Any]]
    legend: list[Any] | None = None


def prepare_questions(questions: dict[str, dict]) -> list[PreparedQuestion]:
    """Prepare questions for LocalJev engine."""
    prepared: list[PreparedQuestion] = []

    for index, (key, question) in enumerate(questions.items()):
        q_type = question.get("type", "")
        instructions = question.get("instructions", "")
        criteria = question.get("criteria", {})

        if q_type == "noul":
            choices = [
                ("yes", criteria.get("true") if isinstance(criteria, dict) else None),
                ("no", criteria.get("false") if isinstance(criteria, dict) else None),
            ]
            prepared.append(
                PreparedQuestion(
                    key=key,
                    internal_id=f"q{index + 1}",
                    kind=q_type,
                    instructions=instructions,
                    choices=choices,
                )
            )
            continue

        if q_type == "choice" and isinstance(criteria, dict):
            choices = [(label, criterion) for label, criterion in criteria.items()]
            prepared.append(
                PreparedQuestion(
                    key=key,
                    internal_id=f"q{index + 1}",
                    kind=q_type,
                    instructions=instructions,
                    choices=choices,
                )
            )
            continue

        if isinstance(criteria, dict):
            choices = [(str(score), criterion) for score, criterion in criteria.items()]
            prepared.append(
                PreparedQuestion(
                    key=key,
                    internal_id=f"q{index + 1}",
                    kind=q_type,
                    instructions=instructions,
                    choices=choices,
                    legend=list(criteria.values()),
                )
            )

    return prepared


if __name__ == "__main__":
    import json
    import sys

    data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    questions = data.get("questions", {})
    prepared = prepare_questions(questions)
    payload = [
        {
            "key": q.key,
            "internal_id": q.internal_id,
            "kind": q.kind,
            "instructions": q.instructions,
            "choices": q.choices,
            "legend": q.legend,
        }
        for q in prepared
    ]
    print(json.dumps(payload, indent=2))
    sys.exit(0)
