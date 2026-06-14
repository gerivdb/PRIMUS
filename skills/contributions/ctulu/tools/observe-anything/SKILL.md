# SKILL: observe-anything
## Version: 1.0.0 | Score: 0/20 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: [Obs]

---

### CAPACITES
- [ ] `measure-effect` — Compare observed metrics to plan predictions
- [ ] `detect-side-effects` — Find unexpected changes in non-target nodes
- [ ] `verdict` — Classify plan as EFFECTIVE/PARTIAL/INEFFECTIVE/ADVERSE
- [ ] `drift-signal` — Generate drift signal for drift-detect when divergence found
- [ ] `recommend` — Produce continue/adjust/abort/investigate recommendations

### ENTREE
```json
{"plan": "path", "execution_report": "path", "window_start": "ISO8601", "window_end": "ISO8601"}
```

### SORTIE
```json
{"observation_report": {"measurements": [], "verdict": {"plan_effective": bool, "verdict": "str"}, "recommendations": []}, "drift_signal": {}}
```

### GARANTIES
- [OK] READ-ONLY — measurement only
- [OK] Triggered by act-anything (no spontaneous observation)
- [OK] Always compare to baseline AND prediction
- [OK] Side effects always searched
- [OK] Drift signal auto-generated on significant divergence
- [OK] WAL entry emitted if `--wal`

### DEPENDANCES
- Python 3.10+, pyyaml
- act-anything (PRD-055) for execution report

### EXEMPLES
```bash
observe-anything --plan plan.json --execution-report exec.json
observe-anything --plan plan.json --execution-report exec.json --window-start 2026-06-01 --window-end 2026-06-15
```

---
*gerivdb/CTULU | [CONFORME_NEXUS] | IntentHash: 0xOBSERVE_ANYTHING_20260612*
