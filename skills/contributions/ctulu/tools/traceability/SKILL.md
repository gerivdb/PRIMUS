# SKILL.md — Traceability Chain Manager

## Description

Outil de traçabilité industrielle pour la chaîne **INTENT → PRD → EPIC → TASK** du métacluster gerivdb.

Fonctionnalités :
- **Build** : Parse les artefacts depuis le filesystem et construit le graphe de traçabilité
- **Validate** : Vérifie la cohérence (orphelins, liens cassés, incohérences de statut, collisions)
- **Drift** : Détecte les dérives (frontmatter decay, violations de schéma, modifications terminales)
- **Rollback** : Snapshots + restore avec garde-fous anti-destruction
- **Graph** : Export JSON/DOT/HTML du graphe
- **Metrics** : Métriques de couverture, orphan rate, broken link rate, drift score
- **Snapshot** : Création manuelle de snapshots

## Utilisation

```bash
# Construire le graphe
python -m traceability build --roots D:\DevTools D:\DO\WEB --output .traceability/graph.json

# Valider la cohérence
python -m traceability validate --graph .traceability/graph.json

# Détecter les dérives
python -m traceability drift --graph .traceability/graph.json --report drift.json

# Statut d'une chaîne
python -m traceability status --intent 0xDIFFUSION_GEMMA_METACLUSTER_TRANSPOSITION_φ9.221 --tree

# Métriques
python -m traceability metrics --graph .traceability/graph.json

# Exporter en DOT (Graphviz)
python -m traceability graph --format dot --output traceability.dot

# Snapshot
python -m snapshot --label "pre-deployment"

# Rollback d'un artefact
python -m traceability rollback --artifact EPIC-001 --dry-run
python -m traceability rollback --intent 0xHASH --force --cascade
```

## IntentHash

`0xTRACEABILITY_TOOL_20260614`
