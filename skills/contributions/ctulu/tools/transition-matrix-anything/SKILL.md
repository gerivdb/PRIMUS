# transition-matrix-anything — CTMC Lifecycle Predictor

## Description

Inspiré des **matrices de transition Qt** de DiffusionGemma [Ch.3], construit la
matrice de transition empirique Q des états lifecycle à partir de l'historique
git/GitHub, puis prédit la probabilité d'atteindre un état cible en N jours.

## États lifecycle

`draft → proposed → accepted → deprecated → superseded`
`planned → active → done`
`stale`, `blocked` (états transitoires)

## Usage

```bash
# Construire la matrice depuis un répertoire
transition-matrix-anything build --repo gerivdb/GOVERNANCE-HUB --window 90d

# Prédire une transition
transition-matrix-anything predict --entity ADR-064 --target accepted --horizon 14d

# Auditer les anomalies
transition-matrix-anything audit --anomaly-threshold 0.05

# Exporter la matrice
transition-matrix-anything matrix --format yaml
transition-matrix-anything heatmap --format mermaid
```

## Output

Le rapport inclut la matrice Q, les prédictions par entité, les anomalies
détectées, et le score `ecosystem_flow_health` (0=bloqué, 1=fluide).

## Strate

L2/L3 hybride — modélisation probabiliste (L2) + collecte données git (L3).
Algorithme matriciel pur, local, zéro GPU.

---

*IntentHash: 0xCTULU_TRANSITION_MATRIX_ANYTHING_φ7.104*
*PRD: PRD-051-v1-transition-matrix-anything.md*
*[CONFORME_NEXUS]*
