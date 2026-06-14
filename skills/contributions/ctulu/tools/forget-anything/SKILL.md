# SKILL: forget-anything
## Version: 1.0.0 | Score: 0/20 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: [C, Obs]

---

### CAPACITES
- [ ] `purge-obsolete` — Archive edges/nodes marked obsolete by learn-anything
- [ ] `detect-orphans` — Remove nodes with no edges
- [ ] `graveyard-archive` — Move purged items to graveyard (restorable)
- [ ] `noise-reduction` — Report net noise reduction ratio

### ENTREE
```json
{"dag": "path", "obsolescence_threshold": 0.1, "obsolescence_duration": "14d"}
```

### SORTIE
```json
{"edges_purged": [], "nodes_purged": [], "preserved": [], "summary": {"edges_before": int, "edges_after": int, "net_noise_reduction": float}}
```

### GARANTIES
- [OK] Only purges what learn-anything marked obsolete
- [OK] Archive by default (never hard-delete without HITL)
- [OK] Deterministic: same input = same purge
- [OK] No cycles created by purge
- [OK] WAL entry emitted if `--wal`

### DEPENDANCES
- Python 3.10+, pyyaml
- learn-anything (PRD-051) for obsolete markings

### EXEMPLES
```bash
forget-anything --dag dag.json --obsolescence-duration 14d
forget-anything --dag dag.json --archive-mode hard-delete  # requires HITL
```

---
*gerivdb/CTULU | [CONFORME_NEXUS] | IntentHash: 0xFORGET_ANYTHING_20260612*
