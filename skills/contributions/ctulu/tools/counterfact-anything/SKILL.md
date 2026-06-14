# SKILL: counterfact-anything
## Version: 1.0.0 | Score: 0/20 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: [Obs, C]

---

### CAPACITES
- [ ] `twin-network` — Abduction → Action → Prediction (Pearl Level 3)
- [ ] `necessity-sufficiency` — Classify causes as necessary/sufficient/contributing
- [ ] `minimal-change` — Enforce single-antecedent modification (parsimony)
- [ ] `exogenous-preservation` — Keep background noise identical between real and CF worlds

### ENTREE
```json
{"dag": "path", "factual_node": "id", "factual_value": float, "hypothetical_value": float, "consequent_node": "id"}
```

### SORTIE
```json
{"counterfactual_report": {"query": "str", "factual": {}, "counterfactual": {}, "verdict": {"necessary_cause": bool, "sufficient_cause": bool, "classification": "str"}, "confidence": float}}
```

### GARANTIES
- [OK] READ-ONLY — simulation only
- [OK] Anchored to observed event (no free-floating CF)
- [OK] Single antecedent modified per call
- [OK] Exogenous variables preserved between worlds
- [OK] `--dry-run` available
- [OK] WAL entry emitted if `--wal`

### DEPENDANCES
- Python 3.10+, pyyaml
- cause-anything (PRD-045) for DAG input

### EXEMPLES
```bash
counterfact-anything --dag dag.json --factual-node refactoring --factual-value 0.9 --hypothetical-value 0.1 --consequent-node phi_CPS
```

---
*gerivdb/CTULU | [CONFORME_NEXUS] | IntentHash: 0xCOUNTERFACT_ANYTHING_20260612*
