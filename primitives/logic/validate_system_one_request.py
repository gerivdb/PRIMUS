#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : validate_system_one_request
Catégorie : logic
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Valide qu'une requête System-1 contient les champs requis.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ValidationResult:
    valid: bool = True
    error_count: int = 0
    errors: list[str] | None = None


def validate_system_one_request(request: dict[str, Any]) -> ValidationResult:
    """Valide une requête System-1."""
    errors: list[str] = []
    if "questions" not in request:
        errors.append("missing questions")
    if "state" not in request:
        errors.append("missing state")
    questions = request.get("questions")
    if not isinstance(questions, dict):
        errors.append("questions must be an object")
    return ValidationResult(
        valid=len(errors) == 0,
        error_count=len(errors),
        errors=errors,
    )
