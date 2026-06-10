---
id: PRD-003
title: Packaging Python — pyproject.toml et __init__.py racine
repo: gerivdb/PRIMUS
status: READY
priority: P0
created: 2026-06-10
author: gerivdb
consumers:
  - CTULU (imports Python depuis src/)
  - SKILLS (imports depuis skill_loader.py)
  - NEXUS (imports dans engines métier)
---

# PRD-003 — Packaging Python PRIMUS

## Contexte

PRIMUS n'a pas de `pyproject.toml`, de `setup.py`, ni de `__init__.py` à la racine. Il ne peut pas être importé comme package Python (`from primitives.parsing.repo_tree_parser import ...`) sans manipulation manuelle du `sys.path`. Les consommateurs CTULU, SKILLS, NEXUS doivent actuellement injecter le chemin manuellement dans leurs scripts.

## Problème

- `import primitives.parsing.repo_tree_parser` échoue si PRIMUS n'est pas installé.
- `pip install -e path/to/PRIMUS` est impossible sans `pyproject.toml`.
- Les tests GitHub Actions ne peuvent pas être configurés sans manifest de package.

## Objectif

1. Créer `pyproject.toml` minimal (PEP 517, `hatchling` ou `setuptools`).
2. Créer `primitives/__init__.py` racine.
3. Définir l'entrée de package `primus = "primitives"`.
4. Ajouter `requirements.txt` (PyYAML optionnel pour yaml_parser, jsonschema optionnel pour json_schema_validator).

## Critères d'acceptation

- [ ] `pyproject.toml` créé avec `name = "primus"`, `version = "0.1.0"`
- [ ] `primitives/__init__.py` créé
- [ ] `pip install -e .` fonctionne depuis le repo cloné
- [ ] `python -c "from primitives.parsing.repo_tree_parser import repo_tree_parser"` fonctionne
- [ ] `requirements-optional.txt` documentant PyYAML et jsonschema

## Effort estimé

~10 min
