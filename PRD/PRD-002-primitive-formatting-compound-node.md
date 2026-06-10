---
id: PRD-002
title: Primitive formatting — compound_node_formatter
repo: gerivdb/PRIMUS
status: READY
priority: P0
created: 2026-06-10
author: gerivdb
consumers:
  - CTULU/keel-adapter
  - CTULU/gitnote-adapter
linked_backlog: CTULU/REGISTRY.yaml champ primitives:
---

# PRD-002 — Primitive formatting manquante : compound_node_formatter

## Contexte

`CTULU/REGISTRY.yaml` déclare `compound_node_formatter` comme dépendance PRIMUS pour `keel-adapter` et `gitnote-adapter`. Ces deux adapters produisent des `CompoundNode[]` (structure JSON pour le dag-navigator). La primitive `primitives/formatting/` est entièrement vide (`.gitkeep`).

## Problème

Sans cette primitive, les adapters CTULU ne peuvent pas sérialiser leur output vers un format `CompoundNode` standardisé, ce qui rend impossible l'intégration avec `dag-navigator` (frontend Cytoscape.js).

## Définition d'un CompoundNode

```json
{
  "id": "string (unique)",
  "label": "string",
  "parent": "string | null",
  "type": "cluster | leaf | gateway",
  "meta": {}
}
```

## Objectif

```
Input  : id: str, label: str, node_type: str,
         parent: Optional[str] = None, meta: Dict = {}
Output : Dict  (CompoundNode JSON-serializable)
Deps   : stdlib uniquement
```

Fonctions complémentaires :
- `format_compound_nodes(items: List[Dict]) -> List[Dict]` — batch
- `validate_compound_node(node: Dict) -> bool` — vérifie les champs obligatoires

## Critères d'acceptation

- [ ] `primitives/formatting/compound_node_formatter.py` — ≤ 70 lignes
- [ ] `primitives/formatting/__init__.py` créé
- [ ] `tests/test_compound_node_formatter.py` — ≥ 5 tests
- [ ] `schemas/compound_node_formatter.contract.json` créé
- [ ] Output JSON-serializable (pas de types Python custom non sérialisables)

## Impact aval

Débloquer CTULU : `keel-adapter` et `gitnote-adapter` peuvent être implémentés et produire des `CompoundNode[]` consommables par `dag-navigator`.

## Effort estimé

~25 min
