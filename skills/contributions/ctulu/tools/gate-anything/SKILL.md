# SKILL: gate-anything
## Version: 0.1.0 | Score: 16/20 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: [E, C]

---

### CAPACITES
- [ ] `gate` — Intercepte toute transition déstructive et demande confirmation HITL
- [ ] `gate --mode auto` — Gate automatisé (CI/CD sans intervention)
- [ ] `gate --mode hitl` — Gate manuel (confirmation humaine obligatoire)
- [ ] `gate --mode dry` — Simulation sans effet

### ENTREE
```json
{"target": "string", "mode": "auto|hitl|dry"}
```

### SORTIE
```json
{
  "status": "ok|blocked|error",
  "target": "string",
  "gate_decision": "approved|rejected|pending",
  "wal_entry": "string|null"
}
```

### GARANTIES
- [OK] `--dry-run` disponible — aucun blocage réel
- [OK] `--json` retourne JSON valide parseable
- [OK] Toute action destructive est interceptable
- [OK] Idempotent en mode dry
- [OK] WAL entry émise si `--wal`

### DEPENDANCES
- Python 3.10+

### EXEMPLES
```bash
gate-anything --target gerivdb/NEXUS --mode hitl
gate-anything --target migrate-anything --mode auto --wal --output json
```

---
*Généré par scaffold-anything --template skill-md | gerivdb/CTULU | [CONFORME_NEXUS]*
