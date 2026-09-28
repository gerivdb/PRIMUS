#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : decode_answers
Catégorie : logic/localjev
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Decode les reponses brutes du modele en reponses structurees.

Contrat :
  - Input  : raw: dict, questions: list[PreparedQuestion]
  - Output : dict[str, dict]
  - Side effects: none
  - Dépendances: stdlib uniquement
"""
import math
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


def _number_probability(value: Any, path: str) -> float:
    if not isinstance(value, (int, float)):
        raise TypeError(f"{path} must be a number")
    if not math.isfinite(value):
        raise TypeError(f"{path} must be a number")
    if value < 0 or value > 1:
        raise ValueError(f"{path} must be between 0 and 1")
    return float(value)


def _normalize_distribution(value: Any, size: int, path: str) -> list[float]:
    if not isinstance(value, list) or len(value) != size:
        raise TypeError(f"{path} must be an array of exactly {size} probabilities")
    probabilities = [_number_probability(item, f"{path}[{index}]") for index, item in enumerate(value)]
    total = sum(probabilities)
    if total <= 0:
        raise ValueError(f"{path} probabilities must have a positive sum")
    return [p / total for p in probabilities]


def _confidence(probabilities: list[float]) -> float:
    if not probabilities:
        return 0.0
    entropy = 0.0
    for p in probabilities:
        if p > 0:
            entropy -= p * math.log(p)
    n = len(probabilities)
    if n <= 1:
        return 1.0
    value = 1.0 - entropy / math.log(n)
    return max(0.0, min(1.0, value))


def decode_answers(raw: Any, questions: list) -> dict:
    """Decode raw model output into structured answers."""
    if not isinstance(raw, dict) or set(raw.keys()) != {"answers"}:
        raise TypeError("root object must contain only 'answers'")

    values = raw["answers"]
    expected_ids = [q.internal_id for q in questions]
    if not isinstance(values, dict) or len(values) != len(expected_ids):
        raise TypeError("answers must contain every requested internal question id and no others")
    if any(qid not in values for qid in expected_ids):
        raise TypeError("answers must contain every requested internal question id and no others")

    answers = {}

    for question in questions:
        value = values[question.internal_id]

        if question.kind == "noul":
            answers[question.key] = {
                "type": "noul",
                "noul": _number_probability(value, question.internal_id),
            }
            continue

        probabilities = _normalize_distribution(value, len(question.choices), question.internal_id)
        probability_map = {label: probabilities[index] for index, (label, _) in enumerate(question.choices)}
        certainty = _confidence(probabilities)

        if question.kind == "choice":
            best = 0
            for index in range(1, len(probabilities)):
                if probabilities[index] > probabilities[best]:
                    best = index
            answers[question.key] = {
                "type": "choice",
                "choice": question.choices[best][0],
                "probabilities": probability_map,
                "confidence": certainty,
            }
        else:
            answers[question.key] = {
                "type": "score",
                "score": sum(index * probability_map[label] for index, (label, _) in enumerate(question.choices)),
                "legend": {str(index): item for index, item in enumerate(question.legend or [])},
                "probabilities": probability_map,
                "confidence": certainty,
            }

    return answers
