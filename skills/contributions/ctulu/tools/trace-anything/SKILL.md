# SKILL: trace-anything
## Version: 2.0.0 | Score: 0/20 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: [Obs, C]

---

### CAPACITES
- [ ] `trace-chain` — Reconstruct causal chain from target to root causes via DAG traversal
- [ ] `find-evidence` — Find WAL evidence for each causal step
- [ ] `build-timeline` — Build ordered timeline of causal events
- [ ] `identify-gaps` — Flag missing evidence or low-confidence links

### ENTREE
```json
{"target": "string", "dag": "path", "wal": "path", "depth": 5, "min_confidence": 0.0}
```

### SORTIE
```json
{"causal_chain": {"target": "string", "chain": [], "root_causes": {}, "timeline": [], "confidence_overall": float, "gaps": []}}
```

### GARANTIES
- [OK] READ-ONLY on sources
- [OK] `--dry-run` available
- [OK] WAL entry emitted if `--wal-log`
- [OK] Cause-before-effect temporal validation
- [OK] Gaps explicitly reported, never silently filled

### DEPENDANCES
- Python 3.10+, pyyaml
- cause-anything (PRD-045) for DAG input

### EXEMPLES
```bash
trace-anything --target phi_CPS_drop --dag dag.json --depth 5
trace-anything --target incident_2026-05-14 --dag dag.json --wal D:/wal/ --output text
```

---
*gerivdb/CTULU | [CONFORME_NEXUS] | IntentHash: 0xTRACE_ANYTHING_20260612*
