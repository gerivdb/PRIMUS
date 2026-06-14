# SKILL: alfred-anything
## Version: 1.0.0 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: C

---

### CAPACITES
- [x] `plan` — Génère un plan d'exécution ordonné topologiquement
- [x] `critical-path` — Identifie le chemin critique (longest path)
- [x] `unblock` — Propose résolution pour dépendances bloquées
- [x] `simulate` — Simule l'impact d'un retard sur le plan
- [x] `gantt` — Génère diagramme Gantt Mermaid

### ENTREE
```bash
alfred-anything --target <epic|adr|milestone|graph> \
                --mode plan|critical-path|unblock|simulate|gantt \
                [--horizon <days>] [--dry-run] [--wal] [--output json|gantt|text]
```

### SORTIE
```json
{
  "status": "ok|error",
  "plan": { "target": "...", "steps": [...], "critical_path": [...], "blockages": [...] },
  "wal_entry": "path|null"
}
```

### GARANTIES
- [OK] `--dry-run` disponible — aucun effet de bord
- [OK] `--output json` retourne JSON valide parseable
- [OK] `--output gantt` produit Mermaid renderable
- [OK] Idempotent en mode dry-run
- [OK] WAL entry émise si `--wal`
- [OK] Topological sort avec détection de cycles
- [OK] Critical path via longest path DAG

### DEPENDANCES
- Python 3.10+
- PyYAML (pour graph files YAML)

### EXEMPLES
```bash
# Plan pour un EPIC
python -m alfred_anything --target EPIC-024 --mode plan --output json

# Chemin critique
python -m alfred_anything --target EPIC-024 --mode critical-path

# Déblocage
python -m alfred_anything --target EPIC-024 --mode unblock

# Simulation de retard
python -m alfred_anything --target EPIC-024 --mode simulate --delay 5

# Gantt Mermaid
python -m alfred_anything --target EPIC-024 --mode gantt --output gantt
```

### FONCTEUR
```
F: C(dependency_graph) → C(execution_plan) ∘ Obs(bottleneck_report)
```

Alfred est C primaire : il ne modifie jamais les artefacts,
ne fait que calculer et ordonner.

---
*IntentHash: 0xCTULU_ALFRED_ANYTHING_20260612 | gerivdb/CTULU | Phase 7 | 2026-06-12*
