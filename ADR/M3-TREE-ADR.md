---
type: STD
status: proposed
date: "2026-11-23"
intent_hash: 0xSTD_M3_TREE_ADR_PRIMUS_20261123
repo: PRIMUS
stratum: L4-TOOLS
topos_node: L4-TOOLS
---

# M3 TREE ADR — Dépôt PRIMUS (L4-TOOLS)

## Objectif
Indexer tous les ADR du dépôt PRIMUS dans une structure arborescente topologique (M3 TREE) à 5 niveaux, permettant de détecter les contradictions, dépendances et conflits entre ADR avant validation.

TOPOS (L1-INFRA) est la cartographie de référence. Ce M3 TREE s'appuie sur TOPOS comme fondement topologique et ne crée pas de carte parallèle.

## Structure topologique

```
M3 TREE ADR — PRIMUS (L4-TOOLS)
│
├─ NIVEAU 1 — REPO : PRIMUS
│  └─ Strate : L4-TOOLS
│  └─ Nœud TOPOS : L4-TOOLS / PRIMUS
│
├─ NIVEAU 2 — STRATE : L4-TOOLS
│  └─ Dépendance : GOVERNANCE-HUB (L0-CANON, SOT known_repositories.yaml)
│
├─ NIVEAU 3 — ÉCOSYSTÈME LOCAL (ENV2 global)
│  └─ M3-BRANCH central : GOVERNANCE-HUB
│
├─ NIVEAU 4 — MULTI ENV2-ENV3 (hybride ENV2 ↔ ENV3)
│  └─ Aucun ADR transverse identifié à ce stade
│
└─ NIVEAU 5 — MULTI-ENV (ENV6 et autres ENV)
   └─ Aucun ADR transverse identifié à ce stade

## Index des ADR (niveau 1 — dépôt PRIMUS)

Aucun ADR trouvé dans ce dépôt. Dispensé de M3 TREE détaillé jusqu'à création du premier ADR, conformément à la norme STD-M3-TREE-ADR-REPO (section 5).

## Règles de cohérence (gardiens CHECK / G-PROOF)

1. **Fibrosité** : tout ADR futur dans PRIMUS doit être rattaché à un nœud TOPOS (L4-TOOLS).
2. **Pas de doublon d'intent_hash** : avant création d'un nouvel ADR dans PRIMUS, vérifier qu'aucun ADR des autres dépôts ne couvre le même intent_hash.
3. **Statut de propagation** : un ADR `accepted` dans GOVERNANCE-HUB (niveau 3) s'impose à PRIMUS (niveau 1, strate L4-TOOLS) en cas de conflit.
4. **Vérification pré-commit** : tout nouveau ADR dans PRIMUS doit être indexé dans ce M3 TREE avant commit.

## Statut
proposed — en attente de validation HITL architecte

## Référence
- **STD** : STD-M3-TREE-ADR-REPO (REPO-STANDARDS/standards/, accepté `d03f735`)
- **ADR** : ADR-M3-TREE-ADR-COHERENCE (GOVERNANCE-HUB/ADR/, accepté `f6e71055`)
- **Dépôt** : PRIMUS (L4-TOOLS) / ADR/
- **IntentHash** : 0xSTD_M3_TREE_ADR_PRIMUS_20261123
