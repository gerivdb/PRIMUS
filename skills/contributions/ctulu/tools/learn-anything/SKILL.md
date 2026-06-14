# SKILL: learn-anything
## Version: 1.0.0 | Score: 0/20 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: [C, Obs]

---

### CAPACITES
- [ ] `update-dag` — Correct DAG edge strengths from drift report
- [ ] `apply-strength-drift` — Bounded adjustment of edge weights
- [ ] `handle-structural-drift` — Mark obsolete edges, propose new edges (HITL)
- [ ] `ontology-gate` — Reject changes violating ONTOLOGY hard constraints

### ENTREE
```json
{"dag": "path", "drift_report": "path", "learning_rate": 0.3}
```

### SORTIE
```json
{"changes_applied": [], "changes_rejected": [], "hitl_proposals": [], "requires_hitl": bool, "dag_diff": {}}
```

### GARANTIES
- [OK] Only tool that writes to DAG (with forget-anything)
- [OK] No write without drift report trigger
- [OK] Bounded changes (max_edge_delta)
- [OK] HITL required for structural changes
- [OK] ONTOLOGY constraints inviolable
- [OK] Full traceability (WAL + dag_diff)

### DEPENDANCES
- Python 3.10+, pyyaml
- drift-detect (PRD-050) for drift report input

### EXEMPLES
```bash
learn-anything --dag dag.json --drift-report drift.json --learning-rate 0.3
learn-anything --dag dag.json --drift-report drift.json --validation-mode hitl
```

---
*gerivdb/CTULU | [CONFORME_NEXUS] | IntentHash: 0xLEARN_ANYTHING_20260612*
