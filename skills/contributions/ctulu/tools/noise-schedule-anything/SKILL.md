# noise-schedule-anything — Adaptive Pass Scheduler

## Description

Inspiré du **Scheduler** de DiffusionGemma [Ch.5], implémente un scheduler
de passes adaptatif pour les batches CTULU. Alloue dynamiquement les passes
par entité en fonction de φ-CPS.

## Schedule types

| Type | Comportement | Analogue |
|------|-------------|----------|
| `linear` | N passes fixe (legacy) | Steps fixes |
| `cosine` | Décroissance cosinus | Cosine noise schedule |
| `adaptive` | Passes ∝ 1/confiance (φ-CPS) | Adaptive stopping |
| `entropy` | Arrêt si H(drift) < ε | Entropy-bounded |

## Formule (mode adaptive)

```
passes_i = max(1, round(N_max × (1 - φ_CPS_i / 10)))
T_k = T_0 × cos(π/2 × k/passes_i)
```

## Usage

```bash
noise-schedule-anything plan     --batch batch-13 --mode adaptive
noise-schedule-anything execute  --batch batch-13 --schedule plan.yaml
noise-schedule-anything report   --batch batch-13
noise-schedule-anything calibrate --history batch-10,batch-11,batch-12
```

## Strate

L3 — scheduler pur, zéro dépendance externe, zéro GPU.

---

*IntentHash: 0xCTULU_NOISE_SCHEDULE_ANYTHING_φ6.098*
*PRD: PRD-054-v1-noise-schedule-anything.md*
*[CONFORME_NEXUS]*
