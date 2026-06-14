# SKILL: intervene-anything
## Version: 1.0.0 | Score: 0/20 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: [Obs, C]

---

### CAPACITES
- [ ] `do-calculus` — Simulate do(X=x) by cutting incoming edges to target node
- [ ] `propagate-effects` — Monte Carlo propagation of intervention downstream
- [ ] `compare-obs-vs-inter` — Compute observational vs interventional distributions
- [ ] `sensitivity-analysis` — Rank downstream nodes by sensitivity to intervention

### ENTREE
```json
{"dag": "path", "target_node": "id", "forced_value": "any", "intervention_type": "hard|soft"}
```

### SORTIE
```json
{"intervention_report": {"target": "id", "do_distribution": [], "comparison": {}, "sensitivity": [], "overall_confidence": float}}
```

### GARANTIES
- [OK] READ-ONLY — simulation only, no real state modified
- [OK] DAG required (from cause-anything)
- [OK] Cut edges explicitly listed in output
- [OK] Delta = causal effect pure (deconfounded)
- [OK] `--dry-run` available
- [OK] WAL entry emitted if `--wal`

### DEPENDANCES
- Python 3.10+, pyyaml
- cause-anything (PRD-045) for DAG input

### EXEMPLES
```bash
intervene-anything --dag dag.json --target-node PR_size --forced-value 0.3 --hard
intervene-anything --dag dag.json --target-node HITL_gate --forced-value 1.0 --effect-nodes phi_CPS
```

---
*gerivdb/CTULU | [CONFORME_NEXUS] | IntentHash: 0xINTERVENE_ANYTHING_20260612*
