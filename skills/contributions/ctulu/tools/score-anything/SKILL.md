# score-anything — Interface ternaire −/○/+ vers FLUENCE

## Description

Interface ternaire `−/○/+` (négatif/neutre/positif) vers FLUENCE.
Transpose les scores de confiance (0.0–1.0) en notation ternaire
compatible avec le Chessboard V3 et le moteur FLUENCE Base-243.

## Usage

```bash
score-anything transpose  --value 0.8
score-anything fluence    --input scores.json --output fluence_export.yaml
score-anything thresholds --show
score-anything coherence   --scores-a sa.json --scores-b sb.json
```

## Seuils

- `< 0.33` → `−` (négatif)
- `0.33–0.66` → `○` (neutre)
- `≥ 0.66` → `+` (positif)

## Strate

L2/L3 hybride — transposition déterministe, zéro apprentissage.

---

*IntentHash: 0xCTULU_SCORE_ANYTHING_20260612*
*PRD: PRD-051-metacluster-chessboard-2026-06-06.md*
*[CONFORME_NEXUS]*
