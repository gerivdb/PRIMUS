# epic-anything v2 — Générateur Causal par EPIC

## Description
Générateur à conscience causale complète : chaque EPIC connaît l'écosystème entier.

## Usage
```bash
python epic_generator.py create --title "Mon EPIC" --slug mon-epic --theme governance
python epic_generator.py inspect --epic EPIC-249
python epic_generator.py validate --epic EPIC-249
```

## 6 Capacités v2
1. **auto_routing** — Consulte known_repositories.yaml (176 repos)
2. **strate_tagging** — Déduit L0→L9 depuis REGISTRY.yaml
3. **intent_hash** — Génère 0x[SLUG]_φ[X.XXX] unique
4. **dep_inference** — Analyse titres → deps probables
5. **phi_cps_estimate** — Calcule φ-CPS, bloque si < 4.559
6. **closes_tracking** — Détecte "remplace EPIC-XXX"

## Strate
L3 (DevTools) — générateur pur. Lecture L0+L1.
