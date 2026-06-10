---
id: PRD-004
title: Primitives comparison et deduction — backlog P3
repo: gerivdb/PRIMUS
status: DRAFT
priority: P3
created: 2026-06-10
author: gerivdb
consumers:
  - SKILLS (jurisdiction-checker → eligibility_deducer)
  - NEXUS (engines métier)
  - ONTOLOGY/primitives/ (specs académiques)
---

# PRD-004 — Primitives comparison et deduction

## Contexte

Les catégories `primitives/comparison/` et `primitives/deduction/` existent en tant que dossiers `.gitkeep` dans PRIMUS mais aucune primitive n'y est planifiée dans `CTULU/REGISTRY.yaml` à ce stade. Elles sont citées dans le README PRIMUS comme catégories futures consommées par SKILLS et NEXUS.

## Primitives candidates — comparison

| Primitive | Description | Consommateur pressenti |
|---|---|---|
| `diff_dict` | Diff structurel de deux dicts Python | SKILLS/skill_registry |
| `similarity_score` | Score de similarité textuelle (0–1, Jaccard ou Levenshtein stdlib) | NEXUS/matching engines |
| `jurisdiction_checker` | Vérifie si un repo/tool appartient à un périmètre déclaré | SKILLS/VERSEContext |

## Primitives candidates — deduction

| Primitive | Description | Consommateur pressenti |
|---|---|---|
| `eligibility_deducer` | Déduit si un objet satisfait un ensemble de règles déclaratives | SKILLS/skill_loader |
| `classifier_primitive` | Classifie un objet dans une taxonomie déclarative | ONTOLOGY/primitives |

## Critères d'acceptation (quand activé)

- [ ] Chaque primitive : ≤ 100 lignes, stateless, stdlib uniquement
- [ ] 1 test unitaire minimum par primitive
- [ ] Schema contract JSON associé
- [ ] Déclarée dans `CTULU/REGISTRY.yaml` si consommée par un tool CTULU

## Note

Ce PRD est en DRAFT — aucune implémentation tant que les P0/P1 ne sont pas clos. À activer quand un consommateur concret émerge.

## Effort estimé

~2h (quand activé)
