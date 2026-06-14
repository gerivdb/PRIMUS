# batch-anything — Orchestrateur Holographique de Batch

## Description
Génère des batches d'EPICs complets avec conscience causale de l'écosystème entier.
6 étapes algorithmiques : LOAD → SNAP → HASH → DAG → DELTA → EMIT.

## Usage
```bash
# Générer un batch
python batch_orchestrator.py generate \
  --theme-map theme.yaml \
  --known-repos known_repositories.yaml \
  --out ./batch_output/

# Valider (dry-run)
python batch_orchestrator.py validate --batch-dir ./batch_output/

# Push simulé
python batch_orchestrator.py push --batch-dir ./batch_output/
```

## 6 Étapes

1. **LOAD** — Charge `known_repositories.yaml` (176 repos) → résout `repo_cible`
2. **SNAP** — NEXUS snapshot J0 → détecte EPICs draft/closes
3. **HASH** — Génère IntentHash `0x[SLUG]_φ[X.XXX]` → vérifie unicité
4. **DAG** — Construit `dep_graph.yaml` → détecte cycles → déduit `execution_order`
5. **DELTA** — Génère `index_cleanup_delta.yaml` (EPICs à fermer)
6. **EMIT** — Produit EPICs complets + artefacts batch

## Outputs
- `EPIC-NNN-slug.md` — EPICs avec frontmatter complet
- `dep_graph.yaml` — DAG du batch
- `execution_order.yaml` — Séquence parallélisation
- `index_cleanup_delta.yaml` — EPICs originaux à fermer
- `batch_manifest.yaml` — Résumé stats + gates

## Dépendances
- `dag-anything` : construction DAG
- `phi-anything` : calcul φ-CPS
- `batch-governor` : GATE-0→4

## Strate
L3 (DevTools) — automatisation pur. Sources : L0 (GOVERNANCE-HUB), L1 (NEXUS).
