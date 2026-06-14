# SKILL: plan-anything
## Version: 1.0.0 | Score: 0/20 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: [C, Obs]

---

### CAPACITES
- [ ] `generate-plan` — Produce sequential action plan to reach goal state
- [ ] `rank-actions` — Rank interventions by causal impact on target
- [ ] `add-hitl-gates` — Mark irreversible steps as HITL gates
- [ ] `add-rollback` — Attach rollback plan to each step
- [ ] `add-abort-conditions` — Define plan abort triggers
- [ ] `simulate-plan` — Monte Carlo estimate of plan success probability

### ENTREE
```json
{"dag": "path", "goal_node": "id", "goal_value": float, "deadline": "30d"}
```

### SORTIE
```json
{"plan": {"id": "str", "goal": "str", "steps": [], "hitl_gates": [], "abort_conditions": [], "simulation_results": {}}}
```

### GARANTIES
- [OK] READ-ONLY — no real state modified
- [OK] HITL gates at all irreversible points
- [OK] Rollback plan for every step
- [OK] Abort conditions explicit
- [OK] Success probability from Monte Carlo
- [OK] WAL entry emitted if `--wal`

### DEPENDANCES
- Python 3.10+, pyyaml
- cause-anything (PRD-045), predict-anything (PRD-048), intervene-anything (PRD-046)

### EXEMPLES
```bash
plan-anything --dag dag.json --goal-node phi_CPS --goal-value 0.8 --deadline 30d
plan-anything --dag dag.json --goal-node compliance --goal-value 0.95 --deadline 14d
```

---
*gerivdb/CTULU | [CONFORME_NEXUS] | IntentHash: 0xPLAN_ANYTHING_20260612*
