#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Primitive : intent_hash_gen
Catégorie : validation
Spec      : ONTOLOGY/primitives/ (voir schema ci-dessous)

Responsabilité unique :
  Génère un IntentHash valide à partir d'un slug humain.
  Vérifie l'unicité contre les hashes existants dans le dossier INTENTS/.

Contrat :
  - Input  : slug: str (ex: "INTENT-MCP-SYNAPTIC-ECOSYSTEM-VISION-20260819_v10")
  - Output : IntentHash  (str, format 0xSLUG_MAJUSCULES)
  - Collision detection: oui
  - Side effects: none
  - Dependances: stdlib uniquement
"""
import os
import re
from pathlib import Path


def slug_to_intent_hash(slug: str) -> str:
    """
    Convertit un slug en IntentHash valide.
    Règles:
      - Supprime les caractères non alphanumériques
      - Uppercase
      - Préfixe 0x
    """
    cleaned = re.sub(r"[^a-zA-Z0-9_-]", "", slug).upper()
    if not cleaned:
        raise ValueError(f"Slug vide après nettoyage: {slug!r}")
    return f"0x{cleaned}"


def check_collision(intent_hash: str, intents_dir: str | Path) -> bool:
    """
    Vérifie que l'IntentHash n'existe pas déjà dans intents_dir.
    Retourne True si collision, False sinon.
    """
    intents_path = Path(intents_dir)
    if not intents_path.exists():
        return False
    for md_file in intents_path.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        if f"intent_hash: {intent_hash}" in content:
            return True
    return False


def generate_intent_hash(
    slug: str,
    intents_dir: str | Path = "INTENTS",
) -> str:
    """
    Génère un IntentHash unique pour un nouveau INTENT.
    Lève ValueError si collision détectée.
    """
    intent_hash = slug_to_intent_hash(slug)
    if check_collision(intent_hash, intents_dir):
        raise ValueError(
            f"Collision IntentHash: {intent_hash} existe déjà dans {intents_dir}"
        )
    return intent_hash


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python intent_hash_gen.py <slug> [intents_dir]")
        sys.exit(1)
    slug = sys.argv[1]
    intents_dir = sys.argv[2] if len(sys.argv) > 2 else "INTENTS"
    try:
        ih = generate_intent_hash(slug, intents_dir)
        print(ih)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
