# SKILL: selena-anything
## Version: 1.0.0 | Score: 16/20 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L2b (IRIS/KRONOS/FLUX) | ternary_role: Obs

---

### CAPACITES
- [x] `snapshot` — Capture l'état sémantique courant → SemanticReport
- [x] `watch` — Mode continu, émet alertes sur drift (timeout 300s)
- [x] `diff` — Compare deux snapshots, détecte drift > threshold
- [x] `correlate` — Calcule corrélations inter-repos
- [x] `report` — Rapport consolidé ARGUS-compatible

### ENTREE
```json
{
  "target": "gerivdb|repo|org|watchlist|signal|all",
  "mode": "snapshot|watch|diff|correlate|report",
  "threshold": 0.05,
  "wal": true,
  "output": "json|text"
}
```

### SORTIE
```json
{
  "timestamp": "ISO-8601",
  "target": "string",
  "mode": "snapshot|watch|diff|correlate|report",
  "anomalies": [{"type": "str", "severity": "INFO|WARNING|CRITICAL", "detail": "str", "source": "str"}],
  "drifts": [{"target": "str", "phi_cps_delta": "float", "direction": "up|down|stable", "detail": "str"}],
  "correlations": [{"source": "str", "target": "str", "phi_cps": "float", "lag_ticks": "int"}],
  "phi_cps_score": "float",
  "metadata": {"repos_scanned": "int", "scan_duration_ms": "float", "version": "str", "argus_compatible": "bool"}
}
```

### GARANTIES
- [x] `--dry-run` disponible — aucun effet de bord
- [x] `--wal` écrit une entrée WAL JSONL
- [x] `--output json` retourne du JSON valide parseable
- [x] `validate_report()` vérifie la structure SemanticReport
- [x] Mode `watch` sans memory leak (> 1h via timeout 300s + iteration loop)
- [x] Sortie pipe-able vers `scan-anything`, `trace-anything`, `gate-anything`
- [x] ARGUS-compatible via `metadata.argus_compatible`

### DEPENDANCES
- Python 3.10+
- PyYAML
- ECOYSTEM (Selena engine — fallback simulé si absent)

### PIPES
```bash
# Export JSON vers ARGUS WAL
selena-anything report --target gerivdb --wal --output json

# Watch avec seuil custom
selena-anything watch --target gerivdb --threshold 0.1

# Corrélation inter-repos vers trace-anything
selena-anything correlate --target all --output json | trace-anything --mode causal

# Diff entre deux snapshots
selena-anything diff --target gerivdb --threshold 0.05
```

### EXEMPLES
```bash
# Snapshot sémantique de tout l'org
selena-anything snapshot --target gerivdb --output json

# Watch mode — détection drift temps réel
selena-anything watch --target gerivdb --threshold 0.05

# Rapport consolidé ARGUS
selena-anything report --target gerivdb --wal

# Dry-run (simulation)
selena-anything snapshot --target gerivdb --dry-run --output text

# Corrélations inter-repos
selena-anything correlate --target all
```

---
*IntentHash: 0xCTULU_SELENA_ANYTHING_20260612 | gerivdb/CTULU | Phase 7 | 2026-06-12*
