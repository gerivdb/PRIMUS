# SKILL: simulate-anything
## Version: 1.0.0 | Score: 0/20 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: [Obs, C]

---

### CAPACITES
- [ ] `multi-world` — Monte Carlo simulation of N worlds (default: 100)
- [ ] `multi-intervention` — Apply simultaneous interventions
- [ ] `feedback-loops` — Propagate feedback effects (optional)
- [ ] `sensitivity-analysis` — Rank intervention nodes by influence
- [ ] `emergent-behaviors` — Detect non-obvious patterns across worlds
- [ ] `interaction-detection` — Find synergistic/antagonistic intervention pairs
- [ ] `reproducible` — Same seed = same results

### ENTREE
```json
{"dag": "path", "interventions": "node1=val1,node2=val2", "horizon": "30d", "n_worlds": 100}
```

### SORTIE
```json
{"simulation_report": {"n_worlds_simulated": int, "worlds": {"summary": {}, "trajectories": {}, "critical_events": [], "sensitivity_analysis": [], "emergent_behaviors": []}, "tags": []}}
```

### GARANTIES
- [OK] READ-ONLY — simulation only
- [OK] Reproducible (random seed logged)
- [OK] N worlds ≥ 50 (below = SIMULATION_FAIBLE tag)
- [OK] Convergence checked (below 50% = SCENARIO_INSTABLE tag)
- [OK] Sensitivity analysis always produced
- [OK] WAL entry emitted if `--wal`

### DEPENDANCES
- Python 3.10+, pyyaml
- cause-anything (PRD-045), intervene-anything (PRD-046)

### EXEMPLES
```bash
simulate-anything --dag dag.json --interventions "PR_size=0.3,HITL_gate=1.0" --horizon 30d --n-worlds 200
simulate-anything --dag dag.json --interventions "PR_size=0.3" --horizon 90d --seed 42
```

---
*gerivdb/CTULU | [CONFORME_NEXUS] | IntentHash: 0xSIMULATE_ANYTHING_20260612*
