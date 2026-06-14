# index-anything v2 — Index Vivant Auto-Synchronisé

## Description
L'index est une **vue calculée**, pas un document à maintenir. Source de vérité = git log + frontmatters.

## Usage
```bash
python index_sync.py sync --repo gerivdb/GOVERNANCE-HUB
python index_sync.py audit --retroactive --since EPIC-109
python index_sync.py status --format matrix
python index_sync.py orphan --report
python index_sync.py roadmap-sync
```

## 5 Capacités v2
1. **auto_close** — Détecte `closes:` → statut completed
2. **status_matrix** — % completed par thème/batch/strate
3. **orphan_detection** — EPICs absents de l'index
4. **retroactive_audit** — Reconstruction depuis git log
5. **roadmap_sync** — Cascade vers ROADMAP.md

## Strate
L3 (DevTools) — lecture/écriture L0.
