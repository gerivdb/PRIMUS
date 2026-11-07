#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : yaml_parser
Catégorie : parsing
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Parse un contenu YAML brut en objet Python (dict ou list).

Contrat :
  - Input  : content: str (contenu YAML brut)
  - Output : Dict | List (objet Python parsé)
  - Effets de bord : aucun
  - Dépendances : stdlib uniquement
"""

import json
from typing import Any, Union


def yaml_parser(content: str) -> Union[dict, list]:
    """Parse un contenu YAML brut en objet Python (dict ou list).

    Args:
        content: Contenu YAML brut à parser.

    Returns:
        Objet Python parsé (dict ou list).

    Raises:
        ValueError: Si le contenu n'est ni du JSON valide ni du YAML simple supporté.
    """
    stripped = content.strip()
    if not stripped:
        return {}

    # Tentative JSON (sous-ensemble de YAML, stdlib uniquement)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass

    # Parser YAML minimaliste (clé:valeur, listes de premier niveau, scalaires)
    lines = [
        l for l in stripped.split("\n")
        if l.strip() and not l.strip().startswith("#")
    ]
    if not lines:
        return {}

    if all(l.lstrip().startswith("- ") for l in lines):
        return [_parse_scalar(l.lstrip()[2:].strip()) for l in lines]

    result: dict = {}
    for line in lines:
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        if not key:
            raise ValueError(f"Clé vide invalide dans la ligne: {line}")
        result[key] = _parse_scalar(value.strip()) if value.strip() else {}

    return result


def _parse_scalar(value: str) -> Any:
    """Convertit une chaîne en scalaire Python (bool, null, number, str)."""
    low = value.lower()
    if low in {"true", "false"}:
        return low == "true"
    if low in {"null", "~", ""}:
        return None
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        pass
    if (value.startswith('"') and value.endswith('"')) or \
       (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value
