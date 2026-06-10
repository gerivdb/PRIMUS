---
id: PRD-000
title: Index des PRD PRIMUS
repo: gerivdb/PRIMUS
created: 2026-06-10
author: gerivdb
---

# PRD PRIMUS — Index

> Chaque PRD couvre un gap identifié lors de l'audit écosystème du 2026-06-10.
> Les PRD sont prioritisés P0 (bloquant) → P3 (future).

| PRD | Titre | Priorité | Statut |
|---|---|---|---|
| [PRD-001](PRD-001-primitives-parsing-missing.md) | yaml_parser + text_line_parser manquants | P0 | READY |
| [PRD-002](PRD-002-primitive-formatting-compound-node.md) | compound_node_formatter | P0 | READY |
| [PRD-003](PRD-003-package-setup.md) | pyproject.toml + packaging Python | P0 | READY |
| [PRD-004](PRD-004-primitives-comparison-deduction.md) | comparison + deduction (backlog) | P3 | DRAFT |

## Dépendances aval

```
PRD-001 + PRD-002 → débloquent CTULU PRD-002 et PRD-003
PRD-003           → débloque imports SKILLS et NEXUS
PRD-004           → activé par besoin consommateur
```

## Liens écosystème

- [CTULU/REGISTRY.yaml](https://github.com/gerivdb/CTULU/blob/main/REGISTRY.yaml)
- [SKILLS/ctulu_resolver.py](https://github.com/gerivdb/SKILLS/blob/main/ctulu_resolver.py)
- [VERSES/WorkflowVerse/workflow_executor.py](https://github.com/gerivdb/VERSES/blob/main/WorkflowVerse/workflow_executor.py)
