# moe-router-anything — Intent-Driven Tool Router

## Description

Inspiré du **MoE Router** de Gemma 4 [DiffusionGemma Ch.4], implémente un
routeur d'intent → sous-ensemble d'outils. Donné un intent CTULU, sélectionne
automatiquement les K outils à activer (K << 55).

## Architecture

```
Intent → [Intent Classifier] → vecteur de features
       → [MoE Router — scoring] → top-K tools
       → [Dependency Resolver] → ajoute les deps obligatoires
       → batch-governor GATE-0 → exécution ordonnée
```

## Usage

```bash
moe-router-anything route   --intent "auditer drift ADRs" --k 5
moe-router-anything route   --intent INTENT-002 --k 8
moe-router-anything explain --intent "analyser batch" --verbose
moe-router-anything calibrate --history batch-11,batch-12
moe-router-anything dry-run --intent INTENT-002
```

## Contraintes

- K configurable de 1 à 15 (plafond mémoire batch-governor)
- Jamais activer > 15 outils simultanément
- Le router lui-même est toujours exclu de la sélection

## Strate

L2/L3 hybride — logique de routing et scoring (L2) + exécution (L3).
Algorithme vectoriel pur, zéro GPU, zéro API externe.

---

*IntentHash: 0xCTULU_MOE_ROUTER_ANYTHING_φ7.445*
*PRD: PRD-053-v1-moe-router-anything.md*
*[CONFORME_NEXUS]*
