#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : decode_answers
Catégorie : logic
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Décode les réponses brutes en réponses structurées.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class DecodedAnswer:
    type: str
    value: Any
    confidence: float = 0.0


def decode_answers(
    raw: dict[str, Any],
    questions: list[dict[str, Any]],
) -> dict[str, DecodedAnswer]:
    """Décode les réponses brutes en réponses structurées."""
    answers: dict[str, DecodedAnswer] = {}
    for question in questions:
        internal_id = question["internal_id"]
        key = question["key"]
        kind = question["kind"]
        value = raw.get(internal_id)
        if kind == "noul":
            confidence_value = float(value) if value is not None else 0.0
            answers[key] = DecodedAnswer(type="noul", value=confidence_value, confidence=confidence_value)
        else:
            if not isinstance(value, list):
                value = [value]
            confidence_value = max(value) if value else 0.0
            answers[key] = DecodedAnswer(type=kind, value=value, confidence=confidence_value)
    return answers
