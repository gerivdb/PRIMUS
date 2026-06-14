# SKILL: migrate-anything
## Version: 0.1.0 | Score: 16/20 | Status: ACTIVE
## Repo: gerivdb/CTULU | Strate: L3_EMERGENCE | ternary_role: E

---

### CAPACITES
- [ ] `migrate` — Applique une migration structurelle sur un artefact
- [ ] `migrate --migration add-ternary-role` — Annote ternary_role dans known_repositories.yaml
- [ ] `migrate --migration add-strate` — Ajoute champ strate manquant
- [ ] `migrate --migration add-ceobs-fields` — Complète champs CEObs
- [ ] `migrate --migration normalize-metadata` — Normalise métadonnées selon RSS-v1

### ENTREE
```json
{"target": "string", "migration": "string"}
```

### SORTIE
```json
{
  "status": "ok|warn|error",
  "target": "string",
  "changes": [{"field": "", "before": "", "after": ""}],
  "wal_entry": "string|null"
}
```

### GARANTIES
- [OK] `--dry-run` disponible — prévisualise sans modifier
- [OK] `--json` retourne JSON valide parseable
- [OK] Toute migration est réversible via WAL
- [OK] Idempotent — double migration = même résultat
- [OK] WAL entry émise si `--wal`

### DEPENDANCES
- Python 3.10+
- PyYAML
- gate-anything (protection HITL)

### EXEMPLES
```bash
migrate-anything --target known_repositories.yaml:BRAIN --migration add-ternary-role --dry-run
migrate-anything --target gerivdb/NEXUS --migration add-ceobs-fields --wal
```

---
*Généré par scaffold-anything --template skill-md | gerivdb/CTULU | [CONFORME_NEXUS]*
