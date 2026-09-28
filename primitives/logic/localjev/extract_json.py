#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : extract_json
Catégorie : logic/localjev
Spec      : PRIMUS primitive contract

Responsabilité unique :
  Extrait un objet JSON d'une chaine brute, en gerant les blocs markdown.

Contrat :
  - Input  : text: str
  - Output : dict
  - Side effects: none
  - Dépendances: stdlib uniquement
"""
import json
import re


def extract_json(text: str) -> dict:
    """Extract a JSON object from raw text."""
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
        raise ValueError("response contains no JSON object")

    depth = 0
    quoted = False
    escaped = False

    for index in range(start, len(candidate)):
        character = candidate[index]

        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
            continue

        if character == '"':
            quoted = True
        elif character == "{":
            depth += 1
        elif character == "}" and depth == 1:
            return json.loads(candidate[start : index + 1])
        elif character == "}":
            depth -= 1

    raise ValueError("response contains an incomplete JSON object")


if __name__ == "__main__":
    import json as json_module
    import sys

    text = sys.stdin.read() if not sys.stdin.isatty() else ""
    try:
        result = extract_json(text)
        print(json_module.dumps(result, indent=2))
        sys.exit(0)
    except ValueError as e:
        print(json_module.dumps({"error": str(e)}, indent=2))
        sys.exit(1)
