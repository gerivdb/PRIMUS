#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : extract_json
Catégorie : logic
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Extrait un objet JSON d'une chaîne brute.
"""
from __future__ import annotations

import json
from typing import Any


def extract_json(text: str) -> dict[str, Any]:
    """Extrait un objet JSON d'une chaîne brute."""
    candidate = text.strip()
    if candidate.startswith("```"):
        candidate = candidate[3:]
        if candidate.lower().startswith("json"):
            candidate = candidate[4:]
        candidate = candidate.strip()
        if candidate.endswith("```"):
            candidate = candidate[:-3].strip()
    start = candidate.find("{")
    if start < 0:
        raise SyntaxError("response contains no JSON object")
    decoder = json.JSONDecoder()
    try:
        return decoder.raw_decode(candidate, start)[0]
    except Exception as exc:
        raise SyntaxError(f"invalid JSON: {exc}") from exc
