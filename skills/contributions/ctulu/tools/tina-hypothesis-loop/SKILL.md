# tina-hypothesis-loop — Validation neurosymbolique

## Description

Génère des hypothèses à partir du DAG causal, les valide contre les données
observées, et produit un rapport CONFIRMED / UNCERTAIN / REFUTED.

## Usage

```bash
tina-hypothesis-loop generate  --dag dag.json
tina-hypothesis-loop validate  --dag dag.json --hypotheses hypotheses.yaml
tina-hypothesis-loop report    --dag dag.json --output report.yaml
tina-hypothesis-loop status    --dag dag.json
```

## Statuts

- **CONFIRMED** : Poids d'arête ≥ 0.7 — hypothèse validée
- **UNCERTAIN** : Poids 0.3–0.7 — données insuffisantes
- **REFUTED** : Poids < 0.3 — hypothèse contredite

## Strate

L2/L3 hybride — raisonnement symbolique (L2) + données causales (L3).

---

*IntentHash: 0xCTULU_TINA_HYPOTHESIS_LOOP_20260613*
*PRD: PRD_TINAHypothesisLoop_v100.md*
*[CONFORME_NEXUS]*
