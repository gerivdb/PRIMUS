#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : prepare_questions
Catégorie : logic
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Transforme un dictionnaire de questions en liste préparée normalisée.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class PreparedQuestion:
    key: str
    internal_id: str
    kind: str
    instructions: str
    choices: list[tuple[str | None, Any]]
    legend: list[Any] | None = None


def prepare_questions(questions: dict[str, dict[str, Any]]) -> list[PreparedQuestion]:
    """Prépare les questions pour l'inférence."""
    prepared: list[PreparedQuestion] = []
    for index, (key, question) in enumerate(questions.items()):
        kind = question.get("type", "")
        instructions = question.get("instructions", "")
        criteria = question.get("criteria", {})
        if kind == "noul":
            choices = [("yes", criteria.get("true")), ("no", criteria.get("false"))]
            legend = None
        elif kind == "choice":
            choices = [(label, criterion) for label, criterion in criteria.items()]
            legend = None
        else:
            if isinstance(criteria, dict):
                choices = [(str(score), criterion) for score, criterion in enumerate(criteria)]
                legend = list(criteria.values())
            else:
                choices = [(str(score), criterion) for score, criterion in enumerate(criteria)]
                legend = list(criteria)
        prepared.append(
            PreparedQuestion(
                key=key,
                internal_id=f"q{index + 1}",
                kind=kind,
                instructions=instructions,
                choices=choices,
                legend=legend,
            )
        )
    return prepared
