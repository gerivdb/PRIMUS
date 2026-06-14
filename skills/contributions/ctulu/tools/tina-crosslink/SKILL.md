# tina-crosslink — TINA Crosslink

## Description

Intégration TINA (SymbolGraph) avec les 12 outils causaux.
`detect_transpositions()` identifie les patterns récurrents entre les outils.

## NodeType CAUSAL_TOOL

Les 12 outils causaux sont enregistrés comme `NodeType.CAUSAL_TOOL` dans le
SymbolGraph TINA, avec les transitions ternaires (−1, 0, +1).

## Usage

```bash
tina-crosslink detect  --dag dag.json --tools cause-anything,drift-detect
tina-crosslink audit   --dag dag.json
tina-crosslink report  --dag dag.json --output report.yaml
tina-crosslink validate --dag dag.json
```

## Patterns détectés

- `predict→drift→learn` — Boucle de correction prédictive
- `trace→intervene→observe` — Chaîne d'intervention causale
- `simulate→plan→act` — Pipeline de planification
- `cause→trace→intervene→act→observe` — Boucle causale complète

## Strate

P1 — Infrastructure causale transverse.

---

*IntentHash: 0xCTULU_TINA_CROSSLINK_20260612*
*PRD: PRD-049-mc-rnn-architecture-2026-06-07.md*
*[CONFORME_NEXUS]*
