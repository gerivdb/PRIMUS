---
id: PRD-001
title: Primitives parsing manquantes — yaml_parser et text_line_parser
repo: gerivdb/PRIMUS
status: READY
priority: P0
created: 2026-06-10
author: gerivdb
consumers:
  - CTULU/watchlist-router       # yaml_parser
  - CTULU/keel-adapter           # text_line_parser
  - CTULU/iris-adapter           # yaml_parser
linked_backlog: CTULU/REGISTRY.yaml champ primitives:
---

# PRD-001 — Primitives parsing manquantes

## Contexte

`CTULU/REGISTRY.yaml` déclare `yaml_parser` (consommé par watchlist-router et iris-adapter) et `text_line_parser` (consommé par keel-adapter) comme dépendances PRIMUS. Ces deux primitives sont absentes de `primitives/parsing/`. La chaîne CTULU → PRIMUS est donc déclarative mais non exécutable pour ces tools.

## Problème

- `watchlist-router` et `iris-adapter` ne peuvent pas traiter les fichiers `.yaml` sans parser atomique.
- `keel-adapter` ne peut pas lire les `.keel` (format lignes taguées) sans `text_line_parser`.
- Le contrat PRIMUS (stdlib only, stateless, < 100 lignes) n'est pas respecté tant que les tools appellent `yaml.safe_load` directement sans passer par une primitive nommée.

## Objectif

Fournir deux primitives exécutables dans `primitives/parsing/` :

### yaml_parser

```
Input  : content: str (contenu YAML brut)
Output : Dict | List (objet Python parsé)
Fallback : ValueError si YAML invalide
Deps   : PyYAML (stdlib fallback : json si YAML simple)
```

### text_line_parser

```
Input  : content: str, comment_char: str = "#", strip: bool = True
Output : List[str]  (lignes non vides, non commentées)
Deps   : stdlib uniquement
```

## Critères d'acceptation

- [ ] `primitives/parsing/yaml_parser.py` — ≤ 60 lignes
- [ ] `primitives/parsing/text_line_parser.py` — ≤ 40 lignes
- [ ] `primitives/parsing/__init__.py` exporté mis à jour
- [ ] `tests/test_yaml_parser.py` — ≥ 5 tests (valid, invalid, empty, list root, nested)
- [ ] `tests/test_text_line_parser.py` — ≥ 4 tests (comments, empty lines, strip, unicode)
- [ ] `schemas/yaml_parser.contract.json` créé
- [ ] `schemas/text_line_parser.contract.json` créé

## Impact aval

Débloquer CTULU : `watchlist-router`, `iris-adapter`, `keel-adapter` peuvent être implémentés.

## Effort estimé

~30 min
