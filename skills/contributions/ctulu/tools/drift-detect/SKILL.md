# SKILL: drift-detect
## Version: 1.0.0 | Score: 0/20 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: [Obs, C]

---

### CAPACITES
- [ ] `detect-structural-drift` — Find added/removed edges and nodes between DAGs
- [ ] `detect-strength-drift` — Find edges whose causal strength changed significantly
- [ ] `detect-predictive-drift` — Compare predictions to actual observations
- [ ] `detect-nodal-drift` — Identify new or disappeared nodes
- [ ] `generate-alerts` — Produce severity-graded alerts with recommendations

### ENTREE
```json
{"dag_ref": "path", "dag_current": "path", "predictions": "path|null"}
```

### SORTIE
```json
{"drift_report": {"overall_drift_score": float, "drift_detected": bool, "categories": {}, "alerts": []}}
```

### GARANTIES
- [OK] READ-ONLY on both DAGs
- [OK] Drift score 0.0 (stable) to 1.0 (total drift)
- [OK] `--dry-run` available
- [OK] WAL entry emitted if `--wal`
- [OK] Triggers learn-anything (PRD-051) when significant

### DEPENDANCES
- Python 3.10+, pyyaml
- cause-anything (PRD-045) for DAG input

### EXEMPLES
```bash
drift-detect --dag-ref dag_v1.json --dag-current dag_v2.json
drift-detect --dag-ref ref.json --dag-current cur.json --predictions pred.json
```

---
*gerivdb/CTULU | [CONFORME_NEXUS] | IntentHash: 0xDRIFT_DETECT_20260612*
