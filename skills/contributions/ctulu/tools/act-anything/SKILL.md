# SKILL: act-anything
## Version: 1.0.0 | Score: 0/20 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: [E, C]

---

### CAPACITES
- [ ] `execute-plan` — Execute action plan on real ecosystem (WRITE_REAL)
- [ ] `hitl-gate` — Require HITL approval token for real execution
- [ ] `dry-run-default` — Default to simulation mode (safe)
- [ ] `auto-rollback` — Automatic rollback on step failure
- [ ] `invariant-check` — Continuous invariant monitoring (pre/post conditions)
- [ ] `batch-control` — Max steps per batch (default: 3)

### ENTREE
```json
{"plan": "path", "approval_token": "str|null", "dry_run": true}
```

### SORTIE
```json
{"execution_report": {"status": "completed|partial|aborted|failed", "steps_executed": [], "rollback_log": [], "safety_violations": []}, "observation_trigger": {}}
```

### GARANTIES
- [OK] Only tool that writes to real ecosystem
- [OK] HITL token required for real execution (dry-run default)
- [OK] Automatic rollback on any step failure
- [OK] Invariants checked continuously (abort on violation)
- [OK] WAL entry written BEFORE each action
- [OK] Max 3 steps per batch

### DEPENDANCES
- Python 3.10+, pyyaml
- plan-anything (PRD-054) for plan input

### EXEMPLES
```bash
act-anything --plan plan.json --dry-run
act-anything --plan plan.json --approval-token <token>
```

---
*gerivdb/CTULU | [CONFORME_NEXUS] | IntentHash: 0xACT_ANYTHING_20260612*
